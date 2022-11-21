import os
import pathlib
import time
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import kde

from rattletrap import query_replay, Replay

file_directory = pathlib.Path(__file__).parent.absolute()

# this script reads the RL replay file and parses it into a json(internally) using rattletrap.exe
# afterwards the necessary it extracted and then turned into a heatmap, displays the match in 2d; see specific explanation below
# the main player is the player from which the replay was grabbed

player_ids = {}

player_int = []
player_nam = {}
vip = ""
teamnr = 0
teamord = {}
timex = []
ballids = []


def get_car_paths(replay: Replay):
    global vip, teamnr, teamord
    actor_positions, actor_boosts = {},{}

    # this first loop gathers the player names into a dict, and makes a dict for the ids of each player(see below)
    for index, names in enumerate(replay.header.data["body"]["properties"]["value"]["PlayerStats"]["value"]["array"]):
        if index == 0:
            vip = str(names["value"]["Name"]["value"]["str"])
            teamnr = names["value"]["Team"]["value"]["int"]
        teamord[index] = str(names["value"]["Name"]["value"]["str"])
        player_ids[index] = []

        player_nam[index] = []
    player_ids[6] = []
    player_nam[6] = []
    # the extracted json uses "frames" to denote new information. not sure if a frame is made every x ms, or made when new info is needed
    for frame in replay.content.data["body"]["frames"][:]:
        # print(f"Time: {frame['time']}")
        for replication in frame["replications"]:
            # every frame has an actor id; data tied to that actor id. can be a car, ball, boost pads etc..
            actor_id = replication["actor_id"]["value"]
            # frames have spawned and update types. both can be in a single frame.
            if "spawned" in replication["value"]:
                if actor_id not in actor_positions:
                    # find a frame for which the spawn tag is for a car
                    if replication["value"]["spawned"]["object_name"] == "Archetypes.Car.Car_Default":
                        # initiate a empty array for the corresponding actor id.
                        actor_positions[actor_id] = []
                    try:
                        loc = replication["value"]["spawned"]["initialization"]["location"]
                        actor_positions[actor_id].append({"time": frame["time"], "x": loc["x"], "y": loc["y"]})
                    except:
                        pass

                    if replication["value"]["spawned"]["object_name"] == "Archetypes.Ball.Ball_Default":
                        actor_positions[actor_id] = []
                        actor_boosts[actor_id] = []
                        player_ids[6].append(actor_id)
            if "updated" in replication["value"]:
                for update in replication["value"]["updated"]:
                    # sometimes, new actor ids are spawned for the same player, here we find a frame with that info
                    # and then put all actor ids of each specific player into their corresponding array.

                    if update["name"] == "Engine.Pawn:PlayerReplicationInfo":
                        # print(update["value"]["flagged_int"]["int"])
                        if update["value"]["flagged_int"]["int"] not in player_int and update["value"]["flagged_int"][
                            "int"] > 0:
                            # get the player identifier. this is different than an actor id.
                            player_int.append(update["value"]["flagged_int"]["int"])
                        # here we use the array generated at the top to store the multiple "car ids" of each player
                        for op in range(len(player_int)):
                            if update["value"]["flagged_int"]["int"] == player_int[op] and actor_id not in player_ids[
                                op]:
                                player_ids[op].append(actor_id)
                                print("cars: " + f"{actor_id}")
                    if update["name"] == "Engine.PlayerReplicationInfo:PlayerName":
                        for op in range(len(player_int)):
                            if actor_id == player_int[op]:
                                player_nam[op] = update["value"]["string"]

                    # finally, find the xyz data and add that to a dict for each "car id".
                    # the list we just made above is used later in the code to connect all the xyz data for each player together
                    if update["name"] == "TAGame.RBActor_TA:ReplicatedRBState" and actor_id in actor_positions:
                        rigid_body_location = update["value"]["rigid_body_state"]["location"]
                        # print(f"Body {actor_id} location: {rigid_body_location})
                        # append to name positions

                        actor_positions[actor_id].append({"time": frame["time"], "x": (rigid_body_location["x"] / 100),
                                                          "y": (rigid_body_location["y"] / 100)})

    # print(car_ids)
    # print(actor_boosts)
    return actor_positions, actor_boosts

def car_positions_to_histories(positions: dict) -> List['dict']:
    history_plots = []
    global timex

    for actor_id in positions.keys():
        actor_history = positions[actor_id]
        xs = []
        ys = []
        times = []
        for position in actor_history:
            xs.append(position["x"])
            ys.append(position["y"])
            times.append(position["time"])
        xs = np.array(xs)
        ys = np.array(ys)
        times = np.array(times)
        timex = times
        if xs.shape[0] > 0:
            history_plots.append({
                "times": times,
                "xs": xs,
                "ys": ys,
                "actor_id": actor_id
            })
    return history_plots


