import sys
import numpy as np

# The fisrt digit is the number of portals
# The next lines contains input pos, output pos, and initial state

"""
Property: All portals to the left of the ant are always inactive; therefore, the steps needed to go through a portal and come back are always the same.
"""

MAX_OUT = 998244353

class AntPort:
    def __init__(self, x, y, s, n) -> None:
        self.x = x
        self.y = y
        self.s = s
        self.n = n
        self.port_costs = np.zeros(n+1)

    def add_to_cumsum(self, cost, i) -> None:
        self.port_costs[i+1] = self.port_costs[i] + cost


    """

        The cost of an ant going through a portal is defined:
        cost = (X - Y) + sum of all portal costs between X and Y
        Where X is the position of the original portal and Y is the position of the destination portal(The delta is simply how many steps the ant has taken).
        To optimize summation of the portals between X and Y, we can use a cumulative sum array.
        To find the lower bound portal we can use a binary search.

    """
    def simulate(self, start) -> int:
        global MAX_OUT
        steps = 0
        x = start
        for i in range(self.n):
            steps += (self.x[i] - x)
            x = self.x[i]
            # Binary search for the lower bound portal
            # Returns the leftmost index where the destination position can be inserted
            l_b = np.searchsorted(self.x, self.y[i])
            # Total cost of going through portal i
            cost = (x-self.y[i]) + (self.port_costs[i]-self.port_costs[l_b])
            # Store cost in cumulative sum array
            self.add_to_cumsum(cost, i)
            steps += cost*self.s[i]

        return steps % MAX_OUT
    
def parse():
    infile = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    with open(infile, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    n = int(lines[0])
    x = np.zeros(n)
    y = np.zeros(n)
    s = np.zeros(n)
    for i, l in enumerate(lines[1:]):
        tmp = l.split(' ')
        x[i] = int(tmp[0])
        y[i] = int(tmp[1])
        s[i] = int(tmp[2])
    return x, y, s, n


if __name__ == "__main__":
    x, y, s, n = parse()
    ant_port = AntPort(x, y, s, n)
    print("Steps: ", int(ant_port.simulate(0)+1) % MAX_OUT)
