# Value constants
FOOD_VALUE = 2
HEAD_KILL_VALUE = 3
MIN_MOVE_VALUE = float("-inf")
DEFAULT_MOVE_VALUE = 0
HEALTH_THRESHOLD = 40


# ----------------------------------------------------------------------------
# SNAKE BASIC BEHAVIOR
# -----------------------------------------------------------------------------


# Calculate the Mahattan distance between the two entities
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