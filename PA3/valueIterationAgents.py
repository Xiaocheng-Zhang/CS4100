# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()
        self.temp_values = util.Counter()
        # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        states = self.mdp.getStates()
        while self.iterations > 0:
            self.temp_values = util.Counter()
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                max_val = float('-inf')
                for action in actions:
                    val = self.getQValue(state, action)
                    if val > max_val:
                        max_val = val
                        self.temp_values[state] = max_val
            self.values = self.temp_values
            self.iterations -= 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        state_list = self.mdp.getTransitionStatesAndProbs(state, action)
        for next_state, prob in state_list:
            reward = self.mdp.getReward(state, action, next_state)
            q_value += prob * (reward + self.discount * self.getValue(next_state))
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        best_action = None
        if self.mdp.isTerminal(state):
            return best_action
        max_val = float('-inf')
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            val = self.computeQValueFromValues(state, action)
            if val > max_val:
                max_val = val
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        """*** YOUR CODE HERE ***"""
        max_value = float('-inf')
        states = self.mdp.getStates()
        max_values = []
        for i in range(self.iterations):
            current = util.Counter()
            length = len(states)
            state = states[i % length]
            if not self.mdp.isTerminal(state):
                max_values.clear()
            else:
                current[state] = 0
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                value = 0
                for nextAction, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    reward = self.mdp.getReward(state, action, nextAction)
                    value = value + prob * (reward + self.discount * self.values[nextAction])
                max_values.append(value)
                max_value = max(value, max_value)
                length = len(max_values)
                if length != 0:
                    current[state] = max(max_values)
            self.values[state] = current[state]


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        """*** YOUR CODE HERE ***"""
        priority_queue = util.PriorityQueue()
        states = self.mdp.getStates()
        accumulator = {}
        self.iterate_transposition_states(states, accumulator)
        self.iterate_states(states, priority_queue)
        self.iterate_priority_queue_state(accumulator, priority_queue)

    def iterate_transposition_states(self, states, accumulator):
        for tmp_state in states:
            previous = set()
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    states_and_prob = self.mdp.getTransitionStatesAndProbs(state, action)
                    for next_state, probability in states_and_prob:
                        if not probability == 0:
                            if tmp_state == next_state:
                                previous.add(state)
            accumulator[tmp_state] = previous

    def iterate_states(self, states, priority_queue):
        for state in states:
            if self.mdp.isTerminal(state) is False:
                current = self.values[state]
                q_val = []
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    temp_value = self.computeQValueFromValues(state, action)
                    q_val.append(temp_value)
                max_value = max(q_val)
                offset = current - max_value
                if offset > 0:
                    offset *= -1
                priority_queue.push(state, offset)

    def iterate_priority_queue_state(self, accumulator, priority_queue):
        for i in range(0, self.iterations):
            if priority_queue.isEmpty():
                break
            state = priority_queue.pop()
            if not self.mdp.isTerminal(state):
                saved_values = []
                for action in self.mdp.getPossibleActions(state):
                    val = 0
                    for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        reward = self.mdp.getReward(state, action, next_state)
                        val += prob * (reward + (self.discount * self.values[next_state]))
                    saved_values.append(val)
                self.values[state] = max(saved_values)
            for prev_state in accumulator[state]:
                current = self.values[prev_state]
                q_values = []
                for action in self.mdp.getPossibleActions(prev_state):
                    q_values.append(self.computeQValueFromValues(prev_state, action))
                max_value = max(q_values)
                offset = abs((current - max_value))
                if offset > self.theta:
                    priority_queue.update(prev_state, -offset)
