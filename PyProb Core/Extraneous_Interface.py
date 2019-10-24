from tkinter import *
import Edit_Curve as EC


class TitlePane:
    def __init__(self, rp, master=None):
        print("Title Pane")
        master = Tk()
        self.master = master
        self.master.geometry("400x120")
        self.master.wm_title("Titles and Labels")
        self.menubar = Menu(self.master)
        self.master.resizable(0, 0)
        self.window = rp
        self.canvas = rp.canvas
        self.curvemanager = self.window.grapher.curve_manager

        self.master.protocol('WM_DELETE_WINDOW', self.close_window)

        # These are the entry boxes and Labels for the Edit Title Screen
        self.bigtitle = StringVar(self.master)
        self.bigtitle.set(self.curvemanager.title)  # sticky is the alignment and it is North East South West
        Label(self.master, text="Title:").grid(row=0, column=0, sticky=W, padx=12, pady=4)
        Entry(self.master, textvariable=self.bigtitle, width=45
              ).grid(row=0, column=1, columnspan=5, sticky=W, padx=12, pady=4)

        self.XAxis = StringVar(self.master)
        self.XAxis.set(self.curvemanager.settings["XLabel"])
        Label(self.master, text="X Axis:").grid(row=1, column=0, sticky=W, padx=12, pady=4)
        Entry(self.master, textvariable=self.XAxis, width=45
              ).grid(row=1, column=1, columnspan=5, sticky=W, padx=12, pady=4)

        self.YAxis = StringVar(self.master)
        self.YAxis.set(self.curvemanager.settings["YLabel"])
        Label(self.master, text="Y Axis:").grid(row=2, column=0, sticky=W, padx=12, pady=4)
        Entry(self.master, textvariable=self.YAxis, width=45
              ).grid(row=2, column=1,  columnspan=5, sticky=W, padx=12, pady=4)

        Button(self.master, text="OK", command=self.apply).grid(row=3, column=2, sticky="NEWS", padx=5, pady=5)
        Button(self.master, text="Cancel", command=self.close_window).grid(row=3, column=3, sticky="NEWS", padx=5, pady=5)

    def apply(self):
        self.curvemanager.title = self.bigtitle.get()  # curvemanager handles the big titles
        self.curvemanager.settings["XLabel"] = self.XAxis.get()  # The Graph gets its axis labels from the settings in the .prb
        self.curvemanager.settings["YLabel"] = self.YAxis.get()

        # this is the same function as Grapher.update()
        self.window.grapher.leglines.clear()
        self.window.grapher.clear()
        self.window.grapher.plot()
        self.canvas.draw()

    def show(self):
        self.window.titles = True
        self.window.editwins.append(self)
        self.master.pack_propagate(0)
        self.master.mainloop()

    def close_window(self):
        self.window.titles = False
        self.window.editwins.remove(self)
        self.master.destroy()


class EditAllPane:
    def __init__(self, rp, master=None):
        print("Edit All Curves Pane")
        master = Tk()
        self.master = master
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self.master.geometry("435x255+%d+%d" % (screen_width/2, screen_height/2))
        self.master.wm_title("Edit Curve")
        self.menubar = Menu(self.master)
        self.master.resizable(0, 0)
        self.window = rp
        self.canvas = rp.canvas
        self.curvemanager = self.window.grapher.curve_manager

        self.master.protocol('WM_DELETE_WINDOW', self.close_window)

        self.which_curve = StringVar(self.master)
        Label(self.master, text="Edit which curve?").grid(row=0, column=0, sticky=W, padx=12, pady=4)
        Entry(self.master, textvariable=self.which_curve, width=68, justify="center"
              ).grid(row=1, column=0, columnspan=5, sticky="NEWS", padx=12, pady=5)

        Button(self.master, text="OK", command=self.apply, width=5).grid(row=2, column=0, sticky="NEWS", padx=(150, 10), pady=5)
        Button(self.master, text="Cancel", command=self.close_window, width=5).grid(row=2, column=1, sticky="NEWS",
                                                                                    padx=(10, 100), pady=5)
        Label(self.master, text="""                       
                     Enter curves by number\n\n 
                   Curve ranges can be entered using a dash like this:\n
                      '3-8' will select curves 3 through 8\n\n
                   Simply enter 'all' to select all the curves.""").grid(row=3, column=0, sticky="NEWS", padx=12, pady=4, columnspan=2)

    def show(self):
        self.window.editwins.append(self)
        self.master.pack_propagate(0)
        self.master.mainloop()

    def apply(self):
        self.parse(self.which_curve.get())

    def parse(self, string):
        to_be_read = string
        indices = list()
        allwindows = list()

        if '-' in to_be_read:
            to_be_read = to_be_read.split('-')
            print(to_be_read)
            for x in range(int(to_be_read[0]), int(to_be_read[1])+1):
                indices.append(x)
        elif to_be_read.lower() == 'all':
            to_be_read = to_be_read.lower()
            for x in range(0, len(self.curvemanager.curves)):
                print(x)
                indices.append(x)
            print(indices)
        elif to_be_read.isdigit():
            indices.append(int(to_be_read))
            print(indices)
        else:
            self.which_curve.set("Not a Number")

        for index in range(0, len(indices)) if to_be_read == 'all' else indices:
            print("ok please")
            this_toggles = self.curvemanager.curves[index] if to_be_read == 'all' else self.curvemanager.curves[index-1]
            allwindows.append(EC.EditPane(this_toggles, self.window))
        print(allwindows)
        # I've spent 4 hours trying to get this to work I have no Idea why It works I'm so sorry if it breaks
        # Because I have no idea how to fix it because I don't even know what the heck is going on I need
        for windows in allwindows:
            print(self.window)
            for x in allwindows:
                self.window.editwins.append(x)
                self.window.editcurves.append(x.curve)
            windows.showNoAppend()

    def close_window(self):
        self.window.titles = False
        self.window.editwins.remove(self)
        self.master.destroy()
