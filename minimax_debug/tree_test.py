import sys
sys.path.append('/path/to/directory/containing/minimax.py')
from minimax import *
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


class Node:
    def __init__(self, grid):
        self.grid = grid
        self.curr_snake = None
        self.turn = None
        self.value = None
        self.up = None
        self.down = None
        self.right = None
        self.left = None


# The snake MiniMax algorithm
def miniMaxTree(game_state, depth, curr_snake_id, main_snake_id, previous_snake_id):
    # when given game_state is over, return the current state point
    if (game_state == None):
        # Return -inf if our main snake dies, return inf if an opponent snake dies
        if (previous_snake_id and previous_snake_id == main_snake_id):
            # our snake killed itself last move
            curr_root = Node(None)
            curr_root.turn = "end"
            curr_root.curr_snake = curr_snake_id[-2:]
            curr_root.value = float('-inf')
            return curr_root, curr_root.value
        elif (previous_snake_id and previous_snake_id != main_snake_id):
            # some other snake killed itself
            curr_root = Node(None)
            curr_root.turn = "end"
            curr_root.curr_snake = curr_snake_id[-2:]
            curr_root.value = float('inf')
            return curr_root, curr_root.value

    if (depth == 0):
        curr_root = Node(game_state["board"]["state_board"])
        curr_root.turn = game_state["turn"]
        curr_root.curr_snake = previous_snake_id[-2:]
        curr_root.value = evaluatePoint(game_state, depth, main_snake_id, previous_snake_id)
        return curr_root, curr_root.value

    # get the id of the next snake that we're gonna minimax
    curr_index = 0
    for index, snake in enumerate(game_state["snakes"]):
        if (snake["id"] == curr_snake_id):
            curr_index = index
            break

    # Select the next snake id inside the snake array
    next_snake_id = game_state["snakes"][(
        curr_index + 1) % len(game_state["snakes"])]["id"]

    curr_root = Node(game_state["board"]["state_board"])

    moves = ["up", "down", "right", "left"]

    if (curr_snake_id == main_snake_id):
        highest_value = float("-inf")
        best_move = None
        for move in moves:
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_node, curr_val = miniMaxTree(
                new_game_state, depth - 1, next_snake_id, main_snake_id, curr_snake_id)

            if (move == "up"):
                curr_root.up = curr_node
            elif (move == "down"):
                curr_root.down = curr_node
            elif (move == "right"):
                curr_root.right = curr_node
            else:
                curr_root.left = curr_node

            if (curr_val > highest_value):
                best_move = move
                highest_value = curr_val

        curr_root.turn = game_state["turn"]
        curr_root.curr_snake = curr_snake_id[-2:]
        curr_root.value = highest_value
        return curr_root, highest_value

    else:
        min_value = float("inf")
        best_move = None
        for move in moves:
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_node, curr_val = miniMaxTree(
                new_game_state, depth - 1, next_snake_id, main_snake_id, curr_snake_id)

            if (move == "up"):
                curr_root.up = curr_node
            elif (move == "down"):
                curr_root.down = curr_node
            elif (move == "right"):
                curr_root.right = curr_node
            else:
                curr_root.left = curr_node

            if (min_value > curr_val):
                best_move = move
                min_value = curr_val

        curr_root.turn = game_state["turn"]
        curr_root.curr_snake = curr_snake_id[-2:]
        curr_root.value = min_value
        return curr_root, min_value


# Main function
def createMinimaxTree(game_state):
    current_game_state = createGameState(game_state, game_state["you"]["id"])

    depth = 2

    root, highest_value = miniMaxTree(
                current_game_state, depth, game_state["you"]["id"], game_state["you"]["id"], None)
    # print(f"Minimax value: {result_value}, Best move: {best_move}")

    return root


def draw_decision_tree(tree_root):
    def build_graph(node, graph, depth=0, x_offset=0, spacing_factor=1.5):
        nonlocal max_x
        nonlocal max_depth
        if node is None:
            return x_offset

        graph.add_node(node, pos=(x_offset, -depth * sibling_spacing * (spacing_factor ** depth)), grid=node.grid, value=node.value, turn=node.turn, curr_snake=node.curr_snake)
        max_x = max(max_x, x_offset)
        max_depth = max(max_depth, depth)

        x_offset = build_graph(node.up, graph, depth + 1, x_offset)
        x_offset = build_graph(node.down, graph, depth + 1, x_offset)
        x_offset = build_graph(node.right, graph, depth + 1, x_offset)
        x_offset = build_graph(node.left, graph, depth + 1, x_offset)

        if node.up:
            graph.add_edge(node, node.up)
        if node.down:
            graph.add_edge(node, node.down)
        if node.right:
            graph.add_edge(node, node.right)
        if node.left:
            graph.add_edge(node, node.left)

        return x_offset + 1

    sibling_spacing = 100
    graph = nx.DiGraph()
    max_x = 0
    max_depth = 0
    build_graph(tree_root, graph)

    pos = nx.get_node_attributes(graph, 'pos')
    grid_labels = nx.get_node_attributes(graph, 'grid')
    value_labels = nx.get_node_attributes(graph, 'value')
    turn_labels = nx.get_node_attributes(graph, 'turn')
    snake_labels = nx.get_node_attributes(graph, 'curr_snake')

    labels = {}
    for node in graph.nodes:
        if grid_labels[node] is not None:
            grid_str = '\n'.join([' '.join([str(cell) for cell in row]) for row in grid_labels[node]])
            labels[node] = f"Snake: {snake_labels[node]}\n{grid_str}\nValue: {value_labels[node]}\nTurn: {turn_labels[node]}"
        else:
            labels[node] = f"Snake: {snake_labels[node]}\nValue: {value_labels[node]}\nTurn: {turn_labels[node]}"

    plt.rcParams["font.size"] = 1
    plt.figure(figsize=(max_x, int(max_depth * max_depth * sibling_spacing * (1.5 ** max_depth) / 4)))
    nx.draw(graph, pos, with_labels=False, node_size=5000, node_color='lightblue')
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, arrows=True)
    plt.show()



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

    root = createMinimaxTree(current_game_state)
    draw_decision_tree(root)


if __name__ == "__main__":
    main()
