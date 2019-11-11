
def main(filename):
    parse_gff_genes_to_csv(filename)


def parse_gff_genes_to_csv(filename):
    print("Parsing of file has been started")
    count = 0
    #filename = "dmell-allr5.6.gff"

    f = open(filename, 'r')
    f_out = open('blank.csv', 'w')
    f_out.write(_make_svc_gene_header())

    while True:
        line = f.readline()
        if line:
            if count % 100000 == 0 and count != 0:
                print(f"{count} genes has been read")
            # end of the
            if line.startswith("##FASTA"):
                break

            # Metainformation
            elif line.startswith("#"):
                continue

            # Information about a gene in db
            else:
                """
                Example of gene
                2L	FlyBase	chromosome_band	-204333	1326937	.	+	.	ID=band-21_chromosome_band;Name=band-21;
                """
                data = line.split()
                chromosome_name = data[0]
                #data_base_name = data[1]
                gene_type = data[2]
                left_position = data[3]
                right_position = data[4]
                # _ = data[5]
                strand_direction = data[5]
                # _ = data[6]

                gene_id = None
                gene_name = None

                extra_line_data = data[8].split(";")
                for key in extra_line_data:
                    if len(key)>0:
                        if key.startswith("ID"):
                            gene_id = key.split("=")[1]
                        elif key.startswith('Name'):
                            gene_name = key.split("=")[1]
                f_out.write("\n")
                f_out.write(_make_svc_gene_line(chromosome_name, gene_type, left_position, right_position, strand_direction, gene_id, gene_name))
                count += 1
    f.close()
    f_out.close()
    print(f"Parsing {filename} gff file genes into CVS genes files has finished")


def _make_svc_gene_header():
    return "ID,NAME,TYPE,CHR,START,END,STRAND"


def _make_svc_gene_line(chomosome_name, gene_type, start, end, strand, Id, name):
    line = f"{Id},{name},{gene_type},{chomosome_name},{start},{end},{strand}"
    return line





