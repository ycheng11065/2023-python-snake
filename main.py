# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we"ve included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

#Value constants
FOOD_VALUE = 2
HEAD_KILL_VALUE = 3;
MIN_MOVE_VALUE = float('-inf')
DEFAULT_MOVE_VALUE = 0;
# HEALTH_TRESHOLD = 40;

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#4C0099",  # TODO: Choose color
        "head": "",  # TODO: Choose head
        "tail": "",  # TODO: Choose tail
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
    collision(game_state,is_move_safe)
      
    # Are there any safe moves left?
    safe_moves = {}
    available_moves = []
    for move, isSafe in is_move_safe.items():
        # print(f"Move:{move}, Value:{isSafe}")
        if isSafe >= DEFAULT_MOVE_VALUE: 
            safe_moves[f"{move}"] = isSafe
            available_moves.append(move)

    print(safe_moves);
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    findFood(game_state, safe_moves)

    best_value = max([value for _, value in safe_moves.items()])
    best_move = [move for move, value in safe_moves.items() if value == best_value]

    # Choose a random move from the best ones
    next_move = random.choice(best_move)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# Calculate the distance between the two entities
def calculateDist(a, b):
  return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"]);

# Prevents snake going backwards
def preventBack(game_state, is_move_safe):
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
      is_move_safe["left"] += MIN_MOVE_VALUE;

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
      is_move_safe["right"] += MIN_MOVE_VALUE

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
      is_move_safe["down"] += MIN_MOVE_VALUE

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
      is_move_safe["up"] += MIN_MOVE_VALUE
  

# Prevents the snake from going off board
def outOfBounds(game_state, is_move_safe):
   my_head = game_state["you"]["body"][0]
   board_width = game_state["board"]["width"]
   board_height = game_state["board"]["height"]

   if my_head["x"] >= board_width - 1:
     is_move_safe["right"] += MIN_MOVE_VALUE;
   if my_head["x"] <= 0:
     is_move_safe["left"] += MIN_MOVE_VALUE
   if my_head["y"] >= board_height - 1:
     is_move_safe["up"] += MIN_MOVE_VALUE
   if my_head["y"] <= 0:
     is_move_safe["down"] += MIN_MOVE_VALUE

# Prevents the snake from running into itself
def selfCollision(game_state, is_move_safe):
    my_body = game_state["you"]["body"]
    my_head = game_state["you"]["body"][0]
    head_x = my_head["x"];
    head_y = my_head["y"];

    for i in range(len(my_body)):
      currBody = my_body[i];
      currX = currBody["x"];
      currY = currBody["y"];
      
      if (head_x + 1 == currX and head_y == currY):              
        is_move_safe["right"] += MIN_MOVE_VALUE;
      elif (head_x - 1 == currX and head_y == currY):
        is_move_safe["left"] += MIN_MOVE_VALUE;
      elif (head_x == currX and head_y + 1 == currY):
        is_move_safe["up"] += MIN_MOVE_VALUE;
      elif (head_x == currX and head_y - 1 == currY):
        is_move_safe["down"] += MIN_MOVE_VALUE;


# Prevent snake from colliding to opponent body, control head collision
def collision(game_state, is_move_safe):
    my_id = game_state["you"]["id"];
    my_head = game_state["you"]["head"];
    head_x = my_head["x"];
    head_y = my_head["y"];
    my_size = game_state["you"]["length"];
    opponents = game_state["board"]["snakes"];
    for snake in opponents:
      opponent_id = snake["id"];
      opponent_head = snake["head"]
      opponent_size = snake["length"];

      # Skip if snake is our snake
      if (opponent_id == my_id): continue
          
      for currSnake_body in snake["body"]:
        currSnake_X = currSnake_body["x"];
        currSnake_Y = currSnake_body["y"];
        
        # Check Head, Add headkill value if snake can win head collision
        if (currSnake_body == opponent_head and my_size > opponent_size):
          if (head_x + 1 == currSnake_X and head_y ==  currSnake_Y):
            is_move_safe["right"] += HEAD_KILL_VALUE;
          elif (head_x - 1 == currSnake_X and head_y ==  currSnake_Y):
            is_move_safe["left"] = HEAD_KILL_VALUE;
          elif (head_x == currSnake_X and head_y + 1 ==  currSnake_Y):
            is_move_safe["up"] = HEAD_KILL_VALUE;
          elif (head_x == currSnake_X and head_y - 1 ==  currSnake_Y):
            is_move_safe["down"] = HEAD_KILL_VALUE;
          
        else:
          if (head_x + 1 == currSnake_X and head_y == currSnake_Y):
            is_move_safe["right"] += MIN_MOVE_VALUE;
          elif (head_x - 1 == currSnake_X and head_y == currSnake_Y):
            is_move_safe["left"] += MIN_MOVE_VALUE;
          elif (head_x == currSnake_X and head_y + 1 == currSnake_Y):
            is_move_safe["up"] += MIN_MOVE_VALUE;
          elif (head_x == currSnake_X and head_y - 1 == currSnake_Y):
            is_move_safe["down"] += MIN_MOVE_VALUE;   


def findFood(game_state, safe_moves):
    foods = game_state["board"]["food"]
    my_head = game_state["you"]["body"][0]
    head_x = my_head["x"];
    head_y = my_head["y"];
    closest_dist = float('inf')
    closest = {}

    # Find closest food
    for food in foods:
      curr_dist = calculateDist(my_head, food)
      if (curr_dist < closest_dist):
        closest = food;
        closest_dist = curr_dist;

    if (head_x < closest["x"] and "right" in safe_moves):
      #go right
      safe_moves["right"] += FOOD_VALUE
    elif (head_x > closest["x"] and "left" in safe_moves):
      #go left
      safe_moves["left"] += FOOD_VALUE
    elif (head_y < closest["y"] and "up" in safe_moves):
      #go up
      safe_moves["up"] += FOOD_VALUE
    elif (head_y > closest["y"] and "down" in safe_moves):
      #go down  
      safe_moves["down"] += FOOD_VALUE

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
