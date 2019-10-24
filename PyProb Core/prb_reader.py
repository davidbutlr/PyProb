import statistics

from scipy.stats import norm
import math

# prb_reader: David Butler 7/30/2019
# This file is the part of the code that makes the pseudo-file .prb be read into
# all of the different objects that are needed to plot the data

# Curve Class 7/11/2019

# This is the Class definition for each of the Curves that are plotted onto the window.
# They are held in a CurveManager that manages the whole view of the graph
# Right now They have two cases for being read from the .prb:
# Either their data is one column list of data or two column list data
# and they have to handle for each of those cases naturally without direction from the user

colors = ["#ff0000", "#0F3FFF", "#36AA0E", "#EFA512", "#00FFFF",
          "#737373", "#3F1F09", "#FF00FF", "#FF6666", "#4CA6FF",
          "#7CF37C"]

markers = [ '\\alpha', '\\beta',
           '\gamma', '\sigma','\infty', '\spadesuit', '\heartsuit', '\diamondsuit', '\clubsuit',
           '\\bigodot', '\\bigotimes', '\\bigoplus', '\imath', '\\bowtie', '\\bigtriangleup',
           '\\bigtriangledown', '\oslash', '\\ast', '\\times', '\circ', '\\bullet', '\star', '+',
            '\Theta', '\Xi', '\Phi', '\$', '\#', '\%', '\S']


class Curve:
    # counter for the marker and number values
    i = 0

    # (xdata, pdata) is the convention for all of these data lists.
    # They are just an array of two arrays that are x (actual number values) and p
    # (either the number of points at or below that actual number value or the cdf probability value respectively
    def __init__(self, s="No Title", cd=None):
        # name that will be displayed in the legend
        self.title = s

        # the color and the marker are determined by the order in which the curves are drawn
        self.color = colors[Curve.i % len(colors)]
        self.marker = "$" + markers[Curve.i % len(markers)] + "$"  # matplotlib needs the $ to be able to read it
        self.display_marker = markers[Curve.i % len(markers)]
        Curve.i += 1

        # stat values
        self.mean = 0
        self.median = 0
        self.standard_deviation = 0

        # these are the variables that store the state of the aesthetic changes for the grapher to update
        self.show_mean = False
        self.show_median = False
        self.show_std_dev = False
        self.label_min = 0
        self.label_max = 0
        self.annotative_step = 1

        # This is the big array of string values that represent the numerical data that is read form the .prb
        self.curve_data = [] if cd is None else cd

        # percent_data is initialized after int_data because when we calculate our cdf
        # we are plugging the values into the second list of this array
        self.percent_data = []

    # make_percent():
    # The .prb file has the cumulative sum running up from whatever the starting frequency is, but we cant graph that.
    # So make_percent() takes the raw data and turns it into a makeshift cumulative distributive function data.
    def make_percent(self):
        # soon to be the holder of all of the cdf data
        percents = list()

        # Make a weighted distribution
        if self.curve_data[1]:
            for x in self.curve_data[1]:
                if not x == (self.curve_data[1][-1]):
                    percents.append(x/(self.curve_data[1][-1]))

            self.percent_data = [self.curve_data[0][:-1], percents]
        else:
            print("I had to make this")
            for i, x in enumerate(self.curve_data[0]):
                percents = norm.cdf(self.curve_data[0], statistics.mean(self.curve_data[0]), statistics.stdev(self.curve_data[0]))
                self.percent_data = [self.curve_data[0][:-1], percents.tolist()]

    # add_data():
    # puts as much data as you want into any curve you want. Forever.
    def add_data(self, data):
        if len(data) > 0:
            print("pass")
            for i in data:
                self.curve_data.append(i)
            # print(self.curve_data)

    # testing_string():
    # Mostly for testing and debugging. Just prints out the data and the title of the curve.
    def testing_string(self):
        return "Title: " + self.title + "\n\tColor: " + self.color + "\n\tMarker: " + self.marker

    # save():
    # this method is for writing to the .prb file that we're saving
    def save(self):
        string = "RawCurve\t %s\n" % self.title
        if self.curve_data[1]:
            for x, p in zip(self.curve_data[0], self.curve_data[1]):
                string += "%d\t%d\n" % (x, p)
        else:
            for x in self.curve_data[0]:
                string += "%d\n" % x
        return string

    # This function makes the mean out of the data in the curve object
    def make_mean(self):
        # check if the data is 1 or 2 dimensional
        two_d = bool(self.curve_data[1])
        # last value read
        prev = 0
        # sum
        sigma = 0
        # mean
        avg = 0

        if two_d:
            final_pvalue = self.curve_data[1][-1]
            for x, p in zip(self.curve_data[0], self.curve_data[1]):
                sigma += x * ((p-prev)/final_pvalue)
                avg = sigma/len(self.curve_data[0])
        else:
            for x in self.curve_data[0]:
                sigma += x
                avg = sigma/len(self.curve_data[0])
        # debug and calculatory check
        print("curve title: " + self.title)
        print("\tsigma: " + str(sigma))
        print("\tavg: " + str(avg))
        return avg

    # finds the median
    def make_median(self):
        two_d = bool(self.curve_data[1])
        median_index = 0
        if two_d:
            final_pvalue = self.curve_data[1][-1]
            rough_median_count = int(final_pvalue/2)

            for i, x in enumerate(self.curve_data[1]):
                if x > rough_median_count > self.curve_data[1][i - 1]:
                    print("\tmedian: " + str(self.curve_data[0][i]))
                    return self.curve_data[0][i]

    # finds the standard deviation
    def make_standard_deviation(self):
        two_d = bool(self.curve_data[1])
        prev = 0
        sigma = 0
        std_dev = 0

        if two_d:
            final_pvalue = self.curve_data[1][-1]
            for x, p in zip(self.curve_data[0], self.curve_data[1]):
                sigma += (((x * ((p - prev) / final_pvalue)) - self.mean) ** 2)
                variance = sigma / len(self.curve_data[0])
                std_dev = math.sqrt(variance)
        else:
            for x in self.curve_data[0]:
                sigma += (x - self.mean) ** 2
                variance = sigma / len(self.curve_data[0])
                std_dev = math.sqrt(variance)
        print("\tstd_dev: " + str(std_dev))
        return std_dev

    # runs all three functions at once
    def make_stats(self):
        self.mean = self.make_mean()
        self.median = self.make_median()
        self.standard_deviation = self.make_standard_deviation()




