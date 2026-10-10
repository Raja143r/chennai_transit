# Chennai Transit Navigator - Core Routing Enhancements
## Implementation Plan

---

## Current Architecture Summary
- **Backend**: FastAPI (`app.py`) with Dijkstra on multimodal graph (Metro, Suburban, Bus, Walk)
- **Graph**: Built from `transit_data.py` (NODES + EDGES) at startup
- **Routing**: `find_route_by_coords()` → virtual SRC/DST nodes → Dijkstra with priority cost functions
- **Frontend**: Leaflet map + vanilla JS search/routing UI

---

## 1. Real-Time Data Integration (Live Arrivals)

### 1.1 Research & API Discovery
| Source | API Availability | Notes |
|--------|------------------|-------|
| **CMRL Metro** | No public real-time API | May need GTFS-RT or scraping |
| **MTC Bus** | No public real-time API | Some third-party aggregators |
| **Southern Railway** | IRCTC/NTES APIs | Requires registration |
| **Chennai Open Data** | data.chennai.gov.in | Static GTFS available |

### 1.2 Implementation Strategy
```
Phase 1: Static GTFS Schedule Integration (Immediate)
  ├─ Parse GTFS feeds (routes, trips, stop_times, calendar)
  ├─ Store in SQLite/Redis with time-indexed lookups
  ├─ Add `next_departures(stop_id, time, limit)` function
  └─ Extend EDGE model: add `schedule: List[DepartureTime]`

Phase 2: Real-Time Feeds (When Available)
  ├─ GTFS-Realtime consumer (protobuf)
  ├─ WebSocket push to frontend for live updates
  └─ Fallback to schedule when real-time unavailable
```

### 1.3 Data Model Extensions
```python
# transit_data.py additions
from dataclasses import dataclass
from typing import List, Optional
from datetime import time

@dataclass
class ScheduledDeparture:
    route_id: str
    trip_id: str
    departure_time: time      # scheduled
    realtime_departure: Optional[time] = None  # live
    headsign: str = ""
    wheelchair_accessible: bool = False

# EDGE extension
EDGES = [
    {
        "from": "...", "to": "...", 
        "schedule": [ScheduledDeparture(...), ...],  # NEW
        ...
    }
]
```

### 1.4 API Endpoints
```
GET /live/arrivals?stop=<node_name>&limit=5
  → Returns next 5 departures with real-time vs scheduled

GET /live/trip/<trip_id>/position
  → Vehicle position for bus tracking (if GTFS-RT available)
```

---

## 2. Time-Based Routing (Peak/Off-Peak, Last Service)

### 2.1 Schedule-Aware Edge Weights
```python
# app.py - Enhanced edge_cost function
def edge_cost(conn: dict, departure_time: datetime) -> float:
    base_time = conn["time"]
    wait_time = calculate_wait_time(conn, departure_time)
    
    # Peak multiplier
    if is_peak_hour(departure_time):
        base_time *= PEAK_MULTIPLIER[conn["type"]]  # e.g., METRO 1.2x, BUS 1.5x
    
    # Last service check
    if is_after_last_service(conn, departure_time):
        return INF  # Edge unavailable
    
    return base_time + wait_time
```

### 2.2 Time-Expanded Graph (for accurate wait times)
| Approach | Pros | Cons |
|----------|------|------|
| **Time-dependent Dijkstra** | Accurate wait times | Complex, slower |
| **Frequency-based approximation** | Fast, simple | Less accurate for low-frequency |
| **Precomputed timetables** | Exact | Memory heavy |

**Recommendation**: Frequency-based for buses (high freq), timetable for metro/train.

### 2.3 New Request Model
```python
class RouteRequest(BaseModel):
    src_lat: float
    src_lng: float
    src_name: str
    dst_lat: float
    dst_lng: float
    dst_name: str
    priority: str = "fastest"
    departure_time: Optional[datetime] = None  # NEW: default=now
    arrival_by: Optional[datetime] = None      # NEW: reverse routing
```

### 2.4 Service Hours Data
```python
# transit_data.py
SERVICE_HOURS = {
    "METRO": {"first": "05:00", "last": "23:00", "peak": [("07:00","10:00"), ("17:00","20:00")]},
    "SUBURBAN": {"first": "04:00", "last": "23:30", "peak": [...]},
    "BUS": {"first": "04:30", "last": "22:30", "peak": [...]},
    "MRTS": {"first": "05:00", "last": "22:00", "peak": [...]},
}
```

---

## 3. Multi-Criteria Optimization (Pareto Frontier)

### 3.1 Current Limitation
Single scalar cost function → single "optimal" path per priority.

