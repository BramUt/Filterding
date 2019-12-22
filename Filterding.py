from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import *
import traceback


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
        return int(self.props.get())


class GUICombobox:

    def __init__(self, window, values, default, column, row, sticky=W):
        self.props = ttk.Combobox(window, values=values, textvariable=default)
        self.props.grid(column=column, row=row, sticky=sticky)

    def get_value(self):
        return self.props.get()


class GUIEntry:
    def __init__(self, window, default, column, row, sticky=W):
        self.props = Entry(window, textvariable=default)
        self.props.grid(column=column, row=row, sticky=sticky)

    def get_value(self):
        return self.props.get().split(",")


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

        return [self.default[o].get() for o in (range(len(self.default)))
                if self.default[o].get()] + \
               [self.non_default[p].get() for p in
                (range(len(self.non_default))) if self.non_default[p].get()]


def file_opener():
    """Opens a window asking the user to select a file. Returns this path."""
    return filedialog.askopenfilename(title="Select a file.",
                                      initialdir=".")


def filter_func(condition_list, data_list):
    """Checks if the data in data_list meets the conditions in condition list.

    Input:  condition_list - list, list with conditions.
            data_list - list, list with data.

    Output: boolean
    """

    if (int(data_list[0]) >= condition_list[0] and                      # reads
        int(data_list[1]) >= condition_list[1] and                      # variation reads
        # data_list[2] >= condition_list[2] and                    # PhyloP
        float(data_list[3]) >= condition_list[3] and                    # Percent variation
        data_list[4] == condition_list[4] and                           # Synonymous
        any([gen in data_list[5] for gen in condition_list[5]]) and     # Gene component
        any([dis in data_list[6] for dis in condition_list[6]]) and     # OMIM disease
        data_list[7] == ""                                              # SNP id
    ):

        return True
    else:
        return False


def file_reader(condition_list):
    """Reads a tsv file and returns the candidate genes based on some
    parameters.

    Output: candidates - list, nested list with candidate genes
            header_line - list, list containing the contents of the first row
                          of the tsv.
    """
    candidates = []
    error_count = 0

    with open(file_opener()) as file:
        for counter, line in enumerate(file):
            if not counter:
                header_line = line.rstrip().split("\t")

                reads_i = header_line.index("reads")
                phylop_i = header_line.index("phyloP")
                var_reads_i = header_line.index("variation reads")
                perc_var_i = header_line.index("% variation")
                snp_i = header_line.index("SNP id")
                synonymous_i = header_line.index("Synonymous")
                gen_comp_i = header_line.index("Gene component")
                omim_dis_i = header_line.index("OMIM_DISEASE")
                caus_pro_i = header_line.index("Causative - Projects")
                index_list = [reads_i, phylop_i, var_reads_i, perc_var_i,
                              snp_i, synonymous_i, gen_comp_i, omim_dis_i,
                              caus_pro_i]
                print(index_list)
            elif line != "":
                try:
                    line = line.rstrip()
                    line_list = line.split("\t")
                    data_list = [line_list[reads_i], line_list[var_reads_i],
                                 line_list[phylop_i], line_list[perc_var_i],
                                 line_list[synonymous_i],
                                 line_list[gen_comp_i],
                                 line_list[omim_dis_i],
                                 line_list[snp_i]]
                    if counter == 1:
                        print(data_list, condition_list)

                    if filter_func(condition_list, data_list):
                        print("Geen SNP", data_list)
                        candidates.append(line_list)
                    elif ("HGMD" in line_list[caus_pro_i] and
                          (any([dis in data_list[6] for dis in
                                condition_list[6]]))
                    ):
                        print("SNP", data_list)
                        candidates.append(line_list)
                except IndexError:
                    error_count += 1
                    pass
            else:
                break

    print("Index errors:", error_count)

    return candidates, header_line


def file_writer(candidates, header_line):

    print("Aantal regels:", len(candidates))
    while True:
        try:
            with open("Filterding results.tsv", "w") as file:
                file.write("\t".join(header_line) + "\n")
                for c in candidates:
                    file.write("\t".join(c) + "\n")
                break
        except PermissionError:
            input("Permission to denied 'Filterding results.tsv'")


def main():
    guidata = MainGUI().condition_list

    print(guidata)

    candidates, header_line = file_reader(guidata)

    file_writer(candidates, header_line)


main()
