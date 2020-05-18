#Projekt 2 - Analyse Corona-Zahlen

import pandas as pd
import datetime
import time
import itertools
import matplotlib.pyplot as plt

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

    def meanTotal(self, df: pd.DataFrame) -> float:
        return df.iloc[0,-1] / (len(list(df.columns.values)) - 4)

    def meanWeek(self, df: pd.DataFrame) -> float:
        return (df.iloc[0,-1] - df.iloc[0,-7])/ 7

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
        total = 0
        inf = inf.iloc[:,-7:]
        rec = rec.iloc[:,-7:]
        dt = dt.iloc[:,-7:]
        ill = inf - rec- dt
        return(int(ill.mean(axis=1)))
        
    def maxIll(self, inf: pd.DataFrame, rec: pd.DataFrame, dt: pd.DataFrame) -> int:
        ill = inf.iloc[:,4:] - rec.iloc[:,4:] - dt.iloc[:,4:]
        return int(max(ill.iloc[0,:]))       

    def zwischenlinie(self):
        print("".join(c for c in itertools.repeat("-", 100)))

    def print_statistics(self, country: str, state: str, treshold = 1000):

        #vielleicht alles als Klasse implementieren und dann inf, rec, dt, col als Attribute (so muss nur beim Start einmal initialisiert werden)

        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        
        print("Abruf am:", datetime.date.today())
        title = "Information for " + country + " - " + state
        print("".join(c for c in itertools.repeat("#", len(title) +6)))
        print("# ", title, " #")
        print("".join(c for c in itertools.repeat("#", len(title) +6)))
        
        frames = {"Infected": inf, "Recovered": rec, "Deaths": dt}
        #Total
        for data in frames:
            print("| Total",data,":\t\t", self.total(frames[data]), end=" ")
        self.zwischenlinie()
        #today, mean, week
        for data in frames:
            print("|", data, "Today:\t\t", self.today(frames[data]), "\t", end="")
        print("\n", end="")
        for data in frames:
            print("|", data, "Mean Total:\t", int(self.meanTotal(frames[data])), "\t", end="")
        print("\n", end="")
        for data in frames:
            print("|", data, "Mean Week:\t", int(self.meanWeek(frames[data])), "\t", end="")
        self.zwischenlinie()
        
        #currently Ill
        print("| Currently Ill:\t\t", self.currentlyIll(inf, rec, dt), "\t| Mean Ill Week:\t\t", 
              self.meanIllWeek(inf, rec, dt), "\t| Maximum Ill:\t", self.maxIll(inf,rec,dt))
        print("| Treshold:\t\t\t\t", treshold, "\t| Days Above:\t\t\t", 
              self.daysAbove(inf, treshold), "\t| Days Above Week:", 
              self.daysAboveWeek(inf, treshold))
        self.zwischenlinie()

    def verlauf(self):
        
        #17-5-20: Funktioniert noch nicht wie gewünscht: Plot wird nicht aktualisiert
        
        #Längen- und Breitengrad auf gerade Werte bringen
        self.inf["Lat"] = self.inf["Lat"] - min(self.inf["Lat"])
        self.inf["Long"] = self.inf["Long"] - min(self.inf["Long"])
        #nach Ländern gruppiert und die Breiten- und Längengerade gemittelt
        self.inf = self.inf.groupby(["Country/Region"]).mean()
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        #1. Initialisierung:
        maxWert = max(self.inf[[4]])
        minWert = min(self.inf[[4]])
        self.inf[[4]] = (self.inf[[4]] - minWert) / (maxWert - minWert)
        x = self.inf[[2]]
        y = self.inf[[3]]
        ax.set_xlabel = "Breitengrad"
        ax.set_ylabel = "Längengrad"
        for index in range(4,len(self.col)):
            ax = fig.add_subplot(1,1,1)
            maxWert = max(self.inf[[index]])
            minWert = min(self.inf[[index]])
            #die jeweilige Spalte wird normiert
            self.inf[[index]] = (self.inf[[index]] - minWert)/(maxWert - minWert)
            ax.scatter(x, y, c = "red", s = self.inf[[index]]*100)
            plt.show()
            time.sleep(0.1)
            ax.remove()

    #Logarithmus: plt.xscale('log')    

    def plot_data(self,country: str, state: str, log: bool, ticks = 20):
        inf = self.prep(self.inf, country, state)
        rec = self.prep(self.rec, country, state)
        dt = self.prep(self.dt, country, state)
        col = list(inf.iloc[:,4:].columns.values)
        plt.title(str("Corona in " + country + " - " + state))
        plt.xticks(range(0,len(col),ticks), col[::ticks])
        if log == True: plt.yscale("log")
        plt.plot(col, inf.loc[country][4:], "r")
        plt.plot(col, rec.loc[country][4:], "g")
        plt.plot(col, dt.loc[country][4:], "k")
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
        plt.plot(col, ill.loc[country], "k")
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
        plt.plot(col, diffInf, "r")
        plt.plot(col, diffRec, "g")
        plt.plot(col, diffDt, "k")
        plt.show()
    
    def plot_above_treshold(self, country: str, state: str, log: bool,treshold=1000, ticks=24):
        #vermutlich fill_between
        pass

def main():
    c = Corona()
    c.print_statistics("Germany", "total")
    #c.verlauf()
    #test
    #test
    c.plot_data("Germany", "total", True)
    c.plot_current_infected("Spain", "total", False)
    c.plot_diff("Germany", "total", True)

if __name__ == "__main__":
    main()