### 3.2 Pareto Frontier Algorithm
```python
def find_pareto_routes(graph, src, dst, max_solutions=5):
    """
    Returns non-dominated routes across (time, fare, transfers, walking)
    Uses label-setting algorithm with dominance pruning.
    """
    # State: (node, time, fare, transfers, walk_time, path)
    # Dominance: A dominates B if A.time <= B.time AND A.fare <= B.fare 
    #            AND A.transfers <= B.transfers AND A.walk <= B.walk
    #            (with at least one strict)
```

### 3.3 API Response
```json
{
  "pareto_routes": [
    {
      "label": "Fastest",
      "steps": [...],
      "total_time": 45,
      "total_fare": 60,
      "transfers": 2,
      "walk_minutes": 8
    },
    {
      "label": "Cheapest",
      "steps": [...],
      "total_time": 65,
      "total_fare": 25,
      "transfers": 1,
      "walk_minutes": 15
    },
    {
      "label": "Balanced",
      "steps": [...],
      "total_time": 50,
      "total_fare": 40,
      "transfers": 1,
      "walk_minutes": 10
    }
  ]
}
```

### 3.4 Frontend: Route Comparison View
- Toggle between Pareto options
- Radar chart: Time vs Cost vs Transfers vs Walk
- "Why this route?" explanation

---

## 4. Accessibility Routing

### 4.1 Station Accessibility Data Model
```python
# transit_data.py
STATION_ACCESSIBILITY = {
    "Chennai Central Metro": {
        "elevator": True,
        "escalator": True,
        "ramp": True,
        "tactile_paving": True,
        "audio_announcements": True,
        "accessible_toilet": True,
        "platform_gap_cm": 5,
        "staff_assistance": True,
    },
    "Guindy Metro": {
        "elevator": True,
        "escalator": False,
        ...
    },
    # Default: assume not accessible unless specified
}
```

### 4.2 Accessibility-Aware Routing
```python
def edge_cost(conn, departure_time, accessibility_profile):
    # Profile: "wheelchair", "limited_mobility", "visual_impairment", "none"
    
    if accessibility_profile == "wheelchair":
        # Penalize non-accessible transfers heavily
        if conn["type"] == "WALK" and not is_accessible_path(conn["from"], conn["to"]):
            return INF
        if conn["type"] in ("METRO", "SUBURBAN") and not station_accessible(conn["to"]):
            return INF
    
    # Add transfer penalty for elevator/escalator wait
    if is_transfer(conn) and needs_elevator(conn):
        wait_time += ELEVATOR_WAIT_MINUTES  # ~3-5 min
```

### 4.3 New Request Parameter
```python
class RouteRequest(BaseModel):
    ...
    accessibility: Optional[str] = None  # "wheelchair", "limited_mobility", "visual", "none"
```

### 4.4 Frontend: Accessibility Toggle
- Profile selector in UI
- Route results show accessibility badges per station
- "Accessible alternative" suggestion if primary route fails

---

## 5. Fare Integration

### 5.1 Fare Structure Data
```python
# transit_data.py
FARE_STRUCTURE = {
    "METRO": {
        "token": {0: 10, 2: 10, 5: 20, 10: 30, 15: 40, 20: 50, 25: 60, 30: 70},  # km: fare
        "qr_discount": 0.10,  # 10% off
        "daily_pass": 150,
        "monthly_pass": 2500,
    },
    "SUBURBAN": {
        "ticket": {0: 5, 10: 10, 20: 15, 30: 20, 40: 25, 50: 30},
        "monthly_pass": 1200,
    },
    "BUS": {
        "ordinary": 8, "express": 15, "deluxe": 25, "ac": 40,
        "daily_pass": 80,
    },
    "MRTS": {...}
}
```

### 5.2 Dynamic Fare Calculation
```python
def calculate_fare(route_steps, ticket_type="token", pass_type=None):
    total = 0
    for step in route_steps:
        if step["type"] == "METRO":
            dist = metro_distance(step["from"], step["to"])
            total += METRO_FARE_TABLE[dist]
        elif step["type"] == "BUS":
            total += BUS_FARE_BY_ROUTE_TYPE[step.get("route_type", "ordinary")]
        # Apply pass logic
    if pass_type == "daily" and total > DAILY_PASS_COST:
        return DAILY_PASS_COST
    return total
```

### 5.3 QR Ticket Deep Links
```python
QR_TICKET_URLS = {
    "METRO": "https://chennaimetrorail.org/qr-ticket?from={from}&to={to}&fare={fare}",
    "BUS": "https://mtcbus.org/ticket?route={route}&stages={stages}",
    "SUBURBAN": "https://utsonmobile.indianrail.gov.in/...",
}
```

