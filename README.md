# ScoutingApp2024
[https://www.youtube.com/watch?v=xCGu5Z_vaps](https://www.youtube.com/watch?v=xCGu5Z_vaps)
A remake of the scouting app for the 2024 FRC season

Python is better for statistics, and that's what we need to be in the scouting app.
## Usage
#### Installing
- download python 3.11 https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe (Python 3.12 no worky)   
`git clone https://github.com/Team4388/ScoutingApp2024`    
`cd ScoutingApp2024`   
`pip install -r requirements.txt`   
`python3 ./main.py`   
- On windows, for a python dependency, you must download https://visualstudio.microsoft.com/visual-cpp-build-tools/ and select 'Desktop development with C++' To download

#### Initialization
- go to: http://localhost:4388
- To init a match, you must go to the 'TBA' tab and select the correct year, and event.
- Then click 'Save Matches'. This will create a file at 'data/[event code]/matches.jsonpack'. This file is used to provides a list of matches and teams to the scouters.
- In an actual match, this file should be shared around to the other match scouters and pit scouters. Either using the 'Send' tab, or by USB.
- Everyone should click on the 2nd field in the top-right, and select the new event.
- Also, everyone should click the 3rd feild in the top-right and enter their actual name.
- Match scouters should click the first field in the top-right and select their position
- Match scouters should go to the 'scouting / Match scouting' tabs
- Pit scouters should go to the 'scouting / Pit scouting' tabs

#### Data usage
- After all the matches and pits have been scouted, everyone should transfer their data to one device ( the device used by the team leader when choosing alliances ).
- This is most likely easiest done with USB drives, because of the large file size.
- The 'Data / Dashboard' Tab is used to display what matches & pits have been scouted.
- The 'Data / Leaderboard' Tab is used to display what teams have the highest stats ( and who should be recruited )
- By clicking on a team, you can see what notes the scouters have taken on them.
- The 'Data / Predictor' Tab is used to predict the outcome of a match, using multiple statistics.
- The 'Data / Selector' Tab is used to find the best machups avalible. ( This is buggy, and the avalible matchups should be visable to team leader, via the screens )

#### Fakescout
- The 'fakescout.py' script is useful for generating data to test from TBA

## TODO


- ~~Clean up code~~
- ~~Get rid of "frc" in team names~~
- ~~Add "sort" button in file send~~
- ~~Format team page better~~
- ~~Add an 'Event' Page, to view all the data about a single event~~
- ~~Add "view on TBA" buttons~~
- Make a tool to convert data to new format
- ~~Practice mode (First Events API?)~~
- make not use socket-io
- ~~Fix persistant scouting data issue~~
- ~~Add data version (maybe?)~~

- ~~Write scouting / pit scouting frontend~~
- ~~^ Names of the people who did the scouting~~
- ~~Copy code from chief delphi to calculate best teams from scouting data~~
- ~~Write data visualisation frontend~~
- ~~^ show stats like OTP and win % first, then scouting notes,~~ then throw the rest of the data at the user (from TBA)
- Incorperate TBA in-depth data somehow into visualizations

## Also TODO
- ~~Finish writing optional wifi transfer mode~~
- ~~Add a "This requires an internet connection" warning for anything that requires an internet connection~~
- ~~Make the UI GOOD!!~~
- ~~^ make it mobile friendly for the tablets~~
