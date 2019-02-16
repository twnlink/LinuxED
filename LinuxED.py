# -*- coding: utf-8 -*-

# written by Creatable

# credits:
# - Tcll5850: https://gitlab.com/Tcll
#   for cleaning up the code, making it more maintainable, and extending it's functionality, as well as fixing issues with older python versions.

import os
import sys
if os.name == 'nt': print('WARNING: it appears you are running the Linux installer on Windows.\n'
                          'If you are unaware of what you\'re doing, it\'s recommended you close this installer.\n'
                          'Otherwise you may continue at your own risk.\n')
# Define the starting variables, these are all their own thing.
username = os.environ['USER']
dirpath = os.path.dirname(os.path.realpath(__file__))
enhanceddir = dirpath + "/EnhancedDiscord"
injdir = 'process.env.injDir = "%s"' % enhanceddir
# this is not my code but it's what I put at the end of index.js
patch = """%s
require(`${process.env.injDir}/injection.js`);
module.exports = require('./core.asar');"""%injdir

# Tcll: should we really be using static versions??
discordstableversion = "0.0.5"
discordcanaryversion = "0.0.65"
discordptbversion = "0.0.10"
discordsnapversion = "0.0.5"
discordflatversion = "0.0.5"

detect_versions = lambda discordpath,idxsubpath: [
    (discordpath+vsn+idxsubpath, vsn) for vsn in (os.listdir(discordpath) if os.path.exists(discordpath) else []) if os.path.isdir(discordpath+vsn) and len(vsn.split('.')) == 3 ]

print('Welcome to the LinuxED installation script.')

# TODO: detect patched clients
if sys.platform == 'darwin':
    baseclients = {
    "STABLE" : detect_versions('/Users/%s/Library/Application Support/discord/'%username, '/modules/discord_desktop_core/index.js'),
    "CANARY" : detect_versions('/Users/%s/Library/Application Support/discordcanary/'%username, '/modules/discord_desktop_core/index.js'),
    "PTB"    : detect_versions('/Users/%s/Library/Application Support/discordptb/'%username, '/modules/discord_desktop_core/index.js'),
    "SNAP"   : detect_versions('/home/%s/snap/discord/82/.config/discord/'%username, '/modules/discord_desktop_core/index.js'),
    "FLATPAK": detect_versions('/home/%s/.var/app/com.discordapp.Discord/config/discord/'%username, '/modules/discord_desktop_core/index.js')
}
else:
    baseclients = {
        "STABLE" : detect_versions('/home/%s/.config/discord/'%username, '/modules/discord_desktop_core/index.js'),
        "CANARY" : detect_versions('/home/%s/.config/discordcanary/'%username, '/modules/discord_desktop_core/index.js'),
        "PTB"    : detect_versions('/home/%s/.config/discordptb/'%username, '/modules/discord_desktop_core/index.js'),
        "SNAP"   : detect_versions('/home/%s/snap/discord/82/.config/discord/'%username, '/modules/discord_desktop_core/index.js'),
        "FLATPAK": detect_versions('/home/%s/.var/app/com.discordapp.Discord/config/discord/'%username, '/modules/discord_desktop_core/index.js')
    }

clients = [ (str(i+1),cpv) for i,cpv in enumerate( (c,p,v) for c in [ "STABLE", "CANARY", "PTB", "SNAP", "FLATPAK" ] if baseclients[c] for p,v in baseclients[c] ) ]
clients.append( (str(len(clients)+1), ("CUSTOM",'', '')) )
getclient = dict(clients).get

def validate_custom_client():
    while True:
        print("\nPlease enter the location of your client's index.js file.")
        jspath = input('> ')
        if os.path.exists(jspath): return 'CUSTOM', jspath, '' # TODO: can we detect the version of a custom client?
        elif not jspath:
            print("\nOperation cancelled...")
            return 'CUSTOM', jspath, ''
        else:
            print("\nError: The specified location was not valid.")
            print("Please enter a valid location or press Enter to cancel.")

