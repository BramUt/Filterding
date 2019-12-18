from tkinter import *
from tkinter import filedialog
from tkinter import ttk

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
        syn_var.set("False")
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
        self.selector_syn = GUICombobox(self.window, ["False", "True"],
                                        syn_var, 0, 7)

        self.label_omim = GUILabel(self.window, "OMIM Disease", 0, 8)
        self.selector_omim = GUIEntry(self.window, omim_var, 0, 9)
        self.testlabel = GUILabel(self.window, "test", 0, 20)

        self.label_cause = GUILabel(self.window, "Causative projects", 0, 10)
        self.selector_cause = GUIEntry(self.window, cause_var, 0, 11)

        self.label_gen_comp = GUILabel(self.window, "Gene component", 0, 12)
        # self.selector_
        exit_button = Button(self.window, text="Exit",
                             command=lambda: self.window.quit())
        exit_button.grid(column=0, row=20, sticky=E)

        self.window.mainloop()


class GUILabel:

    def __init__(self, window, text, column, row, sticky=W):
        self.props = Label(window, text=text, font=("Arial", 12)
                           ).grid(column=column, row=row, sticky=sticky)


class GUISpinbox:

    def __init__(self, window, from_, to, width, text, column, row, sticky=W):
        self.props = Spinbox(window, from_=from_, to=to, width=width,
                             textvariable=text, font=("Arial", 12)
                             ).grid(column=column, row=row, sticky=sticky)


class GUICombobox:

    def __init__(self, window, values, default, column, row, sticky=W):
        self.props = ttk.Combobox(window, values=values, textvariable=default
                                  ).grid(column=column, row=row, sticky=sticky)


class GUIEntry:
    def __init__(self, window, default, column, row, sticky=W):
        self.props = Entry(window, textvariable=default
                           ).grid(column=column, row=row, sticky=sticky)


class GUICheckbox:
    def __init__(self, window, default, non_default, row):
        self.options = []
        column = 0
        for op in default:
            var = IntVar()
            # check = C



def file_opener():
    """Opens a window asking the user to select a file. Returns this path."""
    return filedialog.askopenfilename(title="Select a file.",
                                      initialdir=".")


def file_reader():
    """Reads a tsv file and returns the candidate genes based on some
    parameters.

    Output: candidates - list, nested list with candidate genes
            header_line - list, list containing the contents of the first row
                          of the tsv.
    """
    candidates = []

    with open(file_opener()) as file:
        for counter, line in enumerate(file):
            if not counter:
                header_line = line.rstrip().split("\t")

                print(header_line)
                reads_i = header_line.index("reads")
                phylop_i = header_line.index("phyloP")
                var_reads_i = header_line.index("variation reads")
                perc_var_i = header_line.index("% variation")
                snp_i = header_line.index("SNP id")
                synonymous_i = header_line.index("Synonymous")
                gen_comp_i = header_line.index("Gene component")
                omim_dis_i = header_line.index("OMIM_DISEASE")
                caus_pro_i = header_line.index("Causative - Projects")
                print(reads_i, phylop_i, var_reads_i, perc_var_i, snp_i,
                      synonymous_i, gen_comp_i)
            else:
                try:
                    line = line.rstrip().split("\t")
                    if (
                            float(line[phylop_i]) >= 2.5 and
                            int(line[reads_i]) >= 5 and
                            line[snp_i] == "" and
                            int(line[var_reads_i]) >= 5 and
                            float(line[perc_var_i]) >= 20 and
                            line[synonymous_i] == "FALSE" and
                            line[gen_comp_i] in ("EXON_REGION", "SA_SITE") and
                            "Retinitis" in line[omim_dis_i]
                    ) or "HGMD" in line[caus_pro_i]:
                        candidates.append(line)
                except IndexError:
                    print(line)

    return candidates, header_line


def file_writer(candidates, header_line):

    while True:
        try:
            with open("Filterding results.tsv", "w") as file:
                file.write("\t".join(header_line) + "\n")
                for c in candidates:
                    file.write("\t".join(c) + "\n")
                break
        except PermissionError:
            input("Permission to denied 'Filterding results.tsv'")


def filter_func():
    pass


def main():
    gui = MainGUI()

    # candidates, header_line = file_reader()
    #
    # file_writer(candidates, header_line)


main()
