from collections import deque
import heapq


class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    def get_neighbors(self, position, grid_size, walls):
        """
        Returns all valid neighboring cells and the action
        required to move to each cell.
        """

        x, y = position
        width, height = grid_size

        possible_moves = [
            ((x, y + 1), 'Up'),
            ((x, y - 1), 'Down'),
            ((x - 1, y), 'Left'),
            ((x + 1, y), 'Right')
        ]

        neighbors = []

        for new_position, action in possible_moves:

            nx, ny = new_position

            # Stay inside the grid
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Do not move through walls
            if new_position in walls:
                continue

            neighbors.append((new_position, action))

        return neighbors

    # ==========================================
    # BFS
    # ==========================================

    def bfs_search(self, start, goal, grid_size, walls):

        frontier = deque()

        # Store starting position and path
        frontier.append((start, []))

        reached = {start}

        while frontier:

            current, path = frontier.popleft()

            if current == goal:
                return path

            for neighbor, action in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                if neighbor not in reached:

                    reached.add(neighbor)

                    new_path = path + [action]

                    frontier.append(
                        (neighbor, new_path)
                    )

        return []

    # ==========================================
    # DFS
    # ==========================================

    def dfs_search(self, start, goal, grid_size, walls):

        frontier = []

        # Stack for DFS
        frontier.append((start, []))

        reached = {start}

        while frontier:

            current, path = frontier.pop()

            if current == goal:
                return path

            for neighbor, action in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                if neighbor not in reached:

                    reached.add(neighbor)

                    new_path = path + [action]

                    frontier.append(
                        (neighbor, new_path)
                    )

        return []

    # ==========================================
    # UCS
    # ==========================================

    def ucs_search(self, start, goal, grid_size, walls):

        frontier = []

        counter = 0

        # (cost, counter, position, path)
        heapq.heappush(
            frontier,
            (0, counter, start, [])
        )

        reached = {start: 0}

        while frontier:

            cost, _, current, path = heapq.heappop(
                frontier
            )

            if current == goal:
                return path

            for neighbor, action in self.get_neighbors(
                current,
                grid_size,
                walls
            ):

                # Every movement has a cost of 1
                new_cost = cost + 1

                if (
                    neighbor not in reached
                    or new_cost < reached[neighbor]
                ):

                    reached[neighbor] = new_cost

                    counter += 1

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            neighbor,
                            new_path
                        )
                    )

        return []

    # ==========================================
    # Select Search Algorithm
    # ==========================================

    def search(self, start, goal, grid_size, walls):

        if self.active_algo == 'BFS':

            return self.bfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'DFS':

            return self.dfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'UCS':

            return self.ucs_search(
                start,
                goal,
                grid_size,
                walls
            )

        return []

    # ==========================================
    # Find Closest Food
    # ==========================================

    def find_closest_food(
        self,
        start,
        food_positions,
        grid_size,
        walls
    ):

        closest_food = None
        closest_path = None

        for food in food_positions:

            food = tuple(food)

            path = self.search(
                start,
                food,
                grid_size,
                walls
            )

            if path:

                if (
                    closest_path is None
                    or len(path) < len(closest_path)
                ):

                    closest_food = food
                    closest_path = path

        return closest_food, closest_path

    # ==========================================
    # Sense and Act
    # ==========================================

    def sense_and_act(self, percept):

        # Create a new plan only when
        # there is no existing plan.
        if not self.plan:

            start = tuple(percept['agent_pos'])

            grid_size = percept['grid_size']

            walls = {
                tuple(wall)
                for wall in percept['walls']
            }

            all_food = [
                tuple(food)
                for food in percept['all_food']
            ]

            _, path = self.find_closest_food(
                start,
                all_food,
                grid_size,
                walls
            )

            if path is not None:
                self.plan = path

        # Execute the plan one action at a time
        if self.plan:
            return self.plan.pop(0)

        # Fallback if no path exists
        return 'Up'