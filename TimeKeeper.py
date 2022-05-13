#!/Users/nothing/mambaforge/bin/python
import os
import subprocess
from time import time, sleep
sleep(20)

# Parameters
time_log_location = "/Users/nothing/TimeLog.csv"
poll_interval = 30

# A self-contained swift script to listen for the unlock event IOT log when the computer is unlocked
# Allows for computation of time while computer is locked/asleep from last recorded non-idle event

# Goes inside of Swift stuff IOT run Anki etc
# func onUnlock() {
#     _ = NSWorkspace.shared.open(
#     	URL(fileURLWithPath: "/Users/nothing/PythonCode/Apple/OnUnlock.app"))
# }

# onUnlock()

swift_lock_script = '''echo 'import Foundation
import AppKit
import SwiftUI
import Cocoa

func logUnlock() {
  do {  let dataString = String(Date().timeIntervalSince1970)+",\\"unlock\\",\\"unlock\\"\\n"
        guard let fileUrl = URL(string: "'''+time_log_location+'''") else {
            preconditionFailure("Invalid static URL string:'''+time_log_location+'''")
        }
        let fileHandle = try FileHandle(forWritingTo: fileUrl)
            fileHandle.seekToEndOfFile()
            fileHandle.write(dataString.data(using: .utf8)!)
            fileHandle.closeFile()
    } catch {
        print("Error writing to file \(error)")
    }
}

let notificationCenter = DistributedNotificationCenter.default()

notificationCenter.addObserver(forName: NSNotification.Name(rawValue: "com.apple.screenIsUnlocked"),
                               object: nil,
                               queue: nil,
                               using: { _ in
  logUnlock()

                                
})

RunLoop.current.run()' | swift - ''' 

# Returns the window program name e.g. Chrome or Microsoft Word
window_script = '''osascript -e 'global frontApp, frontAppName, windowTitle

set windowTitle to ""
tell application "System Events"
	set frontApp to first application process whose frontmost is true
	set frontAppName to name of frontApp
	tell process frontAppName
		tell (1st window whose value of attribute "AXMain" is true)
			set windowTitle to value of attribute "AXTitle"
		end tell
	end tell
end tell

return frontAppName' '''

# Same as window script, but returns window title (both can be done together, but I got fed up with string parsing)
title_script = '''osascript -e 'global frontApp, frontAppName, windowTitle

set windowTitle to ""
tell application "System Events"
	set frontApp to first application process whose frontmost is true
	set frontAppName to name of frontApp
	tell process frontAppName
		tell (1st window whose value of attribute "AXMain" is true)
			set windowTitle to value of attribute "AXTitle"
		end tell
	end tell
end tell

return windowTitle' '''

# This line returns the idle time, used to check that the system has been idle for <30s IOT write entry
idle_time_script = '''ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}' '''

# Backgrounds the swift process to listen for unlocks
subprocess.Popen(swift_lock_script, executable='/bin/bash', shell=True).pid

# Polls the active window every 30s, if the computer has been idle for <30s
while True:
	sleep(poll_interval)
	idle_time = subprocess.Popen(idle_time_script, shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read().decode().rstrip('\n').replace(', ',',')
	try:
		idle_time = float(idle_time)
		if idle_time < poll_interval:
			window = subprocess.Popen(window_script, shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read().decode().replace('\n','').replace(', ',',').replace('"','``')
			title = subprocess.Popen(title_script, shell=True, executable='/bin/bash', stdout=subprocess.PIPE).stdout.read().decode().replace('\n','').replace(', ',',').replace('"','``')
			with open(time_log_location,'a+') as f:
				f.write(f'{time()},"{window}","{title}"\n')
	except:
		print(idle_time)
		pass
	
