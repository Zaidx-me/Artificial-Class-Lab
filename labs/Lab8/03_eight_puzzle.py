#8 puzzle problem using a star search in python

class Puzzle:
    def __init__(self, start, goal):
        self.start = tuple(start)
        self.goal = tuple(goal)

    # count the tiles that are not in their goal position
    def misplaced(self, state):
        count = 0

        for i in range(9):
            if state[i] != 0 and state[i] != self.goal[i]:
                count = count + 1

        return count

    # swap two tiles and return the new state
    def swap(self, state, i, j):
        new = list(state)
        temp = new[i]
        new[i] = new[j]
        new[j] = temp
        return tuple(new)

    # all states reachable by sliding a tile into the blank
    def neighbours(self, state):
        moves = []

        blank = state.index(0)   # position of the blank tile
        row = blank // 3
        col = blank % 3

        if row > 0:
            moves.append(self.swap(state, blank, blank - 3))

        if row < 2:
            moves.append(self.swap(state, blank, blank + 3))

        if col > 0:
            moves.append(self.swap(state, blank, blank - 1))

        if col < 2:
            moves.append(self.swap(state, blank, blank + 1))

        return moves

    # print a state as a 3 x 3 grid
    def printState(self, state):
        for i in range(0, 9, 3):
            print(state[i], state[i + 1], state[i + 2])
        print()

    # a star search using misplaced tiles as the heuristic
    def solve(self):

        # every item stores state, g, f and the states taken to reach it
        open_list = [[self.start, 0, self.misplaced(self.start), [self.start]]]

        closed = []
        expanded = 0

        while len(open_list) > 0:

            # pick the state with the smallest f value
            best = 0
            for i in range(1, len(open_list)):
                if open_list[i][2] < open_list[best][2]:
                    best = i

            state, g_cost, f_cost, path = open_list[best]
            del open_list[best]

            # already expanded, skip it
            if state in closed:
                continue

            closed.append(state)
            expanded = expanded + 1

            # print the moves that lead to the goal
            if state == self.goal:
                print("Start state:")
                self.printState(self.start)

                for step in range(1, len(path)):
                    print(f"Step {step}:")
                    self.printState(path[step])

                print("Goal reached !")
                print("Moves:", len(path) - 1)
                print("States expanded:", expanded)
                return

            # every move costs 1, so g is the number of moves made
            for neighbour in self.neighbours(state):
                if neighbour not in closed:
                    new_g = g_cost + 1
                    new_f = new_g + self.misplaced(neighbour)
                    open_list.append([neighbour, new_g, new_f, path + [neighbour]])

        print("Goal not reachable from the start state")


# start and goal states used in the manual
puzzle = Puzzle(
    [1, 2, 3,
     0, 4, 6,
     7, 5, 8],
    [1, 2, 3,
     4, 5, 6,
     7, 8, 0]
)

print("8 Puzzle using A* Search (misplaced tiles heuristic)")
print()
puzzle.solve()
