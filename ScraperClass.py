import requests 
from bs4 import BeautifulSoup

class Scraper(object):

    loginPage = 'https://api.500px.com/v1/session'
    discoverPage = 'https://500px.com/discover'
    siteSession = requests.session()

    parsedDiscoverPage = ''

    def __init__(self, loginPayload):
        self.loginPayload = loginPayload

    def doLogin(self):
        try:
            print('-> Attempting login...')
            response_login_request = self.siteSession.post(
                self.loginPage,
                data=self.loginPayload,
                allow_redirects=False
            )
            # Print the cookies just got
            print('-> Cookies got {}'.format(self.siteSession.cookies))

            # Prepare another request to get the homepage and check if we've logged in correctly
            print('-> Retrieving /discover page... ')

            cookieSetup = False

            responseObjHomeURL = self.siteSession.get(self.discoverPage)
            discoverPage = BeautifulSoup(responseObjHomeURL.text.replace('\n', ''), 'lxml')

            loggedTopNavElm = discoverPage.findAll('li', {'class': 'px_topnav__profile'})
            if len(loggedTopNavElm) > 0:
                cookieSetup = True
                self.parsedDiscoverPage = discoverPage
            print('-> Login status --> {}'.format(cookieSetup))

        except requests.exceptions.RequestException as e:
            print(e)

    def discoverImagesTag(self):
        div_immagini = self.parsedDiscoverPage.findAll('div', {'class': 'photo_thumbnail'})

        for div in div_immagini:
            print(str(div.get_text()))