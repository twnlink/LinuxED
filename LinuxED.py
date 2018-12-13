#Import all of the shit. Yes, I know this code is terrible and unreadable. No, I won't rewrite it.
import os
import pwd
from shutil import copyfile
import platform
discordstableversion = "0.0.5"
discordcanaryversion = "0.0.63"
discordptbversion = "0.0.9"
discordsnapversion = "0.0.5"
discordmenu = ""
def indexjsselect(toornottoinstall, toorfrom):
    global pathtoindexjs
    global discordmenu
    pathtoindexjs = "invalidpath"
    if os.path.exists(f'/home/{username}/.config/discord/{discordstableversion}/modules/discord_desktop_core/index.js'):
        discordmenu = discordmenu + "Stable\n"
    if os.path.exists(f'/home/{username}/.config/discordcanary/{discordcanaryversion}/modules/discord_desktop_core/index.js'):
        discordmenu = discordmenu + "Canary\n"
    if os.path.exists(f'/home/{username}/.config/discordptb/{discordptbversion}/modules/discord_desktop_core/index.js'):
        discordmenu = discordmenu + "PTB\n"
    if os.path.exists(f'/home/{username}/snap/discord/82/.config/discord/{discordsnapversion}/modules/discord_desktop_core/index.js'):
        discordmenu = discordmenu + "Snap\n"
    if discordmenu == "Stable\n":
        pathtoindexjs = (f'/home/{username}/.config/discord/{discordstableversion}/modules/discord_desktop_core/index.js')
    elif discordmenu == "":
        nodiscordmenu = input("You don't seem to have Discord installed, or your version is unsupported by the installer...\n Would you like to enter a custom index.js path? (y/N)\n>")
        if nodiscordmenu.upper() == "YES" or nodiscordmenu.upper() == "Y":
            pathtoindexjs = input("Please type the path to your index.js...\n>")
        else:
            print("Sorry that the installer wasn't able to help.\nExiting...")
            exit()
    else:
        selectionmenu = input("---\nThese are all installed versions of Discord you have: \n" + discordmenu + f"Custom\n---\nPlease type the name of the Discord version you want to {toornottoinstall} EnhancedDiscord {toorfrom}.\n>")
        if selectionmenu.upper() == "STABLE":
            pathtoindexjs = (f'/home/{username}/.config/discord/{discordstableversion}/modules/discord_desktop_core/index.js')
        if selectionmenu.upper() == "CANARY":
            pathtoindexjs = (f'/home/{username}/.config/discordcanary/{discordcanaryversion}/modules/discord_desktop_core/index.js')
        if selectionmenu.upper() == "PTB":
            pathtoindexjs = (f'/home/{username}/.config/discordptb/{discordptbversion}/modules/discord_desktop_core/index.js')
        if selectionmenu.upper() == "SNAP":
            pathtoindexjs == (f'/home/{username}/snap/discord/82/.config/discord/{discordsnapversion}/modules/discord_desktop_core/index.js')
        if selectionmenu.upper() == "CUSTOM":
            pathtoindexjs = input("Please type the path to your index.js...\n>")
    if os.path.exists(pathtoindexjs):
        print("Index.js found!")
    else:
        print("---\nCan't find index.js. Are you sure that exists?\nExiting...\n---")
        exit()
#Check if some idiot is running this on Windows... Like, seriously... Why the hell would you run LinuxED on Windows???
if platform.system() == "Windows":
    print("This is a Linux installer for EnhancedDiscord... It says it in the name, LinuxED... Why are you using this?")
    exit()
#Define the starting variables, these are all their own thing. 
#Dirpath is the current directory the script is running from
dirpath = os.path.dirname(os.path.realpath(__file__))
#Username is the actual username of the person running the script
username = pwd.getpwuid(os.getuid()).pw_name
#the menu. that's it. what exactly do you want from me?
menu = input("Welcome to LinuxED!\n---\n1. Install ED\n2. Uninstall ED\n3. Update ED\n4. Update LinuxED\n5. Exit\n>")
if menu == "2":
    indexjsselect("uninstall", "from")
    if os.path.exists(pathtoindexjs + ".backup"):
        #delete modified indexjs so that we can replace it with the unmodified one
        os.remove(pathtoindexjs)
        print("---\nRemoved modified index.js...")
        #make unmodified one have the proper name
        os.rename(pathtoindexjs + ".backup", pathtoindexjs)
        print("Renamed index.js backup...")
        print("Successfully uninstalled EnhancedDiscord\n---!")
    else:
        #if the backup isn't there inform the user and then exit
        print("---\nCouldn't find index.js backup, did you use the installer to install ED?")
        print("Exiting...\n---")
