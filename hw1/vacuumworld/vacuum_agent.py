### 
# Code was adapted from the following repository: https://github.com/aimacode/aima-python/blob/master/vacuum_world.ipynb
###


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
    def __init__(self, filename):
        self.status = self.read_initial_state(filename)
        self.moves_remaining = 0
        self.initial_state = ( 3 - 1 , 4 - 1)
        self.print_grid()
        # TODO: Read in file of filename
            # TODO: Read grid dimensions
            # TODO: Read dirt map

    # TODO: Document me
    def read_initial_state(self, filename):
        grid = []
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

        return grid

    # TODO: Modify function to additionally output neighboring square states (if visible to agent)
    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""
        return (agent.location, self.status[agent.location])

    # TODO: Modify execute action function to work with a grid space instead of a two location space
    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'R':
            agent.location = loc_B
            agent.performance -= 1
        elif action == 'L':
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'S':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'

    def default_location(self, thing):
        """Agents start in either location at random."""
        return random.choice([loc_A, loc_B])
    
    # TODO: Call at the end of the execute_action function
    def print_grid(self):
        for i in range(len(self.status)):
            for j in range(len(self.status[0])):
                if (i,j) == self.initial_state:
                    print("[", end="")
                print(self.status[i][j], end="")
                if (i,j) == self.initial_state:
                    print("]", end="")
                if j+1 is not len(self.status[0]):
                    print(" ", end="")
            print("", end="\n")
            

    # TODO: Call at the end of the execute_action function
    def print_action(self):
        pass

## Base Class to represent Agent
class Agent():
    def __init__(self, knows_neighbors=False):
        self.knows_neighbors = knows_neighbors
    
    def select_action():
        """Given state information available to agent, select an action to execute"""
        pass
        

## Subclass to represent ReflexAgent (Part A)
class ReflexAgent(Agent):
    def __init__():
        super().__init__(knows_neighbors=False)

## Subclass to represent GreedyAgent (Part B)

## Class to represent MemoryAgent (Part C)


if __name__ == '__main__':
    VacuumEnvironment("environ.txt")