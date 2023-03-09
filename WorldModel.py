""" World model method. Creates and manages the network of agents.

The world includes the state of the interaction network and the state of the agents.

Michael A. Goodrich
Brigham Young University
August 2022 """

from telnetlib import GA
from AssortativeNetworkManager import *
from AgentManager import *
from math import inf

class worldManager:
    def __init__(self):
        self.myNetwork = MixedNetworkFormation(color_template=['b', 'm', 'c', 'y', 'r', 'c', 'g'])
        self.num_agents = self.myNetwork.getGraph().number_of_nodes()
        self.agent_list = []
        for i in list(self.myNetwork.getGraph().nodes):
            self.agent_list.append(agentHandler(agent_id = i, agent_state = 'NEUTRAL'))
    
    """ Public Methods """
    def getGraph(self): return self.myNetwork.getGraph()
    def getGroundTruthColors(self): return self.myNetwork.getGroundTruthColors()
    def getNumberOfAgents(self): return self.myNetwork.getGraph().number_of_nodes()
    def getNumberOfNeighbors(self,agent_id): return self.myNetwork.getGraph().degree(agent_id)
    def getNeighbors(self,agent_id): return self.myNetwork.getGraph().neighbors(agent_id)
    def agentID_ToAgent(self,agent_id): return self.agent_list[agent_id]
    def getColorTemplate(self): return self.myNetwork.getColorTemplate()
    """ Public methods for managing collection of agents """
    def getAgent_ColorMap(self):
        color_map = []
        for agent in self.agent_list:
            color_map.append(agent.getAgentColor())
        return color_map
    def getCollectiveState(self):
        state_list = []
        for agent in self.agent_list:
            state_list.append(agent.getAgentState())
        return state_list
    def advanceCollectiveState(self,contact_list = None):
        """ Have each agent make exactly one decision """
        nextStateDict= dict()
        # First, see what the next state would be given the current collective configuration
        for agent in self.agent_list:
            agent_ID = agent.getAgentID()
            numMagentaNeighbors,numCyanNeighbors,numBlueNeighbors = self._getNumNeighborsByColor(agent_ID)
            if contact_list != None:
                if agent_ID == contact_list['MAGENTA']: numMagentaNeighbors += 1
                elif agent_ID == contact_list['CYAN']: numCyanNeighbors += 1
                elif agent_ID == contact_list['BLUE']: numBlueNeighbors += 1

            #next_state = agent.updateState_SimpleMajority(numBlueNeighbors,numMagentaNeighbors,numCyanNeighbors)
            next_state = agent.updateState_SimpleMajority_WithThreshold(numBlueNeighbors,numMagentaNeighbors,numCyanNeighbors)
            nextStateDict[agent] = next_state
        # Second, update the states. Don't update in the previous because otherwise you get bias
        for agent in nextStateDict.keys():
            agent.setAgentState(nextStateDict[agent])
    def initializeCollective(self,adopters):
        # Something external chooses the early adopters
        for color in adopters.keys():
            print("Agent ", adopters[color].getAgentID(), " adopts color ",color)
            adopters[color].setAgentState(color)
        return

    """ Private Methods """
    def _getNumNeighbors(self,agent_id):
        return self.myNetwork.getGraph().neighbors(agent_id)
    def _getNumNeighborsByColor(self,agent_id):
        numMagentaNeighbors = 0
        numCyanNeighbors = 0
        numBlueNeighbors = 0
        neighbors = self.myNetwork.getGraph().neighbors(agent_id)
        for neighbor in neighbors:
            neighbor_state = self.agent_list[neighbor].getAgentState()
            if neighbor_state == 'MAGENTA': numMagentaNeighbors += 1
            elif neighbor_state == 'CYAN': numCyanNeighbors += 1
            elif neighbor_state == 'BLUE': numBlueNeighbors += 1
            #print("agent ", agent_id, " has neighbor ",neighbor_columns[i], 
            #    " with state ", neighbor_state)
        return numMagentaNeighbors,numCyanNeighbors,numBlueNeighbors
 