from grid_game import GridHuntGame
from agent import SimpleReflexAgent, ModelBasedAgent


def run_agent(agent, agent_name):

    print("\n======================================")
    print(f" Running {agent_name}")
    print("======================================")

    env = GridHuntGame()

    while not env.is_done():

        # Agent receives only its percept
        percept = env.get_percept(agent)

        # Agent chooses an action
        action = agent.sense_and_act(percept)

        # Environment executes the action
        env.execute_action(agent, action)

        print(
            f"Percept: {percept} | "
            f"Action: {action} | "
            f"Score: {env.score} | "
            f"Food Left: {len(env.food_positions)}"
        )

    print(
        f"\n{agent_name} finished!"
    )

    print(
        f"Final Score: {env.score}"
    )

    print(
        f"Steps: {env.steps}"
    )

    print(
        f"Food Remaining: "
        f"{len(env.food_positions)}"
    )


def run_grid_hunt():

    # ---------------------------------------------------------
    # SIMPLE REFLEX AGENT
    # ---------------------------------------------------------

    simple_agent = SimpleReflexAgent()

    run_agent(
        simple_agent,
        "Simple Reflex Agent"
    )

    # ---------------------------------------------------------
    # MODEL-BASED AGENT
    # ---------------------------------------------------------

    model_agent = ModelBasedAgent()

    run_agent(
        model_agent,
        "Model-Based Agent"
    )


if __name__ == "__main__":
    run_grid_hunt()