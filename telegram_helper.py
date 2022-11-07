from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos



def get_chat_from_id(chat_id, chats):
    return [chat for chat in chats if chat_id == chat['id']][0]

def select_chat(chats):
    chat_input = input('Type the name or the Id: ')

    if chat_input[0] == '-' and chat_input[1:].isdigit():
        print(f'\nInput type: Chat Id')
        chat_input = int(chat_input) # make chat_input an integer

        if chat_input in [chat['id'] for chat in chats]:
            print(f'Entered chat Id: {chat_input}')
            print(f'Chat found: {get_chat_from_id(chat_input, chats).get("name")}')
            print()
            return chat_input
        else: 
            print('\nInvalid chat Id, try again')
            select_chat(chats)
    else: 
        print(f'Input type: Chat name')
        try:
            selected_chat_id = int([chat.get('id') for chat in chats if chat_input.lower().strip() == chat['name'].lower().strip()][0])
            print(f'Chat found: {get_chat_from_id(selected_chat_id, chats).get("name")}')
            print()
            return selected_chat_id
        except IndexError: # index error because no chats in list -> if chat name exists, list should have one element only # todo -> add verification for one item in list
            print('\nInvalid chat name, try again')
            select_chat(chats)
        
async def greet(client):
    me = await client.get_me()
    print(f'\nLogged-in to Telegram as: {me.first_name} {me.last_name} ({me.username})')


# async def get_shared_releases(client):
#     chats = []
#     chat_image_messages = []
#     # Limits the number of messages to search for
#     message_limit = None

#     async for dialog in client.iter_dialogs():
#         if str(dialog.id)[0] == '-':
#             chats.append(
#                 {
#                     'id': dialog.id,
#                     'name': dialog.name
#                 }
#             )
#             print(f'{dialog.name} has ID {dialog.id}')
        
#     # print()
#     print('\nWhich group do you want to search?')
#     chat_id = select_chat(chats)
#     print()


#     async for message in client.iter_messages(chat_id, limit=message_limit, filter=InputMessagesFilterPhotos): # consider using get_messages() instead
#         if message.id % 100 == 0:
#             print(f'Processing messages with photos, {message.id} remaining')

#         chat_image_messages.append(
#             {
#                 'id': message.id,
#                 'photo': message.photo,
#                 'text': message.text,
#                 'message': message.message 
#             }
#         )

#     print(f'\nFound {len(chat_image_messages)} shared releases in {get_chat_from_id(chat_id, chats).get("name")} chat') 

    
    ## get discogs want list
    # for release in discogs want list:
    #    if catalog number in chat_image_messages:
    #        add release name to list

    # print list of releases in chat and discogs want list
    

