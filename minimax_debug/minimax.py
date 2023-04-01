import copy
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# current_game_state = {'game': {'id': '0979620c-9e49-4e0e-8d50-e8ec5f75b0e0', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 0, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_cCpbKfRGwpBprRRfyFW4S6Wb', 'name': '2023_Test', 'latency': '', 'health': 100, 'body': [{'x': 1, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 1}], 'head': {'x': 1, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_JkHjV4xXpj4XY3xTbyDw7vqP', 'name': 'test_123', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 1}, {'x': 9, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}], 'food': [{'x': 0, 'y': 2}, {'x': 8, 'y': 0}, {'x': 5, 'y': 5}], 'hazards': []}, 'you': {'id': 'gs_JkHjV4xXpj4XY3xTbyDw7vqP', 'name': 'test_123', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 1}, {'x': 9, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}}

current_game_state = {'game': {'id': '6948db1c-8b7d-430c-bdc3-29e26ef358b9', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 9, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_fWdBSd47dkQJMCSmmSBK8SRb', 'name': '2023_Test', 'latency': '234', 'health': 93, 'body': [{'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}, {'x': 1, 'y': 9}], 'head': {'x': 2, 'y': 7}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_wrFgD6DTj9rhcF6b7kvRPTFQ', 'name': 'test_123', 'latency': '91', 'health': 99, 'body': [{'x': 3, 'y': 8}, {'x': 4, 'y': 8}, {'x': 5, 'y': 8}, {'x': 6, 'y': 8}, {'x': 7, 'y': 8}], 'head': {'x': 3, 'y': 8}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}], 'food': [{'x': 5, 'y': 5}, {'x': 2, 'y': 8}], 'hazards': []}, 'you': {'id': 'gs_fWdBSd47dkQJMCSmmSBK8SRb', 'name': '2023_Test', 'latency': '234', 'health': 93, 'body': [{'x': 2, 'y': 7}, {'x': 1, 'y': 7}, {'x': 1, 'y': 8}, {'x': 1, 'y': 9}], 'head': {'x': 2, 'y': 7}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}}
current_game_state1 = {
    'game': {
        'id': '6f7716f8-c8de-4132-b5ab-0552e401f8fd',
        'ruleset': {
            'name': 'standard',
            'version': 'v1.2.3',
            'settings': {
                'foodSpawnChance': 15,
                'minimumFood': 1,
                'hazardDamagePerTurn': 0,
                'hazardMap': '',
                'hazardMapAuthor': '',
                'royale': {
                    'shrinkEveryNTurns': 0
                },
                'squad': {
                    'allowBodyCollisions': False,
                    'sharedElimination': False,
                    'sharedHealth': False,
                    'sharedLength': False
                }
            }
        },
        'map': 'standard',
        'timeout': 500,
        'source': 'custom'
    },
    'turn': 113,
    'board': {
        'height': 11,
        'width': 11,
        'snakes': [
            {'id': 'gs_PKxWVJ6yDFQtMv4dDcxHCgDR',
             'name': 'test_123',
             'latency': '33',
             'health': 63,
             'body': [{'x': 1, 'y': 4}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}, {'x': 1, 'y': 0}],
             'head': {'x': 1, 'y': 4},
             'length': 5,
             'shout': '',
             'squad': '',
             'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}
        ],
        'food': [
            {'x': 6, 'y': 0}, {'x': 7, 'y': 5}, {'x': 4, 'y': 9}, {'x': 5, 'y': 6}, {'x': 7, 'y': 8}, {'x': 5, 'y': 5}, {'x': 8, 'y': 7}, {'x': 6, 'y': 10}, {
                'x': 10, 'y': 3}, {'x': 6, 'y': 4}, {'x': 8, 'y': 5}, {'x': 6, 'y': 5}, {'x': 9, 'y': 9}, {'x': 2, 'y': 2}, {'x': 5, 'y': 4}, {'x': 4, 'y': 4}
        ],
        'hazards': []
    },
    'you': {'id': 'gs_PKxWVJ6yDFQtMv4dDcxHCgDR', 'name': 'test_123', 'latency': '33', 'health': 63, 'body': [{'x': 1, 'y': 4}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 1, 'y': 1}, {'x': 1, 'y': 0}], 'head': {'x': 1, 'y': 4}, 'length': 5, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}}


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


# Remove killed snake from the snake state list
def removeKilledSnake(new_snake_state, killed_snake_index):
    new_snake_state.pop(killed_snake_index)


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


# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
    board_width = len(game_state["board"]["state_board"][0])
    board_height = len(game_state["board"]["state_board"])

    # new game state to update, change the id to current snake
    new_game_state = copy.deepcopy(game_state)
    new_board_state = new_game_state["board"]["state_board"]
    new_head_state = new_game_state["board"]["head_board"]
    new_snake_state = new_game_state["snakes"]
    new_game_state["turn"] = game_state["turn"] + 1
    new_game_state["curr_snake_id"] = curr_snake_id

    # Our destination coordinate after performing move
    head_x, head_y = None, None

    for y in range(board_height):
        for x in range(board_width):
            if (new_head_state[y][x] == curr_snake_id[-2:]):
                head_x = x
                head_y = y
                break
        if (head_x != None):
            break

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
        updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
        # print("Snake hit border")
        return None

    destination_cell = new_board_state[head_y][head_x]
    destination_cell_head = new_head_state[head_y][head_x][-2:]

    # Check if snake runs into another snake
    if (destination_cell not in [0, 1]):

        # Check if collision is with the head of a snake smaller than current snake
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

            # Our size is bigger, else we return None signifying that we died
            if (destination_snake_length < curr_snake_length):

                # Remove the destination snake
                for body in destination_snake_body:
                    body_x = body["x"]
                    body_y = body["y"]

                    new_board_state[body_y][body_x] = 0

                # Snake moves forward and updates all coords in new game state
                moveForward(new_board_state, new_head_state, new_snake_state,
                            curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

                curr_health = updateSnakeHealth(
                    new_snake_state, curr_snake_index, True, False)

                if (curr_health <= 0):
                    return None

                # Remove killed snake from snake state list
                removeKilledSnake(new_snake_state, destination_snake_index)

                return new_game_state

            else:
                updateSnakeHealth(
                    new_snake_state, curr_snake_index, False, False)
                return None

        updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
        return None

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

        if (curr_health <= 0):
            return None

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


# Calculate the value of the current game state based on the length of all the snakes
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
    if (curr_snake_head is None): return float("-inf")

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
                food_distance = abs(curr_snake_head["x"] - x) + abs(curr_snake_head["y"] - y)
                closest_food = min(food_distance, closest_food)

              
    # Discourage our snake to go to the outer bounds of the board
    if (head_x == 0 or head_y == 0 or head_x == board_width - 1 or head_y == board_height - 1):
      outer_bound_weight -= 6
      

    # Encourage middle control
    if (head_x in [4,5,6]):
      center_control_weight += 6


    # Edge kill
    if (head_x == 1 or head_y == 1 or head_x == board_width - 2 or head_y == board_height - 2):
      for snake in other_edge_snakes:
        edge_head_x = snake["head"]["x"]
        edge_head_y = snake["head"]["y"]

        if ((head_x == 1 and edge_head_x == 0) or (head_x == board_width - 2 and edge_head_x == board_width - 1)):
          if(snake["body"][1]["y"] < edge_head_y):
            if (head_y > edge_head_y):
              edge_kill_weight += 16
          elif (snake["body"][1]["y"] > edge_head_y):
            if (head_y < edge_head_y):
              edge_kill_weight += 16

        elif ((head_y == 1 and edge_head_y == 0) or (head_y == board_height - 2 and edge_head_y == board_height - 1)):
          if(snake["body"][1]["x"] < edge_head_x):
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
        curr_snake_distance = abs(head_x - curr_head_x) + abs(head_y - curr_head_y)
        closest_smallest_snake = min(closest_smallest_snake, curr_snake_distance)

      if ((abs(head_x - curr_head_x) + abs(head_y - curr_head_y) < 3)):
        if (len(snake["body"]) > size):
          head_losing_weight -= float("-inf")
        elif (len(snake["body"]) == size):
          head_losing_weight -= 100
          
        
    return (curr_snake_health/2 + (available_space * available_space_weight) + (size_difference * size_difference_weight) 
    + outer_bound_weight + edge_kill_weight + head_losing_weight + center_control_weight + food_weight / (closest_food + 1)
    + head_kill_weight /(closest_smallest_snake + 1) + curr_snake_size * 7)


# The snake MiniMax algorithm
def miniMax(game_state, depth, curr_snake_id, main_snake_id, previous_snake_id, return_move, alpha, beta):
    # when given game_state is over, return the current state point
    if (game_state == None):
        # Return -inf if our main snake dies, return inf if an opponent snake dies
        if (previous_snake_id and previous_snake_id == main_snake_id):
            # our snake killed itself last move
            return float('-inf')
        elif (previous_snake_id and previous_snake_id != main_snake_id):
            # some other snake killed itself
            return float('inf')

    if (depth == 0):
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



def createGrid(state):
    for row in state:
        row = " ".join(str(el).rjust(2, ' ') for el in row)
        print(row)


def foodSpawm(state, x, y):
    board = state["board"]["board_state"]
    board[x][y] = 1


def main():
    game_state = createGameState(
        current_game_state, 'gs_Xkqb4BwwxrJcrPQBQtd6cq8X')
    board_state = game_state["board"]["state_board"]
    head_state = game_state["board"]["head_board"]



if __name__ == "__main__":
    main()
