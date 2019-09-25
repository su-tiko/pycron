# pycron
Python implementation of Cron daemon. 

For now the program is able to read a crontab-like file and execute its tasks at specified intervals. 
It is also able to monitor the specified file for re-reading it if it's updated.

## Usage
It is recommended to create and activate a virtualenv for installing `pycron` inside it.

First install the package with: `make install`

Then you can launch it with: `pycron <file>`

A `.crontab` file is included as example. It will open `/` each minute.

## Requirements
- croniter
- pytz
- watchdog


## ToDo

- Add 'execute as user' capabilities
- Better error and exit handling
- Make `FileWatcher` a daemon
- Add logging and remove `print`
- ~~Package it and make it installable~~ **(DONE)**
