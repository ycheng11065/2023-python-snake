import copy
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# current_game_state = {'game': {'id': '0979620c-9e49-4e0e-8d50-e8ec5f75b0e0', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 0, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_cCpbKfRGwpBprRRfyFW4S6Wb', 'name': '2023_Test', 'latency': '', 'health': 100, 'body': [{'x': 1, 'y': 1}, {'x': 1, 'y': 1}, {'x': 1, 'y': 1}], 'head': {'x': 1, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_JkHjV4xXpj4XY3xTbyDw7vqP', 'name': 'test_123', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 1}, {'x': 9, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}], 'food': [{'x': 0, 'y': 2}, {'x': 8, 'y': 0}, {'x': 5, 'y': 5}], 'hazards': []}, 'you': {'id': 'gs_JkHjV4xXpj4XY3xTbyDw7vqP', 'name': 'test_123', 'latency': '', 'health': 100, 'body': [{'x': 9, 'y': 1}, {'x': 9, 'y': 1}, {'x': 9, 'y': 1}], 'head': {'x': 9, 'y': 1}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#000000', 'head': 'do-sammy', 'tail': 'do-sammy'}}}

current_game_state = {'game': {'id': '9762c05e-7d8e-4229-9134-80e93be8a1c9', 'ruleset': {'name': 'standard', 'version': 'v1.2.3', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 0, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 0}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': 'custom'}, 'turn': 2, 'board': {'height': 11, 'width': 11, 'snakes': [{'id': 'gs_rWHr64bBgwdWwF44xdSXHJp6', 'name': '2023_Test', 'latency': '169', 'health': 100, 'body': [{'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 1, 'y': 5}, {'x': 1, 'y': 5}], 'head': {'x': 0, 'y': 6}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}, {'id': 'gs_YJpjkBp4TKc7FFXVJcJmRR9C', 'name': 'Devious Devin', 'latency': '413', 'health': 100, 'body': [{'x': 4, 'y': 0}, {'x': 5, 'y': 0}, {'x': 5, 'y': 1}, {'x': 5, 'y': 1}], 'head': {'x': 4, 'y': 0}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#99cc00', 'head': 'trans-rights-scarf', 'tail': 'rbc-necktie'}}], 'food': [{'x': 5, 'y': 5}], 'hazards': []}, 'you': {'id': 'gs_rWHr64bBgwdWwF44xdSXHJp6', 'name': '2023_Test', 'latency': '169', 'health': 100, 'body': [{'x': 0, 'y': 6}, {'x': 1, 'y': 6}, {'x': 1, 'y': 5}, {'x': 1, 'y': 5}], 'head': {'x': 0, 'y': 6}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#4c0099', 'head': 'default', 'tail': 'default'}}}

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
            new_head_state[head_y][head_x] = curr_snake_id
            updateSnakeHead(new_snake_state, curr_snake_index, head_x, head_y)
        else:
            if (new_head_state[prev_y][prev_x] == curr_snake_id):
                new_head_state[prev_y][prev_x] = "0"
            if (body_index > 0):
                updateSnakeBody(new_snake_state, curr_snake_index,
                                body_index, prev_x, prev_y)
            new_board_state[prev_y][prev_x] = curr_snake_id

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
    removeKilledSnakeBody(new_board_state, new_head_state,
                          new_snake_state, snake_index)
    new_snake_state.pop(snake_index)


# Find snake corresponding to the given current ID and return its info
def findCurrentSnake(new_snake_state, curr_snake_id):
    curr_snake_index = 0
    curr_snake_length = 0
    curr_snake_body = None
    curr_snake_health = 0
    curr_snake_tail = None

    for i in range(len(new_snake_state)):
        curr_snake = new_snake_state[i]
        if (curr_snake["id"] == curr_snake_id):
            curr_snake_index = i
            curr_snake_body = curr_snake["body"]
            curr_snake_length = len(curr_snake_body)
            curr_snake_health = curr_snake["health"]
            curr_snake_tail = curr_snake_body[-1]

    return curr_snake_index, curr_snake_length, curr_snake_body, curr_snake_health, curr_snake_tail


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
            if (new_head_state[y][x] == curr_snake_id):
                head_x = x
                head_y = y
                break
        if (head_x != None):
            break

    return head_x, head_y


# Update head coordinate to its future head coordinate after move
def updateHeadCoord(x, y, move):
    if (move == "up"):
        y = y - 1
    elif (move == "down"):
        y = y + 1
    elif (move == "left"):
        x = x - 1
    elif (move == "right"):
        x = x + 1

    return x, y


# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
    board_width = len(game_state["board"]["state_board"][0])
    board_height = len(game_state["board"]["state_board"])

    # new game state to update, change the id to current snake
    new_game_state, new_board_state, new_head_state, new_snake_state = createNewGameState(
        game_state, curr_snake_id)

    # Our snake's head coordinates
    head_x, head_y = findHeadCoord(
        board_width, board_height, new_head_state, curr_snake_id)

    # Current snake does not exist
    if (head_x is None or head_y is None):
        return None

    # Update head coordinate value to destination after move is applied
    head_x, head_y = updateHeadCoord(head_x, head_y, move)

    # Acquire current snake info
    curr_snake_index, curr_snake_length, curr_snake_body, curr_snake_health, curr_snake_tail = findCurrentSnake(
        new_snake_state, curr_snake_id)

    # print(curr_snake_index)
    # print(new_snake_state)

    # Check if snake destination hits border
    if not (0 <= head_x < board_width and 0 <= head_y < board_height):
        removeKilledSnake(new_board_state, new_head_state,
                          new_snake_state, curr_snake_index)
        # updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
        return new_game_state

    destination_cell = new_board_state[head_y][head_x]
    destination_cell_head = new_head_state[head_y][head_x]

    # Checks if snake runs into another snake or edge boundary
    if (destination_cell not in [0, 1]):

        # Check if collision is with the head of a snake
        if (destination_cell == 2 and destination_cell_head != 0):
            destination_snake_length = 0
            destination_snake_body = None
            destination_snake_index = 0

            # Find the snake the current snake is about to collide with
            for snake in new_snake_state:
                if (snake["id"] == destination_cell_head):
                    destination_snake_body = snake["body"]
                    destination_snake_length = len(destination_snake_body)
                    break

                destination_snake_index += 1

            # Our size is bigger and we kill the another snake
            if (destination_snake_length < curr_snake_length):

                # Remove destination snake from game board and snake state
                removeKilledSnake(new_board_state, new_head_state,
                                  new_snake_state, destination_snake_index)
                
                # Index might have changed when snake is removed
                curr_snake_index, _, _, _, _ = findCurrentSnake(new_snake_state, curr_snake_id)
                
                # Snake moves forward and updates all coords in new game state
                moveForward(new_board_state, new_head_state, new_snake_state,
                            curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)

                curr_health = updateSnakeHealth(
                    new_snake_state, curr_snake_index, True, False)

                # check if our snake ran out of health
                if (curr_health <= 0):
                    removeKilledSnake(
                        new_board_state, new_head_state, new_snake_state, curr_snake_index)

            # Our snake is smaller or same size
            else:
                removeKilledSnake(new_board_state, new_head_state,
                                  new_snake_state, curr_snake_index)

                # Index might have changed when snake is removed
                destination_snake_index, _, _, _ = findCurrentSnake(new_snake_state, destination_snake_index)

                # Same size case
                if (destination_snake_length == curr_snake_length):
                    removeKilledSnake(
                        new_board_state, new_head_state, new_snake_state, destination_snake_index)

                # updateSnakeHealth(
                #     new_snake_state, curr_snake_index, False, False)

        else:
            if (destination_cell == curr_snake_id):
                if (head_x == curr_snake_tail["x"] and head_y == curr_snake_tail["y"]):
                    # Snake moves forward and updates all coords in new game state
                    moveForward(new_board_state, new_head_state, new_snake_state,
                            curr_snake_id, curr_snake_index, curr_snake_body, head_x, head_y)
                    updateSnakeHealth(new_snake_state, curr_snake_index, False, False)
                    
            else:
                removeKilledSnake(new_board_state, new_head_state,
                              new_snake_state, curr_snake_index)

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
            removeKilledSnake(new_board_state, new_head_state,
                              new_snake_state, curr_snake_index)

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


# Returns boolean depending on if snake state does not contain given id, snake is deleted when it is dead
def isGameOver(game_state, snake_id):
    if (snake_id is None):
        return False

    if (game_state is None):
        return True

    snake_state = game_state["snakes"]

    for snake in snake_state:
        if (snake["id"] == snake_id):
            return False
    return True


# Determines if given head coordinate is on edge
def isOnEdge(head_x, head_y, board_width, board_height):
    return (head_x == 0 or head_y == 0 or head_x == board_width - 1 or head_y == board_height - 1)


# Search through snake state and find curr snake, snakes on edge and average length
def snakeInfoLoop(game_state, curr_snake_id, board_width, board_height):
    curr_snake_head = None
    curr_snake_size = 0
    curr_snake_health = 0
    average_snake_size = 0
    other_edge_snakes = []

    total_snake_amount = 0
    curr_length_total = 0

    for snake in game_state["snakes"]:
        head_x = snake["head"]["x"]
        head_y = snake["head"]["y"]

        if (snake["id"] == curr_snake_id):
            curr_snake_health = snake["health"]
            curr_snake_head = snake["head"]
            curr_snake_size = len(snake["body"])
        else:
            total_snake_amount += 1
            curr_length_total += len(snake["body"])

            if isOnEdge(head_x, head_y, board_width, board_height):
                other_edge_snakes.append(snake)

    if (total_snake_amount > 0):
      average_snake_size = curr_length_total // total_snake_amount

    return curr_snake_head, curr_snake_size, curr_snake_health, average_snake_size, other_edge_snakes


# Return the Manhattan distance of the closest food
def closestFoodDistance(board_state, width, height, head_x, head_y):
    closest_food = float("inf")

    for y in range(height):
        for x in range(width):
            if (board_state[y][x] == 1):
                food_distance = abs(
                    head_x - x) + abs(head_y - y)
                closest_food = min(food_distance, closest_food)

    return closest_food


# Determines if current head coordinates are on cells one before edge
def isOnEdgeBorder(head_x, head_y, board_height, board_width):
    return (head_x == 1 or head_y == 1 or head_x == board_width - 2 or head_y == board_height - 2)


# Return edge kill value of current snake
def edgeKillValue(board_width, board_height, head_x, head_y, other_edge_snakes, main_snake_id):
    main_snake_edge_kill_weight = -2000
    other_snake_edge_kill_weight = 25

    if (isOnEdgeBorder(head_x, head_y, board_width, board_height)):
        for snake in other_edge_snakes:
            curr_edge_kill_weight = other_snake_edge_kill_weight
            edge_head_x = snake["head"]["x"]
            edge_head_y = snake["head"]["y"]

            # If the snake on the edge is our main snake
            if (snake["id"] == main_snake_id):
                curr_edge_kill_weight = main_snake_edge_kill_weight

            if ((head_x == 1 and edge_head_x == 0) or (head_x == board_width - 2 and edge_head_x == board_width - 1)):
                if (snake["body"][1]["y"] < edge_head_y):
                    if (head_y > edge_head_y):
                        return curr_edge_kill_weight

                elif (snake["body"][1]["y"] > edge_head_y):
                    if (head_y < edge_head_y):
                        return curr_edge_kill_weight

            elif ((head_y == 1 and edge_head_y == 0) or (head_y == board_height - 2 and edge_head_y == board_height - 1)):
                if (snake["body"][1]["x"] < edge_head_x):
                    if (head_x > edge_head_x):
                        return curr_edge_kill_weight

                elif (snake["body"][1]["x"] > edge_head_x):
                    if (head_x < edge_head_x):
                        return curr_edge_kill_weight

    return 0


# Finds the closest smallest snake distance as well as returning head collision values
def headCollisionInfo(game_state, head_x, head_y, curr_snake_size, curr_snake_id, main_snake_id):
    smallest_snake_distance = float("inf")
    other_head_losing_weight = -500
    main_head_losing_weight = 200

    other_head_equal_weight = -300

    for snake in game_state["snakes"]:
        curr_head_losing_weight = 0
        curr_head_x = snake["head"]["x"]
        curr_head_y = snake["head"]["y"]

        if (snake["id"] == curr_snake_id):
            continue

        if (len(snake["body"]) < curr_snake_size):
            curr_snake_distance = abs(
                head_x - curr_head_x) + abs(head_y - curr_head_y)
            smallest_snake_distance = min(
                smallest_snake_distance, curr_snake_distance)

        # If current snake size is smaller or equal
        if ((abs(head_x - curr_head_x) + abs(head_y - curr_head_y) < 2)):
            # If current snake size is smaller
            if (len(snake["body"]) > curr_snake_size):
                curr_head_losing_weight = other_head_losing_weight

                # If current snake is going up against our main snake
                if (curr_snake_id != main_snake_id and snake["id"] == main_snake_id):
                    curr_head_losing_weight = main_head_losing_weight

            # If current snake size is equal
            elif (len(snake["body"]) == curr_snake_size):
                curr_head_losing_weight = other_head_equal_weight

    return smallest_snake_distance, curr_head_losing_weight


# Calculate the value of the current game state for our main snake
def evaluatePoint(game_state, depth, main_snake_id, curr_snake_id):
    curr_weight = 0

    snake_health_weight = 2
    opponent_death_weight = float("inf")
    food_weight = 20
    small_size_penalty_weight = -400
    available_space_weight = 0.5
    outer_bound_weight = -12
    center_control_weight = 12
    head_kill_weight = 50
    turn_weight = 100

    depth_discount_factor = 0.4

    # If the game state given somehow does not exist
    if (game_state is None):
        if (curr_snake_id == main_snake_id):
            return float("-inf")
        else:
            return float("inf")

    # Check if our main snake has died
    if (isGameOver(game_state, main_snake_id)):
        return float("-inf")

    # Check if the current snake has died (not main snake)
    if (curr_snake_id != main_snake_id and isGameOver(game_state, curr_snake_id)):
        return opponent_death_weight

    board_state = game_state["board"]["state_board"]
    board_width = len(board_state[0])
    board_height = len(board_state)
    turns = game_state["turn"]

    # Find current snake as well as average snake size and snakes that are on the edge
    curr_snake_head, curr_snake_size, curr_snake_health, average_snake_size, other_edge_snakes = snakeInfoLoop(
        game_state, curr_snake_id, board_width, board_height)
      
    # # Add weight if current snake is smaller than average size of snakes
    # if (curr_snake_size < average_snake_size):
    #     curr_weight += small_size_penalty_weight

    snake_size_weight = 15
    
    # Add weight the bigger the snake is, currently + 15 for each growth
    curr_weight += curr_snake_size * snake_size_weight

    # Add weight the more health the snake has
    # curr_weight += curr_snake_health / snake_health_weight

    # # # FloodFill determines available space for current snake to move, add space weight
    # available_space = floodFill(game_state, curr_snake_head)
    # curr_weight += available_space * available_space_weight

    # Current snake head coordinates
    head_x = curr_snake_head["x"]
    head_y = curr_snake_head["y"]

    # Closest distance to food, add weight scaling depending on how close is curr snake to food
    closest_food_distance = closestFoodDistance(
        board_state, board_width, board_height, head_x, head_y)
    curr_weight += food_weight/(closest_food_distance + 1)

    # # # Add weight if snake is on edge of board
    # if (isOnEdge(head_x, head_y, board_width, board_height)):
    #     curr_weight += outer_bound_weight

    # # Add weight if snake is in center of board
    # if (head_x in [4, 5, 6]):
    #     curr_weight += center_control_weight

    # # Add the edge kill weight
    # curr_weight += edgeKillValue(board_width, board_height,
    #                              head_x, head_y, other_edge_snakes, main_snake_id)

    smallest_snake_distance, head_collision_value = headCollisionInfo(
        game_state, head_x, head_y, curr_snake_size, curr_snake_id, main_snake_id)
    
    curr_weight += head_collision_value
    curr_weight += head_kill_weight / (smallest_snake_distance + 1)

    # curr_weight *= depth_discount_factor * depth
    if (curr_snake_id == main_snake_id):
        return curr_weight
    else:
        return curr_weight * -1

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

    depth = 4

    result_value, best_move = miniMax(
        current_game_state, depth, game_state["you"]["id"], game_state["you"]["id"], None, True, float("-inf"), float("inf"))
    print(f"Minimax value: {result_value}, Best move: {best_move}")

    if (best_move is not None):
        if (best_move in safe_moves):
            safe_moves[best_move] += result_value


    return best_move


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