def heatmap(histories: List['dict']):
    xs,ys = [],[]
    for index3, history in enumerate(histories):
        if history["actor_id"] in player_ids[1]:
            for px, py in zip(history["xs"], history["ys"]):
                xs.append((px * -1))
                ys.append(py)

    return xs,ys


def history_to_heat_map(histories: List['dict']) -> np.ndarray:
    heat_map = np.zeros(xi.shape)

    for history in histories:
        if history["actor_id"] in player_ids[1]:
            for px, py in zip(history["xs"], history["ys"]):
                pxi = int((px*-1)/step) +offset
                pyi = int(py/step)+offset
                heat_map[pxi, pyi] += 1

    return heat_map

def grapher(histories: List['dict'], start, end):
    index11 = 0
    xs = {}
    ys = {}

    for a in range(len(player_nam)):
        xs[a] = []
        ys[a] = []
    for k in range(len(player_nam)):

        if vip == player_nam[k]:
            index11 = k

    indexx = 1
    for l in range(len(player_nam)):
        if index11 != l:
            for index3, history in enumerate(histories):
                if history["actor_id"] in player_ids[l]:
                    for px, py, timeg in zip(history["xs"], history["ys"], history["times"]):
                        if start < timeg < end:
                            xs[indexx].append((px * -1))
                            ys[indexx].append(py)
            indexx += 1
        else:
            for index3, history in enumerate(histories):
                if history["actor_id"] in player_ids[l]:
                    for px, py, timeg in zip(history["xs"], history["ys"], history["times"]):
                        if start < timeg < end:
                            xs[0].append((px * -1))
                            ys[0].append(py)
    return xs, ys


queried_replay = query_replay(os.path.join(file_directory, "DF23AC9C459DB2DAB126DA825631338C.replay"))

car_positions = get_car_paths(queried_replay)
# print(car_positions)

car_histories = car_positions_to_histories(car_positions[0])
# boost_histories = car_boosts_to_histories(car_boost)


fig ,axs = plt.subplot_mosaic("AAB;AAC")

# axs["A"] = plt.figure()
axs["A"].set_xlim(-8000, 8000)
axs["A"].set_ylim(-8000, 8000)
axs["A"].autoscale()

img = plt.imread("simple-pitch.png")

xxx = []
yyy = []
ln, = axs["A"].plot(xxx, yyy)

lines = []

for o in range(8):
    if o == 0:
        lobj = axs["A"].imshow(img, extent=[-4100, 4100, -6000, 6000])
    elif o == 1:
        lobj = axs["A"].plot([], [], color="green")[0]
    else:
        if teamnr == 0:
            if player_nam[o - 1] == teamord[0] or player_nam[o - 1] == teamord[1]:
                lobj = axs["A"].plot([], [], color="blue")[0]
            elif o < 7:
                lobj = axs["A"].plot([], [], color="orange")[0]
            else:
                lobj = axs["A"].plot([], [], color="black")[0]
        else:
            if player_nam[o - 1] == teamord[0] or player_nam[o - 1] == teamord[1]:
                lobj = axs["A"].plot([], [], color="orange")[0]
            elif o < 7:
                lobj = axs["A"].plot([], [], color="blue")[0]
            else:
                lobj = axs["A"].plot([], [], color="black")[0]
    lines.append(lobj)

heat = heatmap(car_histories)

posx = np.array(heat[0])
posy = np.array(heat[1])
k = kde.gaussian_kde((posx,posy))
pmin=-6000
pmax=6000
step=80
offset = int(((pmax - pmin) / step) / 2)
xi, yi = np.mgrid[pmin:pmax:step,pmin:pmax:step]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))

heatmap = history_to_heat_map(car_histories)
heat_map = heatmap / np.max(heatmap)
heat_map = np.vectorize(lambda x: x**0.5)(heat_map)

axs["C"].pcolormesh(xi, yi, zi.reshape(xi.shape), shading="gouraud", cmap="magma")

axs["B"].pcolor(xi, yi, heat_map, cmap='seismic')
axs["B"].set_xlabel(player_nam[1])
def init():
    for line in lines:
        if line is not lines[0]:
            line.set_data([], [])
    return lines


def update(frame):
    timer = time.time() - start
    xxx, yyy = grapher(car_histories, timer - 1, timer)
    for lnum, line in enumerate(lines):
        if lnum is not 0:
            line.set_data(xxx[lnum - 1], yyy[lnum - 1])
    return lines


start = time.time()
anim = FuncAnimation(fig, update, init_func=init, interval=25, blit=True)
plt.show()