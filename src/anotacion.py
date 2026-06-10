import pandas as pd
from Bio import SeqIO

archivo_csv = "orfs_estres_hidrico.csv"
archivo_rna_gigante = "oryza_sativa_GCF_034140825.1/rna.fna"  
archivo_orfs_salida = "orfs_nucleotidos.fasta"

try:
    with open(archivo_csv, 'r') as f:
        primera_linea = f.readline()
        separador = ";" if ";" in primera_linea else ","
    
    df = pd.read_csv(archivo_csv, sep=separador)

    orfs_extraidos = []
    palabra_clave = "expansin-B1"

    for record in SeqIO.parse(archivo_rna_gigante, "fasta"):
        if palabra_clave.lower() in record.description.lower():
            orfs_extraidos.append(record)
            print(f"ORF de ARN encontrado: {record.id} ({record.description[:60]}...)")

    if orfs_extraidos:
        unicos = {rec.id: rec for rec in orfs_extraidos}
        SeqIO.write(unicos.values(), archivo_orfs_salida, "fasta")
        print(f"Se aislaron {len(unicos)} ORFs únicos de nucleótidos en '{archivo_orfs_salida}'")

except Exception as e:
    print(f"Error")