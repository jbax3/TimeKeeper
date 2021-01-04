# Time Keeper
## About
This is a very simple Python glue script written for **OSX** for polling the active window every 30s and logging a 3-tuple (timestamp [UTC], window name [most often application name], window title [often task specific like website of document name]) to a CSV file.

It has four components:
1. A backgrounded Swift/OSX native listener for unlock events, which will log: (timestamp,"unlock","unlock") to make time away from the computer easier to identify.
2. Two AppleScripts that are identical apart from returning a different piece (one returns the window, the other title). This is two components is to make creating the CSV line not require additional string parsing.
3. A call to a command line utility (ioreg) to get the idle time.
4. a While-True loop with a 30s sleep. If after 30s, the idle time < 30s, then the window and title are logged, otherwise they are omitted presuming you are engaging in a low-interaction task and if you interact again, you'll see the same task immediately adjacent with a long time window without an unlock event.

## Parameters
1. `time_log_location` - this variable sets your logging location and log name.
2. `poll_interval` - this variable allows you to set your polling interval and idle time (same number).

## Testing
You can test the script and its output as follows:
`python TimeKeeper.py`

## Installing it as a Service
`sudo launchctl load lock.plist`

## Achieving greater browser granularity for web apps
Lets say you use a web app that has multiple focusable components, i.e. Google Hangouts, you can figure out on your own how to identify the in-focus element, and then add a click event to change the document title to include some transparent feature of the in-focus element such as who you are chatting with. An example javascript snippet for this has been included targeted toward JupyterLab.
