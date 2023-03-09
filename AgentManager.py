""" Agent Manager stores an agent's state and applies
    a decision rule based on various inputs.
    
Michael A. Goodrich
July 2022
Brigham Young University """

#import StateManager
import random
from Constants import LegalStateValues 
class agentHandler:

    def __init__(self,agent_id = 0, agent_state = 'NEUTRAL'):
        if self._isStateLegal(agent_state): self.agent_state = agent_state
        else: print("Tried to set agent state to illegal value. Exiting");exit(-1)
        self.agent_id = agent_id
        self._updateAgentColor()
    
    """ Private methods """
    def _isStateLegal(self,state):
        return state in set(LegalStateValues.keys())
    def _updateAgentColor(self):
        if self.agent_state == 'NEUTRAL': self.agent_color = 'w'
        elif self.agent_state == 'BLUE': self.agent_color = 'b'
        elif self.agent_state == 'MAGENTA': self.agent_color = 'm'
        else: self.agent_color = 'CYAN' #cyan
    def _findAllMaxima(self,neighbor_states):
        """ Returns list of all indices of a list that are maximal values """
        max_list = [i for i in range(len(neighbor_states)) if neighbor_states[i] == max(neighbor_states)]
        return max_list
    def _randomlyChooseMax(self,neighbor_states):
        max_list = self._findAllMaxima(neighbor_states)
        arg_max = random.choice(max_list)
        if arg_max == 0: next_state = 'BLUE'
        elif arg_max == 1: next_state = 'MAGENTA'
        elif arg_max == 2: next_state = 'CYAN'
        else: next_state = 'NEUTRAL'
        return next_state

    """ Public access methods """
    def getAgentState(self): return self.agent_state
    def setAgentState(self,agent_state):
        if self._isStateLegal(agent_state): 
            self.agent_state = agent_state
            self._updateAgentColor()
        else: print("Tried to set agent state to illegal value. Exiting");exit(-1)
    def getAgentColor(self): return self.agent_color
    def getAgentID(self): return self.agent_id
    def isAgentNeutral(self): 
        if self.agent_color == 'NEUTRAL': return True
        else: return False
    
    """ Public decision methods """
    def updateState_SimpleMajority(self,num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors):
        """ return the state that matches the maximum number of neighbors with that color.
        Ties are broken randomly """
        neighbor_states = [num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors]
        next_state = self._randomlyChooseMax(neighbor_states)
        if max(neighbor_states) == 0: next_state = self.agent_state
        return next_state
    def updateState_SimpleMajority_WithThreshold(self,num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors,threshold = 2):
        """ return the state that matches the maximum number of neighbors with that color.
        Ties are broken randomly. 
        Must have at least threshold neighbors of a given color to change """
        neighbor_states = [num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors]
        next_state = self._randomlyChooseMax(neighbor_states)
        if max(neighbor_states) < threshold: next_state = self.agent_state
        return next_state
    def updateState_MaxExpectedUtility(self,num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors,num_neighbors):
        neighbor_states = [num_blue_neighbors,num_magenta_neighbors,num_cyan_neighbors]
        expected_values = dict()
        expected_values['BLUE'] = num_blue_neighbors/num_neighbors*LegalStateValues['BLUE']
        expected_values['MAGENTA'] = num_magenta_neighbors/num_neighbors*LegalStateValues['MAGENTA']
        expected_values['CYAN'] = num_cyan_neighbors/num_neighbors*LegalStateValues['CYAN']
        if max[neighbor_states] == 0: self.agent_state = 'NEUTRAL'
        elif expected_values['BLUE'] == max(expected_values.values()): self.agent_state = 'BLUE'
        elif expected_values['MAGENTA'] == max(expected_values.values()): self.agent_state = 'MAGENTA'
        else: self.agent_state = 'CYAN'
        self._updateAgentColor()
        # Known bias. Tie-breakers are blue over magenta and cyan, and magenta over cyan