import ScraperClass
import AnalyticsClass
import operator
from itertools import islice

loginPayload = {
    'session[email]': '<user_email>',
    'session[password]': '<user_password>',
    'authenticity_token': '<user_token>'
}

graph_reference = {}

scraper = ScraperClass.Scraper(loginPayload, 'Andrea Paciolla')
# All the code should be executed inside this method
if scraper.doLogin() == True:
    print('-> Login status --> [OK]')
    
    users = scraper.getUsers(5)
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
    
    # Draw the network
    graph_reference.draw_network()
    graph_reference.draw_pdf(False)
    #graph_reference.draw_cdf(True)

    # Get info about the network
    print('Network edges {} with {} nodes.' . format(graph_reference.get_total_edges(), graph_reference.get_total_nodes()))
    print('Network info {}' . format(graph_reference.get_stats()))

    # Know the hubs
    hubs = graph_reference.get_hubs()
    for user in hubs:
        print('Hub {}' . format(user.get('fullname')))

    # Know the most important nodes. Returns [{<id>:<centrality>},{<id>:<centrality>}]
    nodes_centrality = graph_reference.get_nodes_centrality()
    #print("Nodes centrality {}" . format(nodes_centrality))
    # Ascending order
    sorted_nodes_centrality = sorted(nodes_centrality.items(), key=operator.itemgetter(1))
    # Sort revers, desc order
    sorted_nodes_centrality.reverse()
    # Know something more about nodes
    index = 1
    for user in islice(sorted_nodes_centrality, 3):
        user_info = scraper.getUserById( user[0] ) # get just the id
        print('#{} is {} with {} betweenness centrality value and {} of affection' . format(index, user_info.get('fullname'), user[1], user_info.get('affection')))
        index = index + 1

else:
    print('-> Login status --> [NOK]. Program execution is stopping...')