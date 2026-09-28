from visual_grid_game import VisualGridHuntGame
from agent import SearchAgent


def run_search_agent(algorithm):

    print()
    print("======================================")
    print(f" Running {algorithm} Search Agent")
    print("======================================")

    # Create the environment
    env = VisualGridHuntGame(
        width=10,
        height=10,
        num_food=10,
        num_opponents=0
    )

    # Create the search agent
    agent = SearchAgent()

    # Select BFS, DFS or UCS
    agent.active_algo = algorithm

    while not env.is_done():

        # Get the current percept
        percept = env.get_percept()

        # Ask the agent for the next action
        action = agent.sense_and_act(percept)

        print(
            f"Position: {percept['agent_pos']} | "
            f"Action: {action} | "
            f"Score: {percept['score']} | "
            f"Food Left: {percept['remaining_food']}"
        )

        # Execute the selected action
        env.execute_action(action)

    print()
    print(f"{algorithm} Search Agent finished!")
    print(f"Final Score: {env.score}")
    print(f"Steps: {env.steps}")
    print(f"Food Remaining: {len(env.food_positions)}")


if __name__ == "__main__":

    run_search_agent('BFS')

    run_search_agent('DFS')

    run_search_agent('UCS')