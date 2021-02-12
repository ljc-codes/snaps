import sys
import subprocess
from src.objects import Controller
from src import dirs
from src import static


if __name__ == '__main__':

    if '-v' in sys.argv:
        sys.argv.remove('-v')
        verbose = True
    else:
        verbose = False

    controller = Controller(data_dir=dirs.DATA_DIR,verbose=verbose)
    

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        print('Welcome to snaps gui. Here\'s a list of what you can do:')
        print('\t\v(1) take a snapshot (make sure you configure the `config.json`)')
        print('\t\v(2) list all snapshots currently stored')
        print('\t\v(3) retrieve a particular snapshot')
        print('\t\v(4) purge all snapshots\n')
        valid_selection = False
        while not valid_selection:

            user_selection = input('Please select the number corresponding to your desired action: ').replace('(','').replace(')','')
            
            if user_selection == '1':
                command = 'snap'
                message = input('Please include a message for this snapshot: ')
                valid_selection = True
            elif user_selection == '2':
                command = 'list'
                valid_selection = True
            elif user_selection == '3':
                command = 'retrieve'
                valid_selection = True
            elif user_selection == '4':
                command = 'purge'
                valid_selection = True
            else:
                print('Invalid selection!')
        print('\n')

    if command == 'snap':
        # selects message if provided in commandline
        if len(sys.argv) > 2:
            message = sys.argv[3] if sys.argv[2] == '-m' else ''
        elif len(sys.argv) == 2:
            message = ''
        controller.create_snapshot(message)
    elif command == 'retrieve':
        # selects message if provided in commandline
        if len(sys.argv) > 2:
            which = sys.argv[3]
        else:
            controller.list_snapshots()
            which = input('Select the number corresponding to your desired snapshot: ')
        
        controller.retrieve_snapshot(which)
    elif command == 'list':
        controller.list_snapshots()
    elif command == 'purge':
        should_purge = input('Are you sre you want to purge all snapshots?\nThis action is irreversible. (Y/N): ').lower()
        if should_purge == 'y':
            controller.purge_snapshots()
        else:
            print('* No Snapshots purged')
    else: 
        static.invalid_arguments()
        quit()