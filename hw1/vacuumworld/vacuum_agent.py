### 
# Code was adapted from the following repository: https://github.com/aimacode/aima-python/blob/master/vacuum_world.ipynb
###

import random
import time
import sys

## Class to represent the environment state
## Major modifications to TrivialVacuumEnvironment in AIMA code:
## * There are more than just 2 locations. We are now looking at a grid.
## * We are now looking each cell having a continuous cleanliness state rather than a binary clean vs dirty
## * We can now perform the following actions L, R, U, D, S
## * Modify performance to be a measure of how much dirt was picked up
## * Need to figure out where to keep track of moves (either Agent or VacuumEnvironment)

class VacuumEnvironment():

    """This environment has two locations, A and B. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    # TODO: Read in initial state information from text file
    def __init__(self, filename=None):
        # TODO: Update how we are receiving input file. Not file name, but as input
        (self.grid_size, self.status, self.moves_total, self.initial_state) = self.read_initial_state(filename)
        # print(f"Starting at position {self.initial_state} with {self.moves_total} moves")
        self.moves_curr = 0

    # TODO: Document me
    def read_initial_state(self, filename):
        grid = []
        lines = None
        if filename is None:
            lines = sys.stdin.read().splitlines()
        else: 
            with open(filename, "r") as f:
                lines = f.readlines()

        # Find where the dirt section starts
        dirt_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith("DIRT:"):
                dirt_start = i + 1
                break

        # Read grid dimensions
        grid_line = [l for l in lines if l.startswith("GRID:")][0]
        rows, cols = map(int, grid_line.replace("GRID:", "").strip().split())

        # Extract dirt rows
        for i in range(dirt_start, dirt_start + rows):
            row_values = list(map(float, lines[i].strip().split()))
            if len(row_values) != cols:
                raise ValueError(f"Row {i} does not have {cols} columns")
            grid.append(row_values)

        # Read moves
        moves_line = [l for l in lines if l.startswith("MOVES:")][0]
        moves = int(moves_line.replace("MOVES:", "").strip())

        # Read initial position
        initial_line = [l for l in lines if l.startswith("INITIAL:")][0]
        x, y = map(int, initial_line.replace("INITIAL:", "").strip().split())

        return ((rows,cols),grid, moves, (x-1,y-1))

    # TODO: Modify function to additionally output neighboring square states (if visible to agent)
    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""

        # Create a structure indicating if neighbors are walls
        walls = {'R': False, 'L': False, 'U': False, 'D': False }
        walls['R'] = self.check_walls(agent.location,'R')
        walls['L'] = self.check_walls(agent.location,'L')
        walls['U'] = self.check_walls(agent.location,'U')
        walls['D'] = self.check_walls(agent.location,'D')
        if agent.knows_neighbors:
            # Initialize neighbors, None will mean wall
            neighbors = {'R': None, 'L': None, 'U': None, 'D': None }
            if not walls['D']:
                neighbors['D'] = self.status[agent.location[0] + 1][agent.location[1]]
            if not walls['U']:
                neighbors['U'] = self.status[agent.location[0] - 1][agent.location[1]]
            if not walls['R']:
                neighbors['R'] = self.status[agent.location[0]][agent.location[1] + 1]
            if not walls['L']:
                neighbors['L'] = self.status[agent.location[0]][agent.location[1] - 1]        
            return (self.status[agent.location[0]][agent.location[1]], neighbors, agent.location)
        else: 
            return (self.status[agent.location[0]][agent.location[1]], walls)

    def check_walls(self, position, dir):
        """Checks if the cell to the dir of position is a wall"""
        if dir == 'D':
            return position[0] + 1 == self.grid_size[0]        
        elif dir == 'U':
            return position[0] == 0
        elif dir == 'R':
            return position[1] + 1 == self.grid_size[1]
        elif dir == 'L':
            return position[1] == 0
        else: # invalid input
            return None
        
    # TODO: Modify execute action function to work with a grid space instead of a two location space
    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score increases by the amount of dirt sucked each turn."""
        if self.check_walls(agent.location, action):
                print("Attempted to execute invalid action")
                time.sleep(1)
                return # Attempting to move to wall, not a valid action, should never get here
        if action == 'D':
            agent.location[0] +=1
        elif action == 'U':
            agent.location[0] -=1
        elif action == 'R':
            agent.location[1] +=1
        elif action == 'L':
            agent.location[1] -=1
        elif action == 'S':
            agent.performance += self.status[agent.location[0]][agent.location[1]]
            self.status[agent.location[0]][agent.location[1]] = 0.
        self.moves_curr += 1
        self.print_action(action, agent)
        if self.moves_curr % 5 == 0:
            self.print_grid(agent)

    
    # TODO: Call at the end of the execute_action function
    def print_grid(self,agent):
        print()
        for i in range(len(self.status)):
            for j in range(len(self.status[0])):
                if list((i,j)) == agent.location:
                    print("[", end="")
                print(self.status[i][j], end="")
                if list((i,j)) == agent.location:
                    print("]", end="")
                if j+1 is not len(self.status[0]):
                    print(" ", end="")
            print("", end="\n")
        print()
            

    # TODO: Call at the end of the execute_action function
    def print_action(self, action, agent):
        print(f"{action} {agent.performance}")