### 5.4 API Response Extension
```json
{
  "steps": [...],
  "total_time": 45,
  "total_fare": 45,
  "fare_breakdown": [
    {"step": 1, "mode": "METRO", "distance_km": 12, "fare": 30, "ticket_type": "token"},
    {"step": 2, "mode": "BUS", "route": "MTC 5E", "fare": 15, "ticket_type": "ordinary"}
  ],
  "pass_recommendation": {
    "type": "metro_daily",
    "cost": 150,
    "savings": 105,
    "break_even_trips": 5
  },
  "qr_ticket_url": "https://..."
}
```

---

## 🏗️ Implementation Order & Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: Foundation (Week 1-2)                                  │
├─────────────────────────────────────────────────────────────────┤
│ 1.1 Add requirements.txt, pytest, type hints                   │
│ 1.2 Extract graph building to separate module (router.py)      │
│ 1.3 Add unit tests for find_route_by_coords                    │
│ 1.4 Create config.yaml for service hours, fare tables          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: Time-Based Routing (Week 2-3)                         │
├─────────────────────────────────────────────────────────────────┤
│ 2.1 Add departure_time/arrival_by to RouteRequest              │
│ 2.2 Implement is_peak_hour(), is_after_last_service()          │
│ 2.3 Frequency-based wait time estimation                       │
│ 2.4 Add GTFS static parser (optional, for accurate schedules)  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: Pareto Frontier (Week 3-4)                            │
├─────────────────────────────────────────────────────────────────┤
│ 3.1 Implement label-setting multi-objective Dijkstra           │
│ 3.2 Add /route/pareto endpoint                                 │
│ 3.3 Frontend: route comparison UI                              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: Accessibility (Week 4)                                │
├─────────────────────────────────────────────────────────────────┤
│ 4.1 Add STATION_ACCESSIBILITY to transit_data.py               │
│ 4.2 Implement accessibility-aware edge costs                   │
│ 4.3 Add accessibility parameter to API                         │
│ 4.4 Frontend: accessibility profile selector                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: Fare Integration (Week 4-5)                           │
├─────────────────────────────────────────────────────────────────┤
│ 5.1 Add FARE_STRUCTURE to transit_data.py                      │
│ 5.2 Implement calculate_fare() with pass optimization          │
│ 5.3 Add fare_breakdown + pass_recommendation to response       │
│ 5.4 QR ticket deep link generation                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 6: Real-Time (Week 5+) — When APIs Available             │
├─────────────────────────────────────────────────────────────────┤
│ 6.1 GTFS-Realtime consumer service                             │
│ 6.2 Redis cache for live departures                            │
│ 6.3 WebSocket / SSE for frontend push                          │
│ 6.4 /live/arrivals endpoint                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## ❓ Clarifying Questions

| Question | Options | Recommendation |
|----------|---------|----------------|
| **Real-time data priority?** | A) Build GTFS static first, real-time later<br>B) Mock real-time for demo, integrate later | **A** — solid foundation first |
| **Pareto vs single-route?** | A) Replace single-route with Pareto<br>B) Keep both: default single, "Show alternatives" button | **B** — simpler UX, progressive disclosure |
| **Accessibility data source?** | A) Manual curation (current 147 nodes)<br>B) Crowdsourced / OpenStreetMap tags<br>C) Official CMRL/Railway data | **A** to start, **B** for scale |
| **Fare pass optimization?** | A) Per-trip optimization only<br>B) Multi-trip (weekly/monthly) with usage prediction | **A** first, **B** later |
| **Deployment target?** | A) Local dev only<br>B) Cloud (Render, Fly.io, Railway)<br>C) Docker + k8s | **B** for sharing/demo |

---

## 📦 New Files to Create

```
/home/maharaja/Documents/chennai_transit/
├── requirements.txt
├── config.yaml                    # Service hours, fares, multipliers
├── router/
│   ├── __init__.py
│   ├── graph.py                   # Graph building, time-expanded
│   ├── dijkstra.py                # Core routing algorithms
│   ├── pareto.py                  # Multi-objective label-setting
│   ├── accessibility.py           # Accessibility-aware costs
│   ├── fares.py                   # Fare calculation, pass optimization
│   └── schedule.py                # GTFS parsing, wait times
├── tests/
│   ├── test_router.py
│   ├── test_pareto.py
│   ├── test_fares.py
│   └── test_accessibility.py
├── transit_data.py                # Extended with accessibility, fares
└── app.py                         # Updated endpoints
```

---

## ✅ Ready to Proceed?

**Recommended starting point**: Phase 1 (Foundation) to establish testing and modular structure, then Phase 2 (Time-Based Routing) since it enhances the core routing immediately.

The clarifying questions above should be decided before Phase 1 begins.