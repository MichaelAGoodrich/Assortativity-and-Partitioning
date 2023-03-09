""" WizardManager.py

Manages a simulated sales persons
for the guided diffusion of innovations game.

Michael Goodrich
Brigham Young University
August 2022
"""

from Constants import LegalAgentColors
import random

class wizardHandler:
    def __init__(self,world_model,wizard_color,assigned_community):
        if self._isColorLegal(wizard_color): self.wizard_color = wizard_color
        else: print("Tried to set wizard color to illegal value. Exiting");exit(-1)
        # Assume that sales agents are only selling to agents within their assigned community
        # This assumption will need to be changed for a good study to be performec
        self.world_model = world_model # to access states of the sales agents in the world
        self.assigned_community = assigned_community

    """ Public methods """
    def chooseEarlyAdopter(self):
        max_degree = 0
        most_connected_agent_id = self.assigned_community[0]
        for agent_id in self.assigned_community:
            degree = self.world_model.getNumberOfNeighbors(agent_id)
            if degree > max_degree:
                max_degree = degree
                most_connected_agent_id = agent_id
        return self.world_model.agentID_ToAgent(most_connected_agent_id)
    def getWizardColor(self): return self.wizard_color
    def chooseNextSalesCall(self):
        """ ALGORITHM 
            1. For each agent that has adopted the wizard's color
            2.      randomly choose a neighbor that is either neutral or has a color that differs from the wizard
            3.      pitch to that neutral neighbor
            Only check neighbors that are both adjacent to one that has committed and that are in the community
        """
        committed_agents = self._getAgentsOfWizardColor()
        random.shuffle(committed_agents) # Randomly choose order
        for agent_ID in committed_agents:
            neighbors = set(self.world_model.getNeighbors(agent_ID))
            neutral_neighbors = list(set(neighbors).difference(committed_agents))
            # Neutral neighbors can include those in the community that have adopted another state
            # besides the wizard's color. Since the color from another community can
            # diffuse into the wizard's assigned community, agents within the wizard's
            # community can be any color. It's fair game to sell to agents within the
            # wizar'd community who have adopted another color.
            if len(neutral_neighbors) > 0: # Set not empty
                random.shuffle(neutral_neighbors)
                neighbor_ID = neutral_neighbors[0] # Choose first element of shuffled set
                #print("The ",str(self.wizard_color), " wizard wants to sell to agent ",neighbor_ID)
                return neighbor_ID
        return random.choice(self.assigned_community) # if there is no one left in the community to sell to choose randomly
    def chooseNextSalesCall_GARBAGE(self):
        """ POSSIBLE ALGORITHM
            1. Find all agents that have adopted the wizard's color
            2. For each of those agents, find all NEUTRAL neighbors
            3. Return the NEUTRAL neighbor with highest number of its own neutral neighbors

            Order N^3 since I need neighbors of neighbors for each agent
            Can reduce this somewhat if agents only search over their assigned communities


            DIFFERENT ALGORITHM
            1. Randomly choose an agent from the community that has exactly one neighbor who has adopted the wizard's color
            3. Pitch to that agent
        """
        most_connections_by_neutral_neighbor = 0
        most_connected_neutral_neighborID= None
        for agent in self.agent_list:
            if agent.getAgentColor() != self.wizard_color: continue
            neutral_neighbors = self._getNeutralNeighborIDList(agent.getAgentID())
            for neighbor_ID in range(len(neutral_neighbors)):
                num_neutral_neighbors_of_neutral_neighbors = sum(self._getNeutralNeighborIDList(neighbor_ID))
                if num_neutral_neighbors_of_neutral_neighbors > most_connections_by_neutral_neighbor:
                    most_connections_by_neutral_neighbor = num_neutral_neighbors_of_neutral_neighbors
                    most_connected_neutral_neighborID = neighbor_ID
        return most_connected_neutral_neighborID

    """ Private methods """
    def _getAgentsOfWizardColor(self):
        committed_agents = []
        for agent_ID in self.assigned_community:
            agent = self.world_model.agentID_ToAgent(agent_ID)
            if agent.getAgentState() == self.wizard_color: 
                committed_agents.append(agent_ID)
        return committed_agents
    def _isColorLegal(self,state):
        return state in set(LegalAgentColors)
    def _getNeutralNeighborIDList(self,agent_id):
        neighborIDs = self.world_model.getNeighbors(agent_id)
        IDs_of_neutral_neighbors = []
        for id in neighborIDs:
            if self.agent_list[neighborIDs[id]].isAgentNeutral():
                IDs_of_neutral_neighbors.append(id)
        return IDs_of_neutral_neighbors