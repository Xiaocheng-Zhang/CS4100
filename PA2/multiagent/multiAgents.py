# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = newFood.asList()
        minTime = float('inf')
        offset = float('inf')
        minDis = float('inf')
        length = len(newFoodList)
        for scaredTime in newScaredTimes:
            minTime = min(scaredTime, minTime)
            if minTime == 40:
                return float('inf')
        for food in newFoodList:
            offset = min(util.manhattanDistance(newPos, food), offset)
        for ghost in newGhostStates:
            minDis = min(util.manhattanDistance(ghost.getPosition(), newPos), minDis)
            if minDis <= 1 and minTime < 3:
                return float('-inf')
        # all useful data has been generated.
        if minTime == float('inf'):
            minTime = 0
        if minDis == float('inf'):
            minDis = 0
        if offset == float('inf'):
            offset = 0
        # check all data is valid
        # random value help pacman make decision for separate paths
        if minTime != 40 and minTime > 3:
            utility = -3 * offset - length * 67 + minDis - random.randint(0, 8)
        else:
            utility = -3 * offset - length * 67 + random.randint(0, 8)
        # print(action, utility)
        return utility


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # gameState.getLegalActions(agentIndex)
        # gameState.generateSuccessor(agentIndex, action)
        # gameState.getNumAgents()
        # value: gameState
        pacmanActions = gameState.getLegalActions(0)
        maxValue = float('-inf')
        action_index = 0
        depth = 1
        agentIndex = 1
        # print(self.depth)
        for i in range(0, len(pacmanActions)):
            successorGameState = gameState.generateSuccessor(0, pacmanActions[i])
            # pass in the current depth and agentIndex start from 1
            value = self.min_value(successorGameState, depth, agentIndex)
            if value > maxValue:
                maxValue = value
                action_index = i
        return pacmanActions[action_index]

    def min_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        ghostActions = gameState.getLegalActions(agentIndex)
        # print(ghostActions)
        minValue = float('inf')
        # print("index: ", agentIndex)
        for action in ghostActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents() - 1:
                minValue = min(self.min_value(successorGameState, depth, agentIndex + 1), minValue)
            else:
                minValue = min(self.max_value(successorGameState, depth + 1), minValue)
        return minValue

    def max_value(self, gameState, depth):
        # end at next depth
        # print("depth: ", depth, self.depth)
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)
        pacmanActions = gameState.getLegalActions(0)
        maxValue = float('-inf')
        for action in pacmanActions:
            successorGameState = gameState.generateSuccessor(0, action)
            maxValue = max(self.min_value(successorGameState, depth, 1), maxValue)
        return maxValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacmanActions = gameState.getLegalActions(0)
        maxValue = float('-inf')
        action_index = -1
        alpha = float('-inf')
        beta = float('inf')
        depth = 1
        agent_index = 1
        # print(self.depth)
        for index in range(0, len(pacmanActions)):
            successorGameState = gameState.generateSuccessor(0, pacmanActions[index])
            value = self.alpha_min_value(successorGameState, alpha, beta, depth, agent_index)
            if maxValue < value:
                maxValue = value
                action_index = index
            # update the first max's alpha, it caused a lot of bugs...
            alpha = max(maxValue, alpha)
        return pacmanActions[action_index]

    def alpha_min_value(self, gameState, alpha, beta, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        value = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents() - 1:
                value = min(self.alpha_min_value(successorGameState, alpha, beta, depth, agentIndex + 1), value)
            if agentIndex == gameState.getNumAgents() - 1:
                value = min(self.alpha_max_value(successorGameState, alpha, beta, depth + 1), value)
            if value < alpha:
                return value
            beta = min(value, beta)
        return value

    def alpha_max_value(self, gameState, alpha, beta, depth):
        # if self.depth is 4, since it start from 1, it will reach 5, which is the end.
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)
        value = float('-inf')
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            value = max(self.alpha_min_value(successorGameState, alpha, beta, depth, 1), value)
            if value > beta:
                return value
            alpha = max(value, alpha)
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacmanActions = gameState.getLegalActions(0)
        maxValue = float('-inf')
        action_index = 0
        depth = 1
        agentIndex = 1
        for i in range(0, len(pacmanActions)):
            successorGameState = gameState.generateSuccessor(0, pacmanActions[i])
            # pass in the current depth and agentIndex start from 1
            value = self.expect_value(successorGameState, depth, agentIndex)
            if value > maxValue:
                maxValue = value
                action_index = i
        return pacmanActions[action_index]

    def expect_value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        ghostActions = gameState.getLegalActions(agentIndex)
        accumulateValue = 0
        count = 0
        for action in ghostActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            count += 1
            if agentIndex < gameState.getNumAgents() - 1:
                # get expect value of sum of all ghost
                accumulateValue += self.expect_value(successorGameState, depth, agentIndex + 1)
            else:
                # next depth
                accumulateValue += self.max_value(successorGameState, depth + 1)
        return accumulateValue / count

    def max_value(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)
        pacmanActions = gameState.getLegalActions(0)
        maxValue = float('-inf')
        for action in pacmanActions:
            successorGameState = gameState.generateSuccessor(0, action)
            maxValue = max(self.expect_value(successorGameState, depth, 1), maxValue)
        return maxValue


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    powerDots = currentGameState.getCapsules()

    newFoodList = newFood.asList()
    minTime = float('inf')
    offset = float('inf')
    minDis = float('inf')
    length = len(newFoodList)
    dotDis = float('inf')

    for dot in powerDots:
        dotDis = min(util.manhattanDistance(dot, newPos), dotDis)
    for scaredTime in newScaredTimes:
        minTime = min(scaredTime, minTime)
    for food in newFoodList:
        offset = min(util.manhattanDistance(newPos, food), offset)
    for ghost in newGhostStates:
        minDis = min(util.manhattanDistance(ghost.getPosition(), newPos), minDis)
        if minDis == 0 and minTime <= 0:
            # avoid the ghosts when they are not scared
            # print("run", minTime)
            return float('-inf')

    # all useful data has been generated.
    if minTime == float('inf'):
        minTime = 0
    if minDis == float('inf'):
        minDis = 0
    if offset == float('inf'):
        offset = 0
    if dotDis == float('inf'):
        dotDis = 0
    # check all data is valid
    # random value help pacman make decision for separate paths
    if minTime > 0:
        # print("eat")
        # encourage pacman to attack ghost
        if minDis == 0:
            return float('inf')
        utility = -7 * minDis
        # + random.randint(0, 7)
    else:
        # print("no")
        utility = -3 * offset - length * 67 + random.randint(0, 8) - 57 * dotDis
    # print(action, utility)
    return utility


# Abbreviation
better = betterEvaluationFunction
