import carball
import matplotlib.pyplot as plt
import json
import pandas as pd
import time
import numpy as np
from scipy.stats import kde
import os
from carball.json_parser.game import Game
from carball.analysis.analysis_manager import AnalysisManager
from os import path
path_to_json = "../rocket_league_analytics-main/data/json/"

# analysis = carball.analyze_replay_file("C0B836B64B3EB849DD87FCB6681529B1.replay")
# with open('game1.json', 'w') as fo:
#     analysis.write_json_out_to_file(fo)

bgoalsx,bgoalsy,ogoalsx,ogoalsy = [],[],[],[]
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
blue, orange = [],[]
playernam = ["games5425898691","enpitsu"]
#playernam = ["1","2","3"]
playerids = []
datatype = ["boostUsage","numLargeBoosts","numSmallBoosts","timeFullBoost","timeNoBoost","averageSpeed","timeAtSlowSpeed","timeAtSuperSonic"]
playerdata = {}
best_data = {}
dat = []
for k in playernam:
    playerdata[k] = []
for i in datatype:
    best_data[i] = []
# print(best_data)
for index, file in enumerate(json_files):
    with open(path_to_json+file,"r") as fo:
        data = json.load(fo)
    if index == 0:
        for x in data["players"]:
            if x["name"] == playernam:
                playerids.append(x["id"]["id"])
    if index == len(json_files)-1:
        for x in data["players"]:
            for k in playernam:
                if x["name"] == k:
                    s = x["stats"]["speed"]
                    a = x["stats"]["averages"]
                    b = x["stats"]["boost"]
                    playerdata[k].append(b["boostUsage"])
                    playerdata[k].append(b["numLargeBoosts"])
                    playerdata[k].append(b["numSmallBoosts"])
                    playerdata[k].append(b["timeFullBoost"])
                    playerdata[k].append(b["timeNoBoost"])
                    playerdata[k].append(a["averageSpeed"])
                    playerdata[k].append(s["timeAtSlowSpeed"])
                    playerdata[k].append(s["timeAtSuperSonic"])
    for j in data["players"]:
        s = j["stats"]["speed"]
        a = j["stats"]["averages"]
        b = j["stats"]["boost"]
        for i,k in enumerate(datatype):
            if i < 5:
                try:
                    best_data[k].append(b[k])
                except:
                    best_data[k].append(0)
            elif i < 6:
                try:
                    best_data[k].append(a[k])
                except:
                    best_data[k].append(0)
            else:
                try:
                    best_data[k].append(s[k])
                except:
                    best_data[k].append(0)


    for x in data["gameStats"]["hits"]:
        if "goal" in x:
            # if x["playerId"]["id"] in playerids:
            bgoalsx.append(x["ballData"]["posX"])
            bgoalsy.append(x["ballData"]["posY"])

for i,k in enumerate(best_data):
    if i == 4 or i == 6:
        dat.append(min(best_data[k]))
    else:
        dat.append(max(best_data[k]))

# print(dat)
goals = np.array([bgoalsx,bgoalsy])
k = kde.gaussian_kde(goals)
pmin=-5140
pmax=5140
step=80
xi, yi = np.mgrid[pmin:pmax:step,pmin:pmax:step]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

# collabel = [playernam[0],playernam[1],playernam[2],"best stats"]
collabel = [playernam[0],playernam[1],"best stats"]

g = pd.DataFrame(playerdata)
g["best"] = dat
print(g)

fig, axs = plt.subplot_mosaic("AABB;AACC")
img = plt.imread("simple-pitch.png")

axs["A"].pcolormesh(xi, yi, zi.reshape(xi.shape), shading="gouraud", cmap="magma")
axs["A"].set_label("Heatmap of where goals were scored from")

axs["B"].axis("off")


extent = axs["A"].get_window_extent().transformed(fig.dpi_scale_trans.inverted())

axs["C"].axis("off")





table = axs["B"].table(cellText=g.values,colLabels=collabel,rowLabels=datatype,loc="center")


extent = axs["B"].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig("table.png",bbox_inches=extent.expanded(2.25,1),dpi=600)
table.auto_set_font_size(False)
table.set_fontsize(12)
plt.show()
