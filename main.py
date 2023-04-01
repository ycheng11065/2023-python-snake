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
from collections import deque

# Value constants
FOOD_VALUE = 2
HEAD_KILL_VALUE = 3
MIN_MOVE_VALUE = float("-inf")
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
    collision(game_state, is_move_safe)

    # Are there any safe moves left?
    safe_moves = {}
    available_moves = []
    for move, isSafe in is_move_safe.items():
        # print(f"Move:{move}, Value:{isSafe}")
        if isSafe >= DEFAULT_MOVE_VALUE:
            safe_moves[f"{move}"] = isSafe
            available_moves.append(move)

    print(safe_moves)
    if len(safe_moves) == 0:
        board_copy = createBoardState(game_state)
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        for row in board_copy["state_board"]:
            format_row = " ".join(str(el).rjust(2, ' ') for el in row)
            print(format_row)
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # findFood(game_state, safe_moves)

    miniMax_value(game_state, safe_moves)

    best_value = max([value for _, value in safe_moves.items()])
    best_move = [move for move, value in safe_moves.items()
                 if value == best_value]

    # Choose a random move from the best ones
    next_move = random.choice(best_move)
    print(
        f"MOVE {game_state['turn']}: {next_move}, SNAKE HEALTH: {game_state['you']['health']}")
    return {"move": next_move}

# ----------------------------------------------------------------------------
# SNAKE BASIC BEHAVIOR
# -----------------------------------------------------------------------------

# Calculate the distance between the two entities


def calculateDist(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

# Prevents snake going backwards


def preventBack(game_state, is_move_safe):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] += MIN_MOVE_VALUE

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
        is_move_safe["right"] += MIN_MOVE_VALUE
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
    head_x = my_head["x"]
    head_y = my_head["y"]

    for i in range(len(my_body)):
        currBody = my_body[i]
        currX = currBody["x"]
        currY = currBody["y"]

        if (head_x + 1 == currX and head_y == currY):
            is_move_safe["right"] += MIN_MOVE_VALUE
        elif (head_x - 1 == currX and head_y == currY):
            is_move_safe["left"] += MIN_MOVE_VALUE
        elif (head_x == currX and head_y + 1 == currY):
            is_move_safe["up"] += MIN_MOVE_VALUE
        elif (head_x == currX and head_y - 1 == currY):
            is_move_safe["down"] += MIN_MOVE_VALUE


# Prevent snake from colliding to opponent body, control head collision
def collision(game_state, is_move_safe):
    my_id = game_state["you"]["id"]
    my_head = game_state["you"]["head"]
    head_x = my_head["x"]
    head_y = my_head["y"]
    my_size = game_state["you"]["length"]
    opponents = game_state["board"]["snakes"]
    for snake in opponents:
        opponent_id = snake["id"]
        opponent_head = snake["head"]
        opponent_size = snake["length"]

        # Skip if snake is our snake
        if (opponent_id == my_id):
            continue

        for currSnake_body in snake["body"]:
            currSnake_X = currSnake_body["x"]
            currSnake_Y = currSnake_body["y"]

            # Check Head, Add headkill value if snake can win head collision
            if (currSnake_body == opponent_head and my_size > opponent_size):
                if (head_x + 1 == currSnake_X and head_y == currSnake_Y):
                    is_move_safe["right"] += HEAD_KILL_VALUE
                elif (head_x - 1 == currSnake_X and head_y == currSnake_Y):
                    is_move_safe["left"] = HEAD_KILL_VALUE
                elif (head_x == currSnake_X and head_y + 1 == currSnake_Y):
                    is_move_safe["up"] = HEAD_KILL_VALUE
                elif (head_x == currSnake_X and head_y - 1 == currSnake_Y):
                    is_move_safe["down"] = HEAD_KILL_VALUE

            else:
                if (head_x + 1 == currSnake_X and head_y == currSnake_Y):
                    is_move_safe["right"] += MIN_MOVE_VALUE
                elif (head_x - 1 == currSnake_X and head_y == currSnake_Y):
                    is_move_safe["left"] += MIN_MOVE_VALUE
                elif (head_x == currSnake_X and head_y + 1 == currSnake_Y):
                    is_move_safe["up"] += MIN_MOVE_VALUE
                elif (head_x == currSnake_X and head_y - 1 == currSnake_Y):
                    is_move_safe["down"] += MIN_MOVE_VALUE


