import ScraperClass
import AnalyticsClass

loginPayload = {
    'session[email]': 'email',
    'session[password]': 'password',
    'authenticity_token': 'VYYzqfBu6pi+0Qx+QLEPTtG1zOadug9FwIbJ09AM5dpciok6INz9KcFmKuTO1jvarTi1aypmWRmp8xqmoPGxJg=='
}

graph_reference = {}

scraper = ScraperClass.Scraper(loginPayload, 'Andrea Paciolla')
# All the code should be executed inside this method
if scraper.doLogin() == True:
    print('-> Login status --> [OK]')
    
    users = scraper.getUsers(50)
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

else:
    print('-> Login status --> [NOK]. Program execution is stopping...')