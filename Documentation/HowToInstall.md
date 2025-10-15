# How to Install 

There are a few things you'll need to download and install for this app to work. Then there a few things you'll need to do to get the app running for the first time. Here is a quick list of downloads and actions then their description below:

### Downloaods
* This app
* Google Chrome
* ChromeDriver
* Python 3
* Selenium
* Flask
* JQ
* Asp.NET
### Actions
* Date FilePathCompendium.json
* Give permission to launch.sh
* Test launch.sh
* Create desktop quick launch icon

## Downloads/Installs

### This app
Get this app from Github, preferably clone it to your Desktop. 

### How to Download/Install Google Chrome
Unfortunately the scraper depends on the Google Chrome Browser, other browsers are not an option. You will need to download Chrome, get the latest version from here: 
* https://www.google.com/intl/en_uk/chrome/

### How to Download/Install Chrome Driver
The correct ChromeDriver should already be inclued in the Utilities dir of this project but these instructions are for if it's not or you need to update in the future. 

ChromeDriver and Chrome Browser version numbers are mismatched. Current latest Driver is V114 and Browser is V141 (as of 07/10/2025). The driver tends to trail behind the browser so if there are compatability issues try downloading an earlier verions of Chrome Browser. The list of Driver versions can be found here:

* https://sites.google.com/chromium.org/driver/downloads

Click on one of those drivers and you'll be taken to a page like this;

* https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/

Select the Linux version, download it then extract the zip to MyKY/Utilities dir.

This step has a lot of curve balls, many incorrect links that look similar on the surface. You may need to repeat this step a few times if the Driver and Browser versions are not compatable. 
\
In a few steps from now, after you've downloaded and installed Selenium you'll be able to test if the ChromeDriver download was correct.

### How to Download/Install Python 3
In the terminal first update the package list with:

* sudo apt update

Then download with:

* sudo apt install python3

Then test it with:

* python3 --version

That should write the version to the terminal output. You'll then need to install a download tool for Python called "PIP". Do this with:

* sudo apt install python3-pip

If successful it will say so in the terminal output. 

### How to Download/Install Selenium
Selenium is the software that I've used to actually do the real estate website scraping. It opens an instance of the Chrome Browser and operates like a normal human user clicking on things. It can be blocked by CAPTCHA's and other anti-machine systems but overall it's a good scraping system. Download with this command:

* pip3 install selenium

There should be a set of download messages. To test the download and install was correct first open a Python terminal by entering this in the standard terminal:

* python3

Then enter these:

* import selenium
* print(selenium.__version__)

If Python Selenium was downloaded and installed correctly you'll see a version number like "4.27.1".

Exit to the python terminal back to the standard terminal with:

* exit()

To test that Selenium is using the ChromeDriver correctly, first in the terminal cd to the project root dir if you're not already there, then run this command:
 
 * python3 Utilities/SeleniumAndWebDriverTest.py

 If Selenium and the ChromeDriver and both correctly downloaded and installed, there will be a brief pause, the Chrome Browser will open with a message in the headder saying it's being controlled by automated software, it will go to google.com then the browser will close. Then a message will appear in the terminal saying "Google". This confirms Selenium and the ChromeDriver are working correctly. 

### How to Download/Install Flask

Flask is needed so the frontend dashboard can "talk" to the backend Python code which handles scraping. To install, in the terminal, navigate to the project root dir if not already there. Then enter this command:

* pip install -r Utilities/requirements.txt

To test that was installed correctly enter this command in the terminal to open a Python terminal

* python3

Then enter:

* import flask
* print(flask.__version__)

That should return the version of Flask installed confirming it has been installed correctly.

### How to Download/Install JQ
JQ is so launch.sh can read the a file with all the pathing to the files this app needs. This is a design choice that makes it much easier to update and refactor code, over all it's an excellent design but adds a bit of extra setup with JQ. 

To install JQ in Linux, Ubuntu 20.4 (probably other versions too), open the terminal and paste this command: 

* sudo apt-get install jq

Test that with: 

* jq --version

You should see the version number like "jq-1.6".

### How to Download/Install Asp.NET
You will need to install the Asp.NET runtime for the database. This is very specific to this version of Ubuntu 20.4, the 2nd command will be different for other versions, distributions or OSs. Paste each of these commands into the terminal one by one, wait for each command to finish before entering the next:

