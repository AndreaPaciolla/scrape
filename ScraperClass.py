import requests 
import json
import math
import UtilityClass
from bs4 import BeautifulSoup

class Scraper(object):

    pages = {
        'login': 'https://api.500px.com/v1/session',
        'loggedHome': 'https://500px.com/discover',
        'profile': 'https://500px.com/andreapaciolla',
        'users': 'https://api.500px.com/v1/users/top',
        'followers': 'https://api.500px.com/v1/users/*placeholder*/followers',
        'user': 'https://api.500px.com/v1/photos?feature=user',
        'discoveryPics': 'https://webapi.500px.com/discovery/foryou?include_personalized_content=true'
    }

    siteSession = requests.session()

    def __init__(self, loginPayload, loginSuccessAttr):
        self.loginPayload = loginPayload
        self.loginSuccessAttr = loginSuccessAttr

    def __getitem__(self, item):
        return getattr(self, item)
        
    def doLogin(self):
        try:
            print('-> Attempting login...')
            response_login_request = self.siteSession.post(
                self['pages']['login'],
                data=self.loginPayload,
                allow_redirects=False
            )
            # Print the cookies just got
            print('-> Cookies got {}'.format(self.siteSession.cookies))

            # Prepare another request to get the homepage and check if we've logged in correctly
            print('-> Retrieving /profile page... ')

            responseObjHomeURL = self.siteSession.get(self['pages']['profile'])

            if responseObjHomeURL.text.find(self.loginSuccessAttr) > 0:
                return True
            return False

        except requests.exceptions.RequestException as e:
            print(e)

    def getImages(self):
        
        self.siteSession.headers.update({'AUTHORIZATION': 'PxToken pTSWqXdaXlQDGxfuoXT7EFkC+yPh0b4Jc+ZRopAvUtCsOCw6p+hJ5XysMXQvE8+EJY+CrlYN6FUak4LX4NIGLA=='})
        self.siteSession.headers.update({'Origin': 'https://500px.com'})
        self.siteSession.headers.update({'Host': 'webapi.500px.com'})
        self.siteSession.headers.update({'Cookie': 'locale=en; localized_ui_banner_1062343=1; _srt=BAhJIhUxMDYyMzQzOlduUlR3dz09BjoGRVQ%3D--0c90bbf0cc8a161864918fa99471404b31bbf726; remember_user_token=BAhbB1sGaQPHNRBJIhlRUHlzek5oVTZlTHFEc1FoellZRAY6BkVU--8e950c0dd2bb2db46d31761013566fb1f97338d1; username=andreapaciolla; user_first_name=Andrea; _hpx1=BAh7DUkiD3Nlc3Npb25faWQGOgZFVEkiJTRmZTgzYzE1MDZjMDVkZmY2Y2E1MTI0NjJhYjAxZjgxBjsAVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMUNReTZrOUN5RjdGL3R5YWFqbWMwbEh5TmVZMjMzRlpjYVhYVGRYRDlWUHc9BjsARkkiCWhvc3QGOwBGIg41MDBweC5jb21JIhl1c2Vfb25ib2FyZGluZ19tb2RhbAY7AEZUSSIZd2FyZGVuLnVzZXIudXNlci5rZXkGOwBUWwdbBmkDxzUQSSIZUVB5c3pOaFU2ZUxxRHNRaHpZWUQGOwBUSSIJX3NydAY7AEZJIhUxMDYyMzQzOlduUlR3dz09BjsAVEkiEXByZXZpb3VzX3VybAY7AEZJIg4vZGlzY292ZXIGOwBU--4f306abdd473e8873dc0bfe57a6443b976aacd6d'})

        images = self.siteSession.get(self['pages']['discoveryPics'])
        if images.status_code == 200: 
            return images.json()
        return False

    def getUsers(self, usersLimit): 
        
        # Check params
        if not usersLimit:
            print('UsersLimit param must be specified')
            return False

        # Initial setup
        apiURL = self['pages']['users']
        
        self.siteSession.headers.update({'Origin': 'https://500px.com'})
        self.siteSession.headers.update({'Host': 'api.500px.com'})
        self.siteSession.headers.update({'X-CSRF-Token': '6DIUvg9qRCSGVl29hv8xvqK3Rn/vgk+rUoSXJKvJvXThPq4t39hTlfnheycImAUq3jo/8lheGfc78URR2zTpiA=='})
        self.siteSession.headers.update({'Cookie': 'device_uuid=1ecb2213-61aa-4521-aa8a-5e4bdeb6f2e4; locale=en; localized_ui_banner_1062343=1; _srt=BAhJIhUxMDYyMzQzOlduUlR3dz09BjoGRVQ%3D--0c90bbf0cc8a161864918fa99471404b31bbf726; remember_user_token=BAhbB1sGaQPHNRBJIhlRUHlzek5oVTZlTHFEc1FoellZRAY6BkVU--8e950c0dd2bb2db46d31761013566fb1f97338d1; username=andreapaciolla; user_first_name=Andrea; _hpx1=BAh7DUkiD3Nlc3Npb25faWQGOgZFVEkiJTRmZTgzYzE1MDZjMDVkZmY2Y2E1MTI0NjJhYjAxZjgxBjsAVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMUNReTZrOUN5RjdGL3R5YWFqbWMwbEh5TmVZMjMzRlpjYVhYVGRYRDlWUHc9BjsARkkiCWhvc3QGOwBGIhJhcGkuNTAwcHguY29tSSIZdXNlX29uYm9hcmRpbmdfbW9kYWwGOwBGVEkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsHWwZpA8c1EEkiGVFQeXN6TmhVNmVMcURzUWh6WVlEBjsAVEkiCV9zcnQGOwBGSSIVMTA2MjM0MzpXblJUd3c9PQY7AFRJIhFwcmV2aW91c191cmwGOwBGSSIuL3NlYXJjaD9xPXVzZXImdHlwZT1wZW9wbGUmc29ydD1yZWxldmFuY2UGOwBU--50ff865be253848a8151f179076ec09c6d25dbfa'})
        
        # Start with a discovery api in order to know how much users are present
        # and then start with all the requests...
        userDiscovery = self.siteSession.get(apiURL + '?page=1&rpp=10')
        print("Invoking discovery... {}".format(apiURL + '?page=1&rpp=10'))
        if userDiscovery.status_code == 200:
            # Retrieve all the users
            page = 1
            perPage = 50
            returning = []
            pages = math.ceil( int(userDiscovery.json().get('total_users')) / perPage )

            print("Getting all the users in {} pages...".format(pages))
            while pages >= page and usersLimit >= page*perPage:
                apiURL = self['pages']['users'] + '?page=' + str(page) + '&rpp=' + str(perPage)
                print("Invoking... {}".format(apiURL))
                users = self.siteSession.get(apiURL)
                if users.status_code == 200:
                    returning.extend(users.json().get('users'))
                    page += 1
                else:
                    print("Error got during fetching users.")
                    return False
            return returning
        else:
            print('Error during users discovery')
            return False

    def getUserById(self, id): 
        apiURL = self['pages']['user'] + '&stream=photos&user_id=' + str(id)

        self.siteSession.headers.update({'Origin': 'https://500px.com'})
        self.siteSession.headers.update({'Host': 'api.500px.com'})
        self.siteSession.headers.update({'X-CSRF-Token': 'lM0Dx9Oq1e6r+smsCTFJbz+aqHNfrvDi2iMmxUB8AcGdwblUAxjCX9RN7zaHVn37QxfR/uhypr6zVvWwMIFVPQ=='})
        self.siteSession.headers.update({'Cookie': 'device_uuid=1ecb2213-61aa-4521-aa8a-5e4bdeb6f2e4; locale=en; localized_ui_banner_1062343=1; _srt=BAhJIhUxMDYyMzQzOlduUlR3dz09BjoGRVQ%3D--0c90bbf0cc8a161864918fa99471404b31bbf726; remember_user_token=BAhbB1sGaQPHNRBJIhlRUHlzek5oVTZlTHFEc1FoellZRAY6BkVU--8e950c0dd2bb2db46d31761013566fb1f97338d1; username=andreapaciolla; user_first_name=Andrea; _hpx1=BAh7DUkiD3Nlc3Npb25faWQGOgZFVEkiJTRmZTgzYzE1MDZjMDVkZmY2Y2E1MTI0NjJhYjAxZjgxBjsAVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMUNReTZrOUN5RjdGL3R5YWFqbWMwbEh5TmVZMjMzRlpjYVhYVGRYRDlWUHc9BjsARkkiCWhvc3QGOwBGIg41MDBweC5jb21JIhl1c2Vfb25ib2FyZGluZ19tb2RhbAY7AEZUSSIZd2FyZGVuLnVzZXIudXNlci5rZXkGOwBUWwdbBmkDxzUQSSIZUVB5c3pOaFU2ZUxxRHNRaHpZWUQGOwBUSSIJX3NydAY7AEZJIhUxMDYyMzQzOlduUlR3dz09BjsAVEkiEXByZXZpb3VzX3VybAY7AEZJIhAvc2VhbmFyY2hlcgY7AFQ%3D--41aca84ba0f1bcad5457647b5b72530efd16e88f'})
        
        user = self.siteSession.get(apiURL)
        if user.status_code == 200:
            return user.json().get('photos')[0].get('user')
        else:
            print('ScraperClass :: getUser method :: {}'.format( user ))    
            return False

    def getUserFollowersByUserId(self, userId, followersLimit=100): 
        page = 1
        perPage = 50
        apiURL = self['pages']['followers']
        apiURL = apiURL.replace('*placeholder*', '777395')

        returning = []

        self.siteSession.headers.update({'Origin': 'https://500px.com'})
        self.siteSession.headers.update({'Host': 'api.500px.com'})
        self.siteSession.headers.update({'X-CSRF-Token': 'lM0Dx9Oq1e6r+smsCTFJbz+aqHNfrvDi2iMmxUB8AcGdwblUAxjCX9RN7zaHVn37QxfR/uhypr6zVvWwMIFVPQ=='})
        self.siteSession.headers.update({'Cookie': 'device_uuid=1ecb2213-61aa-4521-aa8a-5e4bdeb6f2e4; locale=en; localized_ui_banner_1062343=1; _srt=BAhJIhUxMDYyMzQzOlduUlR3dz09BjoGRVQ%3D--0c90bbf0cc8a161864918fa99471404b31bbf726; remember_user_token=BAhbB1sGaQPHNRBJIhlRUHlzek5oVTZlTHFEc1FoellZRAY6BkVU--8e950c0dd2bb2db46d31761013566fb1f97338d1; username=andreapaciolla; user_first_name=Andrea; _hpx1=BAh7DUkiD3Nlc3Npb25faWQGOgZFVEkiJTRmZTgzYzE1MDZjMDVkZmY2Y2E1MTI0NjJhYjAxZjgxBjsAVEkiGHN1cGVyX3NlY3JldF9waXgzbHMGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMUNReTZrOUN5RjdGL3R5YWFqbWMwbEh5TmVZMjMzRlpjYVhYVGRYRDlWUHc9BjsARkkiCWhvc3QGOwBGIhJhcGkuNTAwcHguY29tSSIZdXNlX29uYm9hcmRpbmdfbW9kYWwGOwBGVEkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsHWwZpA8c1EEkiGVFQeXN6TmhVNmVMcURzUWh6WVlEBjsAVEkiCV9zcnQGOwBGSSIVMTA2MjM0MzpXblJUd3c9PQY7AFRJIhFwcmV2aW91c191cmwGOwBGSSIQL3NlYW5hcmNoZXIGOwBU--77e04259894e894ac7166b8dd435737729f6c8f9'})
        self.siteSession.headers.update({'Referer': 'https://500px.com/seanarcher'})

        discoveryCall = self.siteSession.get(apiURL + '?fullformat=1&page=1&rpp='+str(perPage))

        if discoveryCall.status_code == 200:
            totalPages = math.ceil( int(discoveryCall.json().get('followers_count')) / perPage )
            print( 'There are {} pages of followers in total.' . format(totalPages))

            # Make sure to get only the followers we would like to have (i.e. consider the followersLimit)
            while totalPages >= page and followersLimit >= perPage*page:
                apiURL = (self['pages']['followers']).replace('*placeholder*', str(userId) ) + '?page=' + str(page) + '&rpp=' + str(perPage) 
                print( 'invoking... {}' . format( apiURL ) )
                followers = self.siteSession.get(apiURL)
                if followers.status_code == 200:
                    returning.extend(followers.json().get('followers'))
                else:
                    print( 'Error retrieving followers... {}' . format(followers) )
                    return False
                page += 1
            return returning
        else:
            print( 'error retrieving user followers {}' . format(discoveryCall) )
            return False
        


        