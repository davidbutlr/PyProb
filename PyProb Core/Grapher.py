import time
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle
import prb_reader as pr
import matplotlib.pyplot as plt
import statistics
from matplotlib.ticker import NullFormatter, StrMethodFormatter
from scipy.stats import norm
from matplotlib.lines import Line2D

X_SHIFT = .2  # This is how much the annotations are going to be moved to the Left after every graph.

class Grapher:

    def __init__(self, filename):
        # self.style = st

        # the file that is to be read
        self.filename = filename

        # this is how I'm going to change between linear and logarithmic
        self.log = False
        if self.log:
            self.scale = "log"
        else:
            self.scale = "linear"


        # the prb that will read from the file
        self.prb = pr.PrbReader(filename)
        self.curve_manager = self.prb.read_prb()  # corresponding curve manager

        # these are just plot preferences for the default plot
        self.fig, self.ax = plt.subplots()
        self.yticks = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]  # these don't actually affect the plot rn
        self.memo = self.curve_manager.settings['Memo']  # this isn't what I want
        self.leglines = list()  # these are the lines to be put on to the legend
        self.leg = None  # to be the holder of the legend
        self.annotating = False  # whether or not the grapher should be annotating
        self.annotation_list = dict()  # list of the lines that'll be annotated and the corresponding points to annotate
        self.ax.set_yscale("linear")  # on the beginning plot we don't want the stretched logit scale

    def plot(self):
        # Graph set up
        # style.use(self.style)
        self.ax.set_yticklabels(self.yticks, fontsize=10)
        plt.grid(True) if self.curve_manager.curves else plt.grid(True)
        plt.yticks(self.yticks)
        plt.yscale("logit")

        self.ax.yaxis.set_major_formatter(StrMethodFormatter('{x:0.6g}'))
        # self.ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        # self.ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter("%.6f"))
        self.ax.yaxis.set_minor_formatter(NullFormatter())
        self.ax.tick_params(axis='y', which='minor', labelsize=7)
        # self.ax.tick_params(axis='both', which='minor', labelsize=8)

        # The settings are attributes of the curve manager given to it by the prb reader,
        # so to get this information on the graph we have to consult that instance
        self.ax.set_title(self.curve_manager.title)
        self.ax.set_ylabel(self.curve_manager.settings["YLabel"])
        self.ax.set_xlabel(self.curve_manager.settings["XLabel"])
        plt.tight_layout()

        # if there is data in the CurveManager, then we want to graph that.

        start = time.time()
        if self.curve_manager.curves:
            print(self.curve_manager.print_all())
            i = 0
            # self.ax.set_yticks(self.yticks)
            for curve in self.curve_manager.curves:
                i += 1
                # This is checking if the data comes from a 1d array or a 2d
                if not curve.curve_data[1]:
                    ncurve = curve.curve_data[0]
                    # check this mean and standard deviation against Paul's for the 1d array because you were wrong
                    # when you did it
                    new_curve = Line2D(ncurve, norm.cdf(ncurve, statistics.mean(ncurve), statistics.stdev(ncurve)), color=curve.color,
                                       linestyle='solid', marker=curve.marker, label=curve.title, picker=5)
                    self.ax.plot(ncurve, norm.cdf(ncurve, statistics.mean(ncurve), statistics.stdev(ncurve)), color=curve.color,
                                 linestyle='solid', marker=curve.marker, label=curve.title, picker=5)
                else:
                    curve.make_percent()
                    new_curve = Line2D(curve.percent_data[0], curve.percent_data[1], color=curve.color,
                                       linestyle='solid', marker=curve.marker, label=curve.title, picker=5)
                    self.ax.plot(curve.percent_data[0], curve.percent_data[1], color=curve.color,
                                 linestyle='solid', marker=curve.marker, label=curve.title, picker=5)
                self.leglines.append(new_curve)

                if curve.show_mean:
                    self.leglines.append(Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0, label=("mean: %.2E" % curve.mean)))
                if curve.show_median:
                    self.leglines.append(Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0, label=("median: %d" % curve.median)))
                if curve.show_std_dev:
                    self.leglines.append(Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0, label=("std dev: %d" % curve.standard_deviation)))

        # otherwise we want to display the default new file screen and wait for data to be added or opened
        else:
            self.ax.set_xticks([-20, 0, 20, 40, 60, 80, 100, 120, 140])
        # Legend set up
        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        self.leg = self.ax.legend(handles=self.leglines, loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.1)
        stop = time.time() - start
        print(stop)
        self.ax.set_ylim(bottom=0, top=.999999)
        plt.xscale(self.scale)

        if self.scale == 'log':
            self.ax.xaxis.set_major_formatter(ticker.LogFormatter())
            # self.ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

        # To Label the points of the curve range
        if self.annotating:
            print(self.annotation_list)
            for key in self.annotation_list:
                index = self.get_legline_index(key)
                self.annotate_line(self.annotation_list[key][0], self.annotation_list[key][1],
                                   self.curve_manager.curves[index].annotative_step, self.curve_manager.curves[index])
            # print("big while is over")

    # Comments at the top
    def annotate_line(self, xlist, plist, step, curve):
        curve.make_stats()
        print(curve.standard_deviation)
        print("step: " + str(step))
        prev = 0
        prevx = 0
        prevy = 0
        for i, (x, y) in enumerate(zip(xlist, plist)):
            Y_SHIFT = .1 if y < .87 else 0.05
            if y + Y_SHIFT > 1:
                Y_SHIFT = 0
            X_SHIFT = .2
            # add one global top level X_SHIFT with a description of what each number in what that value means
            x_format = '(%.0f, %.5f)' % (x, y) if x > 1 or x < -1 or x == 0 else '(%.6f, %.5f)' % (x, y)
            print(x, x*X_SHIFT, x - (curve.mean * X_SHIFT))

            if len(curve.curve_data) < 40:
                if prevx != 0 and x / prevx < 1 and x / prevx != 0:
                    # print("this one")
                    Y_SHIFT /= 5
                if y + Y_SHIFT - prev < .04 and 0 < y < .5:
                    # print(x, y)
                    Y_SHIFT = .04 - (y - prev)
                elif y - prev < .02 and .5 < y < .6:
                    Y_SHIFT = .02 - (y - prev) if y + (.02 - (y - prev)) < .9 else 0
                    # print(x, y, y + Y_SHIFT)
            j = 0
            for allcurve in self.curve_manager.curves:
                if allcurve.curve_data[0][0] > x - (curve.mean * X_SHIFT):
                    j += 1
                    print(x)
            X_SHIFT *= -.5 if not j != len(self.curve_manager.curves) else 1
            print("special", x, x * X_SHIFT, x - (curve.standard_deviation * X_SHIFT))
            if x - prevx < 0:
                print("ok")

            if i > 0 and i % step == 0 and prevx != x:
                self.ax.annotate(x_format, xy=(x, y),
                                 xycoords='data', xytext=((x - (curve.standard_deviation * X_SHIFT)), (y + Y_SHIFT)),
                                 arrowprops=dict(arrowstyle='->',
                                                 color='blue',
                                                 lw=1,
                                                 ls='-'), fontsize=7)
            prevx = x
            prevy = y
            prev = y + Y_SHIFT
                # print("annotated")

    def clear(self):
        self.ax.cla()

    def get_legline_index(self, title):
        for i, curve in enumerate(self.curve_manager.curves):
            if curve.title == title:
                return i

