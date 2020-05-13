import agents

b = "X"
w = "O"


class State:
    """ State is a class that represent the state of current game
     it has a list of list as a board. First number is the index of line.
     Second number is the index of the element in the line. """
    def __init__(self):
        board = []
        for i in range(0, 8):
            line = []
            for j in range(0, 8):
                c = " "
                if i is 3 and j is 3:
                    c = b
                if i is 3 and j is 4:
                    c = w
                if i is 4 and j is 3:
                    c = w
                if i is 4 and j is 4:
                    c = b
                line.append(c)
            board.append(line)
        self._board = board
        """ end is a field that sign whether this game end """
        self._end = False
        """ this is a initial result """
        self._result = "Black: 2 White: 2"
        self._resource = [[90, -60, 10, 10, 10, 10, -60, 90],
                          [-60, -80, 5, 5, 5, 5, -80, -60],
                          [10, 5, 1, 1, 1, 1, 5, 10],
                          [10, 5, 1, 1, 1, 1, 5, 10],
                          [10, 5, 1, 1, 1, 1, 5, 10],
                          [10, 5, 1, 1, 1, 1, 5, 10],
                          [-60, -80, 5, 5, 5, 5, -80, -60],
                          [90, -60, 10, 10, 10, 10, -60, 90]]

    def display(self):
        """ Display the Board on the terminal """
        print("GameBoard:")
        for line in self._board:
            one_line = ""
            for cell in line:
                one_line += cell + " "
            print(one_line)
        print(self._result)

    def check_win(self):
        """ Simple checker to find is there a winner.
         If there is any empty cell, it would say False """
        black = 0
        white = 0
        end = True
        for line in self._board:
            for cell in line:
                if cell is b:
                    black += 1
                elif cell is w:
                    white += 1
                elif cell is " ":
                    end = False

        if end:
            if black > white:
                return True, "Black win"
            else:
                return True, "White win"
        else:
            return False, "Black: " + str(black) + " White: " + str(white)

    def change_color(self, color, position):
        """ Change the color base on the returned position.
        Treat the given position as the center of reference. """
        i, j = position
        """ Horizontal line change """
        """ From left to right """
        left = 0
        do = False
        k = j + 1
        while k < 8:
            pos = self._board[i][k]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                left += 1
            k += 1
        if do:
            for m in range(0, left + 1):
                self._board[i][j + m] = color
        """ From right to left """
        right = 0
        do = False
        k = j - 1
        while k > 0:
            pos = self._board[i][k]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                right += 1
            k -= 1
        if do:
            for m in range(0, right + 1):
                self._board[i][j - m] = color
        """ From down to up """
        down = 0
        do = False
        k = i - 1
        while k > 0:
            pos = self._board[k][j]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                down += 1
            k -= 1
        if do:
            for m in range(0, down + 1):
                self._board[i - m][j] = color

        """ From up to down """
        up = 0
        do = False
        k = i + 1
        while k < 8:
            pos = self._board[k][j]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                up += 1
            k += 1
        if do:
            for m in range(0, left + 1):
                self._board[i + m][j] = color

        """ from left bottom to upper right """
        left_down = 0
        do = False
        k = i - 1
        p = j + 1
        while k > 0 and p < 8:
            pos = self._board[k][p]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                left_down += 1
            k -= 1
            p += 1
        if do:
            for m in range(0, left_down + 1):
                self._board[i - m][j + m] = color

        """ From upper left to right bottom """
        left_up = 0
        do = False
        k = i + 1
        p = j + 1
        while k < 8 and p < 8:
            pos = self._board[k][p]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                left_up += 1
            k += 1
            p += 1
        if do:
            for m in range(0, left_up + 1):
                self._board[i + m][j + m] = color

        """ From bottom right to upper left """
        right_down = 0
        do = False
        k = i - 1
        p = j - 1
        while k > 0 and p > 0:
            pos = self._board[k][p]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                right_down += 1
            k -= 1
            p -= 1
        if do:
            for m in range(0, right_down + 1):
                self._board[i - m][j - m] = color

        """ From upper right to left bottom """
        right_up = 0
        do = False
        k = i + 1
        p = j - 1
        while k < 8 and p > 0:
            pos = self._board[k][p]
            if pos is color:
                do = True
                break
            if pos is " ":
                do = False
                break
            if pos is not color:
                right_up += 1
            k += 1
            p -= 1
        if do:
            for m in range(0, right_up + 1):
                self._board[i + m][j - m] = color

    def update(self, black_pos, white_pos):
        """ update the board when an agent give a feedback """
        if black_pos is not None:
            self._board[black_pos[0]][black_pos[1]] = b
            self.change_color(b, black_pos)

        elif white_pos is not None:
            self._board[white_pos[0]][white_pos[1]] = w
            self.change_color(w, white_pos)
        check = self.check_win()
        self._end = check[0]
        self._result = check[1]
        self.display()

    def get_successor(self, color):
        """ Allow agents to get successors by calling this method.
        Given successors are in a set of positions. """
        successors = set()
        for i in range(0, 8):
            for j in range(0, 8):
                cell = self._board[i][j]
                if cell is color:
                    """ Vertical check """
                    for k in range(i - 1, -1, -1):
                        up = self._board[k][j]
                        if up is color or (up is " " and k == i - 1):
                            break
                        if up is " " and k != i - 1:
                            successors.add((k, j))
                            break
                    for p in range(i + 1, 8):
                        down = self._board[p][j]
                        if down is color or (down is " " and p == i + 1):
                            break
                        if down is " " and p != i + 1:
                            successors.add((p, j))
                            break
                    """ Horizontal check """
                    for k in range(j - 1, -1, -1):
                        left = self._board[i][k]
                        if left is color or (left is " " and k == j - 1):
                            break
                        if left is " " and k != j - 1:
                            successors.add((i, k))
                            break
                    for p in range(j + 1, 8):
                        right = self._board[i][p]
                        if right is color or (right is " " and p == j + 1):
                            break
                        if right is " " and p != j + 1:
                            successors.add((i, p))
                            break
                    """ Left diagonal check """
                    k = i - 1
                    p = j - 1
                    while k > 0 and p > 0:
                        upper_left = self._board[k][p]
                        if upper_left is color or (upper_left is " " and k == i - 1 and p == j - 1):
                            break
                        if upper_left is " " and k != i - 1 and p != j - 1:
                            successors.add((k, p))
                            break
                        k -= 1
                        p -= 1

                    k = i + 1
                    p = j - 1
                    while k < 8 and p > 0:
                        lower_left = self._board[k][p]
                        if lower_left is color or (lower_left is " " and k == i + 1 and p == j - 1):
                            break
                        if lower_left is " " and k != i + 1 and p != j - 1:
                            successors.add((k, p))
                            break
                        k += 1
                        p -= 1

                    """ Right diagonal check """
                    k = i + 1
                    p = j + 1
                    while k < 8 and p < 8:
                        lower_right = self._board[k][p]
                        if lower_right is color or (lower_right is " " and k == i + 1 and p == j + 1):
                            break
                        if lower_right is " " and k != i + 1 and p != j + 1:
                            successors.add((k, p))
                            break
                        k += 1
                        p += 1

                    k = i - 1
                    p = j + 1
                    while k > 0 and p < 8:
                        upper_right = self._board[k][p]
                        if upper_right is color or (upper_right is " " and k == i - 1 and p == j + 1):
                            break
                        if upper_right is " " and k != i - 1 and p != j + 1:
                            successors.add((k, p))
                            break
                        k -= 1
                        p += 1

        return successors

    def get_simple_reward(self, action):
        return self._resource[action[0]][action[1]]

    @property
    def end(self):
        return self._end


class Game:
    def __init__(self, agent_black, agent_white):
        self._agent_black = agent_black
        self._agent_white = agent_white
        self._state = State()

    def start(self):
        i = 0
        self._state.display()
        while True:
            black_pos = self._agent_black.get_action(self._state)
            self._state.update(black_pos, None)

            if self._state.end:
                break

            pos_white = self._agent_white.get_action(self._state)
            self._state.update(None, pos_white)

            if self._state.end:
                break
            i += 1


def main():
    g = Game(agents.SimpleMDPAgent(b), agents.SimpleMDPAgent(w))
    g.start()


if __name__ == '__main__':
    main()
