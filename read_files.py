import csv


# ficheiro = open('../arquivos_Pacientes/column_bin_3a_2p.csv', 'rb')
# reader = csv.reader(ficheiro)
# for linha in reader:
#     print(linha)

with open('../arquivos_Pacientes/column_bin_3a_2p.csv', 'r') as ficheiro:
    reader = csv.reader(ficheiro)
    for linha in reader:
        print(linha)