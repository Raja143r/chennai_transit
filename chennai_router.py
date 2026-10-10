from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import heapq


# ---------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------

@dataclass
class Connection:
    destination: str
    transport: str
    duration: int       # minutes
    fare: float
    route_name: str = ""
    wait_time: int = 0


@dataclass
class Step:
    from_place: str
    to_place: str
    transport: str
    duration: int
    fare: float
    route_name: str = ""


# ---------------------------------------------------------
# TRANSPORT NETWORK
# ---------------------------------------------------------

class ChennaiTransportNetwork:

    def __init__(self):
        self.graph: Dict[str, List[Connection]] = {}

    def add_connection(
        self,
        source: str,
        destination: str,
        transport: str,
        duration: int,
        fare: float = 0,
        route_name: str = "",
        wait_time: int = 0
    ):
        if source not in self.graph:
            self.graph[source] = []

        self.graph[source].append(
            Connection(
                destination=destination,
                transport=transport,
                duration=duration,
                fare=fare,
                route_name=route_name,
                wait_time=wait_time
            )
        )

    # -----------------------------------------------------
    # FIND BEST ROUTE
    # -----------------------------------------------------

    def find_route(
        self,
        start: str,
        destination: str,
        priority: str = "fastest"
    ) -> Optional[Tuple[List[Step], int, float]]:

        if start not in self.graph:
            return None

        # priority determines how we calculate route cost
        def calculate_cost(connection: Connection):

            total_time = connection.duration + connection.wait_time

            if priority == "cheapest":
                return connection.fare * 10 + total_time * 0.2

            elif priority == "least_walking":
                if connection.transport == "WALK":
                    return total_time * 5
                return total_time

            elif priority == "fewest_transfers":
                transfer_penalty = 20
                return total_time + transfer_penalty

            else:
                # fastest
                return total_time

        # Heap:
        # (cost, current_location, steps, actual_time, actual_fare)
        heap = [
            (0, start, [], 0, 0)
        ]

        visited = {}

        while heap:

            cost, current, steps, actual_time, actual_fare = heapq.heappop(heap)

            if current == destination:
                return steps, actual_time, actual_fare

            if current in visited and visited[current] <= cost:
                continue

            visited[current] = cost

            for connection in self.graph.get(current, []):

                new_cost = cost + calculate_cost(connection)

                new_step = Step(
                    from_place=current,
                    to_place=connection.destination,
                    transport=connection.transport,
                    duration=connection.duration,
                    fare=connection.fare,
                    route_name=connection.route_name
                )

                heapq.heappush(
                    heap,
                    (
                        new_cost,
                        connection.destination,
                        steps + [new_step],
                        actual_time + connection.duration + connection.wait_time,
                        actual_fare + connection.fare
                    )
                )

        return None


# ---------------------------------------------------------
# DISPLAY ROUTE
# ---------------------------------------------------------

def display_route(result):

    if result is None:
        print("\n❌ No route found.")
        return

    steps, total_time, total_fare = result

    print("\n========================================")
    print("           CHENNAI JOURNEY")
    print("========================================\n")

    for i, step in enumerate(steps, 1):

        if step.transport == "WALK":
            icon = "🚶"
            transport_name = "Walk"

        elif step.transport == "BUS":
            icon = "🚌"
            transport_name = "MTC Bus"

        elif step.transport == "METRO":
            icon = "🚇"
            transport_name = "Chennai Metro"

        elif step.transport == "TRAIN":
            icon = "🚆"
            transport_name = "Train"

        else:
            icon = "➡️"
            transport_name = step.transport

        print(f"{i}. {icon} {transport_name}")

        if step.route_name:
            print(f"   Route: {step.route_name}")

        print(f"   {step.from_place} → {step.to_place}")
        print(f"   Time: {step.duration} minutes")

        if step.fare > 0:
            print(f"   Fare: ₹{step.fare:.0f}")
        else:
            print("   Fare: Free")

        print()

    print("----------------------------------------")
    print(f"⏱ Total time : {total_time} minutes")
    print(f"💰 Total fare : ₹{total_fare:.0f}")
    print(f"🔄 Transfers  : {max(0, len(steps) - 1)}")
    print("----------------------------------------")


# ---------------------------------------------------------
# SAMPLE CHENNAI DATA
# ---------------------------------------------------------

def create_chennai_network():

    network = ChennaiTransportNetwork()

    # -----------------------------------------------------
    # WALKING
    # -----------------------------------------------------

    network.add_connection(
        "User",
        "T Nagar Bus Stop",
        "WALK",
        5
    )

    network.add_connection(
        "Saidapet Metro",
        "Kapaleeshwarar Temple",
        "WALK",
        12
    )

    network.add_connection(
        "Government Estate Metro",
        "Kapaleeshwarar Temple",
        "WALK",
        15
    )

    network.add_connection(
        "Chennai Central",
        "Government Estate Metro",
        "WALK",
        8
    )

    # -----------------------------------------------------
    # MTC BUS
    # -----------------------------------------------------

    network.add_connection(
        "T Nagar Bus Stop",
        "Saidapet Bus Stop",
        "BUS",
        10,
        fare=15,
        route_name="MTC 5E"
    )

    network.add_connection(
        "Saidapet Bus Stop",
        "Saidapet Metro",
        "WALK",
        5
    )

    network.add_connection(
        "T Nagar Bus Stop",
        "Guindy",
        "BUS",
        15,
        fare=15,
        route_name="MTC 21G"
    )

    # -----------------------------------------------------
    # METRO
    # -----------------------------------------------------

    network.add_connection(
        "Guindy",
        "Saidapet Metro",
        "METRO",
        8,
        fare=30,
        route_name="Blue Line"
    )

    network.add_connection(
        "Saidapet Metro",
        "Government Estate Metro",
        "METRO",
        12,
        fare=30,
        route_name="Blue Line"
    )

    network.add_connection(
        "Government Estate Metro",
        "Chennai Central",
        "METRO",
        5,
        fare=20,
        route_name="Blue Line"
    )

    # -----------------------------------------------------
    # TRAIN
    # -----------------------------------------------------

    network.add_connection(
        "Saidapet Bus Stop",
        "Chennai Central",
        "TRAIN",
        20,
        fare=10,
        route_name="Suburban Train"
    )

    network.add_connection(
        "Chennai Central",
        "Saidapet Bus Stop",
        "TRAIN",
        20,
        fare=10,
        route_name="Suburban Train"
    )

    # Reverse connections

    network.add_connection(
        "Saidapet Metro",
        "Guindy",
        "METRO",
        8,
        fare=30,
        route_name="Blue Line"
    )

    network.add_connection(
        "Government Estate Metro",
        "Saidapet Metro",
        "METRO",
        12,
        fare=30,
        route_name="Blue Line"
    )

    network.add_connection(
        "Chennai Central",
        "Government Estate Metro",
        "METRO",
        5,
        fare=20,
        route_name="Blue Line"
    )

    return network


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main():

    network = create_chennai_network()

    print("========================================")
    print("       CHENNAI MULTIMODAL ROUTER")
    print("========================================")

    print("\nAvailable destinations:")
    print("1. Kapaleeshwarar Temple")

    start = "User"
    destination = "Kapaleeshwarar Temple"

    print(f"\n📍 Starting point : {start}")
    print(f"🛕 Destination    : {destination}")

    print("\nSearching for fastest route...")

    result = network.find_route(
        start,
        destination,
        priority="fastest"
    )

    display_route(result)


if __name__ == "__main__":
    main()
