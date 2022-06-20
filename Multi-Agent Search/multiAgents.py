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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFood=newFood.asList()
        foodNum = currentGameState.getFood().count()
        distanceFood=[]
        if len(newFood)==foodNum:
            for f in newFood:
                distanceFood.append(manhattanDistance(newPos,f))
        else:
            distanceFood.append(0)
        
        for ghost in newGhostStates:
            dis=min(distanceFood)+4**(2-manhattanDistance(newPos,ghost.getPosition()))

        return -dis
        return childGameState.getScore()

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def MiniMax(agent,depth,gameState):
            if (depth==self.depth or gameState.isWin()==True or gameState.isLose()==True):      #end the game if we reach max depth of tree or We win or lose 
                return self.evaluationFunction(gameState)

            if (agent==0):         #Pacman plays
                v=-1000000
                for action in gameState.getLegalActions(agent):
                    eval=MiniMax(1,depth,gameState.getNextState(agent,action))    
                    if eval>v:
                        v=eval
                return v
            else:                                               #Ghost plays
                
                nextagent=agent+1
                if (nextagent==gameState.getNumAgents()):
                    nextagent=0
                
                if (nextagent==0):                  #if nextagent==0=pacman then increase the depth of tree because pacman and ghosts have made their move
                    depth+=1
                
                v=1000000
                for action in gameState.getLegalActions(agent):
                    eval=MiniMax(nextagent,depth,gameState.getNextState(agent,action))
                    if eval<v:
                        v=eval
                
                return v
        
        
        #   Main    #
        MinMax=-10000000
        for action in gameState.getLegalActions(0):
            val=MiniMax(1,0,gameState.getNextState(0,action))
            if MinMax<val or MinMax==-10000000:
                MinMax=val
                MinMaxAction=action

        return MinMaxAction
 
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def Alpha_Beta(a,b,agent,depth,gameState):
            if (depth==self.depth or gameState.isWin()==True or gameState.isLose()==True):      #end the game if we reach max depth of tree or We win or lose 
                return self.evaluationFunction(gameState)
            
            if (agent==0):              #Pac-Man plays (max-value)
                v=-1000000
                for action in gameState.getLegalActions(agent):
                    v=max(v,Alpha_Beta(a,b,1,depth,gameState.getNextState(agent,action)))
                    if v>b: return v
                    a=max(a,v)
                return v
            else:                       #Ghosts play (min-value)
                nextagent=agent+1
                if (nextagent==gameState.getNumAgents()):
                    nextagent=0
                
                if (nextagent==0):                  #if nextagent==0=pacman then increase the depth of tree because pacman and ghosts have made their move
                    depth+=1

                v=1000000
                for action in gameState.getLegalActions(agent):
                    v=min(v,Alpha_Beta(a,b,nextagent,depth,gameState.getNextState(agent,action)))
                    if v<a: return v
                    b=min(b,v)
                return v

        #   Main    #
        MinMax=-10000000
        a=-1000000
        b=+1000000
        for action in gameState.getLegalActions(0):
            val=Alpha_Beta(a,b,1,0,gameState.getNextState(0,action))
            if MinMax<val or MinMax==-10000000:
                MinMax=val
                MinMaxAction=action
            if MinMax>b: return MinMaxAction
            a=max(a,MinMax)

        return MinMaxAction
        
        
        
        util.raiseNotDefined()

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
        def Expectimax(agent,depth,gameState):
            if (depth==self.depth or gameState.isWin()==True or gameState.isLose()==True):      #end the game if we reach max depth of tree or We win or lose 
                return self.evaluationFunction(gameState)
            
            if (agent==0):                  #Pac-Man plays (Max-Value)
                v=-1000000
                for action in gameState.getLegalActions(agent):
                    v=max(v,Expectimax(1,depth,gameState.getNextState(agent,action)))
                return v
            else:                       #Ghosts Play (Expectimax value)
                nextagent=agent+1
                if (nextagent==gameState.getNumAgents()):
                    nextagent=0
                
                if (nextagent==0):                  #if nextagent==0=pacman then increase the depth of tree because pacman and ghosts have made their move
                    depth+=1
                
                r=0
                for action in gameState.getLegalActions(agent):
                    r= r+1/(len(gameState.getLegalActions(agent))) * Expectimax(nextagent,depth,gameState.getNextState(agent,action))       #propabillity p(r) is 1/(number of legal moves) which are at most 4
                return r

        #   Main    #
        ExpectiMax=-10000000
        for action in gameState.getLegalActions(0):
            val=Expectimax(1,0,gameState.getNextState(0,action))
            if ExpectiMax<val or ExpectiMax==-10000000:
                ExpectiMax=val
                MinMaxAction=action

        return MinMaxAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position=currentGameState.getPacmanPosition()
    Food=currentGameState.getFood()
    GhostStates=currentGameState.getGhostStates()

    if currentGameState.isLose():
        return -1000000
    
    if currentGameState.isWin():
        return 1000000


    Food=Food.asList()
    distanceFood=[]
    for foodpos in Food:
        distanceFood.append(manhattanDistance(position,foodpos))

    if len(distanceFood)==0:
        distanceFood.append(0)
    # active ghosts are ghosts that aren't scared.
    scaredGhosts=[]
    activeGhosts=[]
    for ghost in GhostStates:
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else: 
            scaredGhosts.append(ghost)
    
    ghostDistanceScared=[]
    ghostDistanceActive=[]
    
    #Distance from active Ghosts
    if len(activeGhosts)!=0:
        for ghost in activeGhosts:
            ghostDistanceActive.append(manhattanDistance(position,ghost.getPosition()))

    if len(ghostDistanceActive)==0:
        ghostDistanceActive.append(0)

    #Distance from scared Ghosts
    if len(scaredGhosts)!=0:
        for ghost in scaredGhosts:
            ghostDistanceScared.append(manhattanDistance(position,ghost.getPosition()))

  
    if len(ghostDistanceScared)==0:
        ghostDistanceScared.append(0)

    dis=-1.5*min(distanceFood)+-4**((min(ghostDistanceActive)))+-2*(min(ghostDistanceScared))+-4*len(Food)+-20*len(currentGameState.getCapsules())
    return dis
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