def findFood(game_state, safe_moves):
    foods = game_state["board"]["food"]
    health = game_state["you"]["health"]
    my_head = game_state["you"]["body"][0]
    head_x = my_head["x"]
    head_y = my_head["y"]
    closest_dist = float('inf')
    closest = {}

    if (health > HEALTH_THRESHOLD):
        return

    # Find closest food
    for food in foods:
        curr_dist = calculateDist(my_head, food)
        if (curr_dist < closest_dist):
            closest = food
            closest_dist = curr_dist

    if (head_x < closest["x"] and "right" in safe_moves):
        # go right
        safe_moves["right"] += FOOD_VALUE
    elif (head_x > closest["x"] and "left" in safe_moves):
        # go left
        safe_moves["left"] += FOOD_VALUE
    elif (head_y < closest["y"] and "up" in safe_moves):
        # go up
        safe_moves["up"] += FOOD_VALUE
    elif (head_y > closest["y"] and "down" in safe_moves):
        # go down
        safe_moves["down"] += FOOD_VALUE

# ----------------------------------------------------------------------------
# SNAKE STRATEGY BEHAVIOR
# -----------------------------------------------------------------------------

# Generates a copy of current game board and another board that tracks snake head positions


def createBoardState(game_state):
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    foods = game_state["board"]["food"]
    all_snake = game_state["board"]["snakes"]
    # 0 is empty space
    # 1 is food
    # 2 is snake head

    # id = corresponding snake body
    # snake head is represented in head_board as the corresponding snake id

    board_copy = [[0 for _ in range(board_width)] for _ in range(board_height)]
    head_board = [["0" for _ in range(board_width)]
                  for _ in range(board_height)]

    for food in foods:
        food_x = food["x"]
        food_y = board_height - 1 - food["y"]
        board_copy[food_y][food_x] = 1

    for snake in all_snake:
        snake_id = snake["id"]
        snake_head = snake["head"]

        for body in snake["body"]:
            body_x = body["x"]
            body_y = board_height - 1 - body["y"]
            if (body == snake_head):
                board_copy[body_y][body_x] = 2
                head_board[body_y][body_x] = snake_id[-2:]
            else:
                board_copy[body_y][body_x] = snake_id[-2:]

    board_state = {
        "state_board": board_copy,
        "head_board": head_board
    }

    return board_state

# Create an array of snakes, each snake is a dict containing id, head and body coord


def snakeState(game_state):
    snakes = game_state["board"]["snakes"]
    board_height = game_state["board"]["height"]

    snake_state = []
    for snake in snakes:
        snake_id = snake["id"]
        health = snake["health"]
        snake_head = {"x": snake["head"]["x"],
                      "y": board_height - 1 - snake["head"]["y"]}
        snake_body = []
        for body in snake["body"]:
            body_x = body["x"]
            body_y = body["y"]
            snake_body.append({"x": body_x, "y": board_height - 1 - body_y})
        # snake_body = [dict(coord) for coord in snake["body"]]

        snake_state.append({
            "id": snake_id,
            "head": snake_head,
            "body": snake_body,
            "health": health
        })

    return snake_state


# Create an entire copy of the current game state, including current board, snakes and curr snake id
def createGameState(game_state, curr_snake_id):
    game_state_copy = {}

    game_state_copy["turn"] = game_state["turn"]
    game_state_copy["board"] = createBoardState(game_state)
    game_state_copy["snakes"] = snakeState(game_state)
    game_state_copy["curr_snake_id"] = curr_snake_id

    return game_state_copy


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


# Update snake's health, -1 health for every turn or 0 if snake dies
def updateSnakeHealth(new_snake_state, curr_snake_index, isAlive, hasAte):
    if (hasAte):
        new_snake_state[curr_snake_index]["health"] = 100
    elif (isAlive):
        new_snake_state[curr_snake_index]["health"] -= 1
    else:
        new_snake_state[curr_snake_index]["health"] = 0

    return new_snake_state[curr_snake_index]["health"]


# Update the snake's movement location in the new board and head state, also updates snake state's coords
def moveForward(new_board_state, new_head_state, new_snake_state, curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y):
    prev_x, prev_y = None, None

    body_index = 0
    for body in curr_snake_body:
        curr_x = body["x"]
        curr_y = body["y"]

        new_board_state[curr_y][curr_x] = 0

        if (body_index == 0):
            new_board_state[head_y][head_x] = 2
            new_head_state[head_y][head_x] = curr_snake_id[-2:]
            updateSnakeHead(new_snake_state, curr_snake_index, head_x, head_y)
        else:
            if (new_head_state[prev_y][prev_x] == curr_snake_id[-2:]):
                new_head_state[prev_y][prev_x] = "0"
            if (body_index > 0):
                updateSnakeBody(new_snake_state, curr_snake_index,
                                body_index, prev_x, prev_y)
            new_board_state[prev_y][prev_x] = curr_snake_id[-2:]

        prev_x = curr_x
        prev_y = curr_y
        body_index += 1


