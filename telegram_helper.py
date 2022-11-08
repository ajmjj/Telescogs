from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
import configparser

def get_chat_from_id(chat_id, chats):
    return [chat for chat in chats if chat_id == chat['id']][0]

def select_chat(chats):
    chat_input = input('Type the name or the Id: ')

    # if chat_input[0] == '-' and chat_input[1:].isdigit():
    if chat_input.isdigit():
        print(f'\nInput type: Chat Id')
        chat_input = int(chat_input) # make chat_input an integer

        if chat_input in [chat['id'] for chat in chats]:
            print(f'Entered chat Id: {chat_input}')
            chat_name = get_chat_from_id(chat_input, chats).get("name")
            print(f'Chat found: {chat_name}')
            print()
            return chat_input, chat_name
        elif chat_input*-1 in [chat['id'] for chat in chats]:
            print("Your entered Id doesn't correspond to a chat, though it corresponds to a channel")
            possible_chat_name = get_chat_from_id(chat_input*-1, chats).get("name")
            print(f"Did you mean to enter the channel: {possible_chat_name}?")
            res = input("Enter 'y' to select the channel, or 'n' to try again: ")
            if res.strip().lower() == 'y' or res.strip().lower() == 'yes':
                corrected_chat_id = chat_input *-1
                chat_name = possible_chat_name
                print(f'Corrected channel Id: {corrected_chat_id}')
                print(f'Channel found: {chat_name}')
                print()
                return corrected_chat_id, chat_name
            elif res.strip().lower() == 'n' or res.strip().lower() == 'no':
                print("Ok, try again")
                select_chat(chats)
        else: 
            print('\nInvalid chat Id, try again')
            select_chat(chats)
    else: 
        print(f'\nInput type: Chat name')
        try:
            selected_chat_id = int([chat.get('id') for chat in chats if chat_input.lower().strip() == chat['name'].lower().strip()][0])
            chat_name = get_chat_from_id(selected_chat_id, chats).get("name")
            print(f'Chat found: {chat_name}')
            print()
            return selected_chat_id, chat_name
        except IndexError: # index error because no chats in list -> if chat name exists, list should have one element only # todo -> add verification for one item in list
            print('\nInvalid chat name, try again')
            select_chat(chats)
        
async def greet(client):
    me = await client.get_me()
    print(f'\nLogged-in to Telegram as: {me.username}')

def check_username(username, config):
    if username == '': # username is not set
        username = input('Enter your Telegram username : @')
        username = '@' + username
        config['Telegram']['username'] = username

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    

