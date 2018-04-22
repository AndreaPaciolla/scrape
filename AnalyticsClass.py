import networkx as nx
import matplotlib.pyplot as plt
import scipy
import numpy
#from statsmodels.distributions.empirical_distribution import ECDF
import scipy.stats as sp 
import pylab

class Analytics(object):

    network_graph = {}

    def __init__(self, model): 
        print('Creating new graph')
        self.network_graph = nx.Graph()
        # Add all the users as nodes of the graph
        for u in model:
            self.network_graph.add_node(u.get('id'), info=u)

    def __getitem__(self, item):
        return getattr(self, item)

    #
    # The model is a single user
    #
    def add_edges(self, modelSource, modelDestination):
        print( 'Adding edge from {} to {} ' . format(modelSource.get('username'), modelDestination.get('username')) )
        # First of all check the node existance
        try:
            # The node exists. Add the edge   
            node = self.network_graph.node[modelDestination.get('id')] 
            self.network_graph.add_edge(modelSource.get('id'), modelDestination.get('id'))
            return True
        except Exception:
            # The node does not exists in the network.
            # Add a node first
            self.network_graph.add_node(modelDestination.get('id'), info=modelDestination)
            # Add the edge
            self.network_graph.add_edge(modelSource.get('id'), modelDestination.get('id'))
            return True
        return False

    def draw_network(self):
        nx.draw_networkx(self.network_graph)
        pylab.show()

    #
    # Total edges
    #
    def get_total_edges(self):
        return self.network_graph.size()

    #
    # Total nodes
    #
    def get_total_nodes(self):
        return self.network_graph.order()

    #
    # Sample stats like mode, median and so on
    #
    def get_stats(self):
        degree_sample = list(dict(self.network_graph.degree).values())
        return {
            'average_degree': numpy.mean(degree_sample),
            'min_degree': numpy.min(degree_sample),
            'max_degree': numpy.max(degree_sample),
            'median': numpy.median(degree_sample),
            'mode': sp.mode(degree_sample).mode[0]
        } 

    #
    # Draw the Cumulative Distribution Function
    #
    def draw_cdf(self, loglog_scale):
        degree_sample = list(dict(self.network_graph.degree).values())
        #cdf = ECDF(degree_sample) @TODO FIX ECDF DEPENDENCY to delete the three lines below
        count_network, bins_network = numpy.histogram( degree_sample, numpy.arange( numpy.min(degree_sample), numpy.max(degree_sample)+2 ) )
        pdf_network = count_network/(self.network_graph.order())
        cdf = numpy.cumsum(pdf_network)

        x = numpy.unique(degree_sample)
        y = cdf(x)
        
        fig = plt.figure(figsize=(16,9))
        axis = fig.gca()

        if loglog_scale == True:
            axis.loglog(x, y, color='red', marker='o', linestyle='--', ms = 8)
        axis.set_xlabel('Degree',size=30)
        axis.set_ylabel('CDF',size=30)

        pylab.show()

    #
    # Draw the Probability Distribution Function 
    #
    def draw_pdf(self, loglog_scale):
        network_degree = list(dict(self.network_graph.degree).values())

        count_network, bins_network = numpy.histogram(network_degree, numpy.arange( numpy.min(network_degree), numpy.max(network_degree) +2 ))

        pdf_network = count_network/(self.network_graph.order())

        fig = plt.figure(figsize=(16,9))
        axis = fig.gca()

        if loglog_scale == True:
            axis.loglog(bins_network[:-1],pdf_network,color='orange', marker='o',linestyle='None', ms = 9)
        else:
            axis.plot(bins_network[:-1], pdf_network, color='orange', marker='o', linestyle='None', ms = 7)

        axis.set_xlabel('Degree', size = 30)
        axis.set_ylabel('PDF', size = 30)

        pylab.show()

    #
    # Get the hubs
    #
    def get_hubs(self):
        network_degree = list(dict(self.network_graph.degree).values())
        # Define a thresold to identify what is "high degree"
        # I choose to check percentile with p = 0.95
        # I know that 95% of total nodes have got a degree which is lower than quantile_95 variable
        quantile_95 = numpy.percentile(network_degree, 95) 
        # Now get the nodes
        hub_nodes = [k for k,v in dict(self.network_graph.degree).items() if v >= quantile_95]
        # Extend the hub_nodes array list with information about users
        # Getting Array<User>
        hubs = []
        for hubId in hub_nodes:
            hubs.append( self.network_graph.node[hubId].get('info') )
        return hubs

    #
    # Compute nodes' centrality (betweenness)
    #
    def get_nodes_centrality(self): 
        return nx.betweenness_centrality(self.network_graph)


