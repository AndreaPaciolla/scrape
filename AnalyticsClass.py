import networkx as nx
import matplotlib.pyplot as plt
import scipy
import numpy
import math
import geocoder
from statsmodels.distributions.empirical_distribution import ECDF
import scipy.stats as sp 
import pylab
import operator
import time
from itertools import islice
from configuration import GOOGLE_GEOCODER_API_KEY

class Analytics(object):

    network_graph = {}

    def __init__(self, model, fromFile=False): 
        print('Creating new graph')
        if fromFile:
            self.network_graph = nx.read_gexf("500px.gexf")
        else:
            self.network_graph = nx.DiGraph()
            # Add all the users as nodes of the graph
            for u in model:
                country_to_add = u.get('country') if u.get('country') else ' ' 
                city_to_add = u.get('city') if u.get('city') else ' ' 
                affection_to_add = u.get('affection') if u.get('affection') else 0
                kwargs_geocode = {'key': GOOGLE_GEOCODER_API_KEY}

                #if country_to_add is not None and city_to_add is not None:
                #    coords = geocoder.google(city_to_add + ' ' + country_to_add, **kwargs_geocode)
                    #if coords.ok == True:
                self.network_graph.add_node(u.get('id'), affection=affection_to_add, country=country_to_add, city=city_to_add, info=u)



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
            country_to_add = modelDestination.get('country') if modelDestination.get('country') else ' ' 
            affection_to_add = modelDestination.get('affection') if modelDestination.get('affection') else 0 
            city_to_add = modelDestination.get('city') if modelDestination.get('city') else ' ' 
            kwargs_geocode = {'key': GOOGLE_GEOCODER_API_KEY}

            #if country_to_add is not None and city_to_add is not None:
            #    time.sleep(5)
            #    coords = geocoder.google(city_to_add + ' ' + country_to_add, **kwargs_geocode)
            #if coords.ok == True:
            self.network_graph.add_node(modelDestination.get('id'), affection=affection_to_add, country=country_to_add, city=city_to_add, info=modelDestination)

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
            'variance': numpy.var(degree_sample),
            'mode': sp.mode(degree_sample).mode[0],
            'transitivity': nx.transitivity(self.network_graph),
            'reciprocity': nx.reciprocity(self.network_graph),
            'natural_cutoff_erdos': math.log(self.network_graph.order()),
            'natural_cutoff_complete': self.network_graph.order() - 1,
            'assortativity': nx.attribute_assortativity_coefficient(self.network_graph, 'country')
        } 

    #
    # Draw the Cumulative Distribution Function
    #
    def draw_cdf(self, loglog_scale):
        degree_sample = list(dict(self.network_graph.degree).values())
        
        cdf = ECDF(degree_sample)
        x = numpy.unique(degree_sample)
        y = cdf(x)
        
        fig = plt.figure(figsize=(16,9))
        axis = fig.gca()
        
        if loglog_scale:
            # Should be y = 1-y and so a CCDF
            axis.set_title('Cumulative Density Function - LogLog Scale')
            axis.loglog(x, y, color = 'red', marker = 'o', linestyle = '', ms = 8) 
        else:
            axis.set_title('Cumulative Density Function - Linear Scale')
            axis.plot(x, y, color='red', marker='o', linestyle='', ms = 8)
        axis.set_xlabel('Degree', size = 30)
        axis.set_ylabel('CDF', size = 30)

        pylab.show()

    #
    # Draw the Complementary Cumulative Distribution Function
    #
    def draw_ccdf(self):
        degree_sample = list(dict(self.network_graph.degree).values())
        
        cdf = ECDF(degree_sample)
        x = numpy.unique(degree_sample)
        y = cdf(x)
        fig = plt.figure(figsize=(16,9))
        axis = fig.gca()
        
        axis.set_title('Complementary Cumulative Density Function')
        axis.loglog(x, 1-y, color = 'red', marker = 'o', linestyle = '', ms = 8) 
        
        axis.set_xlabel('Degree', size = 30)
        axis.set_ylabel('CCDF', size = 30)

        pylab.show()

    #
    # Draw the Probability Distribution Function 
    #
    def draw_pdf(self, loglog_scale):
        network_degree = list(dict(nx.get_node_attributes(self.network_graph,'affection')).values())

        count_network, bins_network = numpy.histogram(network_degree, numpy.arange( numpy.min(network_degree), numpy.max(network_degree) +2 ))

        pdf_network = count_network/(self.network_graph.order())

        # Get a figure instance to draw on
        fig = plt.figure(figsize=(16,9))
        # Chart could have multiple lines. Get an instance of Axes 
        # https://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes
        axis = fig.gca()

        if loglog_scale == True:
            axis.set_title('Probability Density Function - LogLog Scale')
            axis.loglog(bins_network[:-1], pdf_network,color='orange', marker='o',linestyle='', markersize = 8)
        else:
            axis.set_title('Probability Density Function - Linear Scale')
            axis.plot(bins_network[:-1], pdf_network, color='orange', marker='o', linestyle='', markersize = 8)

        
        axis.set_xlabel('Affection', size = 30)
        axis.set_ylabel('PDF', size = 30)

        pylab.show()

    #
    # Get the hubs
    #
    def get_hubs(self):
        network_degree = list(dict(self.network_graph.degree).values())
        # Define a thresold to identify what is "high degree"
        # I choose to check percentile with p = 0.98
        # I know that 98% of total nodes have got a degree which is lower than quantile_98 variable
        quantile_98 = numpy.percentile(network_degree, 98) 
        # Now get the nodes
        hub_nodes = [k for k,v in dict(self.network_graph.degree).items() if v >= quantile_98]
        # Extend the hub_nodes array list with information about users
        # Getting Array<User>
        hubs = []
        for hubId in hub_nodes:
            hubs.append( self.network_graph.node[hubId].get('info') )
        return hubs

    #
    #
    #
    def compare_with_random_network(self):
        network_degree = list(dict(self.network_graph.degree).values())
        average_degree_network = numpy.mean( network_degree )

        # Remember that <k> = p(N-1) so p = <k>/(N-1)
        p = average_degree_network/float(self.network_graph.order()-1)
        # Generate random graph using 
        random_graph = nx.fast_gnp_random_graph(self.network_graph.order(), p)
        # Analyze random graph
        degree_rand = list(dict(random_graph.degree()).values())
        count_rand, bins_rand= numpy.histogram( degree_rand, bins=numpy.arange( numpy.min(degree_rand), numpy.max(degree_rand)+2 ) )

        pdf_rand = count_rand/(random_graph.order())

        # Analyze real graph
        count_network, bins_network = numpy.histogram(network_degree, numpy.arange( numpy.min(network_degree), numpy.max(network_degree) +2 ))
        pdf_network = count_network/(self.network_graph.order())

        # Plot both graphs
        fig = plt.figure(figsize=(16,9))
        axis = fig.gca()
        axis.loglog(bins_rand[:-1], pdf_rand, color='blue', marker='o', linestyle='None', ms = 9)
        axis.loglog(bins_network[:-1], pdf_network, color='orange', marker='o', linestyle='None', ms = 7)
        axis.set_xlabel('Degree',size=30)
        axis.set_ylabel('PDF',size=30)

        pylab.show()

    #
    # Compute nodes' centrality (betweenness)
    #
    def get_nodes_centrality(self, centrality_type):
        return {
            'betweenness': nx.betweenness_centrality(self.network_graph),
            'eigenvector': nx.eigenvector_centrality(self.network_graph),
            'closeness': nx.closeness_centrality(self.network_graph),
            'degree': nx.degree_centrality(self.network_graph)
        }[centrality_type]

    #
    # Find components
    # Only for directed graphs
    # 
    def get_components(self):
        return nx.attracting_components(self.network_graph)

    #
    # Return the graph instance
    # 
    def save_network_graph(self): 
        try:
            nx.write_gexf(self.network_graph, "500px-affection.gexf")
        except OSError as err:
            print("OS error: {0}".format(err))
        except ValueError:
            print("Could not convert data.")
        except:
            print('Cannot write file')

    def save_network_with_country(self):
        graph_to_save = self.network_graph.copy()
        for nodeId in graph_to_save.nodes():
            if graph_to_save.node[nodeId].get('info')['country']:
                graph_to_save.node[nodeId]['country'] = graph_to_save.node[nodeId].get('info')['country']
            else:
                graph_to_save.node[nodeId]['country'] = 'N.D.'
            del graph_to_save.node[nodeId]['info']
        try:
            nx.write_gexf(graph_to_save, "500pxcountry.gexf")
        except:
            print('Cannot write file')

    #
    # Prints out the top n nodes with highest <centrality_type>
    #   
    def get_top_nodes_centrality(self, nodes, centrality_type, scraper):
        # Know the most important nodes. Returns [{<id>:<centrality>},{<id>:<centrality>}]
        nodes_centrality = self.get_nodes_centrality(centrality_type)
        if nodes_centrality == None:
            print('Centrality type {} not allowed' . format(centrality_type))
            return
        #print("Nodes centrality {}" . format(nodes_centrality))
        # Ascending order
        sorted_nodes_centrality = sorted(nodes_centrality.items(), key=operator.itemgetter(1))
        # Sort revers, desc order
        sorted_nodes_centrality.reverse()
        # This counter is needed because for some users API might not return proper user_info so I need to get the following one
        user_listed = 0
        for user in sorted_nodes_centrality:
            if user_listed is nodes:
                return
            user_info = scraper.getUserById( user[0] ) # get just the id
            if user_info:
                user_listed = user_listed + 1
                print('#{} is {} ({}) with {} betweenness centrality value and {} of affection' . format(user_listed, user_info.get('fullname'), user[0], user[1], user_info.get('affection')))