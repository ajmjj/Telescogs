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
    print('\nDisplaying results')
    print('========================================')
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

