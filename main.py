import discogs_helper as disc
import configparser

# Discogs configs
config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['Discogs']['consumer_key']
consumer_secret = config['Discogs']['consumer_secret']
access_token = config['Discogs']['access_token']
access_secret = config['Discogs']['access_secret']

# Static Oauth endpoints
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'

#Unique user-agent is required for Discogs API
user_agent = 'Telespogs/1.0'

client = disc.auth(consumer_key, consumer_secret, user_agent, access_token, access_secret)

disc.get_wantlist(client)