# Update snake state from snake eating food, duplicate tail and add as new tail
def snakeStateFoodGrow(new_snake_state, curr_snake_index):
    last_body = new_snake_state[curr_snake_index]["body"][-1]
    last_x, last_y = last_body["x"], last_body["y"]
    new_snake_state[curr_snake_index]["body"].append(
        {"x": last_x, "y": last_y})


# Replace body part value to 0, removing the killed snake from game board and head board
def removeKilledSnakeBody(new_board_state, new_head_state, new_snake_state, snake_index):
    snake_body = new_snake_state[snake_index]["body"]
    snake_head = new_snake_state[snake_index]["head"]

    for body in snake_body:
        body_x = body["x"]
        body_y = body["y"]

        if (body == snake_head):
            new_head_state[body_y][body_x] = 0
        new_board_state[body_y][body_x] = 0


# Remove killed snake from the snake state list and board
def removeKilledSnake(new_board_state, new_head_state, new_snake_state, snake_index):
    removeKilledSnakeBody(new_board_state, new_head_state, new_snake_state, snake_index)
    new_snake_state.pop(snake_index)


# Find snake corresponding to the given current ID and return its info
def findCurrentSnake(new_snake_state, curr_snake_id):
    curr_snake_index = 0
    curr_snake_length = 0
    curr_snake_body = None
    curr_snake_health = 0

    for i in range(len(new_snake_state)):
        curr_snake = new_snake_state[i]
        if (curr_snake["id"] == curr_snake_id):
            curr_snake_index = i
            curr_snake_body = curr_snake["body"]
            curr_snake_length = len(curr_snake_body)
            curr_snake_health = curr_snake["health"]

    return curr_snake_index, curr_snake_length, curr_snake_body, curr_snake_health


# Creates a deep copy of current game state to create a new game state
def createNewGameState(game_state, curr_snake_id):
    new_game_state = copy.deepcopy(game_state)
    new_board_state = new_game_state["board"]["state_board"]
    new_head_state = new_game_state["board"]["head_board"]
    new_snake_state = new_game_state["snakes"]
    new_game_state["turn"] = game_state["turn"] + 1
    new_game_state["curr_snake_id"] = curr_snake_id

    return new_game_state, new_board_state, new_head_state, new_snake_state


# Find current snake's head coordinates
def findHeadCoord(width, height, new_head_state, curr_snake_id):
    head_x, head_y = None, None
    
    for y in range(height):
        for x in range(width):
            if (new_head_state[y][x] == curr_snake_id[-2:]):
                head_x = x
                head_y = y
                break
        if (head_x != None):
            break
        
    return head_x, head_y


# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
    board_width = len(game_state["board"]["state_board"][0])
    board_height = len(game_state["board"]["state_board"])

    # new game state to update, change the id to current snake
    new_game_state, new_board_state, new_head_state, new_snake_state = createNewGameState(game_state, curr_snake_id)


    # Our snake's head coordinates
    head_x, head_y = findHeadCoord(board_width, board_height, new_head_state, curr_snake_id)

    # Current snake does not exist
    if (head_x is None or head_y is None):
        return None

    # Update head coordinate value to destination after move is applied
    if (move == "up"):
        head_y = head_y - 1
    elif (move == "down"):
        head_y = head_y + 1
    elif (move == "left"):
        head_x = head_x - 1
    elif (move == "right"):
        head_x = head_x + 1

    # Acquire current snake info
    curr_snake_index, curr_snake_length, curr_snake_body, curr_snake_health = findCurrentSnake(
        new_snake_state, curr_snake_id)

    # Check if snake destination hits border
    if not (0 <= head_x < board_width and 0 <= head_y < board_height):
        removeKilledSnake(new_board_state, new_head_state, new_snake_state, curr_snake_index)
        updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
        return new_game_state

    destination_cell = new_board_state[head_y][head_x]
    destination_cell_head = new_head_state[head_y][head_x][-2:]

    # Checks if snake runs into another snake or edge boundary
    if (destination_cell not in [0, 1]):

        # Check if collision is with the head of a snake
        if (destination_cell == 2 and destination_cell_head != 0):
            destination_snake_length = 0
            destination_snake_body = None
            destination_snake_index = 0

            # Find the snake the current snake is about to collide with
            for snake in new_snake_state:
                if (snake["id"][-2:] == destination_cell_head):
                    destination_snake_body = snake["body"]
                    destination_snake_length = len(destination_snake_body)
                    break

                destination_snake_index += 1

            # Our size is bigger and we kill the another snake
            if (destination_snake_length < curr_snake_length):

                # Remove destination snake from game board and snake state
                removeKilledSnake(new_board_state, new_head_state, new_snake_state, destination_snake_index)

                # Snake moves forward and updates all coords in new game state
                moveForward(new_board_state, new_head_state, new_snake_state,
                            curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

                curr_health = updateSnakeHealth(
                    new_snake_state, curr_snake_index, True, False)

                # check if our snake ran out of health
                if (curr_health <= 0):
                    removeKilledSnake(new_board_state, new_head_state, new_snake_state, curr_snake_index)

            # Our snake is smaller or same size
            else:
                removeKilledSnake(new_board_state, new_head_state, new_snake_state, curr_snake_index)

                # Same size case
                if (destination_snake_length == curr_snake_length):
                    removeKilledSnake(new_board_state, new_head_state, new_snake_state, destination_snake_index)

                updateSnakeHealth(
                    new_snake_state, curr_snake_index, False, False)

        else:
            removeKilledSnake(new_board_state, new_head_state, new_snake_state, curr_snake_index)
            updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
        
        return new_game_state

    # Snake move to a cell with food
    elif (destination_cell == 1):

        # Snake moves forward and updates all coords in new game state
        moveForward(new_board_state, new_head_state, new_snake_state,
                    curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

        updateSnakeHealth(new_snake_state, curr_snake_index, True, True)

        # add a new body part
        snakeStateFoodGrow(new_snake_state, curr_snake_index)

        return new_game_state

    # Snake's regular movement to empty spaces
    else:

        # Snake moves forward and updates all coords in new game state
        moveForward(new_board_state, new_head_state, new_snake_state,
                    curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

        curr_health = updateSnakeHealth(
            new_snake_state, curr_snake_index, True, False)

        # Check if snake ran out of health
        if (curr_health <= 0):
            removeKilledSnake(new_board_state, new_head_state, new_snake_state, curr_snake_index)

        return new_game_state


# Calculate available space current game state snake has
def floodFill(game_state, curr_snake_head):
    curr_snake_x = curr_snake_head["x"]
    curr_snake_y = curr_snake_head["y"]
    board_state = game_state["board"]["state_board"]
    board_width = len(board_state[0])
    board_height = len(board_state)
    visited = copy.deepcopy(board_state)

    for y in range(board_height):
        for x in range(board_width):
            if (board_state[y][x] in [0, 1]):
                visited[y][x] = False
            else:
                visited[y][x] = True

    visited[curr_snake_y][curr_snake_x] = False
    space = fill(visited, board_width, board_height,
                 curr_snake_x, curr_snake_y)

    return space - 1


# Recursive function of floodfill
def fill(visited, width, height, x, y):

    queue = deque([(x, y)])
    counter = 0

    while queue:
        x, y = queue.popleft()
        if (0 <= x < width and 0 <= y < height and not visited[y][x]):
            visited[y][x] = True
            counter += 1
            queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    return counter


# Calculate the value of the current game state based on the length of all the snakes, needs to be changed
def evaluatePoint(game_state, depth, curr_snake_id, previous_snake_id):
    board_state = game_state["board"]["state_board"]
    board_width = len(board_state[0])
    board_height = len(board_state)
    turns = game_state["turn"]

    # Calculate current snake score based on its length
    curr_snake_head = None
    curr_snake_size = 0
    curr_snake_health = 0

    other_snake_sizes = []
    other_edge_snakes = []
    size_difference = 0

    for snake in game_state["snakes"]:
        head_x = snake["head"]["x"]
        head_y = snake["head"]["y"]

        if (snake["id"] == curr_snake_id):
            curr_snake_health = snake["health"]
            curr_snake_head = snake["head"]
            curr_snake_size = len(snake["body"])
        else:
            other_snake_sizes.append(len(snake["body"]))
            if (head_x == 0 or head_y == 0 or head_x == board_width - 1 or head_y == board_height - 1):
                other_edge_snakes.append(snake)

    for size in other_snake_sizes:
        size_difference += curr_snake_size - 1

    # if (previous_snake_id == )
    if (curr_snake_head is None):
        return float("-inf")

    # Weights
    food_weight = 75
    size_difference_weight = 1000
    available_space_weight = 100
    outer_bound_weight = 0
    edge_kill_weight = 60
    head_losing_weight = -10
    center_control_weight = 10
    head_kill_weight = 50
    turn_weight = 100

    available_space = floodFill(game_state, curr_snake_head)

    head_x = curr_snake_head["x"]
    head_y = curr_snake_head["y"]

    # Encourage snake to prefer states closer to food
    closest_food = float("inf")
    for y in range(board_height):
        for x in range(board_width):
            if (board_state[y][x] == 1):
                food_distance = abs(
                    curr_snake_head["x"] - x) + abs(curr_snake_head["y"] - y)
                closest_food = min(food_distance, closest_food)

    # Discourage our snake to go to the outer bounds of the board
    if (head_x == 0 or head_y == 0 or head_x == board_width - 1 or head_y == board_height - 1):
        outer_bound_weight -= 6

    # Encourage middle control
    if (head_x in [4, 5, 6]):
        center_control_weight += 6

    # Edge kill
    if (head_x == 1 or head_y == 1 or head_x == board_width - 2 or head_y == board_height - 2):
        for snake in other_edge_snakes:
            edge_head_x = snake["head"]["x"]
            edge_head_y = snake["head"]["y"]

            if ((head_x == 1 and edge_head_x == 0) or (head_x == board_width - 2 and edge_head_x == board_width - 1)):
                if (snake["body"][1]["y"] < edge_head_y):
                    if (head_y > edge_head_y):
                        edge_kill_weight += 16
                elif (snake["body"][1]["y"] > edge_head_y):
                    if (head_y < edge_head_y):
                        edge_kill_weight += 16

            elif ((head_y == 1 and edge_head_y == 0) or (head_y == board_height - 2 and edge_head_y == board_height - 1)):
                if (snake["body"][1]["x"] < edge_head_x):
                    if (head_x > edge_head_x):
                        edge_kill_weight += 16
                elif (snake["body"][1]["x"] > edge_head_x):
                    if (head_x < edge_head_x):
                        edge_kill_weight += 16

    closest_smallest_snake = float("inf")

    for snake in game_state["snakes"]:
        curr_head_x = snake["head"]["x"]
        curr_head_y = snake["head"]["y"]

        if (snake["id"] == curr_snake_id):
            continue

        if (len(snake["body"]) < size):
            curr_snake_distance = abs(
                head_x - curr_head_x) + abs(head_y - curr_head_y)
            closest_smallest_snake = min(
                closest_smallest_snake, curr_snake_distance)

        if ((abs(head_x - curr_head_x) + abs(head_y - curr_head_y) < 3)):
            if (len(snake["body"]) > size):
                head_losing_weight -= float("-inf")
            elif (len(snake["body"]) == size):
                head_losing_weight -= 100

    return (curr_snake_health/2 + (available_space * available_space_weight) + (size_difference * size_difference_weight)
            + outer_bound_weight + edge_kill_weight + head_losing_weight +
            center_control_weight + food_weight / (closest_food + 1)
            + head_kill_weight / (closest_smallest_snake + 1) + curr_snake_size * 7)


# Returns boolean depending on if snake state does not contain given id, snake is deleted when it is dead
def isGameOver(game_state, previous_snake_id):
    if (previous_snake_id is None): return False

    if (game_state is None): return True

    snake_state = game_state["snakes"]

    for snake in snake_state:
        if (snake["id"] == previous_snake_id):
            return False
    return True


# The snake MiniMax algorithm
def miniMax(game_state, depth, curr_snake_id, main_snake_id, previous_snake_id, return_move, alpha, beta):
    # If given game_state reached an end or depth has reached zero, return game_state score
    if (depth == 0 or isGameOver(game_state, previous_snake_id)):
        return evaluatePoint(game_state, depth, main_snake_id, previous_snake_id)

    # get the id of the next snake that we're gonna minimax
    curr_index = 0
    for index, snake in enumerate(game_state["snakes"]):
        if (snake["id"] == curr_snake_id):
            curr_index = index
            break

    # Select the next snake id inside the snake array
    next_snake_id = game_state["snakes"][(
        curr_index + 1) % len(game_state["snakes"])]["id"]

    moves = ["up", "down", "right", "left"]

    if (curr_snake_id == main_snake_id):
        highest_value = float("-inf")
        best_move = None
        for move in moves:
            # Makes a copy of the current game state with the current snake taking a possible move
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha, beta)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (curr_val > highest_value):
                best_move = move
                highest_value = curr_val

            alpha = max(alpha, curr_val)

            if (alpha >= beta):
                break

        # print(f"highest :   {curr_snake_id} {best_move}: {highest_value}")

        return (highest_value, best_move) if return_move else highest_value

    else:
        min_value = float("inf")
        best_move = None
        for move in moves:
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha, beta)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (min_value > curr_val):
                best_move = move
                min_value = curr_val

            beta = min(curr_val, beta)

            if (beta <= alpha):
                break

        return (min_value, best_move) if return_move else min_value


# Main function
def miniMax_value(game_state, safe_moves):
    current_game_state = createGameState(game_state, game_state["you"]["id"])

    depth = 1

    result_value, best_move = miniMax(
        current_game_state, depth, game_state["you"]["id"], game_state["you"]["id"], None, True, float("-inf"), float("inf"))
    # print(f"Minimax value: {result_value}, Best move: {best_move}")

    if (best_move is not None):
        if (best_move in safe_moves):
            safe_moves[best_move] += result_value


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
# In tight situation follow snake's own tail
# Reward snake for lasting longer turns
# Reward snake for getting to cells closer to food

# Current TODO
# Minimax to use pointers
# Decision tree
# Balance evaluation score
# Put up a server


# Notes: Higher health score, snake tries to eath more
#       Higher space score, snake tries to grow less hence increasing space
#       Current snake is always trying to healkill and ends up dying
#       Current snake cannot tell tail is free on movement


# The snake MiniMax algorithm
# def miniMax(game_state, depth, maximizing_player, curr_snake_id, main_snake_id, return_move, alpha, beta):
#     # when given game_state is over, return the current state point
#     if (depth == 0 or game_state is None):
#         # print(f"{curr_snake_id}")
#         # if (game_state is None):
#         #   return float("-inf")

#         # if (game_state is None and curr_snake_id == main_snake_id):
#         #     return float("inf")

#         if (game_state is None):
#             return float("-inf") if not maximizing_player else float("inf")

#         return evaluatePoint(game_state, depth, curr_snake_id)
#       # if maximizing_player else evaluatePoint(game_state, depth, main_snake_id)

#     # get the id of the next snake that we're gonna minimax
#     curr_index = 0
#     for index, snake in enumerate(game_state["snakes"]):
#         if (snake["id"] == curr_snake_id):
#             curr_index = index
#             break


#     next_snake_id = game_state["snakes"][(curr_index + 1) % len(game_state["snakes"])]["id"]

#     moves = ["up", "down", "right", "left"]

#     if (maximizing_player):
#         highest_value = float("-inf")
#         best_move = None
#         for move in moves
#             # Makes a copy of the current game state with the current snake taking a possible move
#             new_game_state = makeMove(game_state, curr_snake_id, move)
#             # if (len(game_state["snakes"]) == 1):
#             #   curr_val = miniMax(new_game_state, depth - 1,
#             #                      True, next_snake_id, main_snake_id, False, alpha, beta)
#             # else:
#             curr_val = miniMax(new_game_state, depth - 1,
#                                False, next_snake_id, main_snake_id, False, alpha, beta)
#             print(f"{curr_snake_id} {move}: {curr_val}")
#             if (curr_val > highest_value):
#                 best_move = move
#                 highest_value = curr_val

#             alpha = max(alpha, curr_val)

#             if (alpha >= beta):
#                 break

#         print(f"highest :   {curr_snake_id} {best_move}: {highest_value}")

#         return (highest_value, best_move) if return_move else highest_value

#     else:
#         min_value = float("inf")
#         best_move = None
#         for move in moves:
#             new_game_state = makeMove(game_state, curr_snake_id, move)
#             curr_val = miniMax(new_game_state, depth - 1,
#                                True, next_snake_id, main_snake_id, False, alpha, beta)
#             # print(f"{curr_snake_id} {move}: {curr_val}")
#             if (min_value > curr_val):
#                 best_move = move
#                 min_value = curr_val

#             beta = min(curr_val, beta)

#             if (beta <= alpha):
#                 break

#         return (min_value, best_move) if return_move else min_value
