from tkinter import *
from tkinter import ttk
from tkinter.ttk import *


root = Tk()
root.withdraw()


class MainGUI:

    def __init__(self):
        self.window = Toplevel()
        self.window.title("Filterding")

        reads, var_reads, perc_var = IntVar(), IntVar(), IntVar()
        reads.set(5)
        var_reads.set(5)
        perc_var.set(20)

        syn_var, omim_var, cause_var = StringVar(), StringVar(), StringVar()
        syn_var.set("FALSE")
        omim_var.set("Retinitis")
        cause_var.set("HGMD")
        gen_comp_def_var = ["EXON_REGION", "SA_SITE"]
        gen_comp_dif_var = ["(empty)", "INTRON_REGION", "microRNA",
                            "SA_SITE_CANONICAL", "UTR"]

        self.label_reads = GUILabel(self.window, "Minimum reads", 0, 0)
        self.selector_reads = GUISpinbox(self.window, 0, 100, 5, reads, 0, 1)

        self.label_var_reads = GUILabel(self.window, "Minimum variation reads",
                                        0, 2)
        self.selector_var_reads = GUISpinbox(self.window, 0, 200, 5, var_reads,
                                             0, 3)

        self.label_perc_var = GUILabel(self.window, "Minimal % variation",
                                       0, 4)
        self.selector_perc_var = GUISpinbox(self.window, 0, 200, 5,
                                            perc_var, 0, 5)

        self.label_syn = GUILabel(self.window, "Synonymous", 0, 6)
        self.selector_syn = GUICombobox(self.window, ["FALSE", "TRUE"],
                                        syn_var, 0, 7)

        self.label_omim = GUILabel(self.window, "OMIM Disease", 0, 8)
        self.selector_omim = GUIEntry(self.window, omim_var, 0, 9)

        self.label_cause = GUILabel(self.window, "Causative projects", 0, 10)
        self.selector_cause = GUIEntry(self.window, cause_var, 0, 11)

        self.label_gen_comp = GUILabel(self.window, "Gene component", 0, 12)
        self.selector_gen_comp = GUICheckbox(self.window, gen_comp_def_var,
                                             gen_comp_dif_var, 0, 13)

        exit_button = Button(self.window, text="Exit",
                             command=lambda: self.window.quit())
        exit_button.grid(column=0, row=20, sticky=E)

        self.window.mainloop()

        self.condition_list = [self.selector_reads.get_value(),
                               self.selector_var_reads.get_value(),
                               2.5, self.selector_perc_var.get_value(),
                               self. selector_syn.get_value(),
                               self.selector_gen_comp.get_gen_comp(),
                               self.selector_omim.get_value()]


class GUILabel:

    def __init__(self, window, text, column, row, sticky=W):
        self.props = Label(window, text=text, font=("Arial", 12))
        self.props.grid(column=column, row=row, sticky=sticky)


class GUISpinbox:

    def __init__(self, window, from_, to, width, text, column, row, sticky=W):
        self.props = Spinbox(window, from_=from_, to=to, width=width,
                             textvariable=text, font=("Arial", 12))
        self.props.grid(column=column, row=row, sticky=sticky)

    def get_value(self):
        """"Returns the value of the spinbox."""
        return int(self.props.get())


class GUICombobox:

    def __init__(self, window, values, default, column, row, sticky=W):
        self.props = ttk.Combobox(window, values=values, textvariable=default)
        self.props.grid(column=column, row=row, sticky=sticky)

    def get_value(self):
        """Returns the value of the combobox."""
        return self.props.get()


class GUIEntry:
    def __init__(self, window, default, column, row, sticky=W):
        self.props = Entry(window, textvariable=default)
        self.props.grid(column=column, row=row, sticky=sticky)

    def get_value(self):
        """Splits the content of the entrybox and returns the list."""
        return self.props.get().split(", ")


class GUICheckbox:
    def __init__(self, window, default, non_default, column, row):
        self.def_tag = default
        self.default = default
        self.non_def_tags = non_default
        self.non_default = non_default
        self.options = []

        for o in range(len(self.default)):
            temp_text = default[o]
            self.default[o] = StringVar()
            self.default[o].set(temp_text)
            self.check = Checkbutton(window, text=temp_text,
                                     variable=self.default[o],
                                     onvalue=temp_text, offvalue=0)
            self.check.grid(column=column, row=row, sticky=W)
            row += 1
        for p in range(len(self.non_default)):
            temp_text = self.non_default[p]
            self.non_default[p] = StringVar()
            check = Checkbutton(window, text=temp_text,
                                variable=self.non_default[p],
                                onvalue=temp_text, offvalue=0)
            check.grid(column=column, row=row, sticky=W)
            row += 1

    def get_gen_comp(self):
        """Returns a list of values each checked checkbox in self.default and
        self.non_default.
        """
        return [self.default[o].get() for o in (range(len(self.default)))
                if self.default[o].get()] + \
               [self.non_default[p].get() for p in
                (range(len(self.non_default))) if self.non_default[p].get()]
