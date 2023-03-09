""" SalesForceManager.py

Manages a collection of simulated sales persons 
for the guided diffusion of innovations game.

Michael Goodrich
Brigham Young University
August 2022
"""
from Constants import LegalAgentColors
from numpy import inf
from WizardManager import *

class salesForceHandler:
    def __init__(self,world_model, communities):
        self.world_model = world_model
        self.communities = communities
        self.wizard_list = self._initalizeWizardList()

    """ Public methods """
    def getEarlyAdopters(self):
        """ Return dictionary of the early adopters for a given wizard color """
        adopters = dict()
        for wizard in self.wizard_list:
            adopters[wizard.getWizardColor()] = wizard.chooseEarlyAdopter()
        return adopters
    def getSalesCalls(self):
        contacts = dict()
        for wizard in self.wizard_list:
            who_to_contact = wizard.chooseNextSalesCall()
            print("The ", wizard.getWizardColor()," wants to sell to ", who_to_contact)
            contacts[wizard.getWizardColor()] = who_to_contact
        return contacts
    """ Private methods """
    def _initalizeWizardList(self):
        if len(self.communities) < 3: 
            print("Not allowed to partition agents into 3 or fewer sets. Exiting")
            exit(-1)
        wizard_list = []
        largest_partitions = self._findThreeLargestCommunities(self.communities)
        color_list = ['MAGENTA','CYAN','BLUE']
        random.shuffle(color_list) # Shuffle so that each sales wizard gets a chance to be assigned the largest community
        for i in range(len(largest_partitions)):
            community = list(self.communities[largest_partitions[i]])
            color = color_list[i]
            wizard = wizardHandler(self.world_model,color,community)
            wizard_list.append(wizard)
        return wizard_list
    def _findThreeLargestCommunities(self,communities):
        """ Returns the three partitions from the communities with the most agents as a list of indices """
        smallest_partition_index = -1
        smallest_partition_size = inf
        partition_number = 0
        for partition in communities:
            if len(partition) < smallest_partition_size:
                smallest_partition_size = len(partition)
                smallest_partition_index = partition_number
            partition_number += 1
        largest_communities = []
        for i in range(len(communities)):
            if i != smallest_partition_index: largest_communities.append(i)
        return largest_communities