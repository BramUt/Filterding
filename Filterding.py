from tkinter import *
from tkinter import filedialog

root = Tk()
root.withdraw()


class MainGUI:

    def __init__(self):

        window = Toplevel()
        window.title("Filterding")
        window.geometry("700x400")

        reads = IntVar()
        reads.set(5)
        var_reads = IntVar()
        var_reads.set(5)
        perc_var = IntVar()
        perc_var.set(20)
        print(reads.get())

        self.label_reads = GUILabel(window, "Minimum reads", 0,0)
        self.selector_reads = GUISpinbox(window, 0, 100, 5, reads, 0, 1)

        self.label_var_reads = GUILabel(window, "Minimum variation reads", 0, 2)
        self.selector_var_reads = GUISpinbox(window, 0, 200, 5, var_reads, 0,
                                             3)

        self.label_perc_var = GUILabel(window, "Minimal % variation", 0, 4)
        self.selector_perc_var = GUISpinbox(window, 0, 200, 5, perc_var, 0, 5)


        self.testlabel = GUILabel(window, "test", 0, 6)

        exit_button = Button(window, text="Exit",
                             command=lambda: window.quit())
        exit_button.grid(column=0, row=10, sticky=E)

        window.mainloop()


class GUILabel:

    def __init__(self, window, text, column, row, sticky=W):
        self.props = Label(window, text=text, font=("Arial", 12)
                           ).grid(column=column, row=row, sticky=sticky)


class GUISpinbox:

    def __init__(self, window, from_, to, width, text, column, row, sticky=W):
        self.props = Spinbox(window, from_=from_, to=to, width=width,
                             textvariable=text, font=("Arial", 12)
                             ).grid(column=column, row=row, sticky=sticky)


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
