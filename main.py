import discogs_helper as disc
import configparser

# Discogs configs
config = configparser.ConfigParser()
config.read('config.ini')

# consumer_key = config['Discogs']['consumer_key']
# consumer_secret = config['Discogs']['consumer_secret']
# access_token = config['Discogs']['access_token']
# access_secret = config['Discogs']['access_secret']

# # Static Oauth endpoints
# authorize_url = 'https://www.discogs.com/oauth/authorize'
# access_token_url = 'https://api.discogs.com/oauth/access_token'

# #Unique user-agent is required for Discogs API
# user_agent = 'Telespogs/1.0'

# client = disc.auth(consumer_key, consumer_secret, user_agent, access_token, access_secret)

# disc.get_wantlist(client)



# Telegram configs
import telegram_helper as tele
from telethon import TelegramClient, sync

from telethon.tl.types import InputMessagesFilterPhotos

telegram_api_id = config['Telegram']['api_id']
telegram_api_hash = config['Telegram']['api_hash']
# telegram_phone  = config['Telegram']['telegram_phone'] # todo -> not needed?
telegram_username = config['Telegram']['username']


# todo -> create function check_tele_username() to check if username is valid
if telegram_username == '': # username is not set
    telegram_username = input('Enter your Telegram username : @')
    telegram_username = '@' + telegram_username
    config['Telegram']['username'] = telegram_username

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        

client = TelegramClient(telegram_username, telegram_api_id, telegram_api_hash)
client.start()
print('Telegram Client Created') # log


async def main():
    chats = []
    chat_image_messages = []
    # Limits the number of messages to search for
    message_limit = None
    # todo --> greet()
    await tele.greet(client)

    print('\nYour chats:')
    print('----------------------------------------')
    async for dialog in client.iter_dialogs():
        if str(dialog.id)[0] == '-':
            chats.append(
                {
                    'id': dialog.id,
                    'name': dialog.name
                }
            )
            print(f'"{dialog.name}" has ID {dialog.id}')
        
    print('\nWhich group do you want to search?')
    chat_id = tele.select_chat(chats)



    async for message in client.iter_messages(chat_id, limit=message_limit, filter=InputMessagesFilterPhotos): # consider using get_messages() instead
        if message.id % 100 == 0:
            print(f'Processing messages with photos, {message.id} remaining')

        chat_image_messages.append(
            {
                'id': message.id,
                'photo': message.photo,
                'text': message.text,
                'message': message.message 
            }
        )

    print(f'\nFound {len(chat_image_messages)} shared releases in {tele.get_chat_from_id(chat_id,chats).get("name")} chat') 

    
    

with client:
    client.loop.run_until_complete(main())
    
# async def main():
#     await tele.greet(client)
#     await tele.get_shared_releases(client)

# with client:
#     client.loop.run_until_complete(main())







    ## get discogs want list
    # for release in discogs want list:
    #    if catalog number in chat_image_messages:
    #        add release name to list

    # print list of releases in chat and discogs want list