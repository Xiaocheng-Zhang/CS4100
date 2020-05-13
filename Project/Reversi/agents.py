from abc import ABC


class Agent(ABC):
    """ Agent abstract class """

    def __init__(self):
        pass

    def get_action(self, state):
        pass


class SimpleMDPAgent(Agent):
    """ Simple MDP Agent which base on the value in the table called resource """

    def __init__(self, color):
        self._color = color

    def get_action(self, state):
        """ return the chosen position as an action to the Game """
        successors = state.get_successor(self._color)
        max_val = float('-inf')
        action = None
        for successor in successors:
            val = state.get_simple_reward(successor)
            if val > max_val:
                action = successor
                max_val = val
        return action
