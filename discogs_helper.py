import json
import oauth2 as oauth
import configparser
import discogs_client
import webbrowser

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['Discogs']['consumer_key']
consumer_secret = config['Discogs']['consumer_secret']
access_token = config['Discogs']['access_token']
access_secret = config['Discogs']['access_secret']

# Static Oauth endpoints
# request_token_url = 'https://api.discogs.com/oauth/request_token'
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'

# #Unique user-agent is required for Discogs API
# user_agent = 'Telespogs/1.0'

def auth(consumer_key, consumer_secret, user_agent, access_token, access_secret ):
    if access_token == '' or access_secret == '':
        print('\nNo access token or secret found, authorizing...')
    # Get auth Url
        client = discogs_client.Client(user_agent,consumer_key,consumer_secret)
        req_token,req_secret,auth_url = client.get_authorize_url()

        # Open authorization URL in browser
        webbrowser.open(auth_url)

        # Get verifier pin from user
        oauth_verifier = input('\nEnter the code shown in the browser: ')

        # Get access token
        access_token,access_secret = client.get_access_token(oauth_verifier)

        # Save access token and secret
        config['Discogs']['access_token'] = access_token
        config['Discogs']['access_secret'] = access_secret

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        greet_user(client)

        return client

    else:
        print('Access token and secret found')
        # Create Client Object
        client = discogs_client.Client(user_agent,consumer_key,consumer_secret,access_token,access_secret)
        
        greet_user(client)
        return client

def greet_user(client):
    me = client.identity()
    print('Logged in as: ' + me.username)

def get_wantlist(client):
    print('\nGetting wantlist from discogs...')
    wantlist_res = client.identity().wantlist
    wantlist = []
    print('Found ' + str(len(wantlist_res)) + ' items in your wantlist')
    for wantlistItem in wantlist_res:
        filtered_release = {
            'id': wantlistItem.release.id,
            'title': wantlistItem.release.title,
            'artist': wantlistItem.release.artists[0].name,
            'label': wantlistItem.release.labels[0].name,
            'catno': wantlistItem.release.data['labels'][0]['catno'],
            'year': wantlistItem.release.data['year']
        }
        wantlist.append(filtered_release)
    return(wantlist)