* sudo apt-get update
* wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
* sudo dpkg -i packages-microsoft-prod.deb
* sudo apt-get install aspnetcore-runtime-6.0

To check the installation was correct enter this command:
 dotnet --version

 If installed correctly you should see "6.0.428" in the terminal response. 

## Actions

### Update FilePathCompendium.json
All the paths used in this app should be handled through 1 file, meaning you need to update 1 line in that 1 file so all paths are relative to your machine. This takes 2 stages. First let's find the root path of this app on your machine. Open a terminal and cd to the root dir of this app "MyKY". Once you're there use this terminal command:

* pwd

That will return something like "/home/samuel/Desktop/MyKY". Take note of the first part like "/home/samuel". 

 Use your folder navigator to go to the MyKY folder, then find and go into the Utilities folder. Open the FilePathCompendium.json file. The very first variable is:  "RootPath": "/home/samuel". Change this to your root path, you found this with the "pwd" command. 

 To test that your path configuration is correct, run this command from the project root directory:

* ./Utilities/test_paths.sh

 This will check that all the paths are correct and that key files exist. If you see any ❌ errors, fix them before proceeding. You should see mostly ✅ checkmarks if everything is configured correctly. 


### Give Permission to kill_protocol.sh ( "Off" button)
Terminating all the processes running in the app is a big deal this has to be set up before running the app or turning off the processes bcomes very messy. "cd" to the project root dir, this will be different on your machien but something like "cd /home/YourUsername/Desktop/MyKY/". Once you're in the project root dir enter this command:

* chmod +x kill_protocol.sh

At the end you'll test the "off button" later once the "on button" is setup and fully working. 

### Give Permmission to launch.sh
In the terminal, change directory to the root of the MyKY app by using "cd -path" to navigate to where you've stored the app folder. For example if it was on your desktop the command would be "cd ~.Desktop/MyKY/". Then enter this command:

* chmod +x launch.sh

This will give the launch.sh file permission to run on your machine. You may have to enter your password if you haven't already done so this session.

### Test the Lanuncher
You must test the launch.sh file is working correctly, cd to the project root dir and enter:

* ./launch.sh


The app should start to launch, there are debugging messages that should appear in the console. This will take a while because it's clearing and building the database from scratch every time since this is the development version, the production version will only run the build so it will start much faster. 

You should see debug messages like "Build succeeded, 0 warnings, 0 errors". and a few "Info" lines with localhost and content root path to project root dir/DatabaseSystem/MyKYWeb.
\
Then a new window should open in your browser and after a moment a blank screen should open with "Goodbye Cruel World!" in the top left. If all that happens that means the app is working correctly and is being launched via the .sh file. But it still needs a Desktop Quicklaunch file.

### Create Desktop Quicklaunch Icon ( "On" button)
You'll need to create a new "MyKY.desktop" file in "applications". First use this command to create a new shortcut launcher:

* nano ~/.local/share/applications/MyKY.desktop

Then you'll be presented with a blank area. You want to paste this block of text in but first make sure the path here is the correct path to where you've put the app folder on your machine, lines "Exec" and "Icon" will need corrected for your machine: 

[Desktop Entry]\
Version=1.0\
Type=Application\
Name=MyKY\
Comment=Launches the local real estate scanner and opens the dashboard\
Exec=/home/YourUsername/Desktop/MyKY/launch.sh\
Icon=/home/YourUsername/Desktop/MyKY/Resources/Imgs/AppLaunchIcon.png\
Terminal=false\
Categories=Utility;"

To save press "Ctrl+O", press enter, then exit with "Ctrl+X". 
\
Then refresh the desktop app list with:

* update-desktop-database ~/.local/share/applications/

You might have to restart or refresh to see the MyKY app icon on your desktop, do that with this command:

* killall gnome-software

Click on the Desktop icon, it will take a moment because this is the development version to start.

To also test the "off button", find the "Kill Protocol" button in the Control Panel, on the popup press the big red "TERMINATE" button, this will kill all processes and the whole app will close. 

## Installation Complete
If you got through all those steps then the app is fully installed and ready to go. 

