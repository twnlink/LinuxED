#the shittiest thing ever (BUT IT STILL WORKS SO IT'S OKAY)
import os
import pwd
from shutil import copyfile
dirpath = os.path.dirname(os.path.realpath(__file__))
print(dirpath)
pathtoindexjs = (f'/home/{pwd.getpwuid(os.getuid()).pw_name}/.config/discord/0.0.5/modules/discord_desktop_core/index.js')
menu = input("Welcome to LinuxED!\n---\n1. Install ED\n2. Uninstall ED\n3. Update ED\n4. Update LinuxED\n5. Exit\n>")
if menu == "2":
    if os.path.exists(pathtoindexjs + ".backup"):
        os.remove(pathtoindexjs)
        print("Removed modified index.js...")
        os.rename(pathtoindexjs + ".backup", pathtoindexjs)
        print("Renamed index.js backup...")
        print("Successfully uninstalled EnhancedDiscord!")
    else:
        print("Couldn't find index.js backup, did you use the installer to install ED?")
        print("Exiting...")
elif menu == "1":
    if os.path.exists(dirpath + "/EnhancedDiscord"):
        print("EnhancedDiscord directory already exists! Skipping...")
    else:
        os.system("git clone https://github.com/joe27g/EnhancedDiscord.git")
    pathyorn = input("Would you like to choose your Discord index.js file location? (Y/N)\n>")
    if pathyorn.upper() == "YES" or pathyorn.upper() == "Y":
        pathtoindexjs = input("What is the path to your index.js file?\n>")
    if os.path.exists(pathtoindexjs):
        if os.path.exists(pathtoindexjs + ".backup"):
            print("Index.js backup already exists, skipping!")
        else:
            copyfile(pathtoindexjs, pathtoindexjs + ".backup")
        openindex = open(pathtoindexjs,"w")
        injdir = f'process.env.injDir = \'{dirpath}/EnhancedDiscord\';'
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
        openindex.write(f"{injdir}\n" + endpart)
        openindex.close()
        print("Patched index.js...")
        opendomshit = open(f"{dirpath}/EnhancedDiscord/dom_shit.js","r")
        originalfirstline = opendomshit.readlines()
        originalfirstline.insert(0, injdir + "\n")
        opendomshit.close()
        opendomshit = open(f"{dirpath}/EnhancedDiscord/dom_shit.js","w")
        opendomshit.writelines(originalfirstline)
        opendomshit.close()
        os.system("git -C EnhancedDiscord add --all")
        os.system("git -C EnhancedDiscord commit -m \\\"Update")
        print("Patched dom shit...")
        if os.path.exists(dirpath + "/EnhancedDiscord/config.json"):
            print("Config already exists, skipping...")
        else:
            makeconfigfile = open(dirpath + "/EnhancedDiscord/config.json", "w+")
            makeconfigfile.write("{}")
            makeconfigfile.close()
            print("Config file successfully made!")
        print("EnhancedDiscord installation complete!")
    else:
        print("Index.js not found. This could be because the script is not up to date, or your path was incorrect.")
    print("Exiting...")
elif menu == "3":
    print("Updating EnhancedDiscord installation...")
    os.system("git -C EnhancedDiscord add --all")
    os.system("git -C EnhancedDiscord commit -m \\\"Update")
    os.system("git -C EnhancedDiscord rebase")
elif menu == "4":
    if os.path.exists(dirpath + "/.git"):
        print("Updating LinuxED installation...")
        os.system("git rebase")
    else:
        print("Can't find LinuxED folder, did you clone the LinuxED repository?")
        print("Exiting...")
elif menu == "5":
    print("Exiting...")
    exit()
