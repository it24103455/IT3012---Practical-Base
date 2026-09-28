# visual_grid_game.py
import random
import tkinter as tk
from agent import SearchAgent


class VisualGridHuntGame:
    """A flexible Pacman-style grid environment with support for configurable opponents and larger scales."""

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=2,
        num_traps=5,
        custom_walls=None
    ):
        # Grid dimensions
        self.width = width
        self.height = height

        # Agent starting position
        self.agent_pos = [0, 0]

        # Create walls
        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            # Generate some default scattered walls for a larger grid
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # ---------------------------------------------------------
        # FOOD GENERATION
        # ---------------------------------------------------------

        # Dynamically generate random food positions
        # avoiding walls and agent start position
        self.food_positions = set()

        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            pos_tuple = (fx, fy)

            if (
                pos_tuple != (0, 0)
                and pos_tuple not in self.walls
            ):
                self.food_positions.add(pos_tuple)

        # ---------------------------------------------------------
        # TOXIC TRAPS - NEW
        # ---------------------------------------------------------

        # Collection containing the positions of toxic traps
        self.toxic_traps = set()

        # Generate random toxic trap positions
        # avoiding:
        # 1. Agent starting position
        # 2. Walls
        # 3. Food
        while len(self.toxic_traps) < num_traps:

            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)

            trap_pos = (tx, ty)

            if (
                trap_pos != (0, 0)
                and trap_pos not in self.walls
                and trap_pos not in self.food_positions
            ):
                self.toxic_traps.add(trap_pos)

        # ---------------------------------------------------------
        # OPPONENT GENERATION
        # ---------------------------------------------------------

        # Generate adversarial opponents
        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            op_pos = [ox, oy]

            if (
                tuple(op_pos) != (0, 0)
                and tuple(op_pos) not in self.walls
                and tuple(op_pos) not in self.food_positions
                and tuple(op_pos) not in self.toxic_traps
            ):
                self.opponents.append(op_pos)

        # ---------------------------------------------------------
        # GAME STATE
        # ---------------------------------------------------------

        self.score = 0
        self.steps = 0
        self.collision = False

    # =============================================================
    # PERCEPTION SYSTEM
    # =============================================================

    def get_percept(self) -> dict:
        """
        Returns the information available to the agent.
        """

        return {
            'agent_pos': list(self.agent_pos),

            'opponent_positions': [
                list(op) for op in self.opponents
            ],

            'smells_food':
                tuple(self.agent_pos) in self.food_positions,

            'smells_toxin':
                tuple(self.agent_pos) in self.toxic_traps,

            'hit_wall':
                tuple(self.agent_pos) in self.walls,

            'collision':
                self.collision,

            'score':
                self.score,

            'remaining_food':
                len(self.food_positions),

            # Practical 03 additions
            'grid_size': (self.width, self.height),
            'walls': list(self.walls),
            'all_food': list(self.food_positions)
                

        }

    # =============================================================
    # ACTION EXECUTION
    # =============================================================

    def execute_action(self, action: str):

        # Increase number of steps
        self.steps += 1

        # Start with current agent position
        new_pos = list(self.agent_pos)

        # ---------------------------------------------------------
        # MOVE AGENT
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # WALL CHECK
        # ---------------------------------------------------------

        if tuple(new_pos) in self.walls:

            # Penalize the agent for hitting a wall
            self.score -= 5

        else:

            # Update the agent's actual position
            self.agent_pos = new_pos

        # ---------------------------------------------------------
        # FOOD CHECK
        # ---------------------------------------------------------

        tuple_pos = tuple(self.agent_pos)

        if tuple_pos in self.food_positions:

            # Remove food after collecting it
            self.food_positions.remove(tuple_pos)

            # Reward the agent
            self.score += 20

        # ---------------------------------------------------------
        # TOXIC TRAP CHECK - NEW
        # ---------------------------------------------------------

        if tuple_pos in self.toxic_traps:

            # Severe penalty for stepping on a toxic trap
            self.score -= 15

        # ---------------------------------------------------------
        # OPPONENT MOVEMENT
        # ---------------------------------------------------------

        for op in self.opponents:

            # Randomly select opponent movement
            move = random.choice([
                'Up',
                'Down',
                'Left',
                'Right',
                'Stay'
            ])

            if move == 'Up' and op[1] < self.height - 1:
                op[1] += 1

            elif move == 'Down' and op[1] > 0:
                op[1] -= 1

            elif move == 'Left' and op[0] > 0:
                op[0] -= 1

            elif move == 'Right' and op[0] < self.width - 1:
                op[0] += 1

            # -----------------------------------------------------
            # COLLISION CHECK
            # -----------------------------------------------------

            if op == self.agent_pos:

                # Severe collision penalty
                self.score -= 50

                self.collision = True

    # =============================================================
    # GAME END CONDITION
    # =============================================================

    def is_done(self) -> bool:

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


# =================================================================
# GUI
# =================================================================