elif menu == "1":
    #checking so you don't have to do git clone enhanceddiscord again
    if os.path.exists(dirpath + "/EnhancedDiscord"):
        print("EnhancedDiscord directory already exists! Skipping...")
    else:
        #clone the enhanceddiscord repo
        os.system("git clone https://github.com/joe27g/EnhancedDiscord.git")
    #start long chain of figuring out what versions of discord exist
    indexjsselect("install", "to")
    #check to see if indexjs path exists, if not exit
    if os.path.exists(pathtoindexjs + ".backup"):
        print("Index.js backup already exists, skipping!")
    else:
        #make backup index.js for uninstallation and recovery in case something goes wrong
        copyfile(pathtoindexjs, pathtoindexjs + ".backup")
    openindex = open(pathtoindexjs,"w")
    injdir = f'process.env.injDir = \'{dirpath}/EnhancedDiscord\';'
    #this is not my code but it's what I put at the end of index.js
    endpart = """const { BrowserWindow, session } = require('electron');
    const path = require('path');

    session.defaultSession.webRequest.onHeadersReceived(function(details, callback) {

       if (!details.responseHeaders["content-security-policy-report-only"] && !details.responseHeaders["content-security-policy"]) return callback({cancel: false});
       delete details.responseHeaders["content-security-policy-report-only"];

       delete details.responseHeaders["content-security-policy"];

       callback({cancel: false, responseHeaders: details.responseHeaders})
    ;
    });

    class PatchedBrowserWindow extends BrowserWindow {
       constructor(originalOptions) {
           const options = Object.create(originalOptions);
           options.webPreferences = Object.create(options.webPreferences);
        
        const originalPreloadScript = options.webPreferences.preload;

           // Make sure Node integration is enabled
           options.webPreferences.nodeIntegration = true;
           options.webPreferences.preload = path.join(process.env.injDir, 'dom_shit.js');
           options.webPreferences.transparency = true;

           super(options);
           this.__preload = originalPreloadScript;
       }
    }

    const electron_path = require.resolve('electron');
    const browser_window_path = require.resolve(path.resolve(electron_path, '..', '..', 'browser-window.js'));
    require.cache[browser_window_path].exports = PatchedBrowserWindow;
    module.exports = require('./core.asar');"""
    #write the shit to the indexjs file
    openindex.write(f"{injdir}\n" + endpart)
    openindex.close()
    print("Patched index.js...")
    #read the dom_shit since there's a bug that makes it so you have to redefine injdir
    opendomshit = open(f"{dirpath}/EnhancedDiscord/dom_shit.js","r")
    #read the original first line of the file i guess (at this point i'm just doing this from memory, i'm too incompetent to remember what thsi does)
    originalfirstline = opendomshit.readlines()
    #replace originalfirstline var with modified one with the injdir
    originalfirstline.insert(0, injdir + "\n")
    opendomshit.close()
    #open it again except this time we can write to it
    opendomshit = open(f"{dirpath}/EnhancedDiscord/dom_shit.js","w")
    #write modified originalfirstline
    opendomshit.writelines(originalfirstline)
    opendomshit.close()
    print("Patched dom shit...")
    #check if config exists so we can make it
    if os.path.exists(dirpath + "/EnhancedDiscord/config.json"):
        print("Config already exists, skipping...")
    else:
        #if it doesn't exist make it
        makeconfigfile = open(dirpath + "/EnhancedDiscord/config.json", "w+")
        makeconfigfile.write("{}")
        makeconfigfile.close()
        print("Config file successfully made!")
    print("EnhancedDiscord installation complete!")
#placeholder for updating ED, but I don't think I'll actually ever do that
elif menu == "3":
    print("Feature not implemented yet! Sorry...")
elif menu == "4":
    #check if .git is there, if it is then I know that this was cloned from the git repo and am free to git pull
    if os.path.exists(dirpath + "/.git"):
        print("Updating LinuxED installation...")
        #git pull latest version. works if script hasn't been modified.
        os.system("git pull --no-edit")
    else:
        print("---\nCan't find LinuxED folder, did you clone the LinuxED repository?")
        print("Exiting...\n---")
elif menu == "5":
    print("---\nExiting...")
    exit() 
