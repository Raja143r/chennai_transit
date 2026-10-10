from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import heapq
import math

from transit_data import NODES, EDGES

app = FastAPI(title="Chennai Navigator")
templates = Jinja2Templates(directory="templates")


# =========================================================
# BUILD TRANSIT GRAPH AT STARTUP
# =========================================================

def build_graph() -> dict:
    """
    Build adjacency list from transit_data.EDGES.
    Every edge is treated as bidirectional.
    """
    graph: dict = {node: [] for node in NODES}

    for edge in EDGES:
        src, dst = edge["from"], edge["to"]

        # Ensure nodes exist (some edges reference bus hubs not in NODES)
        for n in (src, dst):
            if n not in graph:
                graph[n] = []

        conn = {
            "to":    dst,
            "type":  edge["type"],
            "route": edge["route"],
            "time":  edge["time"],
            "fare":  edge["fare"],
        }
        rev = {
            "to":    src,
            "type":  edge["type"],
            "route": edge["route"],
            "time":  edge["time"],
            "fare":  edge["fare"],
        }
        graph[src].append(conn)
        graph[dst].append(rev)

    return graph


TRANSIT_GRAPH = build_graph()


# =========================================================
# HAVERSINE DISTANCE
# =========================================================

def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Returns distance in metres between two WGS-84 points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi   = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


WALK_SPEED_MPM = 80   # metres per minute  ≈ 4.8 km/h
MAX_WALK_M     = 3000 # maximum walk to reach a transit node (3 km)


# =========================================================
# NEAREST TRANSIT NODE LOOKUP
# =========================================================

def find_nearest_nodes(lat: float, lng: float,
                       max_nodes: int = 5,
                       max_dist_m: float = MAX_WALK_M) -> list:
    """
    Returns up to max_nodes transit nodes within max_dist_m metres,
    sorted by distance. Each entry is (distance_m, node_name, walk_minutes).
    """
    results = []
    for name, info in NODES.items():
        d = haversine_m(lat, lng, info["lat"], info["lng"])
        if d <= max_dist_m:
            walk_time = max(1, math.ceil(d / WALK_SPEED_MPM))
            results.append((d, name, walk_time))
    results.sort(key=lambda x: x[0])
    return results[:max_nodes]


# =========================================================
# REQUEST MODEL
# =========================================================

class RouteRequest(BaseModel):
    src_lat:  float
    src_lng:  float
    src_name: str
    dst_lat:  float
    dst_lng:  float
    dst_name: str
    priority: str = "fastest"


# =========================================================
# COORDINATE-BASED DIJKSTRA ROUTER
# =========================================================

def consolidate_steps(steps):
    """
    Consolidate consecutive steps on the same route/line into single steps.
    Only show interchanges when switching lines/modes.
    """
    if not steps:
        return steps

    consolidated = []
    current_group = [steps[0]]

    for step in steps[1:]:
        # Check if this step continues on the same route and transport type
        last = current_group[-1]
        same_route = (step.get("route") and last.get("route") and
                      step["route"] == last["route"])
        same_transport = step["type"] == last["type"]

        if same_route and same_transport and step["type"] != "WALK":
            # Continue the current line
            current_group.append(step)
        else:
            # Finalize current group and start new one
            consolidated.append(create_consolidated_step(current_group))
            current_group = [step]

    # Don't forget the last group
    if current_group:
        consolidated.append(create_consolidated_step(current_group))

    return consolidated


def create_consolidated_step(group):
    """Create a single step from a group of consecutive same-route steps."""
    if len(group) == 1:
        return group[0]

    first = group[0]
    last = group[-1]

    total_time = sum(s["time"] for s in group)
    total_fare = sum(s["fare"] for s in group)

    return {
        "from": first["from"],
        "to": last["to"],
        "type": first["type"],
        "route": first["route"],
        "time": total_time,
        "fare": total_fare,
    }


