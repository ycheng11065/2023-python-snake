import random
import typing
from snake_basic_behaviors import *
from snake_strategy_behaviors import *


# ----------------------------------------------------------------------------
# SERVER STUFF
# -----------------------------------------------------------------------------


def info() -> typing.Dict:
    print("INFO")
    
    # Customizations
    return {
        "apiversion": "1",
        "author": "Netrix",  
        "color": "#BBADFF",  
        "head": "safe",  
        "tail": "nr-booster",  
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # state = game_state
    is_move_safe = {
        "up": DEFAULT_MOVE_VALUE,
        "down": DEFAULT_MOVE_VALUE,
        "left": DEFAULT_MOVE_VALUE,
        "right": DEFAULT_MOVE_VALUE
    }

    # We've included code to prevent your Battlesnake from moving backwards
    preventBack(game_state, is_move_safe)

    # Prevent your Battlesnake from moving out of bounds (Timothy)
    outOfBounds(game_state, is_move_safe)

    # Prevent your Battlesnake from colliding with itself
    selfCollision(game_state, is_move_safe)

    # Prevent your Battlesnake from colliding with other Battlesnakes
    collision(game_state, is_move_safe)

    # Are there any safe moves left?
    safe_moves = {}
    available_moves = []
    for move, isSafe in is_move_safe.items():
        # print(f"Move:{move}, Value:{isSafe}")
        if isSafe >= DEFAULT_MOVE_VALUE:
            safe_moves[f"{move}"] = isSafe
            available_moves.append(move)

    selected_move = miniMax_value(game_state, safe_moves)

    print(game_state)
    # print(safe_moves)
    if (len(safe_moves) == 0 and selected_move is None):
        board_copy = createBoardState(game_state)
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        for row in board_copy["state_board"]:
            format_row = " ".join(str(el).rjust(2, ' ') for el in row)
            print(format_row)
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # findFood(game_state, safe_moves)

    # best_value = max([value for _, value in safe_moves.items()])
    # best_move = [move for move, value in safe_moves.items()
    #              if value == best_value]

    # Choose a random move from the best ones
    best_move = [move for move, value in safe_moves.items()]

    if (selected_move is None):
        if (len(safe_moves) > 0):
            next_move = random.choice(best_move)
    else:
        next_move = selected_move
    print(
        f"MOVE {game_state['turn']}: {next_move}, SNAKE HEALTH: {game_state['you']['health']}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })


# TODO:
# Runs out of health
# Not aggressive when it is bigger
# does not try to edge kill
# does not create loops when in danger 


# TODO multi snake:
# Prevent the snake going in between snakes
# Snake go into circle if surrounded by bigger snakes
# snake does not go to spaces that it cannot come out of
# Weak against snakes that come down from center and edge choke our snake
# Edge kill from more than just border