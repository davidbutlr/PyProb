from tkinter import *
from typing import Any
import pyperclip


class EditPane:
    colornames = {"Red": "#ff0000", "Blue": "#0F3FFF",  "Green": "#36AA0E",  "Orange": "#EF8B12",  "Cyan": "#00FFFF",
                  "Grey": "#737373", "Chocolate": "#3F1F09", "Magenta": "#FF00FF", "LT Red": "#FF6666",
                  "LT Blue": "#4CA6FF", "LT Green": "#7CF37C"}

    def show_choice(self):
        print(self.v.get())

    def __init__(self, curve, rp, master=None):
        print("Edit Pane")
        master = Tk()
        self.curve = curve
        self.master = master
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        self.master.geometry("310x550+%d+%d" % (screen_width/2, (screen_height/2) - (screen_height*.4)))
        self.master.wm_title("Edit Curve: %s" % curve.title)
        self.menubar = Menu(self.master)
        self.master.resizable(0, 0)
        self.window = rp
        self.canvas = rp.canvas
        self.textvariable = StringVar(self.master)
        self.textvariable.set(self.curve.title)
        self.curvemanager = self.window.grapher.curve_manager
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        curve_name = Label(master, text="Curve Title:")
        curve_name.grid(row=0, column=0, sticky=W, padx=5, pady=7)
        e = Entry(master, text=self.curve.title, textvariable=self.textvariable, width=30
                  ).grid(row=0, column=1, columnspan=2, sticky=W, pady=15)

        self.rightFrame = Frame(master, width=200)
        self.labelRangeFrame = Frame(self.rightFrame, bd=1, relief=GROOVE, padx=36, pady=5)
        self.innerFrame = Frame(self.labelRangeFrame)
        self.min = StringVar(self.innerFrame)
        self.max = StringVar(self.innerFrame)
        self.step = StringVar(self.innerFrame)
        self.min.set(self.curve.label_min)
        self.max.set(self.curve.label_max)
        self.step.set(self.curve.annotative_step)
        self.initial_min = self.min.get()
        self.initial_max = self.max.get()
        self.initial_step = self.step.get()
        colorFrame = Frame(master, bd=5)

        self.v = StringVar(self.master)

        for key in EditPane.colornames.keys():
            if self.curve.color == EditPane.colornames[key]:
                self.v.set(key)

        # All the Radio Buttons
        for i, x in enumerate(EditPane.colornames):
            Radiobutton(colorFrame, text=x, padx=10, variable=self.v, cursor="arrow", fg=EditPane.colornames[x],
                        command=self.show_choice, value=x).grid(row=i, column=0, sticky=W)

        self.mean = IntVar(self.master)
        self.median = IntVar(self.master)
        self.stdDev = IntVar(self.master)

        statsFrame = Frame(self.rightFrame, bd=1, relief=GROOVE, padx=20, pady=15)
        Checkbutton(statsFrame, text="Show Mean", variable=self.mean).grid(row=1, column=1, sticky=W)
        Checkbutton(statsFrame, text="Show Median", variable=self.median).grid(row=2, column=1, sticky=W)
        Checkbutton(statsFrame, text="Show Std Dev", variable=self.stdDev).grid(row=3, column=1, sticky=W)
        Button(statsFrame, text="Copy", command=self.copy_curve).grid(row=1, column=2, sticky="N")
        Button(statsFrame, text="Cut").grid(row=2, column=2, sticky="S")
        Button(statsFrame, text="Delete", command=self.delete).grid(row=3, column=2, sticky="S")

        symbolFrame = Frame(self.rightFrame, bd=1, relief=GROOVE, padx=34, pady=15)
        self.symbol = StringVar(symbolFrame)

        Label(symbolFrame, text="Symbol:").grid(row=0, column=0, sticky=W)
        Entry(symbolFrame, text=self.curve.marker, textvariable=self.symbol,  width=10).grid(row=0, column=1, sticky=W)
        self.symbol.set(self.curve.display_marker)
        # Button(symbolFrame, text="Extended Colors").grid(row=1, column=0, columnspan=2)

        legendMoveFrame = Frame(self.rightFrame, bd=1, relief=GROOVE, padx=30, pady=5)
        Label(legendMoveFrame, text="Move Legend Title:").grid(row=0, column=0, columnspan=2)
        Button(legendMoveFrame, text="Up", command=self.up).grid(row=1, column=0, sticky=N, padx=7, pady=7)
        Button(legendMoveFrame, text="Down", command=self.down).grid(row=2, column=0, sticky=N, padx=7, pady=7)
        Button(legendMoveFrame, text="Top", command=self.top).grid(row=1, column=1, sticky=S, padx=7, pady=7)
        Button(legendMoveFrame, text="Bottom", command=self.bottom).grid(row=2, column=1, sticky=S, padx=7, pady=7)


        Label(self.labelRangeFrame, text="Label Range").grid(row=0, column=1, sticky="NEWS")


        Label(self.innerFrame, text="Min:").grid(row=0, column=0, sticky=W, padx=7, pady=3)
        Entry(self.innerFrame, textvariable=self.min, width=5).grid(row=0, column=1, sticky=W, padx=15)
        Label(self.innerFrame, text="Max:").grid(row=1, column=0, sticky=W, padx=7, pady=3)
        Entry(self.innerFrame, textvariable=self.max, width=5).grid(row=1, column=1, sticky=W, padx=15)
        Label(self.innerFrame, text="Step:").grid(row=2, column=0, sticky=W, padx=7, pady=3)
        Entry(self.innerFrame, textvariable=self.step, width=5).grid(row=2, column=1, sticky=W, padx=15)
        Button(self.labelRangeFrame, text="clear", command=self.clear_labels).grid(row=2, column=1, sticky="NEWS")

        navButtonFrame = Frame(master)
        Button(navButtonFrame, text="<", command=self.prev).grid(row=0, column=0, padx=10, pady=5)
        Button(navButtonFrame, text=">", command=self.next).grid(row=0, column=1, padx=10, pady=5)

        confirmButtonFrame = Frame(master)
        Button(confirmButtonFrame, text="OK", command=self.apply).grid(row=0, column=0, padx=10, pady=5)
        Button(confirmButtonFrame, text="Cancel", command=self.close_window).grid(row=0, column=1, padx=10, pady=5)

        self.innerFrame.grid(row=1, column=0, columnspan=3, sticky="NEWS")
        statsFrame.grid(row=0, column=1, columnspan=2, sticky=N)
        symbolFrame.grid(row=1, column=1, columnspan=2, sticky=S)
        legendMoveFrame.grid(row=2, column=1, columnspan=2, sticky=N)
        self.labelRangeFrame.grid(row=3, column=1, columnspan=2, sticky=N)
        navButtonFrame.grid(row=3, column=0)
        self.rightFrame.grid(row=1, column=1, columnspan=1, rowspan=1)
        colorFrame.grid(row=1, column=0, columnspan=1, rowspan=1, sticky=W)
        confirmButtonFrame.grid(row=3, column=1)

    def close_window(self):
        print(self.window.editwins)
        self.window.editwins.remove(self)
        self.window.editcurves.remove(self.curve)
        # print(self.window.editwins)
        self.master.destroy()

    def clear_labels(self):
        self.min.set("0")
        self.max.set("0")
        self.step.set("0")

    def show(self):
        self.window.editwins.append(self)
        self.window.editcurves.append(self.curve)
        print("we appended")
        self.master.pack_propagate(0)
        self.master.mainloop()

    def showNoAppend(self):
        self.master.pack_propagate(0)
        self.master.mainloop()

    def ChangeColor(self, hexa):
        self.curve.color = hexa

    def next(self):
        if self.curvemanager.curves.index(self.curve) < (len(self.curvemanager.curves) - 1):
            self.close_window()
            newEditPane = EditPane(self.curvemanager.curves[self.curvemanager.curves.index(self.curve)+1], self.window)
            newEditPane.show()

    def prev(self):
        if self.curvemanager.curves.index(self.curve) > 0:
            self.close_window()
            newEditPane = EditPane(self.curvemanager.curves[self.curvemanager.curves.index(self.curve)-1], self.window)
            newEditPane.show()

    def get_the_range(self, mini, maxi, step):
        curve = self.curve
        step = step
        start_index = 0
        end_index = 0
        self.curve.label_min = mini
        self.curve.label_max = maxi

        if not curve.percent_data:
            curve.make_percent()
        # print(curve.percent_data)
        for i, x in enumerate(curve.percent_data[1]):
            # print(i, x)
            if x > mini > curve.percent_data[1][i - 1]:
                print(i, x, "mini true")
                start_index = i
            if (i+1) < len(curve.percent_data[1]) and x < maxi < curve.percent_data[1][i + 1]:
                print(i, x, "maxi true")
                end_index = i
                break
            if (i+1) >= len(curve.percent_data[1]):
                print(i, x, "end of array index")
                end_index = i
            if mini == 0 and maxi == 0:
                start_index = 0
                end_index = -1

        range_of_data = [curve.percent_data[0][start_index:end_index+1],
                         curve.percent_data[1][start_index:end_index+1]]
        print(range_of_data)

        if range_of_data:
            self.window.grapher.annotating = True
            self.curve.annotative_step = step
            self.window.grapher.annotation_list.update({curve.title: range_of_data})
        elif mini == 0 and maxi == 0:
            self.window.grapher.annotation_list.pop(curve.title)
        else:
            self.window.grapher.annotating = False

    def up(self):
        self.window.up(self.curve.title)

    def down(self):
        self.window.down(self.curve.title)

    def top(self):
        self.window.top(self.curve.title)

    def bottom(self):
        self.window.bottom(self.curve.title)

    def changetitle(self, newtitle):
        print("this is the new title: " + newtitle)
        self.curve.title = newtitle

    def changesymbol(self, symb):
        # print(str(symb))
        symb = symb
        self.curve.marker = "$" + str(symb) + "$"
        # print(self.curve.marker)

    # All of the functions that make changes to the curves on the graph actually just make changes to the components
    # and then they replot the graph with the changed data. That means that the curves store
    # The state that they're in (color, marker, legend position)
    # so that they can be regraphed in order to maintain the plot
    # update() simply redraws the graph after most changes
    def update(self):
        self.window.grapher.leglines.clear()  # without this line the lines would be appended to the legend without deleting the old ones
        self.window.grapher.clear()  # this clears the whole axis and everything on it
        self.window.grapher.plot()  # This re-graphs the whole plot
        self.canvas.draw()          # this is what shows the newly drawn plot again

    def copy_curve(self):
        pyperclip.copy(self.curve.save())

    def delete(self):
        to_be_deleted = self.curvemanager.get_curve_by_title(self.curve.title)

        self.curvemanager.curves.remove(to_be_deleted)
        self.update()
        self.close_window()

    def apply(self):
        newcolor = self.v.get()
        print(newcolor)
        print(self.curve.color)

        self.label_min = self.min.get()
        self.label_max = self.max.get()
        self.label_step = self.step.get()
        if self.label_min != self.initial_min or self.label_max != self.initial_max or self.label_step != self.initial_step:
            try:
                step = int(self.step.get())
                new_min = float(self.min.get())
                new_max = float(self.max.get())
                print((new_min, new_max))
                self.get_the_range(new_min, new_max, step)
            except Any:
                print("Not valid range")

        mean = self.mean.get()
        median = self.median.get()
        stdDev = self.stdDev.get()
        title = self.textvariable.get()
        symb = self.symbol.get()

        if EditPane.colornames[newcolor] != self.curve.color:
            # Regraph
            self.ChangeColor(EditPane.colornames[newcolor])
            self.canvas.draw()
        if title != self.curve.title:
            self.changetitle(title)
        if symb != self.curve.marker:
            # print(symb)
            self.changesymbol(symb)

        self.curve.show_mean = bool(mean)
        self.curve.show_median = bool(median)
        self.curve.show_std_dev = bool(stdDev)
        self.update()
