from tkinter import filedialog
from Filterding.FilterGUI import MainGUI


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

                    elif filter_func(condition_list, data_list):
                        print("Geen SNP", data_list)
                        candidates.append(line_list)

                    elif ("HGMD" in line_list[caus_pro_i] and
                          (any([dis in data_list[6] for dis in
                                condition_list[6]]))):
                        print("SNP", data_list)
                        candidates.append(line_list)

                except IndexError:
                    print(line_list)
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

    # guidata = MainGUI().condition_list

    print(guidata)

    candidates, header_line = file_reader(guidata)

    file_writer(candidates, header_line)


main()