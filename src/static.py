import os 
from src.dirs import SRC_DIR

def config_display(config):
    print('Current Configuration: \n')
    print('\t{')
    for k,v in config.items():
        print('\t\t"',k,'" : "',v,'"')
    print('\t}\n')

def ascii_art():
    with open(os.path.join(SRC_DIR,'ascii_art.txt')) as f:
        print(f.read())

def config_exception(e): 
    print('\nError Reading in config.\nPlease supply a valid `config.json` \nException: %s\n'%str(e))

def create_exception(message,e):
    print('\nSnapshot with message %s failed to build!\nException: %s\n'%(str(message),str(e)))

def retrieve_exception(which,e):
    print('\nSnapshot %s not available!\nException: %s\n'%(str(which),str(e)))

def purged():
    print('\n* Snapshots purged...\n')

def build_snapshot(date):
    print('\n* Building Snapshot: `%s`\n'%date)

def snapshot_built(date):
    print('\n* Created Snapshot: `%s`\n'%date)

def snapshot_retrieved(date):
    print('\n* Snapshot `%s` retrieved!\n'%date)

def invalid_arguments():
    print('> Invalid commandline argument found!\nTry using "python3 snaps/main.py --help" for a list of commands\n')