def select_client(allow_custom=False):
    if len(clients) > 2 or allow_custom:
        while True:
            print('\nPlease enter the number for the client you wish to patch, or press Enter to exit:')
            result = input('%s\n> '%('\n'.join('%s. %s: %s'%(i,o,v) for i,(o,p,v) in clients)) )
            client, jspath, version = getclient( result, (None,'','') )
            if client=='CUSTOM':
                client, jspath, version = validate_custom_client()
                if not jspath: continue
            if jspath: return client, jspath, version
            if not result:
                print("\nOperation cancelled...")
                #input('Press Enter to Exit...')
                return 'CUSTOM', jspath, ''
            print("\nError: The specified option was not valid.")
    
    elif len(clients) == 1:
        print('\nThe installer could not detect any known Discord clients.')
        print('Do you have Discord installed in a custom location? (y/n)')
        if input("> ").upper() in {"Y","YES"}: return validate_custom_client()
        else:
            print('\nNo Discord client could be found.')
            print('Please install Discord and re-run this installer.')
            #input('Press Enter to Exit...')
            return 'CUSTOM', '', ''
    
    else: return getclient('1')

client, jspath, version = select_client()
if jspath:
    print('\nOperating on client: %s %s\n'%(client,version))
    print('Please type the number for your desired option:')
    
    # room for expansion (other params can be provided here)
    options = [ (str(i+1),o) for i,o in enumerate([
        ('Install ED',),
        ('Uninstall ED',),
        #('Update ED',),
        ('Update LinuxED',),
        ('Select Client',),
        ('Exit',),
    ])]
    getoption = dict(options).get
    
    while True:
        option,*params = getoption( input( '%s\n> '%('\n'.join('%s. %s'%(i,o) for i,(o,*p) in options) ) ), (None,) )
        print()
        
        if option == 'Exit':
            print("Exiting...")
            exit()
            break # shouldn't get here, but just in case.
        
        
        elif option == 'Update LinuxED':
            print("Updating LinuxED installation...")
            # check if .git is there, if it is then I know that this was cloned from the git repo and am free to git pull
            if os.path.exists("%s/.git"%dirpath):
                os.system("git pull --no-edit") # git pull latest version. works if script hasn't been modified.
            else:
                print("Error: Can't find LinuxED folder, did you clone the LinuxED repository?\n")
    
    
        elif option == 'Uninstall ED':
            print('Uninstalling EnhancedDiscord...')
            if os.path.exists("%s.backup"%jspath):
                os.remove(jspath)
                os.rename("%s.backup"%jspath, jspath)
                print("Successfully uninstalled EnhancedDiscord!")
            else:
                print("Error: Couldn't find index.js backup, did you use the installer to install ED?\n")
    
    
        elif option == 'Install ED':
            # TODO: version check
            if not os.path.exists("%s/EnhancedDiscord"%dirpath):
                print("Cloning ED...")
                os.system("git clone https://github.com/joe27g/EnhancedDiscord")
            
            backuppath = "%s.backup"%jspath
            if not os.path.exists(backuppath):
                print("Creating index.js.backup...")
                with open(jspath,'r') as original:
                    with open(backuppath,'w') as backup: backup.write(original.read())
    
            print("Patching index.js...")
            with open(jspath,"w") as idx: idx.write(patch)
            
            cfgpath = "%s/EnhancedDiscord/config.json"%dirpath
            if not os.path.exists(cfgpath):
                print("Creating config.json...")
                with open(cfgpath,"w") as cfg: cfg.write("{}")
        
            print("EnhancedDiscord installation complete!\n")
        
        
        elif option == 'Select Client':
            print("Selecting new Discord client...")
            backup = (client, jspath, version)
            client, jspath, version = select_client(True)
            if not jspath: client, jspath, version = backup
            print('\nOperating on client: %s %s\n'%(client,version))
    
        else:
            print('Error: The specified option was not valid.\n')

        print('Please type the number for your desired option:')
