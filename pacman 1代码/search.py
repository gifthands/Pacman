#coding:utf-8
# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    from game import Directions
 
    # fringe 候选， closed 走过的节点，path 记录路径
    # 深度搜索选择栈
    fringe = Stack()
    closed = []
 
    # 加入起始状态节点
    fringe.push((problem.getStartState(), []))
 
    # 如果候选不为空，则循环搜索
    while not fringe.isEmpty():
        
        # 当前节点
        cur_node, actions = fringe.pop()
 
        # 如果当前节点到达目标位置
        if problem.isGoalState(cur_node):
            return actions
 
        if cur_node not in closed:
            expand = problem.getSuccessors(cur_node)
            closed.append(cur_node)
            for location, direction, cost in expand:
                if (location not in closed):
                    fringe.push((location, actions + [direction]))
 
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    from game import Directions
    # fringe 候选， closed 走过的节点
    # 广度搜索选择栈
    fringe = Queue()
    closed = []
    
    # 加入起始状态节点
    fringe.push((problem.getStartState(), []))
    
    # 如果候选不为空，则循环搜索
    while not fringe.isEmpty():
        
        # 当前节点
        cur_node, actions = fringe.pop()
 
        # 如果当前节点到达目标位置
        if problem.isGoalState(cur_node):
            return actions
 
        if cur_node not in closed:
            # 寻找后继节点
            expand = problem.getSuccessors(cur_node)
            # 当前节点加入到走过路程中
            closed.append(cur_node)
 
            for location, direction, cost in expand:
                # 如果后继节点不在走过路程中，就新建一个候选，这个候选的路径是当前节点路径加上此次方向
                if (location not in closed):
                    fringe.push((location, actions + [direction]))
 
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #扩展的是路径消耗g(n)最小的节点n,用优先队列来实现，对解的路径步数不关心，只关心路径总代价。
    #即使找到目标节点也不会结束，而是再检查新路径是不是要比老路径好，确实好，则丢弃老路径。
 
    
    start_point = problem.getStartState()                           #点
    queue = util.PriorityQueueWithFunction(lambda x: x[2])         #记录当前队列
    queue.push((start_point,None,0))                               #加入队列
    cost=0                                                          #现在的代价.
    visited = []                                                    #标记是否记录
    path = []                                                       #记录路径
    parentSeq = {}
    parentSeq[(start_point,None,0)]=None
    while queue.isEmpty() == False:
        current_fullstate = queue.pop()                            #当前点
        #print current_fullstate
        if (problem.isGoalState(current_fullstate[0])):             #目标状态
            break
        else:
            current_state = current_fullstate[0]
            if current_state not in visited:
                visited.append(current_state)
            else:
                continue
            successors = problem.getSuccessors(current_state)           #继承表后继
            for state in successors:
                cost= current_fullstate[2] + state[2];
                #print state,cost
                if state[0] not in visited:
                    queue.push((state[0],state[1],cost))
                    #parentSeq[state] = current_fullstate
                    parentSeq[(state[0],state[1])] = current_fullstate
 
    child = current_fullstate
 
    while (child != None):
        path.append(child[1])
        if child[0] != start_point:
            child = parentSeq[(child[0],child[1])]
        else:
            child = None
    path.reverse()
    return path[1:]
 
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from sets import Set
    fringe = util.PriorityQueue()                        # 使用优先队列，每次扩展都是选择当前代价最小的方向，即队头
    actions = []                                    # 选择的操作
    fringe.push((problem.getStartState(),actions),0)   # 把初始化点加入队列，开始扩展
    visited = []                                # 标记已经走过的点
    tmpActions = []
    while fringe:
        currState,actions = fringe.pop()      # 当前状态
        if problem.isGoalState(currState):
            break
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for successor, action, cost in successors:
                tempActions = actions + [action]
                nextCost = problem.getCostOfActions(tempActions) + heuristic(successor,problem)      # 对可选的几个方向，计算代价
                if successor not in visited:
                    fringe.push((successor,tempActions),nextCost)
    return actions                # 返回到达终点的操作顺序


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
