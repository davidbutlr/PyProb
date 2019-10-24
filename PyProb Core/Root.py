from tkinter import *
from typing import Any
import Grapher as gg
import Extraneous_Interface as ts
import tkinter.filedialog as tkfiledialog
import re
import prb_reader as pr
import Edit_Curve
import pyperclip
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


# On Linux, pyperclip (the copy and paste module)  makes use of the xclip or xsel commands,
# which should come with the os. Otherwise run “sudo apt-get install xclip” or “sudo apt-get install xsel”
# (Note: xsel does not always seem to work.)

# I pass this folder through to the subsequent windows by putting it into the rp parameters in their __init__s
class RootPane:

    def __init__(self, master, filename='', title='PyProb v0.8.0'):
        # Nice __init__ values
        print("Root Pane")
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        # master is the root pane that you want to put the window in
        self.master = master
        self.master.wm_title(title)  # window title
        self.master.wm_state('zoomed')  # this snaps the window into the full screen
        self.editcurves = list()
        self.editwins = list()
        self.filename = filename
        self.grapher = gg.Grapher(filename)
        self.master.geometry("%dx%d+0+0" % (w, h))
        self.menubar = Menu(master)
        self.canvas = None
        self.lined = dict()
        self.titles = False
        self.edit_pane = False
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)

        # File Dropdown
        #   This same structure is repeated throughout this codebase. These are the dropdown menus
        #   They hold single buttons that are the items in the dropdown menus. Each of those buttons have a command.
        #   I have used the filler function donothing() to have the buttons that don't have functionality yet.
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.NewFile)
        self.filemenu.add_command(label="Open", command=self.OpenFile)
        self.filemenu.add_command(label="Close", command=lambda: self.master.destroy())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save", command=self.SaveFile)
        self.filemenu.add_command(label="Save As", command=self.SaveFileAs)
        self.filemenu.add_separator()
        # self.filemenu.add_command(label="Print", command=self.donothing)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label="Recent Files", command=self.donothing)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label="Revert to Saved", command=self.donothing)
        self.filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Graph Dropdown
        self.graphmenu = Menu(self.menubar, tearoff=0)
        # self.graphmenu.add_command(label="Axis Setup", command=self.donothing)
        # self.graphmenu.add_command(label="Legend Setup", command=self.donothing)
        self.graphmenu.add_command(label="Titles", command=self.TitleMenu)
        # self.graphmenu.add_command(label="Distribution Type", command=self.donothing)
        # self.graphmenu.add_command(label="Edit Lines", command=self.donothing)
        # self.graphmenu.add_command(label="Global Font", command=self.donothing)
        self.graphmenu.add_separator()
        self.graphmenu.add_command(label="Save PNG File", command=self.savePNG)
        # self.graphmenu.add_command(label="Copy PNG File", command=self.donothing)
        # self.graphmenu.add_command(label="Copy Summary Table", command=self.donothing)
        # self.graphmenu.add_separator()
        # self.graphmenu.add_command(label="Sigma Calculator", command=self.donothing)
        self.menubar.add_cascade(label="Graph", menu=self.graphmenu)

        # Curve Dropdown
        self.curvemenu = Menu(self.menubar, tearoff=0)
        self.curvemenu.add_command(label="Edit Curve", command=self.showEditCurve)
        # self.curvemenu.add_command(label="Delete Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Make Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Setup", command=self.donothing)
        # self.curvemenu.add_command(label="Flip Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Combine Curves", command=self.donothing)
        # self.curvemenu.add_command(label="Convolve Curves", command=self.donothing)
        # self.curvemenu.add_command(label="Cumulate Curve", command=self.donothing)
        self.curvemenu.add_separator()
        # self.curvemenu.add_command(label="copy_curve Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Cut Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Paste Curve", command=self.donothing)
        # self.curvemenu.add_command(label="Paste Special", command=self.donothing)
        # self.curvemenu.add_command(label="Paste Combine", command=self.donothing)
        self.menubar.add_cascade(label="Curves", menu=self.curvemenu)

        # Window Dropdown
        # self.winmenu = Menu(self.menubar, tearoff=0)
        # self.winmenu.add_command(label="Cut", command=self.donothing)
        # self.winmenu.add_command(label="Copy", command=self.donothing)
        # self.winmenu.add_command(label="Paste", command=self.donothing)
        # self.winmenu.add_command(label="Duplicate Line", command=self.donothing)
        # self.winmenu.add_command(label="Toggle Case", command=self.donothing)
        # self.menubar.add_cascade(label="Window", menu=self.winmenu)

        # Help Dropdown
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.donothing)
        # self.helpmenu.add_command(label="Dark Mode", command=self.donothing)
        # self.helpmenu.add_command(label="About", command=self.donothing)
        # self.helpmenu.add_command(label="Sigma Calculator", command=self.donothing)
        # self.helpmenu.add_separator()
        # self.helpmenu.add_command(label="Valar Morghulis", command=self.donothing)
        # self.helpmenu.add_command(label="Et Post Transitum", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        master.pack_propagate(0)
        master.config(menu=self.menubar)

    # Show():
    # Literally just shows the window and puts the plot inside of it. I don't know if there is a better way to do this
    def show(self):
        self.grapher.plot()
        leg = self.grapher.leg
        lines = self.grapher.curve_manager.curves
        self.canvas = FigureCanvasTkAgg(self.grapher.fig, master=self.master)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()
        self.canvas.mpl_connect('key_press_event', self.onKey)
        self.canvas.mpl_connect('pick_event', self.onpick)
        self.canvas.mpl_connect('button_press_event', self.onclick)

        self.master.mainloop()

        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(5)  # 5 pts tolerance make a top variable where you could change the tolerance on the picking function
            self.lined[legline] = origline

    ###
    # Interactivity Functions
    ###
    def onclick(self, event):
        # Every time that the user clicks on the graph this print statement runs telling where the click happened
        # and what kind of click it was
        try:
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
        except TypeError:
            print("outside axes")

    def onpick(self, event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        string = str(event.artist)
        print(string)
        title = re.search("\((.*?)\)", string).group(1)
        print(title)

        curve_to_edit = self.grapher.curve_manager.get_curve_by_title(title)
        if curve_to_edit not in self.editcurves:
            newEditPane = Edit_Curve.EditPane(curve_to_edit, self)
            newEditPane.show()
        else:
            print("Selected curve is already open")
        self.canvas.draw()

    # These are all of the events called by keys pressed on the keyboard
    # all you have to do to make a new event is make a new if statement in the
    # event.key == u'<insert shortcut>'  style and put the action afterwards
    def onKey(self, event):
        print(event.key)
        # keyboard shortcut to open the Title Menu
        if event.key == u't':
            tp = ts.TitlePane(self)
            tp.show()
        if event.key == u'L':
            positive = True
            for curve in self.grapher.curve_manager.curves:
                for data in curve.curve_data[0]:
                    if data < 0:
                        print("negative")
                        positive = False
            if self.grapher.log:
                self.grapher.scale = "linear"
                self.grapher.log = False
                positive = False
                print("linear")
            if positive:
                self.grapher.scale = "log"
                self.grapher.log = True
                print("log")

            self.grapher.leglines.clear()  # without this line the lines would be appended to the legend without deleting the old ones
            self.grapher.clear()  # this clears the whole axis and everything on it
            self.grapher.plot()  # This re-graphs the whole plot
            self.canvas.draw()  # this is what shows the newly drawn plot again

        # keyboard shortcut to save the current graph as a PNG
        if event.key == u'm':
            self.savePNG()

        # keyboard short cut for pasting a potential curve
        if event.key == u'ctrl+v':
            print("heres a paste for ya headtops")
            self.paste()

        # keyboard shortcut for making a New File
        if event.key == u'ctrl+n':
            self.NewFile()

        # keyboard shortcut for saving a file
        if event.key == u'ctrl+s':
            if self.filename == "":
                self.SaveFileAs()
            else:
                self.SaveFile()

        if event.key == u'ctrl+S':
            self.SaveFileAs()

        if event.key == u'E':
            self.showEditCurve()

    def close_window(self):
        for curve_window in self.editwins:
            curve_window.close_window()
        self.master.destroy()

    # Function that opens the Title Window
    def TitleMenu(self):
        if not self.titles:
            new_title_pane = ts.TitlePane(self)
            new_title_pane.show()
            self.titles = True

    def showEditCurve(self):
        if not self.edit_pane:
            new_title_pane = ts.EditAllPane(self)
            new_title_pane.show()
            self.edit_pane = True

    ###
    # File Menu Commands
    ###

    # OpenFile():
    # This function opens a file and displays the opened file in the same window
    def OpenFile(self, name=""):
        if len(name) < 1:
            name = tkfiledialog.askopenfilename(initialdir="C:/Desktop/",
                                                filetypes=(("WinProb Files", "*.prb"), ("All Files", "*.*")),
                                                title="Choose a file.")
        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            if len(self.filename) > 0:
                rp = RootPane(Tk(), name)
                rp.show()

                self.grapher.leglines.clear()
                self.grapher.clear()
                self.grapher.plot()
                self.canvas.draw()
            else:
                self.grapher = gg.Grapher(name)
                self.canvas.get_tk_widget().pack_forget()
                self.show()

        except Any:
            print("No file exists")

    # NewFile():
    # This function makes a new file and a new window every time the user preses the new file button
    def NewFile(self):
        print("new")
        try:
            rp = RootPane(Tk(), "")
            rp.show()
        except Any:
            print("No file exists")

    # SaveFile():
    # This function just writes the data contained in the curveManager into a text file, but names it a .prb file
    # This should actually work most of the time, but I have not tested it that thoroughly.
    def SaveFile(self):
        with open(self.filename, "w") as f:
            f.write(self.grapher.curve_manager.save())
            f.close()

    # SaveFileAs():
    # This function is basically just NewFile() + SaveFile(),
    # It simply writes the data into whatever file the user picks in the asksaveasfile dialog
    def SaveFileAs(self):
        print("save file as")
        f = tkfiledialog.asksaveasfile(mode='w', defaultextension=".prb",
                                       initialdir="C:/Desktop/",
                                       filetypes=(("WinProb Files", "*.prb"), ("All Files", "*.*")),
                                       title="Choose a file.")
        try:
            f.write(self.grapher.curve_manager.save())
            f.close()
        except Any:
            print("Not a single valid file, *sigh*")

    ###
    # PNG Commands
    ###
    # I can easily put the png of the graph into a directory of the users choosing, but to have direct access to the
    # system clipboard on any machine is a lot harder because a dev would need to know how many bits the
    # image would take and how many are the image and what's metadata, so someone smarter than I might have to implement
    # such a feature
    def savePNG(self):
        title = self.grapher.curve_manager.title
        plot = self.grapher.fig.savefig(("%s.png" % title[:-1]))
        f = tkfiledialog.asksaveasfile(defaultextension=".png",
                                       initialdir="C:/Desktop/",
                                       filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")),
                                       title="Choose a file.")
        f.write(plot)
        f.close()

    # This is a very streamlined version of the initial prb_reader.read_prb() function
    def paste(self):
        # this is whatever the user wanted to paste
        string = pyperclip.paste()
        # these aren't necessary here because their first use isn't until 329 but it makes reading the code easier
        xnum = 0
        pnum = 0
        # whether or not the reader is reading rawCurve data
        raw = False
        # the actual values
        xdata = []
        # the amount of times they occur
        pdata = []
        # This is the full line by line array of the document.
        arr = []
        # this is the settings dictionary.
        settings = dict()
        # open the file and read line by line and separate the values by spaces

        for line in string.split("\n"):
            arr.append(line.split())

        if arr:
            # there is no way to tell when you're at the end of the .prb , so I add an eof to the data
            arr.append(["END"] if len(arr[-1]) == 1 else ["END", "OF FILE"])

        for x in arr:
            # as long as what we're reading isn't the end of the file or another curve's data,
            # please put that data into the current curve's curve_data attribute
            print(x)
            if x and x[0] != "RawCurve":
                # print("this aint no rawcurve")
                if x[0] != "END" and x[-1] != 'OF FILE' and x[0].isdigit() and x[-1].isdigit():
                    # print("it aint the end either")
                    if len(x) > 1:
                        xnum, pnum = (float(x[0]), float(x[1]))
                    else:
                        xnum = float(x[0])

                    try:
                        xdata.append(xnum)
                        if len(x) > 1:
                            pdata.append(pnum)
                    except ValueError:
                        print(str(x) + " is not a valid float")

                if x[0] == "END":
                    print("this is the end")
                    xdata.sort()
                    pdata.sort()
                    n = xdata
                    p = pdata
                    # Debug statements
                    # print(n)
                    # print(p)
                    # print("n")
                    # for u in n:
                    #     print(u)
                    # print("p")
                    # for u in p:
                    #     print(u)
                    newCurve = pr.Curve(s="Excel Data", cd=[n, p])
                    self.grapher.curve_manager.curves.append(newCurve)
                    print(self.grapher.curve_manager.get_curve_by_index(-1).testing_string())
                    self.grapher.leglines.clear()
                    self.grapher.clear()
                    self.grapher.plot()
                    self.canvas.draw()

    ###
    # Legend Direction Functions
    ###

    # The legend is drawn in the order that the curves are in the curvemanager,
    # so these functions just manipulate the curves list in the curvemanager,
    # clear the legend and then re-make the legend.
    def up(self, title):
        temp_leglines = self.grapher.curve_manager.curves

        # print("This the first leglines")
        # print(temp_leglines)

        length = len(temp_leglines)
        index = self.grapher.get_legline_index(title)
        # print("(length, index): " + str((length, index)))

        if length > 1 and index > 0:
            # print("if was true")
            temp_leglines[index-1], temp_leglines[index] = temp_leglines[index], temp_leglines[index-1]

        # print("This is the after one")
        # print(temp_leglines)

        self.grapher.leglines.clear()
        self.grapher.clear()
        self.grapher.curve_manager.curves = temp_leglines
        self.grapher.plot()
        self.canvas.draw()

    def down(self, title):
        temp_leglines = self.grapher.curve_manager.curves

        # print("This the first leglines")
        # print(temp_leglines)

        length = len(temp_leglines)
        index = self.grapher.get_legline_index(title)
        # print("(length, index): " + str((length, index)))

        if length > 1 and index < (length - 1):
            # print("if was true")
            temp_leglines[index+1], temp_leglines[index] = temp_leglines[index], temp_leglines[index+1]

        # print("This is the after one")
        # print(temp_leglines)

        self.grapher.leglines.clear()
        self.grapher.clear()
        self.grapher.curve_manager.curves = temp_leglines
        self.grapher.plot()
        self.canvas.draw()

    def top(self, title):
        temp_leglines = self.grapher.curve_manager.curves

        # print("This the first leglines")
        # print(temp_leglines)

        length = len(temp_leglines)
        index = self.grapher.get_legline_index(title)
        # print("(length, index): " + str((length, index)))

        if length > 1 and index > 0:
            # print("if was true")
            temp_leglines[0], temp_leglines[index] = temp_leglines[index], temp_leglines[0]

        # print("This is the after one")
        # print(temp_leglines)

        self.grapher.leglines.clear()
        self.grapher.clear()
        self.grapher.curve_manager.curves = temp_leglines
        self.grapher.plot()
        self.canvas.draw()

    def bottom(self, title):
        # print(self.grapher.cm.curves)
        temp_leglines = self.grapher.curve_manager.curves

        # print("This the first leglines")
        # print(temp_leglines)

        length = len(temp_leglines)
        index = self.grapher.get_legline_index(title)
        # print("(length, index): " + str((length, index)))

        if length > 1 and index < (length - 1):
            # print("if was true")
            temp_leglines[length-1], temp_leglines[index] = temp_leglines[index], temp_leglines[length-1]

        # print("This is the after one")
        # print(temp_leglines)

        self.grapher.leglines.clear()
        self.grapher.clear()
        self.grapher.curve_manager.curves = temp_leglines
        self.grapher.plot()
        self.canvas.draw()

    # def CopyPNG(self):
    #
    #     system = sys.platform
    #     if system is "win32":
    #         filename_format = win32clipboard.RegisterClipboardFormat('FileName')
    #         win32clipboard.OpenClipboard()
    #         win32clipboard.EmptyClipboard()
    #         win32clipboard.SetClipboardData(clip_type, data)
    #         win32clipboard.CloseClipboard()

    # Filler Function
    def donothing(self):
        x = 0









