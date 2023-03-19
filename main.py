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
import copy

#Value constants
FOOD_VALUE = 2
HEAD_KILL_VALUE = 3
MIN_MOVE_VALUE = float('-inf')
DEFAULT_MOVE_VALUE = 0
HEALTH_THRESHOLD = 40

# state = None

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
        board_copy = createState(game_state);
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        # for row in board_copy:
        #   format_row = " ".join(str(el).rjust(2, ' ') for el in row);
        #   print(format_row)
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    findFood(game_state, safe_moves)

    best_value = max([value for _, value in safe_moves.items()])
    best_move = [move for move, value in safe_moves.items() if value == best_value]

    # Choose a random move from the best ones
    next_move = random.choice(best_move)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

# ----------------------------------------------------------------------------
# SNAKE BASIC BEHAVIOR
#-----------------------------------------------------------------------------

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
    health = game_state["you"]["health"]
    my_head = game_state["you"]["body"][0]
    head_x = my_head["x"];
    head_y = my_head["y"];
    closest_dist = float('inf')
    closest = {}

    if (health > HEALTH_THRESHOLD): return
      
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

# ----------------------------------------------------------------------------
# SNAKE STRATEGY BEHAVIOR
#-----------------------------------------------------------------------------

# Generates a copy of current game board and another board that tracks snake head positions
def createBoardState(game_state):
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    foods = game_state["board"]["food"]
    our_snake_id = game_state["you"]["id"]
    all_snake = game_state["board"]["snakes"]
      # 0 is empty space
      # 1 is food
      # 2 is snake head
  
      # id = corresponding snake body
      # snake head is represented in head_board as the corresponding snake id
  
    board_copy = [[0 for _ in range(board_width)] for _ in range(board_height)]
    head_board = [["" for _ in range(board_width)] for _ in range(board_height)]
  
    for food in foods:
      food_x = food["x"]
      food_y = abs(board_height - 1 - food["y"])
      board_copy[food_y][food_x] = 1;
      
    for snake in all_snake:
      snake_id = snake["id"]
      snake_head = snake["head"];
      
      for body in snake["body"]:
        body_x = body["x"];
        body_y = abs(board_height - 1 - body["y"])
        if (body == snake_head):
          board_copy[body_y][body_x] = 2
          head_board[body_y][body_x] = snake_id
        else:
          board_copy[body_y][body_x] = snake_id

    board_state = {
      "state_board": board_copy,
      "head_board": head_board
    }
  
    return board_state
  
# Create an array of snakes, each snake is a dict containing id, head and body coord
def snakeState(game_state):
    snakes = game_state["board"]["snakes"]
  
    snake_state = []
    for snake in snakes:
      snake_id = snake["id"]
      snake_head = snake["head"]
      snake_body = [dict(coord) for coord in snake["body"]]
  
      snake_state.append({
        "id": snake_id,
        "head": snake_head,
        "body": snake_body
      })
      
        
    return snake_state

# Create an entire copy of the current game state, including current board, snakes and curr snake id 
def createGameState(game_state, curr_snake_id):
  game_state_copy = {}

  game_state_copy["board"] = createBoardState(game_state)
  game_state_copy["snakes"] = snakeState(game_state)
  game_state_copy["curr_snake_id"] = curr_snake_id;

  
# Update the current snakes's head coordinates
def updateSnakeHead(new_snake_state, curr_snake_index, x_coord, y_coord):
    new_snake_state[curr_snake_index]["head"]["x"] = x_coord
    new_snake_state[curr_snake_index]["head"]["y"] = y_coord
    new_snake_state[curr_snake_index]["body"][0]["x"] = x_coord
    new_snake_state[curr_snake_index]["body"][0]["y"] = y_coord
  
  
# Update the current snake's body part coordinates
def updateSnakeBody(new_snake_state, curr_snake_index, body_index, x_coord, y_coord):
    new_snake_state[curr_snake_index]["body"][body_index]["x"] = x_coord
    new_snake_state[curr_snake_index]["body"][body_index]["y"] = y_coord

  
# Update the snake's movement location in the new board and head state, also updates snake state's coords
def moveForward(new_board_state, new_head_state, new_snake_state, curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y):
  prev_x, prev_y = None, None

  body_index = 0
  for body in curr_snake_body:
    curr_x = body["x"]
    curr_y = body["y"]

    if (body == curr_snake_body[0]):
      new_board_state[head_y][head_x] = 2
      new_head_state[head_y][head_x] = curr_snake_id
      updateSnakeHead(new_snake_state, curr_snake_index, head_x, head_y)
    else:
      if (new_head_state[prev_y][prev_x] == curr_snake_id):
        new_head_state[prev_y][prev_x] = 0;
      if (body_index > 0):
        updateSnakeBody(new_snake_state, curr_snake_index, body_index, prev_y, prev_x)
      new_board_state[prev_y][prev_x] = curr_snake_id
      
    prev_x = curr_x
    prev_y = curr_y
    body_index += 1

    
