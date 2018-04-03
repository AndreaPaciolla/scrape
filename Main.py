import ScraperClass

loginPayload = {
    'session[email]': 'andreapaciolla@gmail.com',
    'session[password]': '<password>',
    'authenticity_token': 'VYYzqfBu6pi+0Qx+QLEPTtG1zOadug9FwIbJ09AM5dpciok6INz9KcFmKuTO1jvarTi1aypmWRmp8xqmoPGxJg=='
}

scraper = ScraperClass.Scraper(loginPayload, 'Andrea Paciolla')
if scraper.doLogin() == True:
    print('-> Login status --> [OK]')
    images = scraper.getImages()
    #print('Image are {}'. format(images))
    #users = scraper.getUsers(False)
    #if users == False:
    #    print("Error while retrieving users")
    #else:
    #    print("Total users in 500px: {} \n".format(users.get('total_users')))
    #    print("Total users retrieved: {} \n".format(len(users.get('users'))))
    #
    #    for user in users.get('users'):
    #        print('User {} with {} affection param'.format(user.get('username'), user.get('affection')))
    
    ###################################################
    #user = scraper.getUserById(777395)
    #if user == False:
    #    print('Error retrieving single user..')
    #else:
    #    print('User retrieved {}'.format(user.get('fullname')))
    ###################################################
    followers = scraper.getUserFollowersByUserId(777395)
    if followers == False:
        print('Error retrieving single user followers')
    else:
        for follower in followers:
            print( 'id {} name {}' . format(follower.get('id'), follower.get('fullname')) )
else:
    print('-> Login status --> [NOK]')