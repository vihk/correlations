import pandas as pd
import numpy as np
import math
import requests
from io import StringIO
import plotly.express as px

url="https://radwatch.berkeley.edu/test/tmp/Station.csv"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

s=requests.get(url, headers=header).text
c=pd.read_csv(StringIO(s))


newpacket = []
areanames = []
timezones = []
for areas in range(1,30):
    try:
        nickname = c['nickname'][areas]
        name = c['Name'][areas]
        timezone = c['timezone'][areas].split("/")[0]
        url="https://radwatch.berkeley.edu/test/tmp/dosenet/" + nickname + "_month.csv"
        sec=requests.get(url, headers=header).text
        cont=pd.read_csv(StringIO(sec))
    except:
        print('error occured, df for ' + nickname + 'skipped')
        continue
    else:
        newpacket.append(cont)
        areanames.append(name)
        timezones.append(timezone)
        print('done.')

newaverages = []
errorFreePackets = []
newCPMS = []
newMEANS = []
listofSUMS = []
cpmlists  = []
for areas in range(len(newpacket)):
    try:
        df = newpacket[areas]
        cpmdf = df['cpm']
        sumdf = cpmdf.sum()
        sumdf = sumdf/len(df)
        print(sumdf)
    except:
        areanames.pop(areas)
        timezones.pop(areas)
        print('area removed, no counts found.')
        continue
    else:
        print('completed.')
        newaverages.append(sumdf)
        errorFreePackets.append(areanames[areas])
        total_counts  = sumdf * 5
        nmin  = len(cpmdf.to_numpy())*5
        mean_unc  = math.sqrt(total_counts)/nmin
        newCPMS.append(mean_unc)
        CPMmean = np.mean(cpmdf)
        newMEANS.append(CPMmean)
        listofSUMS.append(cpmdf.sum())
        cpmlists.append(cpmdf.to_numpy())
data = {'CPMS': newCPMS, 'Sensors': areanames, 
       'Avg. CPM':newMEANS, 'timezones':timezones}
df = pd.DataFrame(data)
fig = px.bar(df, x="Sensors", y="Avg. CPM", error_y = "CPMS", color = timezones)
fig.write_html("/Users/user/Desktop/newfig.html")


