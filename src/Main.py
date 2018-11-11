import ScraperClass
import AnalyticsClass
import operator
from itertools import islice

loginPayload = {
    'session[email]': '<your_email>',
    'session[password]': '<your_password>',
    'authenticity_token': '<your_auth_token>'
}

getFromGexfFile = False

graph_reference = {}

scraper = ScraperClass.Scraper(loginPayload, 'Andrea Paciolla')
# All the code should be executed inside this method
if scraper.doLogin() == True:
    print('-> Login status --> [OK]')
    
    if getFromGexfFile:
        graph_reference = AnalyticsClass.Analytics({}, getFromGexfFile)
    else:
        users = scraper.getUsers(150)
        if users == False:
            print("Error while retrieving users")
        
        # Create the graph
        graph_reference = AnalyticsClass.Analytics(users)
        
        # Create all the connections
        for user in users:
            followers = scraper.getUserFollowersByUserId( user.get('id') )
            if followers == False:
                print('Error retrieving followers for user {}' . format(user.get('fullname')))
            else:
                for follower in followers:
                    print( 'id {} name {}' . format(follower.get('id'), follower.get('fullname')) )
                    if graph_reference.add_edges(user, follower) == False:
                        print( 'Error occured while adding edge' )
        
        # let's save it for gephy
        graph_reference.save_network_graph()

    # Draw the network
    #graph_reference.draw_network()
    
    #graph_reference.save_network_with_country()

    graph_reference.draw_pdf(False)
    graph_reference.draw_pdf(True)

    graph_reference.draw_cdf(False)
    #graph_reference.draw_cdf(True)

    graph_reference.draw_ccdf()

    # Plot an erdos-renyi network against a real-network
    graph_reference.compare_with_random_network()

    # Get info about the network
    print('Network edges {} with {} nodes.' . format(graph_reference.get_total_edges(), graph_reference.get_total_nodes()))
    print('Network info {}' . format(graph_reference.get_stats()))

    # Know the hubs
    hubs = graph_reference.get_hubs()
    for user in hubs:
        print('Hub {} ({})' . format(user.get('fullname'), user.get('id')))

    # Compute centralities
    print('--- Betweenness centrality')
    #graph_reference.get_top_nodes_centrality(3, 'betweenness', scraper)

    #print('--- Closeness centrality')
    #graph_reference.get_top_nodes_centrality(3, 'closeness', scraper)

    #print('--- Eigenvector centrality')
    #graph_reference.get_top_nodes_centrality(3, 'eigenvector', scraper)

    print('--- Degree centrality')
    #graph_reference.get_top_nodes_centrality(3, 'degree', scraper)

    # Know more about components - only for directed graphs
    #components = graph_reference.get_components()
    #print("{}" . format(components))

else:
    print('-> Login status --> [NOK]. Program execution is stopping...')