def find_route_by_coords(src_lat, src_lng, src_name,
                         dst_lat, dst_lng, dst_name,
                         priority="fastest"):
    """
    Route between two arbitrary GPS coordinates by:
      1. Finding the nearest transit nodes to source / destination.
      2. Adding virtual WALK edges from/to those nodes.
      3. Running Dijkstra on the augmented graph.
      4. Consolidating consecutive steps on the same line.
    """

    src_nodes = find_nearest_nodes(src_lat, src_lng)
    dst_nodes = find_nearest_nodes(dst_lat, dst_lng)

    if not src_nodes or not dst_nodes:
        return None

    SRC = "__SRC__"
    DST = "__DST__"

    # Shallow-copy graph so we don't mutate the module-level dict
    g: dict = {k: list(v) for k, v in TRANSIT_GRAPH.items()}
    g[SRC] = []

    # Virtual walk edges: source → nearest transit nodes
    for _, node, walk_time in src_nodes:
        g[SRC].append({"to": node, "type": "WALK", "route": "", "time": walk_time, "fare": 0})

    # Virtual walk edges: nearest transit nodes → destination
    for _, node, walk_time in dst_nodes:
        if node not in g:
            g[node] = []
        g[node].append({"to": DST, "type": "WALK", "route": "", "time": walk_time, "fare": 0})

    # Direct walk fallback (if source and destination are within walking distance)
    direct_d = haversine_m(src_lat, src_lng, dst_lat, dst_lng)
    if direct_d <= MAX_WALK_M:
        direct_walk = max(1, math.ceil(direct_d / WALK_SPEED_MPM))
        g[SRC].append({"to": DST, "type": "WALK", "route": "", "time": direct_walk, "fare": 0})

    g[DST] = []  # sink node

    # ── Cost function ────────────────────────────────────────────
    def edge_cost(conn: dict) -> float:
        t, f = conn["time"], conn["fare"]
        if priority == "cheapest":
            return f * 5 + t * 0.2
        if priority == "least_walking":
            return t * 5 if conn["type"] == "WALK" else t
        return t   # default: fastest

    # ── Dijkstra ─────────────────────────────────────────────────
    # heap: (cost, counter, current_node, path_steps, total_time, total_fare)
    counter = 0
    heap = [(0, counter, SRC, [], 0, 0)]
    visited: dict = {}

    while heap:
        cost, _, node, path, total_time, total_fare = heapq.heappop(heap)

        if node == DST:
            # Rename virtual node placeholders to real names
            clean_path = []
            for step in path:
                frm = src_name if step["from"] == SRC else step["from"]
                to  = dst_name if step["to"]  == DST else step["to"]
                # Skip zero-duration walk steps (already at a transit node)
                if step["type"] == "WALK" and step["time"] == 0:
                    continue
                clean_path.append({**step, "from": frm, "to": to})

            # Consolidate consecutive steps on the same line
            consolidated_path = consolidate_steps(clean_path)
            return {"path": consolidated_path, "time": total_time, "fare": total_fare}

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        for conn in g.get(node, []):
            new_cost = cost + edge_cost(conn)
            step = {
                "from":  node,
                "to":    conn["to"],
                "type":  conn["type"],
                "route": conn["route"],
                "time":  conn["time"],
                "fare":  conn["fare"],
            }
            counter += 1
            heapq.heappush(heap, (
                new_cost,
                counter,
                conn["to"],
                path + [step],
                total_time + conn["time"],
                total_fare + conn["fare"],
            ))

    return None   # no route found


# =========================================================
# OPENSTREETMAP / NOMINATIM SEARCH
# =========================================================

def search_openstreetmap(place: str) -> list:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q":            f"{place}, Chennai, Tamil Nadu, India",
        "format":       "json",
        "limit":        5,
        "countrycodes": "in",
    }
    headers = {"User-Agent": "ChennaiNavigator/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        places = []
        for result in response.json():
            places.append({
                "name":   result.get("display_name"),
                "lat":    float(result["lat"]),
                "lng":    float(result["lon"]),
                "type":   result.get("type"),
                "osm_id": result.get("osm_id"),
            })
        return places
    except requests.RequestException as err:
        print("OpenStreetMap error:", err)
        return []


# =========================================================
# SEARCH API — GET /search?place=...
# =========================================================

@app.get("/search")
def search(place: str):
    if not place.strip():
        return {"success": False, "results": []}
    return {"success": True, "results": search_openstreetmap(place)}


# =========================================================
# ROUTE API — POST /route
# =========================================================

@app.post("/route")
def route(req: RouteRequest):
    result = find_route_by_coords(
        req.src_lat,  req.src_lng,  req.src_name,
        req.dst_lat,  req.dst_lng,  req.dst_name,
        req.priority,
    )
    if result is None:
        return {"success": False, "steps": [], "total_time": 0, "total_fare": 0}

    steps = [
        {
            "from":  s["from"],
            "to":    s["to"],
            "type":  s["type"],
            "route": s["route"],
            "time":  s["time"],
            "fare":  s["fare"],
        }
        for s in result["path"]
    ]
    return {
        "success":    True,
        "steps":      steps,
        "total_time": result["time"],
        "total_fare": result["fare"],
    }


# =========================================================
# NEAREST NODE DEBUG API — GET /nearest?lat=...&lng=...
# =========================================================

@app.get("/nearest")
def nearest(lat: float, lng: float, n: int = 5):
    """Returns the N nearest transit nodes to the given coordinates."""
    nodes = find_nearest_nodes(lat, lng, max_nodes=n)
    return {
        "results": [
            {"name": name, "distance_m": round(d), "walk_min": wt, "type": NODES[name]["type"]}
            for d, name, wt in nodes
        ]
    }


# =========================================================
# MAP PAGE — GET /
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
