""" Run a guided diffusion of innovations problem.
    Create an assortative network.
    Check out its properties by looking at a dendogram.
    Find its communities using the Louvain algorithm.
    Run diffusion of innovations without external input by initializing and running freely
    Figure out how to have three agents guide the diffusion.
    Evaluate the resilience properties using the concepts in the multiagent resilience paper
    
Michael A. Goodrich
July 2022
Brigham Young University
"""

#from scipy.sparse import csr_matrix
from WorldModel import *
from GraphManager import *
from SalesForceManager import *

def main():
    myWorld = worldManager()
    myGraphHandler = graphHandler(myWorld)
    myGraphHandler.showGraph()
    #myGraphHandler.showDendrogram()
    # Partition using the Louvain method and show graph. 
    #partition_list = myGraphHandler.getAgentColors_from_LouvainCommunities()
    #myGraphHandler.showGraph(title = "Louvain partition for the assortative graph",agent_colors=partition_list)
    
    # Partition using the Girvan Newman method, show graph, and select best
    # individuals as early adopters.
    color_map, communities = myGraphHandler.getAgentColors_from_GirvanNewmanCommunities()
    myGraphHandler.showGraph(title = "Girvan-Newman partition for the assortative graph",agent_colors=color_map)
    
    mySalesForceHandler = salesForceHandler(myWorld,communities)
    time_limit = 30
    for t in range(time_limit):
        if t==0:
            early_adopters = mySalesForceHandler.getEarlyAdopters()
            myWorld.initializeCollective(early_adopters)
            myGraphHandler.showGraph(title = "Initial states of agents",agent_colors = myWorld.getAgent_ColorMap()) 
        myWorld.advanceCollectiveState(contact_list = mySalesForceHandler.getSalesCalls())
        my_title = "Collective state after " + str(t+1) + " time steps"
        if t == time_limit - 1:
            myGraphHandler.updateGraph(title = my_title,wait_for_button=True,agent_colors = myWorld.getAgent_ColorMap()) 
        else: myGraphHandler.updateGraph(title = my_title,agent_colors = myWorld.getAgent_ColorMap()) 
    

main()