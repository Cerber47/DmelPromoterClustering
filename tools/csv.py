import pandas as pd


genes_cvs_columns = {
    "name": [], "ID": [],
    "db_name": [], "feature": [],
    "start": [], "end": [], "strand": [],
    "sequence": []
}

LEFT_EDGE = 150
RIGHT_EDGE = 150


def gff_to_csv(f):
    df = pd.DataFrame(genes_cvs_columns)
    filename = 'files/' + f
    print(df, '\n', filename)

    fasta, ids = _split_gff(filename)

    current_seq = ''
    current_chr = ''

    with open(ids) as f_ids:
        line = f_ids.readline()
        while line:
            gene_information = line.split('\t')

            chromo_name = gene_information[0]
            db_name = gene_information[1]
            feature_name = gene_information[2]
            start = int(gene_information[3])
            end = int(gene_information[4])
            strand = gene_information[6]

            name, id_name, parent, dbxref = _parse_gff_extra_line(gene_information[8])

            if current_chr != chromo_name:
                current_seq = _get_sequence(fasta, chromo_name)
                current_chr = chromo_name

            s = start - 1 - LEFT_EDGE
            e = end - 1 + RIGHT_EDGE
            gene_sequence = current_seq[s:e]

            df = df.append({
                "name": [name], "ID": [id_name],
                "db_name": [db_name], "feature": [feature_name],
                "start": [start], "end": [end], "strand": [strand],
                "sequence": [current_seq] })

            line = f_ids.readline()




def _split_gff(filename):
    filename_f = _remove_extension(filename, '.gff') + "_fasta"
    filename_ids = _remove_extension(filename, '.gff') + "_ids"

    with open(filename) as f:
        with open(filename_ids, 'w') as f_ids:
            line = f.readline()
            while line:
                if line.startswith("##FASTA"):
                    break
                elif line.startswith("#"):
                    pass
                else:
                    f_ids.write(line)
                line = f.readline()

        with open(filename_f, 'w') as f_fasta:
            line = f.readline()
            while line:
                if line.startswith("#") or line.startswith(" "):
                    pass
                else:
                    f_fasta.write(line)
                line = f.readline()

    return filename_f, filename_ids


def _remove_extension(name, extension):
    return name.replace(extension, '')

def _get_sequence(filename, chromo_name):
    flag = False

    with open(filename) as f:
        line = f.readline()

        seq = ''
        flag = False

        while line:
            if line.startswith(">"):
                if line.startswith(">" + chromo_name):
                    flag = True
                else:
                    if flag:
                        return seq
            elif flag:
                seq += line.replace("\n", "")
            line = f.readline()


def _parse_gff_extra_line(line):
    data = line.split(";")

    _name = None
    _id = None
    _parent = None
    _Dbxref = None

    for i in data:
        tmp = i.split("=")
        key, value = tmp[0], tmp[1]
        if key == "Name":
            _name = value
        elif key == "Id":
            _id = value
        elif key == "Parent":
            _parent = value
        elif key == "Dbxref":
            _Dbxref = value
        else:
            continue

        return _name, _id, _parent, _Dbxref

def _save(filename, df):
    pass
