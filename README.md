# LinuxED
LinuxED is an alternative installer for EnhancedDiscord that works on Linux. This project is not affiliated with Discord, or EnhancedDiscord in any way. I made this while learning Python and I'm aware of how messy, inconsistent, and poorly coded this script looks.

# LinuxED has been discontinued
EnhancedDiscord has reached End of Life, thus all remaining official support has been dropped. So LinuxED should be shut down as well.

# Operating systems supported
LinuxED supports most major distributions of Linux, MacOS, and even Windows.  
It also supports all versions of Discord (PTB, Stable, Canary, etc.)  

# MacOS Support
If you wish to use this on MacOS you'll first need to download Python 3 via [Brew](https://brew.sh).  
After installing Brew, enter `brew install python3` in a terminal, then follow the installation guide below.
# Features
- Custom index.js location
- EnhancedDiscord updater (this does update ED)
- LinuxED updater (this does not update ED, it updates the LinuxED script)
- Automates all EnhancedDiscord installation on Linux, MacOS, and Windows.
# Requirements
You will need Python's distutils, which most commonly has the package name `python3-distutils`  
To install Python's distutils on Debian or any Debian derivatives (Ubuntu, Linux Mint) do `sudo apt install python3-distutils`

# Installation and Usage
1. Git clone this repo: `git clone https://github.com/Cr3atable/LinuxED/` in a terminal.
2. cd into the newly cloned repo: `cd LinuxED`
3. Execute the Python script: `python3 LinuxED.py` and follow the instructions.
4. Restart Discord entirely.
That's it! EnhancedDiscord is now installed.
