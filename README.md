# extract-xiso-py
Python Script provide a simple commandline interface for [extract-xiso](https://github.com/XboxDev/extract-xiso) by the [XboxDev organisation](https://github.com/XboxDev).

Currently Supports Windows only.

## Usage:

- Download the latest release from [here](https://github.com/TheCraZyDuDee/extract-xiso-py/releases/latest/download/extract-xiso-py.exe)
- Place the extract-xiso-py.exe into the folder with your ISO files or extracted folders.
- Either let the Tool download extract-xiso or place your own copy called extract-xiso.exe besides the main executable.
- Select whatever option to choose by entering the corresponding number (confirm deleting sourcefiles or not).
- Processed files are in a newly created folder called 'output' besides the main executable.

## Building:

- Download the Repository via git or just as zip
- Install [Python](https://www.python.org/downloads/) and add it to System Path
- Install PyInstaller using `pip install pyinstaller`
- cd to the directory containing the icon.ico, extract-xiso.py and extract-xiso-py.spec file and run `pip install -r requirements.txt` and then `pyinstaller extract-xiso-py.spec` or just run the build.bat

## Special Thanks to:

[in](mailto:in@fishtank.com) for creating and [XboxDev organisation](https://github.com/XboxDev) for maintaining [extract-xiso](https://github.com/XboxDev/extract-xiso)
