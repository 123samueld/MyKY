# How to Install 

There are a few things you'll need to download and install for this app to work. Then there a few things you'll need to do to get the app running the first time. Here is a quick list of downloads and actions then their description below:

### Downloaods
* ChromeDriver
* Google Chrome
* Python 3
* JQ
* Asp.NET
### Actions
* Give permission to launch.sh
* Create desktop quick launch icon

## How to install Chrome Driver

## How to install Google Chrome

## How to install Python 3

## How to install JQ
JQ is so launch.sh can read the JSON path to the things in this app that it launches. 

To install this in Linux, Ubuntu 20.4 (probably other versions too), open the terminal and paste this command: 
sudo apt-get install jq

## How to install Asp.NET
You will need to install the Asp.NET runtime for the database. This is very specific to this version of Ubuntu 20.4, the 2nd command will be different for other versions, distributions or OSs. Paste each of these commands into the terminal one by one, wait for each command to finish before entering the next:

* sudo apt-get update
* wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
* sudo dpkg -i packages-microsoft-prod.deb
* sudo apt-get install aspnetcore-runtime-6.0

To check the installation was correct enter this command:
 dotnet --version

 If installed correctly you should see "6.0.428" in the terminal response. 


## Give Permmission to launch.sh
In the terminal, change directory to the root of the MyKY app by using "cd -path" to navigate to where you've stored the app folder. For example if it was on your desktop the command would be "cd ~.Desktop/MyKY/". Then enter this command:
\
* chmod +x launch.sh
\
This will give the launch.sh file permission to run on your machine. You may have to enter your password if you haven't already done so this session.
\
To test the launch.sh file is working correctly, cd to the project root dir and enter:
\
./launch.sh
\ 

The app should start to launch, there are debugging messages that should appear in the console. This will take a minuet because it's building the app from scratch every time since this is the development version, the production version will start much faster. 
\
You should see debug messages like "Build succeeded, 0 warnings, 0 errors". and a few "Info" lines with localhost and content root path to project root dir/DatabaseSystem/MyKYWeb.
\
Then a new window should open in your browser and after a moment a blank screen should open with "Goodbye Cruel World!" in the top left. If all that happens that means the app is working correctly and is being launched via the .sh file. But it still needs a Desktop Quicklaunch file.
\
## Create Desktop Quicklaunch Icon
You'll need to create a new "MyKY.desktop" file in "applications". First use this command to create a new shortcut launcher:
\ 
* nano ~/.local/share/applications/MyKY.desktop
\
Then you'll be presented with a blank area. You want to paste this block of text in but first make sure the path here is the correct path to where you've put the app folder on your machine, lines "Exec" and "Icon" will need corrected for your machine: 
\
\
[Desktop Entry]\
Version=1.0\
Type=Application\
Name=MyKY\
Comment=Launches the local real estate scanner and opens the dashboard\
Exec=/home/YourUsername/Desktop/MyKY/launch.sh\
Icon=/home/YourUsername/Desktop/MyKY/Resources/Imgs/AppLaunchIcon.png\
Terminal=false\
Categories=Utility;"\
To save press "Ctrl+O", press enter, then to exit press "Ctrl+X" \
\
Then refresh the desktop app list with:
\
* update-desktop-database ~/.local/share/applications/
\
You might have to restart or refresh to see the MyKY app icon on your desktop, do that with this command:
\
killall gnome-software
\
Click on the Desktop icon, it will take a moment because this is the development version and builds every time it's run which is slow, the production version will start up much faster. 