# Update snake state from snake eating food, duplicate tail and add as new tail
def snakeStateFoodGrow(new_snake_state, curr_snake_index):
  last_body = new_snake_state[curr_snake_index]["body"][-1]
  last_x , last_y = last_body["x"], last_body["y"]
  new_snake_state[curr_snake_index]["body"].append({"x": last_x, "y": last_y})


# Remove killed snake from the snake state list
def removeKilledSnake(new_snake_state, killed_snake_index):
    new_stake_state.pop(killed_snake_index)
    

# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
  board_width = len(game_state["board"]["state_board"][0])
  board_height = len(game_state["board"]["state_board"])

  # new game state to update, change the id to current snake
  new_game_state = copy.deepcopy(game_state)
  new_board_state = new_game_state["board"]["state_board"]
  new_head_state = new_game_state["board"]["head_board"]
  new_snake_state = new_game_state["snakes"]
  new_game_state["curr_snake_id"] = curr_snake_id
  
  # Our destination coordinate after performing move
  head_x, head_y = None, None

  # find current snake's head 
  for y in range(board_height):
    for x in range(board_width):
      if (new_head_state[y][x] == curr_snake_id):
        head_x = x
        head_y = y
        break;
    if (head_x != None):
      break

  #Update head coordinate value to destination after move is applied
  if (move == "up"):
    head_y = head_y + 1
  elif (move == "down"):
    head_y = head_y - 1
  elif (move == "left"):
    head_x = head_x - 1
  elif (move == "right"):
    head_x = head_x + 1

  
  destination_cell = new_board_state[head_y][head_x]
  destination_cell_head = new_head_state[head_y][head_x]

  curr_snake_index = 0
  curr_snake_length = 0
  curr_snake_body = None
  curr_snake_head = None

  # find our current snake
  for i in range(len(new_snake_state)):
    curr_snake = new_snake_state[i]
    if (curr_snake["id"] == curr_snake_id):
      curr_snake_index = i
      curr_snake_body = curr_snake["body"]
      curr_snake_length = len(curr_snake_body)
      curr_snake_head = curr_snake["head"]
  
  # Check if snake dies or the destination is invalid if this move is performed
  if (head_x < 0 or head_y < 0 or head_x >= board_width or head_y >= board_height or destination_cell not in [0,1]):
    
    # Check if collision is with the head of a snake smaller than current snake
    if (destination_cell == 2 and destination_cell_head != 0):
      destination_snake_length = 0
      destination_snake_body = None
      destination_snake_id = None
      destination_snake_index = 0
      
      # Find the snake the current snake is about to collide with
      for snake in new_snake_state:
        if (snake["id"] == destination_cell_head):
          destination_snake_id = snake["id"]
          destination_snake_body = snake["body"]
          destination_snake_length = len(destination_snake_body)
          break

        destination_snake_index += 1
          
      # Our size is bigger, else we return None signifying that we died
      if (destination_snake_length < curr_snake_length):

        # Remove the destination snake
        for body in destination_snake_body:
          body_x = body["x"]
          body_y = body["y"]

          new_board_state[body_y][body_x] = 0

        # Snake moves forward and updates all coords in new game state
        moveForward(new_board_state, new_head_state, new_snake_state, curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

        # Remove killed snake from snake state list
        removeKilledSnake(new_snake_State, destination_snake_index)

        return new_game_state 
      
      else:
        return None

    return None

  # Snake move to a cell with food
  elif (destination_cell == 1):

    # Snake moves forward and updates all coords in new game state
    moveForward(new_board_state, new_head_State, new_snake_state, curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

    # add a new body part
    snakeStateFoodGrow(new_snake_state, curr_snake_index)
    
    return new_game_state

  # Snake's regular movement to empty spaces
  else:

    # Snake moves forward and updates all coords in new game state
    moveForward(new_board_state, new_head_State, new_snake_state, curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)
    
    return new_game_state


# def gameOver(state):
#    # Implement this function to check if the game is over based on the current state
#    # For example, check if the snake has collided with a wall or another snake
#    pass

# The snake MiniMax algorithm
def miniMax(game_state, depth, maximizing_player, curr_snake_id):
    # when given game_state is over, return the current state point
    if (depth == 0 or gameOver(game_state) == True) { #todo
      return evaluatePoint(game_state, depth, curr_snake_id)  #todo
    }

    # get the id of the next snake that were gonna minimax
    curr_index = 0
    for index, snake in enumerate(game_state["snakes"]):
      if (snake["id"] == curr_snake_id):
        curr_index = index
        break

    next_snake_id = game_state["snakes"][(curr_index + 1) % len(game_state["snakes"])]["id"]

    moves = ["up", "down", "right", "left"]
  
    if (maximizing_player):
      highest_value = float(-inf)
      for move in moves:
        new_game_state = makeMove(game_state, curr_snake_id, move) #todo
        curr_val = miniMax(new_game_state, depth - 1, false, next_snake_id)
        highest_value = max(highest_value, curr_val)
      return best_value
    else:
      min_value = float(inf)
      for move in moves:
        new_game_state = makeMove(game_state, curr_snake_id, move) #todo
        curr_val = miniMax(new_game_state, depth - 1, false, next_snake_id)
        min_value = min(min_value, curr_val)
      return min_value
      
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
        "move": move, 
        "end": end
    })
