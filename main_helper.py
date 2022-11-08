from datetime import datetime
from alive_progress import alive_bar




# todo -> add variable output path
def save_results(chat_name, available_releases):
    date_time = datetime.now().strftime("%Y-%m-%d %H-%M")
    print('\nSaving results to .txt file...')
    with open(f'{chat_name} - {date_time}.txt', 'w') as f:
        counter = 0
        with alive_bar(len(available_releases)) as bar:
            for release in available_releases:
                counter += 1
                f.write(f'\n{counter}. {release["release"]["title"]} - {release["release"]["artist"]} / {release["release"]["label"]} - {release["release"]["catno"]} ({release["release"]["year"]})' )
                bar()


def view_results(chat_name, available_releases):
    print('\nDisplaying results...')

    print('\n========================================')
    print(f'        {len(available_releases)} releases in {chat_name}')
    print('========================================')
    with alive_bar(len(available_releases)) as bar:
        for release in available_releases:
            print(f'{release["release"]["title"]} - {release["release"]["artist"]} / {release["release"]["label"]} - {release["release"]["catno"]} ({release["release"]["year"]})')
            bar()

def yes_results(chat_name,  available_releases):
    while True:
        method = input('Would you like to save or view the results? (s/v) : ')
        if method.lower().strip() == 's' or method.lower().strip() == 'save':
            save_results(chat_name, available_releases)
            break
        elif method.lower().strip() == 'v' or method.lower().strip() == 'view':
            view_results(chat_name, available_releases)
            break
        else:
            print('\nInvalid input, try again')

def res(chat_name, available_releases):
    while True:
        res = input('Would you like to view or save the results? (y/n) : ')
        if res.lower().strip() == 'y' or res.lower().strip() == 'yes':
            yes_results(chat_name, available_releases)
            break
        elif res.lower().strip() == 'n' or res.lower().strip() == 'no':
            print('Results not saved or viewed')
            break
        else:
            print('\nInvalid input, try again')

def match_count(available_releases, chat_name):
    print(f'\nFound {len(available_releases)} releases from your want list available in {chat_name}')

def show_match(match):
    print(f'Match found: {match["release"]["title"]} - {match["release"]["artist"]}')

def check_matches(wantlist, chat_image_messages):
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
                # Sum of boolean values in match (doesn't include release (release not bool)):
                if sum([value for key, value in match.items() if key != 'release']) >= 4:
                    # Add match to available releases
                    available_releases.append(match)

                    # Print the match found to the console (optional)
                        # todo -> make this an optional feature in the settings
                    show_match(match)
                bar()
    return available_releases