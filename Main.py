import ScraperClass

loginPayload = {
    'session[email]': '<email>',
    'session[password]': '<password>',
    'authenticity_token': '<token>'
}

scraper = ScraperClass.Scraper(loginPayload)
scraper.doLogin() 