# Curve Manager Class 7/17/2019
# This is basically The handler for the curves and for the settings on this plot.
class CurveManager:
    def __init__(self, title="This is a Graph!"):
        # I got this list from Paul's code
        # These are in the code because I was a lot more ambitious when I wrote this code
        # But I do use the XLabel, YLabel, and Title
        self.settings = {'WinProb': 'WinProb', 'IsPercent': '1', 'IsLogNormal': '0', 'BoxGraph': '0', 'IsLegend': '1',
                         'IsSecondaryAxis': '0', 'IsLinesInLegend': '1', 'XMinorGrid': '0', 'XMin': '0', 'XMax': '0',
                         'XUnits': '1', 'ShowYAxisType': '1', 'SigmaMax': '5.000000', 'SigmaMin': '-2.000000',
                         'AutoSigmaMax': '1', 'AutoSigmaMin': '1', 'XTicks': '0', 'YTicks': '0', 'XTickNum': '10',
                         'XGrid': '1', 'YGrid': '1', 'ExtraYGrid': '1', 'ThickGrid': '0', 'XAutoMin': '1',
                         'XAutoMax': '1', 'UseExactValues': '0', 'IsSymbols': '1', 'IsLines': '1',
                         'ShowCurveNumber': '0', 'UseCharacterSymbols': '1', 'ShowFitPointX': '1', 'ShowFitText': '1',
                         'ShowN': '0', 'FitDigits': '3', 'YAxisRotate': '1', 'IsMono': '0', 'PinMedian': '0',
                         'PinPercent': '50.000000', 'ShowLegendBorder': '0', 'LegendSpan': '25',
                         'Memo': 'Intel Confidential', 'Date': '6/19/2019',
                         'DateLeader': '', 'ShowMemo': '1', 'ShowDate': '1', 'ShowFile': '1',
                         'TitleName': 'Arial', 'TitleColor': 'Black', 'TitleBold': '1', 'TitleItalic': '0',
                         'TitleSize': '24.000000', 'XAxisName': 'Arial', 'XAxisColor': 'Black',
                         'XAxisBold': '1', 'XAxisItalic': '0', 'XAxisSize': '8.000000', 'YAxisName': 'Arial',
                         'YAxisColor': 'Black', 'YAxisBold': '1', 'YAxisItalic': '0', 'YAxisSize': '8.000000',
                         'XLabelName': 'Arial', 'XLabelColor': 'Black', 'XLabelBold': '1', 'XLabelItalic': '0',
                         'XLabelSize': '14.000000', 'YLabelName': 'Arial', 'YLabelColor': 'Black', 'YLabelBold': '1',
                         'YLabelItalic': '0', 'YLabelSize': '14.000000', 'MemoName': 'Arial', 'MemoColor': 'Black',
                         'MemoBold': '0', 'MemoItalic': '1', 'MemoSize': '8.000000', 'LegendName': 'Arial',
                         'LegendColor': 'Black', 'LegendBold': '1', 'LegendItalic': '0', 'LegendSize': '10.000000',
                         'DateName': 'Arial', 'DateColor': 'Black', 'DateBold': '0', 'DateItalic': '1',
                         'DateSize': '8.000000', 'SymbolName': 'Arial', 'SymbolColor': 'Black', 'SymbolBold': '0',
                         'SymbolItalic': '0', 'SymbolSize': '15.000000', 'SymCharacters': '',
                         'SymbolStyles': '0,0,1', 'SymbolColors': '9,10,12', 'Title': 'This is a Graph!',
                         'XLabel': 'These are about to be data values, crazy', 'YLabel': '% of something',
                         'MltSctPnts': '1', 'InputMax': '9e+100', 'InputMin': '-9e+100', 'CrunchType': '1',
                         'Quantize': '0.000000'}
        self.title = title
        self.curves = list()

    # add_curve():
    # This function just appends the given curve to the big CurveManager List
    def add_curve(self, crve):
        self.curves.append(crve)
        # print("added curve. title: " + crve.title)

    # set_title():
    # self explanatory
    def set_title(self, title):
        self.title = title

    # get_curve_by_index():
    # returns the curve object at the given index
    def get_curve_by_index(self, i):
        return self.curves[i]

    # returns the curve with the same title as the parameter
    def get_curve_by_title(self, title):
        fetched_curve = None
        for curve in self.curves:
            if curve.title == title:
                fetched_curve = curve
        return fetched_curve

    # Prints all the curves in the array
    def print_all(self):
        print("Title: " + self.title)
        for l in self.curves:
            print(l.testing_string())

    # Makes all the stats for ever curve in the .curves list
    def make_all_stats(self):
        for curve in self.curves:
            curve.make_stats()

    # save():
    # this method is for writing to the .prb file that we're saving
    def save(self):
        string = ""
        for key, value in self.settings.items():
            string += "%s=%s\n" % (key, value)
        for curve in self.curves:
            string += curve.save()
        return string


