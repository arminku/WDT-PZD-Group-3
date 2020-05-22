import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import itertools

URL_CORONA_INFECTED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_confirmed_global.csv"
                      
inf = pd.read_csv(URL_CORONA_INFECTED)
inf = inf.groupby(["Country/Region"]).mean()
col = list(inf.columns.values)
index = itertools.count(start=4)

fig = plt.figure()
ax = plt.axes(xlim=(0,2), ylim=(-2,2))
x = inf[col[3]]
y = inf[col[2]]
point = ax.scatter(x, y)

def init():
    minWert = min(inf[col[4]])
    maxWert = max(inf[col[4]])
    size = (inf[col[4]] - minWert) / (maxWert - minWert)
    point.set_data(x,y,c="red", s=size)
    return point

def animate(i):
    if(next(index) < len(col)):
        minWert = min(inf[col[next(index)]])
        maxWert = max(inf[col[next(index)]])
        size = (inf[col[next(index)]] - minWert) / (maxWert - minWert)
        point.set_data(x,y, c="red", s=size)
        return point

anim = FuncAnimation(fig, animate, init_func = init, frames = 200, interval = 200, blit = True)

writer = animation.FFMpegWriter(fps=20, metadata = dict(artist='Me'), bitrate = 1800)

plt.show()
anim.save("basic_animationV2.mp4", writer=writer)