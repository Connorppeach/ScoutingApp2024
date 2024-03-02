import jsonpack as jp
import requests

year = "2024"
matchid = "FLWP"
url = f'https://frc-events.firstinspires.org/{year}/{matchid}/practice'

r = requests.get(url)

data = r.text

data = data.split('<tbody id="match-results" style="white-space: nowrap">')[1]
data = data.split('</tbody>')[0]
data = data.split('<td class="text-start col-2">')
del data[0]

matchIndex = 1

arr = []

for m in data:
  teamList = m.split("<a ")
  del teamList[0]
  teamIndex = 0
  
  red = []
  blue = []
  
  for a in teamList:
    a = a.split('</a>')[0]
    a = a.split('>')[1]
    a = a.split('\n')[0]
    a = "frc" + a
    
    if teamIndex < 3:
      red.append(a)
    else:
      blue.append(a)
    
    teamIndex += 1
    
  arr.append({
    "key": "2024" + matchid.lower() + "_pm" + str(matchIndex),
    "red": red,
    "blue": blue
  })
    
  matchIndex += 1
    
print(jp.pack(arr))