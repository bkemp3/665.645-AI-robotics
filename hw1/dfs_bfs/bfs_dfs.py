# Pseudocode comments adapted from Norvig Russell Textbook
from collections import deque




## PSEUDOCODE FROM FIGURE 3.11 of Norvig Russell AI Textbook
# function BREADTH-FIRST-SEARCH(problem) returns a solution, or failure
def bfs(problem):
#   node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    node = {
        "state": problem.initial_state,
        "path": [problem.initial_state],
        "path_cost": 0
    }
#   if problem.GOAL-TEST(node.STATE) then
    if problem.goal_test(node["state"]):
#       return SOLUTION(node)
        return node
#   frontier ← a FIFO queue with node as the only element
    frontier = deque([node])
#   explored ← an empty set
    explored = set()
#   loop do
    while True:
#       if EMPTY?(frontier) then
        if len(frontier) == 0:
#           return failure
            return None
#       node ← POP(frontier)  // chooses the shallowest node in frontier
        node = frontier.popleft()
#       add node.STATE to explored
        explored.add(node["state"])
        print(f"Explored: {node['state']}")
#       for each action in problem.ACTIONS(node.STATE) do
        for action in problem.actions(node["state"]):
#           child ← CHILD-NODE(problem, node, action)
            child_state = problem.result(node["state"], action)
            child = {
                "state": child_state,
                "path": node["path"] + [child_state],
                "path_cost": node["path_cost"] + 1
            }
#           if child.STATE is not in explored and child.STATE is not in frontier then
            in_frontier = False
            for n in frontier:
                if n["state"] == child["state"]:
                    in_frontier = True
            if (child["state"] not in explored) and ( not in_frontier):
#               if problem.GOAL-TEST(child.STATE) then
                if problem.goal_test(child["state"]):
#                   return SOLUTION(child)
                    return child
#               frontier ← INSERT(child, frontier)
                frontier.append(child)
                

## PSEUDOCODE FROM FIGURE 3.7 of Norvig Russell AI Textbook
# function GRAPH-SEARCH(problem) returns a solution, or failure
def dfs(problem):
#   initialize the frontier using the initial state of problem
    node = {
        "state": problem.initial_state,
        "path": [problem.initial_state],
        "path_cost": 0
    }
    frontier = [node]
#   initialize the explored set to be empty
    explored = set()
#   loop do
    while True:
#       if the frontier is empty then
        if not frontier:
#           return failure
            return None
#       choose a leaf node and remove it from the frontier
        node = frontier.pop()
#       if the node contains a goal state then
        if problem.goal_test(node["state"]):
#           return the corresponding solution
            return node
#       add the node to the explored set
        explored.add(node['state'])
        print(f"Explored: {node['state']}")
#       expand the chosen node, 
        for action in reversed(problem.actions(node["state"])):
            child_state = problem.result(node["state"], action)
            child = {
                "state": child_state,
                "path": node["path"] + [child_state],
                "path_cost": node["path_cost"] + 1
            }
            in_frontier = False
            for n in frontier:
                if n["state"] == child["state"]:
                    in_frontier = True
#           adding the resulting nodes to the frontier only if not in the frontier or explored set
            if (child["state"] not in explored) and (not in_frontier):
                frontier.append(child)




class Problem:
    def __init__(self, initial_state, goal_state, graph):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.graph = graph

    def actions(self, state):
        return self.graph.get(state, [])

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal_state




# Crate graph
# Tree graph
graph = {
    0: [1, 4],
    1: [2, 3],
    4: [5, 6],
    2: [],
    3: [],
    5: [],
    6: []
}

# Create problem object on these attributes
initial_state = 0
goal_state = 6
problem = Problem(initial_state, goal_state, graph)
# Display problem initial and goal states
print(f"Problem {initial_state}->{goal_state}")
# Call bfs on this problem
print(f"BFS Path Found: {bfs(problem)}")
# Call dfs on this 
print(f"DFS Path Found: {dfs(problem)}")