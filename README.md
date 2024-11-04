# Minimax BattleSnake Ai built with Python

![battlesnake](https://github.com/user-attachments/assets/a295f814-f5bf-4487-9980-3dab184069b2)

Orion's Fang was crafted for the 2023 RBC BattleSnake competition, where it secured second place. This competitive snake reached the 16th spot in the global standard ladder and 17th in duels. 
Guided by a paranoid Minimax algorithm with alpha-beta pruning, it analyzes up to 7 steps ahead, making calculated moves based on heuristics such as flood fill and edge control scoring.

## About Orion's Fang

Inspired by the Orion constellation, Orion's Fang is an aggressive yet rational hunter, excelling in area control and edge elimination tactics. However, it is sometimes vulnerable to overthinking, leading to self-inflicted losses.  


![Project Image](image/orion_fang.png)

> Orion's Fang showing his area control capabilities against CoolSnake!

# Debugging Process
Debugging the Minimax decision tree with standard tools proved challenging, prompting the creation of a visual representation of the decision tree. This visual tool renders all possible game states for each snake up to the maximum depth, displaying game boards with indicators (0 for empty cells, 1 for food, 2 for snake heads, and letters for snake bodies). Each game state is scored, and optimal moves are highlighted, allowing the root game state to make the best decision.

![Project Image](image/minimax_visual.png)

> The visual tree at depth 2

# Technology used
 - Coded with Python 3, libraries such as Matplotlib and Networkx were used for creating the visual decision tree
 - Deployed using DigitalOcean





