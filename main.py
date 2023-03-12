# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

#Value constants
FOOD_VALUE = 2
MIN_MOVE_VALUE = float('-inf')


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
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds (Timothy)
    outOfBounds(game_state, is_move_safe)

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    selfCollision(game_state, is_move_safe)

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    collision(game_state,is_move_safe)
      
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    findFood(game_state)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def calculateDist(a, b):
  return abs(a['x'] - b['x']) + abs(a['y'] - b['y']);

def outOfBounds(game_state, is_move_safe):
   my_head = game_state["you"]["body"][0]
   board_width = game_state['board']['width']
   board_height = game_state['board']['height']

   if my_head["x"] >= board_width - 1:
     is_move_safe["right"] = False
   if my_head["x"] <= 0:
     is_move_safe["left"] = False
   if my_head["y"] >= board_height - 1:
     is_move_safe["up"] = False
   if my_head["y"] <= 0:
     is_move_safe["down"] = False


def selfCollision(game_state, is_move_safe):
    my_body = game_state['you']['body']
    my_head = game_state['you']['head'];
    head_x = my_head['x'];
    head_y = my_head['y'];

    for i in range(len(my_body)):
      currBody = my_body[i];
      currX = currBody['x'];
      currY = currBody['y'];
      
      if (head_x + 1 == currX and head_y == currY):              
        is_move_safe["right"] = False;
      elif (head_x - 1 == currX and head_y == currY):
        is_move_safe["left"] = False;
      elif (head_x == currX and head_y + 1 == currY):
        is_move_safe["up"] = False;
      elif (head_x == currX and head_y - 1 == currY):
        is_move_safe["down"] = False;

def collision(game_state, is_move_safe):
    my_head = game_state['you']['head'];
    head_x = my_head['x'];
    head_y = my_head['y'];
    my_size = game_state['you']['length'];
    opponents = game_state['board']['snakes'];
    for snake in opponents:
      opponent_head = snake['head']
      opponent_head_x = opponent_head['x'];
      opponent_head_y = opponent_head['y'];
      opponent_size = snake['length'];
      if (my_size > opponent_size):
        if (head_x + 1 == opponent_head_x and head_y == opponent_head_y):
          is_move_safe["right"] = True;
        elif (head_x - 1 == opponent_head_x and head_y == opponent_head_y):
          is_move_safe["left"] = True;
        elif (head_x == opponent_head_x and head_y + 1 == opponent_head_y):
          is_move_safe["up"] = True;
        elif (head_x == opponent_head_x and head_y - 1 == opponent_head_y):
          is_move_safe["down"] = True;
      
      for currSnake_body in snake['body']:
        currSnake_X = currSnake_body['x'];
        currSnake_Y = currSnake_body['y'];
        if (head_x + 1 == currSnake_X and head_y == currSnake_Y):
          is_move_safe["right"] = False;
        elif (head_x - 1 == currSnake_X and head_y == currSnake_Y):
          is_move_safe["left"] = False;
        elif (head_x == currSnake_X and head_y + 1 == currSnake_Y):
          is_move_safe["up"] = False;
        elif (head_x == currSnake_X and head_y - 1 == currSnake_Y):
          is_move_safe["down"] = False;  


def findFood(game_state):
   foods = game_state['board']['food']
   my_head = game_state["you"]["body"][0]
   head_x = my_head['x'];
   head_y = my_head['y'];
   closest_dist = float("inf")
   closest = {}
  
   for i in foods:
     curr_dist = calculateDist(my_head, i)
     if (curr_dist < closest_dist):
      closest = i;
      closest_dist = curr_dist;

    # if (head_x < closest['x']):
    #   #go right
    # elif (head_x > closest['x']):
    #   #go left
    # elif (head_y < closest['y']):
    #   #go up
    # elif (head_y > closest['y']):
    #   #go down  

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
