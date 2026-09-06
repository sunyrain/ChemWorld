"""Conservative 2D navigation over current asset poses; no hardware motion output."""

import heapq
import math

from .catalog import ASSETS, CATALOG
from .engine import LabError


class Navigator:
    def __init__(self, lab, definition):
        self.lab = lab
        self.definition = definition
        self.radius = (
            CATALOG["robot_01"]["footprint_radius_m"] + definition["navigation"]["clearance_m"]
        )
        self.grid = definition["navigation"]["grid_m"]

    def obstacles(self):
        items = [
            (a["id"], self.lab.poses[a["id"]], a["size"])
            for a in ASSETS
            if a["kind"]
            in {"bench", "oven", "chiller", "cabinet", "waste", "eyewash", "extinguisher"}
        ]
        items += [
            (a["id"], a["position_m"], a["size_m"]) for a in self.definition["static_obstacles"]
        ]
        return items

    def clear(self, p):
        bounds = self.definition["bounds_m"]
        r = self.radius
        if not all(
            bounds[axis][0] + r <= p[i] <= bounds[axis][1] - r for i, axis in enumerate(["x", "y"])
        ):
            return False
        for _, position, size in self.obstacles():
            if (
                abs(p[0] - position[0]) <= size[0] / 2 + r
                and abs(p[1] - position[1]) <= size[1] / 2 + r
            ):
                return False
        return True

    def segment_clear(self, a, b):
        steps = max(1, math.ceil(math.dist(a[:2], b[:2]) / 0.035))
        return all(
            self.clear([a[j] + (b[j] - a[j]) * i / steps for j in range(2)])
            for i in range(steps + 1)
        )

    def path(self, start, goal):
        if not self.clear(start) or not self.clear(goal):
            raise LabError("Robot start or destination overlaps an obstacle / room boundary", 409)
        if self.segment_clear(start, goal):
            return [list(goal)]
        g = self.grid

        def cell(p):
            return (round(p[0] / g), round(p[1] / g))

        def point(c):
            return [c[0] * g, c[1] * g, 0.08]

        first, last = cell(start), cell(goal)
        if not self.segment_clear(start, point(first)) or not self.segment_clear(point(last), goal):
            raise LabError("Destination is too close to an obstacle for the navigation grid", 409)
        queue = [(0, first)]
        cost = {first: 0}
        parent = {}
        closed = set()
        while queue:
            _, cur = heapq.heappop(queue)
            if cur in closed:
                continue
            if cur == last:
                break
            closed.add(cur)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nxt = (cur[0] + dx, cur[1] + dy)
                if nxt in closed or not self.segment_clear(point(cur), point(nxt)):
                    continue
                value = cost[cur] + math.hypot(dx, dy)
                if value < cost.get(nxt, float("inf")):
                    cost[nxt] = value
                    parent[nxt] = cur
                    heapq.heappush(queue, (value + math.dist(nxt, last), nxt))
        if last not in cost:
            raise LabError("No collision-free route within this environment", 409)
        route = [last]
        while route[-1] != first:
            route.append(parent[route[-1]])
        points = [list(start)] + [point(c) for c in reversed(route)] + [list(goal)]
        smooth = []
        i = 0
        while i < len(points) - 1:
            j = len(points) - 1
            while j > i + 1 and not self.segment_clear(points[i], points[j]):
                j -= 1
            smooth.append(points[j])
            i = j
        return smooth
