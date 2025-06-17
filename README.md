# extract-xiso-py
Python Script to provide a simple commandline interface for [extract-xiso](https://github.com/XboxDev/extract-xiso) by the [XboxDev organisation](https://github.com/XboxDev).<br>
Idea and inspiration came from [this](https://github.com/IronRingX/batch-xiso-extract) Script created by [IronRingX](https://github.com/IronRingX)

Supports Windows only.

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

## FaQ:

Q: Why did you create this?<br>
A: I had a large collection of Game Dumps that took to much space over time so i wanted to batch process them with [this](https://github.com/IronRingX/batch-xiso-extract) batch script but figured an interface would be nicer.

Q: Will there be Linux or MacOS Support?<br>
A: While extract-xiso is compatible with those my Script won't be, to be honest mostly because i'm to lazy but everyone is free to fork the repository and do it themselfes.

Q: Will this get frequent Updates?<br>
A: Probably not, i had this script on my PC since last Year Christmas so the only reason i released this is so maybe someone finds use from it. That also means that support is probably limited.

## Special Thanks to:

[in](mailto:in@fishtank.com) for creating and [XboxDev organisation](https://github.com/XboxDev) for maintaining [extract-xiso](https://github.com/XboxDev/extract-xiso)<br>
[IronRingX](https://github.com/IronRingX) for [batch-xiso-extract](https://github.com/IronRingX/batch-xiso-extract)
