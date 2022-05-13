# Starting Things Automatically
## Cron
* It is possible to use crontab, though roughly deprecated.
* https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41

## LaunchCtl
* This works. Make sure to use a Good Plist to specify the user, the shell paths, and a stdout+ file. For a long time this wasn't working for me, and it was because I had some script errors that weren't working early on reboot, and this was invisible to me.
* https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41
* ```
<plist version="1.0">
    <dict>
	<key>UserName</key>
	<string>your_user_name</string>
        <key>Label</key>
        <string>com.timekeeper</string>
        <key>Program</key>
        <string>/Users/your_user_name/PythonCode/TimeKeeper/TimeKeeper.py</string>
        <key>EnvironmentVariables</key>
        <dict>
            <key>PATH</key>
            <string>/bin:/usr/bin:/usr/sbin/:/usr/local/bin</string>
        </dict>
        <key>StandardOutPath</key>
        <string>/tmp/tk.stdout</string>
        <key>StandardErrorPath</key>
        <string>/tmp/tk.stdout</string>
        <key>WorkingDirectory</key>
        <string>/Users/your_user_name</string>
        <key>RunAtLoad</key>
        <true/>
    </dict>
</plist>
```


## Users & Groups > Login Items
* I have used this to start an automator app, I haven't used it to run my Python Script. This might actually be a much better user-friendly way to start something that then contains a bunch of logic about how to restart.
* https://www.macstadium.com/blog/automating-login-and-startup-events-in-macos