class PrbReader:
    def __init__(self, filename):
        self.filename = filename

    # This is the Biggest function in this whole program. Probably the most complicated too,
    # but it reads the file that is passed to it's __init__.
    def read_prb(self):
        curve_manager = CurveManager()
        xnum = 0
        pnum = 0
        # whether or not the reader is reading rawCurve data
        raw = False
        # array for the actual values
        xdata = []
        # arrayt for the corresponding amount of times they occur
        pdata = []
        # This is document split line by line its lines are inner arrays and each word is an element in those inner.
        arr = []
        # this is the settings dictionary to be printed out as to allow backwards compatibility .
        settings = dict()

        if self.filename:
            # open the file and read line by line and separate the values by spaces
            with open(self.filename, "r") as f:
                for line in f:
                    # unless its the title
                    if "XLabel=" in line or "YLabel=" in line or "Title=" in line:
                        # we want everything past the '=' not just the first word
                        arr.append(line.split("="))
                    else:
                        arr.append(line.split())

                if arr:
                    # there is no way to tell when you're at the end of the .prb , so I add an eof to the data
                    arr.append(["END"] if len(arr[-1]) == 1 else ["END", "OF FILE"])

            for x in arr:
                # raw means if the parser has reached a "RawCurve" in the .prb
                # and it should start appending numbers to the temporary lists
                if not raw:
                    # If we didn't use this if statement,the parser would only record the first word of the title and
                    # the x and y labels
                    if x[0] == "XLabel" or x[0] == "YLabel" or x[0] == "Title":
                        # to make for code that can deal with the 1 or 2 dimensional data tables that a prb could have,
                        # we have to reference the 2nd value as the x[-1] as to avoid IndexOutOfBounds exceptions

                        settings[x[0]] = x[-1]  # appending each setting to be read later
                    else:
                        templist = x[0].split('=')
                        # print(templist)
                        settings[templist[0]] = templist[-1]
                if raw:
                    # as long as what we're reading isn't the end of the file or another curve's data,
                    # we're telling the program to please put that data into the current curve's curve_data attribute
                    if x[0] != "RawCurve" and x[0] != "END" and x[-1] != 'OF FILE':
                        # Paul has these tags in some of his files when he saves them,
                        # but they dont actualy show any of these things, so I skip them during the read
                        if x[0] != "ShowMean" and x[0] != "ShowMedian" and x[0] != "ShowStdev":
                            if len(x) > 1:
                                xnum, pnum = (float(x[0]), float(x[1]))
                            else:
                                xnum = float(x[0])
                            # This is where we turn the string read value into a number, but if its not a float
                            # then we catch the value error
                            try:
                                xdata.append(xnum)
                                if len(x) > 1:
                                    pdata.append(pnum)
                            except ValueError:
                                print(str(x) + " is not a valid float")
                    # If we DO get to the end,then we want to temp
                    if x[0] == "RawCurve" or x[0] == "END":
                        n = xdata
                        p = pdata
                        curve_manager.curves[-1].add_data((n, p))
                        # print(curve_manager.get_curve_by_index(-1).testing_string())
                        xdata = []
                        pdata = []
                        raw = False
                if x and not raw:
                    if x[0] == "RawCurve":
                        raw = True
                        t = x[1:]
                        title = ' '.join(word for word in t)
                        curve_manager.add_curve(Curve(title))
        if settings:
            curve_manager.settings = settings
            # print(curve_manager.settings)
            curve_manager.set_title(settings["Title"])
        curve_manager.make_all_stats()
        return curve_manager
