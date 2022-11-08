from alive_progress import alive_bar
from datetime import datetime
import os
import discogs_helper as disc
import configparser

# todo -> in config add option to refine search criteria
  # to be set by apple script with popup
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
print('========================================')
print('             Discogs Init')
print('========================================')
client = disc.auth(consumer_key, consumer_secret, user_agent, access_token, access_secret)

wantlist = disc.get_wantlist(client)



# Telegram configs
import telegram_helper as tele
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos

telegram_api_id = config['Telegram']['api_id']
telegram_api_hash = config['Telegram']['api_hash']
# telegram_phone  = config['Telegram']['telegram_phone'] # todo -> not needed?
telegram_username = config['Telegram']['username']

print('========================================')
print('            Telegram Init')
print('========================================')
# todo -> create function check_tele_username() to check if username is valid
if telegram_username == '': # username is not set
    telegram_username = input('Enter your Telegram username : @')
    telegram_username = '@' + telegram_username
    config['Telegram']['username'] = telegram_username

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        

client = TelegramClient(telegram_username, telegram_api_id, telegram_api_hash)
client.start()
print('\nTelegram Client Created') # log


async def main():
    chat_image_messages = []
    chats = []
    # Limits the number of messages to search for
    message_limit = None

    await tele.greet(client)

    print('\nYour chats:')
    print('----------------------------------------')
    
    with alive_bar() as bar:
        async for dialog in client.iter_dialogs():
            if str(dialog.id)[0] == '-':
                chats.append(
                    {
                        'id': dialog.id,
                        'name': dialog.name
                    }
                )
                print(f'"{dialog.name}" has ID {dialog.id}')
                bar()

    print('\nWhich group do you want to search?')
    # todo -> select chat should return tuple (chat_id, chat_name)
    chat_id = tele.select_chat(chats)

    with alive_bar() as bar:
        async for message in client.iter_messages(chat_id, limit=message_limit, filter=InputMessagesFilterPhotos): # consider using get_messages() instead
            if message.id % 100 == 0:
                print(f'Processing messages, {message.id} remaining')
            chat_image_messages.append(
                {
                    'id': message.id,
                    'photo': message.photo,
                    'text': message.text,
                    'message': message.message 
                }
            )
            bar()
    chat_name = tele.get_chat_from_id(chat_id,chats).get("name")
    print(f'\nFound {len(chat_image_messages)} shared releases in {chat_name} chat') 

    print('Checking matches...')
    available_releases = []
    with alive_bar(len(wantlist)*len(chat_image_messages)) as bar:
        for release in wantlist:
            for message in chat_image_messages:
                # todo -> create function check_match()
                # check if artist, year, catno are 
                # check songs in release
                match = {
                    'release': release,
                    'artist' : False,
                    'label' : False,
                    'title' : False,
                    'catno' : False,
                    'year' : False
                }
                for key in match.keys():
                    if str(release.get(key)) in message['text']:
                        match[key] = True
                # sum of boolean values in match (doesn't include release (release not bool)):
                if sum([value for key, value in match.items() if key != 'release']) >= 4:
                    available_releases.append(match)
                    # todo -> creare function print_match()
                    # print(f'Match found: {available_releases[-1]} === {message["text"]}')
                    print(f'Match found: {match["release"]["title"]} - {match["release"]["artist"]}')
                bar()

    # todo -> create func print_results()
    print(f'\nFound {len(available_releases)} releases from your want list available in {tele.get_chat_from_id(chat_id,chats).get("name")}')
    # todo -> create func save_results()
        # ask user -> would you like to save results?
    # print(available_releases)

    date_time = datetime.now().strftime("%Y%-m-%d %H-%M")
    
    #todo -> create func save_results()
    # todo -> change output location in config
    print('\nSaving results to .txt file...')
    with open(f'{chat_name} - {date_time}.txt', 'w') as f:
        counter = 0
        with alive_bar(len(available_releases)) as bar:
            for release in available_releases:
                counter += 1
                f.write(f'\n{counter}. {release["release"]["title"]} - {release["release"]["artist"]} / {release["release"]["label"]} - {release["release"]["catno"]} ({release["release"]["year"]})' )
                bar()


with client:
    client.loop.run_until_complete(main())






# async def main():
#     await tele.greet(client)
#     await tele.get_shared_releases(client)

# with client:
#     client.loop.run_until_complete(main())








    # print list of releases in chat and discogs want list