## Base Class to represent Agent
class Agent():
    def __init__(self, knows_neighbors=False, memory=False):
        self.knows_neighbors = knows_neighbors
        self.memory = memory
        self.performance = 0
    
    def select_action():
        """Given state information available to agent, select an action to execute"""
        pass
        

## Subclass to represent ReflexAgent (Part A)
class ReflexAgent(Agent):
    def __init__(self):
        super().__init__()
    def select_action(self, percept):
        (status,walls) = percept
        # Suck if there is dirt at current position
        if status > 0.0:
            return "S"
        # Otherwise, randomly move to a nearby square
        valid_keys = [k for k, v in walls.items() if not v]
        if valid_keys:
            return random.choice(valid_keys)

        # Should not get here, but return none if no valid actions
        print("Agent found no valid actions")
        time.sleep(1)
        return None




## Subclass to represent GreedyAgent (Part B)
class GreedyAgent(Agent):
    def __init__(self):
        super().__init__(knows_neighbors=True)
    def select_action(self, percept):
        (status,neighbors,_) = percept
        # Suck if there is dirt at current position
        if status > 0.0:
            return "S"
        # Otherwise, move to adjacent square with the most dirt
        valid_keys = [k for k, v in neighbors.items() if v is not None]
        best_moves = []
        best_value = 0.
        if valid_keys:
            for valid_key in valid_keys:
                if neighbors[valid_key] > best_value:
                    best_value = neighbors[valid_key]
                    best_moves = [valid_key]
                elif neighbors[valid_key] == best_value:
                    best_moves.append(valid_key)
            return random.choice(best_moves)


        # Should not get here, but return none if no valid actions
        print("Agent found no valid actions")
        return None

## SubClass to represent MemoryAgent (Part C)
class MemoryAgent(Agent):
    def __init__(self):
        super().__init__(knows_neighbors=True, memory=True)
        self.loc = None
        # (r,c) -> last-seen dirt
        # GameObject initialized self.known_dirt array and self.grid_size to tell us the indices
        
    def update_memory(self, status, neighbors, pos):
        self.position = pos
        self.known_dirt[pos[0]][pos[1]] = status
        # Update current cell
        self.known_dirt[pos[0]][pos[1]] = status
        # Update neighbors
        for k, val in neighbors.items():
            if val is None:
                continue
            if k == 'U': 
                n_r, n_c = pos[0] - 1, pos[1]
            elif k == 'D': 
                n_r, n_c = pos[0] + 1, pos[1]
            elif k == 'L': 
                n_r, n_c = pos[0], pos[1] - 1
            else:          
                n_r, n_c = pos[0], pos[1] + 1
            self.known_dirt[n_r][n_c] = val

    def select_action(self, percept):
        (status,neighbors,_) = percept
        # Suck if there is dirt at current position
        if status > 0.0:
            return "S"
        # Otherwise, move to adjacent square with the most dirt
        best_dirt = self.get_best_move()
        if best_dirt:
            return self.step_toward_dirt(best_dirt)

    def step_toward_dirt(self, best_dirt):
        curr_row, curr_col = self.loc
        dirt_r, dirt_col = best_dirt
        if dirt_r < curr_row: 
            return 'U'
        if dirt_r > curr_row: 
            return 'D'
        if dirt_col < curr_col: 
            return 'L'
        if dirt_col > curr_col: 
            return 'R'
        return None

    def get_best_move(self):
        best_score = None
        best_targets = []
        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                v = self.known_dirt[r][c]
                if v is None or v <= 1e-9 or (r, c) == self.loc:
                    continue
                d = abs(self.loc[0] - r) + abs(self.loc[1] - c)
                score = v / (d + 1)     # value-per-step
                if (best_score is None) or (score > best_score + 1e-12):
                    best_score = score
                    best_targets = [(r, c)]
                elif abs(score - best_score) <= 1e-12:
                    best_targets.append((r, c))
        return random.choice(best_targets) if best_targets else None
            
    


        



class GameObject():
    def __init__(self,agent,env):
        super().__init__()
        self.agent = agent
        self.env = env
        self.agent.location = list(self.env.initial_state)
        if self.agent.memory:
            self.agent.grid_size = self.env.grid_size
            self.agent.known_dirt = [[None for _ in range(self.agent.grid_size[0])] for _ in range(self.agent.grid_size[0])]

    def next_move(self):
        # Get percepts
        percept = self.env.percept(self.agent)

        # Select action
        action = self.agent.select_action(percept)

        # Execute action
        self.env.execute_action(self.agent, action)
    
    def execute_game(self):
        while self.env.moves_curr < self.env.moves_total:
            self.next_move()




if __name__ == '__main__':
    agent = ReflexAgent()
    agent = GreedyAgent()
    agent = MemoryAgent()
    env = VacuumEnvironment()
    game = GameObject(agent, env)
    game.execute_game()