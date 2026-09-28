class GridHuntGame:
    """A small Pacman-style grid environment where an agent collects food."""

    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height

        # Agent starts at (0, 0)
        self.agent_pos = [0, 0]

        # The direction the agent is currently facing
        self.facing = 'Right'

        # Food positions
        self.food_positions = {
            (1, 2),
            (2, 3),
            (3, 0),
            (2, 1)
        }

        # Wall positions
        self.walls = {
            (1, 1),
            (2, 2)
        }

        self.score = 0
        self.steps = 0

    # ---------------------------------------------------------
    # PERCEPT
    # ---------------------------------------------------------

    def get_percept(self, agent) -> dict:
        """
        Return only local information to the agent.

        The agent does NOT receive its exact global position.
        """

        x, y = self.agent_pos

        # Determine the cell directly ahead
        ahead_x = x
        ahead_y = y

        if self.facing == 'Up':
            ahead_y += 1

        elif self.facing == 'Down':
            ahead_y -= 1

        elif self.facing == 'Left':
            ahead_x -= 1

        elif self.facing == 'Right':
            ahead_x += 1

        # Outside the grid counts as a wall
        wall_ahead = (
            ahead_x < 0
            or ahead_x >= self.width
            or ahead_y < 0
            or ahead_y >= self.height
            or (ahead_x, ahead_y) in self.walls
        )

        # Is there food at the current position?
        food_here = (
            tuple(self.agent_pos)
            in self.food_positions
        )

        return {
            'wall_ahead': wall_ahead,
            'food_here': food_here
        }

    # ---------------------------------------------------------
    # EXECUTE ACTION
    # ---------------------------------------------------------

    def execute_action(self, agent, action: str):
        self.steps += 1

        # -----------------------------------------------------
        # SUCK / COLLECT FOOD
        # -----------------------------------------------------

        if action == 'Suck':
            current_pos = tuple(self.agent_pos)

            if current_pos in self.food_positions:
                self.food_positions.remove(current_pos)
                self.score += 20

            return

        # -----------------------------------------------------
        # TURN LEFT
        # -----------------------------------------------------

        if action == 'TurnLeft':

            directions = [
                'Up',
                'Left',
                'Down',
                'Right'
            ]

            current_index = directions.index(self.facing)

            self.facing = directions[
                (current_index + 1) % 4
            ]

            return

        # -----------------------------------------------------
        # TURN RIGHT
        # -----------------------------------------------------

        if action == 'TurnRight':

            directions = [
                'Up',
                'Right',
                'Down',
                'Left'
            ]

            current_index = directions.index(self.facing)

            self.facing = directions[
                (current_index + 1) % 4
            ]

            return

        # -----------------------------------------------------
        # MOVE FORWARD
        # -----------------------------------------------------

        if action == 'MoveForward':
            action = self.facing

        # -----------------------------------------------------
        # UPDATE FACING DIRECTION
        # -----------------------------------------------------

        if action in [
            'Up',
            'Down',
            'Left',
            'Right'
        ]:
            self.facing = action

        # Start from current position
        new_pos = list(self.agent_pos)

        # -----------------------------------------------------
        # CALCULATE NEW POSITION
        # -----------------------------------------------------

        if action == 'Up':
            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        elif action == 'Down':
            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        elif action == 'Left':
            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        elif action == 'Right':
            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # -----------------------------------------------------
        # WALL COLLISION
        # -----------------------------------------------------

        if tuple(new_pos) in self.walls:

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # -----------------------------------------------------
        # FOOD
        # -----------------------------------------------------

        tuple_pos = tuple(self.agent_pos)

        if tuple_pos in self.food_positions:

            self.food_positions.remove(tuple_pos)

            self.score += 20

    # ---------------------------------------------------------
    # GAME END
    # ---------------------------------------------------------

    def is_done(self) -> bool:

        return (
            len(self.food_positions) == 0
            or self.steps >= 40
        )