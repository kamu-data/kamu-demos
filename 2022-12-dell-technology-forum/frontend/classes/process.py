import time

import numpy as np
from IPython import display
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import gaussian_kde as kde

from typing import List
import pandas as pd



class PreProcess:

    def __init__(self):
        self.player_ids = {}
        self.player_nam = {}
        self.vip = "KrabbyPattie"
        self.teamnr = 0
        self.teamord = {}
        self.timex = []
        self.ballids = []
        self.k = 0
        self.player_int = []


    def get_paths(self,replay):
        actor_positions, actor_boosts = {}, {}
        io = 1
        jo = 3
        for i in range(6):
            self.teamord[i] = []
        # this first loop gathers the player names into a dict, and makes a dict for the ids of each player(see below)
        for index, names in enumerate(
                replay["properties"]["PlayerStats"]):
            if names["Name"] == self.vip:
                self.k = index
                self.teamnr = names["Team"]
                self.teamord[0] = str(names["Name"])
        for index, names in enumerate(
                replay["properties"]["PlayerStats"]):
            self.player_ids[index] = []

            self.player_nam[index] = []

            if names["Team"] == self.teamnr and self.k != index:
                self.teamord[io] = str(names["Name"])
                #             print(str(names["value"]["Name"]["value"]["str"]))
                io += 1
            else:
                if self.k != index:
                    self.teamord[jo] = str(names["Name"])
                    #                 print(str(names["value"]["Name"]["value"]["str"]))
                    jo += 1

        #     print(teamord)
        self.player_ids[6] = []
        self.player_nam[6] = []
        # print(self.player_ids)
        # the extracted json uses "frames" to denote new information. not sure if a frame is made every x ms, or made when new info is needed
        for frame in replay["network_frames"]["frames"][:]:
            if len(frame["new_actors"]) > 0:

                for replication in frame["new_actors"]:
                    # every frame has an actor id; data tied to that actor id. can be a car, ball, boost pads etc..
                    actor_id = replication["actor_id"]
                    # frames have spawned and update types. both can be in a single frame.

                    if actor_id not in actor_positions:
                        # find a frame for which the spawn tag is for a car
                        if replay["objects"][replication["object_id"]] == "Archetypes.Car.Car_Default":
                            # initiate a empty array for the corresponding actor id.
                            actor_positions[actor_id] = []
                        try:
                            loc = replication["initial_trajectory"]["location"]
                            actor_positions[actor_id].append({"time": frame["time"], "x": loc["x"], "y": loc["y"]})
                        except:
                            pass

                        if replay["objects"][replication["object_id"]] == "Archetypes.Ball.Ball_Default":
                            actor_positions[actor_id] = []
                            actor_boosts[actor_id] = []
                            self.player_ids[6].append(actor_id)
            if len(frame["updated_actors"]) > 0:
                for replication in frame["updated_actors"]:
                    actor_id = replication["actor_id"]
                        # sometimes, new actor ids are spawned for the same player, here we find a frame with that info
                        # and then put all actor ids of each specific player into their corresponding array.

                    if replay["objects"][replication["object_id"]] == "Engine.Pawn:PlayerReplicationInfo":
                        if replication["attribute"]["ActiveActor"]["actor"] not in self.player_int:
                            # get the player identifier. this is different than an actor id.
                            self.player_int.append(replication["attribute"]["ActiveActor"]["actor"])
                        # here we use the array generated at the top to store the multiple "car ids" of each player

                    # finally, find the xyz data and add that to a dict for each "car id".
                    # the list we just made above is used later in the code to connect all the xyz data for each player together
                    if replay["objects"][replication["object_id"]] == "TAGame.RBActor_TA:ReplicatedRBState" and actor_id in actor_positions:
                        rigid_body_location = replication["attribute"]["RigidBody"]["location"]

                        # append to name positions

                        actor_positions[actor_id].append(
                            {"time": frame["time"], "x": (rigid_body_location["x"]),
                             "y": (rigid_body_location["y"])})
        for frame in replay["network_frames"]["frames"][:]:
            if len(frame["updated_actors"]) > 0:
                for replication in frame["updated_actors"]:
                    actor_id = replication["actor_id"]

                    if replay["objects"][replication["object_id"]] == "Engine.PlayerReplicationInfo:PlayerName":
                        for op in range(len(self.player_int)):
                            if actor_id == self.player_int[op]:
                                self.player_nam[op] = replication["attribute"]["String"]
                    if replay["objects"][replication["object_id"]] == "Engine.Pawn:PlayerReplicationInfo":
                        for op in range(len(self.player_int)):
                            if replication["attribute"]["ActiveActor"]["actor"] == self.player_int[op] and actor_id not in \
                                    self.player_ids[
                                        op]:
                                self.player_ids[op].append(actor_id)
        # print(actor_positions)
        return actor_positions, actor_boosts

    def car_positions_to_histories(self,positions: dict) -> List['dict']:
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

    def get_var(self):
        return self.teamord, self.player_ids,self.player_nam,self.teamnr,self.vip


