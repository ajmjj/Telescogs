from alive_progress import alive_bar
from datetime import datetime
import os
import main_helper as utils
import discogs_helper as disc
import configparser


# add main to tele helper so that this can be put in main helper
async def new_search(client):
    while True:
        res = input('\nWould you like to search another chat? (y/n) : ')
        if res.lower().strip() == 'y' or res.lower().strip() == 'yes':
            global repeat
            repeat = True
            os.system('cls' if os.name == 'nt' else 'clear')
            await main()
            break
        elif res.lower().strip() == 'n' or res.lower().strip() == 'no':
            print('Thanks for using Telescogs!')
            print('Disconnecting ...')
            await client.disconnect()
            print('Disconnected')
            break

repeat = False

# todo -> in config add option to refine search criteria
  # to be set by apple script with popup
# add dialogue at the beginning
    # If discogs token is not found, prompt user to login
    # If telegram token is not found, prompt user to login
    # what would you like to do? search or change settings?
    # -> update username, etc.
    # -> update default save option
    # -> select if they want each match to be printed to the console (show_match())
    # -> change default download path
    # -> logout of discogs & telegram

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

os.system('cls' if os.name == 'nt' else 'clear')
print('================================================================================')
print('                                Discogs Init')
print('================================================================================')
client = disc.auth(consumer_key, consumer_secret, user_agent, access_token, access_secret)

wantlist = disc.get_wantlist(client)



# Telegram configs
import telegram_helper as tele
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos

telegram_api_id = config['Telegram']['api_id']
telegram_api_hash = config['Telegram']['api_hash']
telegram_username = config['Telegram']['username']

print('================================================================================')
print('                               Telegram Init')
print('================================================================================')
tele.check_username(telegram_username, config)

client = TelegramClient(telegram_username, telegram_api_id, telegram_api_hash)
client.start()
print('Telegram Client Created') # log


async def main():
    chat_image_messages = []
    chats = []
    # Limits the number of messages to search for
    message_limit = None
    if repeat == False:
        await tele.greet(client)

    print('\nYour chats:')
    print('--------------------------------------------------------------------------------')
    
    # Get all user's chats from Telegram
    chats = await utils.get_dialogs(client)

    # Ask user to select a chat
    print('\nWhich group do you want to search?')
    chat_id, chat_name = tele.select_chat(chats)

    # Get all messages from selected chat
    chat_image_messages = await utils.get_chat_messages(client, chat_id, message_limit)

    # Check matches
    print('\nChecking matches...')
    available_releases = utils.check_matches(wantlist, chat_image_messages)    

    # Print number of matches found
    utils.match_count(available_releases, chat_name)

    # Ask user if they want to see/save results
    utils.res(chat_name, available_releases)

    # Ask user if they want to search again, or exit
    await new_search(client)

    
    

    
    

with client:
    client.loop.run_until_complete(main())