class GridGameGUI:
    """Tkinter wrapper that dynamically scales cell sizes to keep larger grids on screen."""

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=12,
        num_opponents=2,
        num_traps=5,
        walls=None
    ):

        self.root = root

        self.agent = SearchAgent()
        self.agent.active_algo = 'AStar'


        self.root.title(
            "IT3012 - Scalable Multi-Agent Grid Hunt"
        )

        # Create the game environment
        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            num_traps=num_traps,
            custom_walls=walls
        )

        # ---------------------------------------------------------
        # CELL SIZE
        # ---------------------------------------------------------

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_w = self.env.width * self.cell_size
        canvas_h = self.env.height * self.cell_size

        # ---------------------------------------------------------
        # CANVAS
        # ---------------------------------------------------------

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        # ---------------------------------------------------------
        # SCORE LABEL
        # ---------------------------------------------------------

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        # ---------------------------------------------------------
        # START BUTTON
        # ---------------------------------------------------------

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12),
            bg="#000066",
            fg="white"
        )

        self.btn.pack(pady=5)

        # Draw initial grid
        self.draw_grid()

    # =============================================================
    # DRAW GRID
    # =============================================================

    def draw_grid(self):

        # Clear previous grid
        self.canvas.delete("all")

        # ---------------------------------------------------------
        # DRAW CELLS AND WALLS
        # ---------------------------------------------------------

        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = x * self.cell_size

                y1 = (
                    self.env.height - 1 - y
                ) * self.cell_size

                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Normal cell or wall
                color = (
                    "#f1f5f9"
                    if (x, y) not in self.env.walls
                    else "#64748b"
                )

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#cbd5e1"
                )

                # Draw W on walls if cell is large enough
                if (
                    self.cell_size >= 40
                    and (x, y) in self.env.walls
                ):

                    self.canvas.create_text(
                        x1 + self.cell_size / 2,
                        y1 + self.cell_size / 2,
                        text="W",
                        fill="white",
                        font=("Arial", 8, "bold")
                    )

        # ---------------------------------------------------------
        # DRAW FOOD
        # ---------------------------------------------------------

        for fx, fy in self.env.food_positions:

            offset = self.cell_size * 0.25

            x1 = (
                fx * self.cell_size
                + offset
            )

            y1 = (
                (self.env.height - 1 - fy)
                * self.cell_size
                + offset
            )

            self.canvas.create_oval(
                x1,
                y1,
                x1 + self.cell_size * 0.5,
                y1 + self.cell_size * 0.5,
                fill="#f59e0b",
                outline="#d97706"
            )

        # ---------------------------------------------------------
        # DRAW TOXIC TRAPS - NEW
        # ---------------------------------------------------------

        for tx, ty in self.env.toxic_traps:

            offset = self.cell_size * 0.2

            x1 = (
                tx * self.cell_size
                + offset
            )

            y1 = (
                (self.env.height - 1 - ty)
                * self.cell_size
                + offset
            )

            # Draw a purple diamond
            center_x = x1 + self.cell_size * 0.3
            center_y = y1 + self.cell_size * 0.3

            size = self.cell_size * 0.3

            self.canvas.create_polygon(
                center_x,
                center_y - size,
                center_x + size,
                center_y,
                center_x,
                center_y + size,
                center_x - size,
                center_y,
                fill="#800080",
                outline="#4B0082"
            )

        # ---------------------------------------------------------
        # DRAW OPPONENTS
        # ---------------------------------------------------------

        for ox, oy in self.env.opponents:

            offset = self.cell_size * 0.2

            x1 = (
                ox * self.cell_size
                + offset
            )

            y1 = (
                (self.env.height - 1 - oy)
                * self.cell_size
                + offset
            )

            self.canvas.create_rectangle(
                x1,
                y1,
                x1 + self.cell_size * 0.6,
                y1 + self.cell_size * 0.6,
                fill="#990000",
                outline="#7a0000"
            )

        # ---------------------------------------------------------
        # DRAW AGENT
        # ---------------------------------------------------------

        ax, ay = self.env.agent_pos

        offset = self.cell_size * 0.15

        x1 = (
            ax * self.cell_size
            + offset
        )

        y1 = (
            (self.env.height - 1 - ay)
            * self.cell_size
            + offset
        )

        self.canvas.create_oval(
            x1,
            y1,
            x1 + self.cell_size * 0.7,
            y1 + self.cell_size * 0.7,
            fill="#000066",
            outline="#1e3a8a"
        )

    # =============================================================
    # SIMULATION LOOP
    # =============================================================

    def run_loop(self):

        # Disable button while simulation is running
        self.btn.config(state="disabled")

        def step():

            if not self.env.is_done():

                percept = self.env.get_percept()
                action = self.agent.sense_and_act(percept)

               
                # Execute action
                self.env.execute_action(action)

                # Redraw the grid
                self.draw_grid()

                # Update score and step information
                self.label.config(
                    text=(
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps} | "
                        f"Action: {action}"
                    )
                )

                # Run next step after 250 milliseconds
                self.root.after(
                    250,
                    step
                )

            else:

                if self.env.collision:

                    end_text = (
                        f"Collision! Game Over! "
                        f"Final Score: {self.env.score}"
                    )

                else:

                    end_text = (
                        f"Finished! "
                        f"Final Score: {self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                # Enable button again
                self.btn.config(
                    state="normal"
                )

        # Start simulation
        step()


# =================================================================
# MAIN PROGRAM
# =================================================================

if __name__ == "__main__":

    root = tk.Tk()

    # Create a 12x12 grid
    # with 15 food items,
    # 3 opponents,
    # and 5 toxic traps
    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=3,
        num_traps=5
    )

    root.mainloop()