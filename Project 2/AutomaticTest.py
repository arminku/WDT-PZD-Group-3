from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

URL_CORONA_INFECTED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_confirmed_global.csv"

inf = pd.read_csv(URL_CORONA_INFECTED)
col = list(inf.columns.values)

index = count(start=4)
inf = inf.groupby(["Country/Region"]).mean() 
x = inf[col[3]]
y = inf[col[2]]

img = plt.imread("weltkarteV4.png")

def animate(i):
     if(next(index) < len(col)):
         maxWert = max(inf[col[next(index)]])
         minWert = min(inf[col[next(index)]])
         size = (inf[col[next(index)]] - minWert) / (maxWert - minWert)
         
         plt.cla()
         ax = plt.subplot()
         ax.imshow(img, extent=[-150,190,-60,100])
         plt.scatter(x,y,c="red", s= size*200, label = col[next(index)])
         plt.tight_layout()
         plt.legend(loc = "best")
        
ani = FuncAnimation(plt.gcf(), animate, interval=200)

plt.tight_layout()
plt.show()