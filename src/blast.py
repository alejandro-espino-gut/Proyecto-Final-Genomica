import subprocess
import pandas as pd

cmd_db = "makeblastdb -in zea_mays.fasta -dbtype prot -out db_maiz"
subprocess.run(cmd_db, shell=True, check=True)

archivo_salida = "resultados_blast.txt"

cmd_blast = (f"blastp -query oryza_sativa.fasta -db db_maiz -out {archivo_salida} "f'-evalue 1e-10 -outfmt "6 qseqid sseqid pident evalue bitscore qcovs"')

subprocess.run(cmd_blast, shell=True, check=True)
columnas = ["Gen_Arroz_ID", "Gen_Maiz_ID", "Identidad", "E_Value", "Bit_Score", "Cobertura"]

try:
    df = pd.read_csv(archivo_salida, sep="\t", names=columnas)
    print(f"Total de matches crudos encontrados por BLAST: {len(df)}")
    
    if df["Identidad"].max() > 100.0:
        df["Identidad"] = df["Identidad"] / 1000 # porque pandas se come el punto si no ponemos esto
    
    df_id = df[df["Identidad"] >= 40.0]
    print(f"Matches que pasaron el filtro de Identidad (>= 40%): {len(df_id)}")
    
    df_filtrado = df_id[df_id["Cobertura"] >= 70.0]
    print(f"Matches que además pasaron el filtro de Cobertura (>= 70%): {len(df_filtrado)}")
    
    df_filtrado = df_filtrado.sort_values(by=["E_Value", "Bit_Score"], ascending=[True, False])
    
    df_filtrado.to_csv("orfs_conservados.csv", index=False, sep=";")

except FileNotFoundError:
    print("Error")