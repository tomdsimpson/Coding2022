# Finding rides of a certain route by length
# Plotting speed over time

import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def read_data(file_path):

    dates = []
    speeds = []

    with open(file_path, "r") as file:
        f = csv.reader(file)

        for counter, line in enumerate(f):

            if counter > 500 and counter < 582:
                if line[3] == "Ride":
                    dates.append(line[1])
                    speeds.append(round(float(line[18]), 1))

    return dates, speeds


def convert_date(dates):

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    new_dates = []

    for x in dates:
        newString = ""
        x = x.split(" ")
        newString += x[2].strip(",") #Year
        newString += "-"
        month =  months.index(x[0])+1
        if month < 10:
            newString += ("0" + str(month))
        else:
            newString += str(month)
        newString += "-"
        newString += x[1].strip(",")

        new_dates.append(newString)
        print(new_dates[0:2])

    return new_dates



def plot_graph(dates, speeds):

    plt.plot(dates, speeds)
    plt.tick_params(labelrotation=90)


    myPlot = plt.gca()

    myPlot.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    myPlot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.show()

dates, speeds = read_data("activities.csv")
dates = convert_date(dates)
plot_graph(dates, speeds)










#Dec 10, 2021, 4:16:12 PM
