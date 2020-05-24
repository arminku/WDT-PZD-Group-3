#Projekt 2 - Analyse Corona-Zahlen

import pandas as pd
import numpy as np
import datetime
import itertools
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

URL_CORONA_INFECTED = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_confirmed_global.csv"
URL_CORONA_RECOVER = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_recovered_global.csv"
URL_CORONA_DEATHS = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" + \
                      "csse_covid_19_data/csse_covid_19_time_series/" + \
                      "time_series_covid19_deaths_global.csv"

class Corona:
    def __init__(self):
        self.inf = pd.read_csv(URL_CORONA_INFECTED)
        self.rec = pd.read_csv(URL_CORONA_RECOVER)
        self.dt = pd.read_csv(URL_CORONA_DEATHS)   
        self.col = list(self.inf.columns.values)        
        
    def prep(self, df: pd.DataFrame, country: str, state: str) -> pd.DataFrame:
        df = df.loc[df[self.col[1]] == country]
        df = df.groupby([self.col[1]]).sum() if state == "total" else df.loc[df[self.col[0]] == state]
        return df

    def total(self, df: pd.DataFrame) -> int:
        return df.iloc[0,-1]

    def today(self, df: pd.DataFrame) -> int:
        return df.iloc[0,-1] - df.iloc[0,-2]

    def meanTotal(self, df: pd.DataFrame) -> int:
        return int(df.iloc[0,-1] / (len(list(df.columns.values)) - 4))

    def meanWeek(self, df: pd.DataFrame) -> int:
        return int((df.iloc[0,-1] - df.iloc[0,-7])/ 7)

    def daysAbove(self, inf: pd.DataFrame, treshold: int) -> int:
        c = 0
        for index in range(4,len(list(inf.columns.values))-1):
            diff = inf.iloc[0,index+1] - inf.iloc[0,index]
            if diff > treshold:
                c+= 1
        return c

    def daysAboveWeek(self, inf: pd.DataFrame, treshold: int) -> int:
        c = 0
        for index in range(-2,-9,-1):
            diff = inf.iloc[0,index+1] - inf.iloc[0,index]
            if diff > treshold:
                c+=1
        return c

    def currentlyIll(self, inf: pd.DataFrame, rec: pd.DataFrame, dt: pd.DataFrame) -> int:
        return inf.iloc[0,-1] - rec.iloc[0,-1] - dt.iloc[0,-1]

    def meanIllWeek(self, inf: pd.DataFrame, rec: pd.DataFrame, dt: pd.DataFrame) -> int:
        inf = inf.iloc[:,-7:]
        rec = rec.iloc[:,-7:]
        dt = dt.iloc[:,-7:]
        ill = inf - rec- dt
        return(int(ill.mean(axis=1)))
        
    def maxIll(self, inf: pd.DataFrame, rec: pd.DataFrame, dt: pd.DataFrame) -> int:
        ill = inf.iloc[:,4:] - rec.iloc[:,4:] - dt.iloc[:,4:]
        return int(max(ill.iloc[0,:]))       

    def zwischenlinie(self):
        print("|\n", end="")
        print("".join(c for c in itertools.repeat("-", 94)))

    def print_statistics(self, country: str, state: str, treshold = 1000):

        #vielleicht alles als Klasse implementieren und dann inf, rec, dt, col als Attribute (so muss nur beim Start einmal initialisiert werden)

        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        
        title = "Information for " + country + " - " + state + " (" + str(datetime.date.today()) + ")"
        print("".join(c for c in itertools.repeat("#", len(title) +6)))
        print("# ", title, " #")
        print("".join(c for c in itertools.repeat("#", len(title) +6)))
        
        frames = {"Infected": inf, "Recovered": rec, "Deaths": dt}
        breite = 30
        
        #Total
        for data in frames:
            anzZus = breite - len(data) - 4*len(" ") - len("Total:") - len(str(self.total(frames[data])))
            zusatz = "".join(c for c in itertools.repeat(" ", anzZus))
            loes = "| Total " + data + ": " + zusatz + str(self.total(frames[data])) 
            print(loes, end=" ")
        self.zwischenlinie()
        #today, mean, week
        for data in frames:
            anzZus = breite - len(data) - 4*len(" ") - len("Today:") - len(str(self.today(frames[data])))
            zusatz = "".join(c for c in itertools.repeat(" ", anzZus))
            loes = "| " +  data + " Today: " + zusatz + str(self.today(frames[data]))
            print(loes, end=" ")
        print("|\n", end="")
        for data in frames:
            anzZus = breite - len(data) - 3*len(" ") - len("Mean Total:") - len(str(self.meanTotal(frames[data])))
            zusatz = "".join(c for c in itertools.repeat(" ", anzZus))
            loes = "| " + data + " Mean Total:" + zusatz + str(self.meanTotal(frames[data]))
            print(loes, end=" ")
        print("|\n", end="")
        for data in frames:
            anzZus = breite - len(data) - 3*len(" ") - len("Mean Week:") - len(str(self.meanWeek(frames[data])))
            zusatz = "".join(c for c in itertools.repeat(" ", anzZus))
            loes = "| " + data + " Mean Week:" + zusatz + str(self.meanWeek(frames[data]))
            print(loes, end=" ")
        self.zwischenlinie()
        
        #currently Ill
        print("| Currently Ill: %13d | Mean Ill Week: %13d | Maximum Ill: %15d |" 
              % (self.currentlyIll(inf, rec, dt), self.meanIllWeek(inf, rec, dt), self.maxIll(inf,rec,dt)))
        print("| Treshold: %18d | Days Above: %16d | Days Above Week: %11d" % (treshold,  
              self.daysAbove(inf, treshold), self.daysAboveWeek(inf, treshold)), end=" ")
        self.zwischenlinie()        
        
    def plot_data(self,country: str, state: str, log: bool, ticks = 20):
        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        col = list(inf.iloc[:,4:].columns.values)
        plt.title(str("Corona in " + country + " - " + state))
        plt.xticks(range(0,len(col),ticks), col[::ticks])
        if log == True: plt.yscale("log")
        plt.plot(col, inf.loc[country][4:], "r", label ="Infected")
        plt.plot(col, rec.loc[country][4:], "g", label = "Recovered")
        plt.plot(col, dt.loc[country][4:], "k", label ="Deaths")
        plt.legend(loc="best")
        plt.show()
     
    def plot_current_infected(self, country: str, state: str, log: bool, ticks = 24):
        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        ill = inf.iloc[:,4:] - rec.iloc[:,4:] - dt.iloc[:,4:]
        col = inf.iloc[:,4:].columns.values
        plt.title(str("Corona in " + country + " - " + state))
        if log == True: plt.yscale("log")
        plt.xticks(range(0,len(col),ticks), col[::ticks])
        plt.plot(col, ill.loc[country], "k", label ="Currently Infected")
        plt.legend(loc="best")
        plt.show()
      
    def plot_diff(self, country: str, state: str, log: bool, ticks=24):
        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        diffInf = []
        diffRec = []
        diffDt = []
        col = inf.iloc[:,3:].columns.values
        for index in range(0,len(col)):
            diffInf.append(inf.iloc[0,index+3] - inf.iloc[0,index+2])
            diffRec.append(rec.iloc[0,index+3] - rec.iloc[0,index+2])
            diffDt.append(dt.iloc[0,index+3] - dt.iloc[0,index+2])
        if log == True: plt.yscale("log")
        plt.title(str("Corona in " + country + " - " + state))
        plt.xticks(range(0,len(col), ticks), col[::ticks])
        plt.plot(col, diffInf, "r", label="Infected")
        plt.plot(col, diffRec, "g", label ="Recovered")
        plt.plot(col, diffDt, "k", label ="Deaths")
        plt.legend(loc="best")
        plt.show()
    
    def plot_above_treshold(self, country: str, state: str, log: bool,treshold=1000, ticks=24):
        inf = self.prep(self.inf, country, state)
        col = inf.iloc[:,5:].columns.values
        diffInf = np.zeros(len(col))
        for index in range(0,len(col)):
            diffInf[index] = inf.iloc[0,index+5] - inf.iloc[0,index+4]
        infAbove = diffInf > treshold
        if log == True: plt.yscale("log")
        plt.xticks(range(0,len(col),ticks), col[::ticks])
        plt.plot(col, diffInf, "y", label="Infected")
        #keine schöne Lösung
        for index in range(0,len(infAbove)):
            if infAbove[index] == True:
                plt.axvspan(index, index+1, facecolor = "r", alpha=0.2)
                #hier vielleicht fill_betweenx verwenden
        plt.legend(loc="best")
        plt.show()
    
    def print_reProdZahl(self, country: str, state: str):
        inf = self.prep(self.inf, country, state)
        diffInf = np.zeros((14))
        for index in range(-17,-3):
            diffInf[index+17] = inf.iloc[0,index+1] - inf.iloc[0,index]
        diffInf.reshape(2,7).sum(axis=1)
        print("Reproduktionszahl", country, "-", state, datetime.date.today(), ":", round(diffInf[0] / diffInf[1],2))

    def globalTotal(self):
        print("Total Infected:\t\t%10d" % self.inf[self.col[-1]].sum())
        print("Total Recovered:\t%10d" % self.rec[self.col[-1]].sum())
        print("Total Deaths:\t\t%10d" % self.dt[self.col[-1]].sum())
        
def main():
    c = Corona()
    c.print_statistics("Russia", "total")
    #c.plot_data("Germany", "total", True)
    #c.plot_current_infected("Spain", "total", False)
    #c.plot_diff("Germany", "total", True)
    c.print_reProdZahl("Germany", "total")
    #c.plot_above_treshold("Germany", "total", True)
    c.globalTotal()

if __name__ == "__main__":
    main()