class Visualize:

    def __init__(self):
        pass

    def heatmap(self,histories: List['dict'],player_ids):
        xs, ys = [], []
        for index3, history in enumerate(histories):
            if history["actor_id"] in player_ids[1]:
                for px, py in zip(history["xs"], history["ys"]):
                    xs.append((px * -1))
                    ys.append(py)

        return xs, ys

    def history_to_heat_map(self,histories: List['dict'],player_ids,xi,step,offset) -> np.ndarray:

        heat_map = np.zeros(xi.shape)

        for history in histories:
            if history["actor_id"] in player_ids[1]:
                for px, py in zip(history["xs"], history["ys"]):
                    pxi = int((px * -1) / step) + offset
                    pyi = int(py / step) + offset
                    heat_map[pxi, pyi] += 1

        return heat_map

    def vis(self,car_histories,scores,teamord,player_ids):
        fig, axs = plt.subplot_mosaic("BBBCCC;BBBCCC;BBBCCC")

        heat = self.heatmap(car_histories,player_ids)

        posx = np.array(heat[0])
        posy = np.array(heat[1])
        k = kde((posx, posy))
        pmin = -6000
        pmax = 6000
        step = 80
        offset = int(((pmax - pmin) / step) / 2)
        xi, yi = np.mgrid[pmin:pmax:step, pmin:pmax:step]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))


        heatmap = self.history_to_heat_map(car_histories,player_ids,xi,step,offset)
        heat_map = heatmap / np.max(heatmap)
        heat_map = np.vectorize(lambda x: x ** 0.5)(heat_map)

        poti = axs["C"].pcolormesh(xi, yi, zi.reshape(xi.shape), shading="gouraud", cmap="magma")
        # plt.show()

        pot = axs["B"].pcolor(xi, yi, heat_map, cmap='seismic')
        fig.colorbar(pot)
        axs["B"].set_xlabel("X dimension in cm")
        axs["B"].set_ylabel("Y dimension in cm")
        axs["B"].title.set_text("Raw dens of loc")

        extent = axs["C"].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig("heatmap.png", bbox_inches=extent, dpi=600)

        axs["C"].set_xlabel("X dimension in cm")
        axs["C"].set_ylabel("Y dimension in cm")
        axs["C"].title.set_text("GB dens of loc")
        axs["C"].axis("off")
        fig.colorbar(poti)

        plt.tight_layout()
        plt.show()
        plt.close()

class Video:
    from matplotlib import pyplot as plt

    def __init__(self, car_histories,player_nam,teamord,player_ids,vip,teamnr):
        self.car_histories = car_histories
        self.player_nam = player_nam
        self.teamord = teamord
        self.player_ids = player_ids
        self.vip = vip
        self.teamnr = teamnr
        self.fps = 0
        self.speedup = 0
        self.lines = []


    def init(self):
        for line in self.lines:
            if line is not self.lines[0]:
                line.set_data([], [])
        return self.lines

    def update(self,frame):

        t_trail = 2
        t_end = float(frame) / self.fps * self.speedup
        t_start = t_end - t_trail
        xxx, yyy = self.grapher(self.car_histories, t_start, t_end)

        for lnum, line in enumerate(self.lines):
            if lnum != 0:
                line.set_data(xxx[lnum - 1], yyy[lnum - 1])

        return self.lines

    def grapher(self,histories: List['dict'], start, end):
        index11 = 0
        xs = {}
        ys = {}



        for a in range(len(self.player_nam)):
            xs[a] = []
            ys[a] = []
        for k in range(len(self.player_nam)):

            if self.vip == self.player_nam[k]:
                index11 = k

        indexx = 0
        for l in range(len(self.player_nam)):
            if index11 != l:
                #             if l == 6:
                indexx += 1
                for index3, history in enumerate(histories):
                    if history["actor_id"] in self.player_ids[l]:
                        for px, py, timeg in zip(history["xs"], history["ys"], history["times"]):
                            if start < timeg < end:
                                xs[indexx].append((px * -1))
                                ys[indexx].append(py)

            else:
                for index3, history in enumerate(histories):
                    if history["actor_id"] in self.player_ids[l]:
                        for px, py, timeg in zip(history["xs"], history["ys"], history["times"]):
                            if start < timeg < end:
                                xs[0].append((px * -1))
                                ys[0].append(py)

        return xs, ys

    def vis(self):
        plt.xlim(-8000, 8000)
        plt.ylim(-8000, 8000)
        plt.autoscale()
        plt.axis("off")

        fig, axs = plt.subplot_mosaic("A")

        img = plt.imread("resources/simple-pitch.png")

        xxx = []
        yyy = []
        ln, = axs["A"].plot(xxx, yyy)


        for o in range(8):
            if o == 0:
                lobj = axs["A"].imshow(img, extent=[-4100, 4100, -6000, 6000])
            elif o == 1:
                lobj, = axs["A"].plot([], [], color="green")
            else:
                if self.teamnr == 0:
                    if self.player_nam[o - 1] == self.teamord[1] or self.player_nam[o - 1] == self.teamord[2]:
                        lobj = axs["A"].plot([], [], color="purple")[0]
                    elif o < 7:
                        lobj = axs["A"].plot([], [], color="red")[0]
                    else:
                        lobj = axs["A"].plot([], [], color="black")[0]
                else:
                    if self.player_nam[o - 1] == self.teamord[1] or self.player_nam[o - 1] == self.teamord[2]:
                        lobj = axs["A"].plot([], [], color="red")[0]
                    elif o < 7:
                        lobj = axs["A"].plot([], [], color="purple")[0]
                    else:
                        lobj = axs["A"].plot([], [], color="black")[0]
            self.lines.append(lobj)

        match_duration = int(max([ch['times'].max() for ch in self.car_histories]))
        speedup = 300.0 / 50
        clip_duration = match_duration / speedup
        fps = 12
        frames = int(clip_duration * fps)

        self.fps = fps
        self.speedup =speedup

        print(f"Rendering {match_duration} s match as {clip_duration} s clip ({speedup} X speed) of {frames} frames")
        start = time.time()
        anim = FuncAnimation(fig, self.update, init_func=self.init, frames=frames, interval=1000.0 / fps, blit=True)


        video = anim.to_html5_video()
        print(f"Rendering took {time.time() - start} s")
        html = display.HTML(video)
        display.display(html)
        plt.close()


