class SimpleReflexAgent:
    """Simple Reflex Agent using only the current percept."""

    def sense_and_act(self, percept: dict) -> str:

        # IF food is here THEN suck it
        if percept['food_here']:
            return 'Suck'

        # IF wall is ahead THEN turn left
        if percept['wall_ahead']:
            return 'TurnLeft'

        # ELSE move forward
        return 'MoveForward'

class ModelBasedAgent:
    """
    Model-Based Agent.

    Uses internal memory of visited positions and previously
    encountered states to avoid repeatedly following the same path.
    """

    def __init__(self):
        self.estimated_pos = [0, 0]
        self.facing = 'Right'

        # Memory
        self.visited_cells = {(0, 0)}
        self.visited_states = set()

        self.last_action = None
        self.last_percept = None

    def move_position(self, position, direction):
        x, y = position

        if direction == 'Up':
            return (x, y + 1)
        elif direction == 'Down':
            return (x, y - 1)
        elif direction == 'Left':
            return (x - 1, y)
        elif direction == 'Right':
            return (x + 1, y)

        return (x, y)

    def turn_left_direction(self):
        directions = ['Up', 'Left', 'Down', 'Right']
        index = directions.index(self.facing)
        self.facing = directions[(index + 1) % 4]

    def turn_right_direction(self):
        directions = ['Up', 'Right', 'Down', 'Left']
        index = directions.index(self.facing)
        self.facing = directions[(index + 1) % 4]

    def update_internal_state(self):

        # Update position after previous MoveForward
        if self.last_action == 'MoveForward':

            if self.last_percept is not None:
                if not self.last_percept['wall_ahead']:

                    new_position = self.move_position(
                        self.estimated_pos,
                        self.facing
                    )

                    self.estimated_pos = list(new_position)

        # Update facing after previous turn
        elif self.last_action == 'TurnLeft':
            self.turn_left_direction()

        elif self.last_action == 'TurnRight':
            self.turn_right_direction()

        # Remember current position
        self.visited_cells.add(tuple(self.estimated_pos))

    def sense_and_act(self, percept: dict):

        # Update internal model from previous action
        self.update_internal_state()

        # Save current percept
        self.last_percept = percept.copy()

        current_state = (
            tuple(self.estimated_pos),
            self.facing
        )

        # Remember this state
        self.visited_states.add(current_state)

        # --------------------------------
        # Rule 1: Food
        # --------------------------------

        if percept['food_here']:
            self.last_action = 'Suck'
            return 'Suck'

        # --------------------------------
        # Rule 2: Wall ahead
        # --------------------------------

        if percept['wall_ahead']:

            # Change direction when blocked
            self.last_action = 'TurnRight'
            return 'TurnRight'

        # --------------------------------
        # Rule 3: Avoid repeated states
        # --------------------------------

        forward_position = self.move_position(
            self.estimated_pos,
            self.facing
        )

        forward_position = tuple(forward_position)

        if forward_position in self.visited_cells:

            # Try changing direction instead of
            # continuing through an already visited cell.

            self.last_action = 'TurnRight'
            return 'TurnRight'

        # --------------------------------
        # Rule 4: Explore new location
        # --------------------------------

        self.last_action = 'MoveForward'
        return 'MoveForward'


class SimpleReflexAgent:
    """Simple Reflex Agent using only the current percept."""

    def sense_and_act(self, percept: dict):

        if percept['food_here']:
            return 'Suck'

        if percept['wall_ahead']:
            return 'TurnLeft'

        return 'MoveForward'