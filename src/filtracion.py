import pandas as pd
from Bio import SeqIO

archivo_csv = "orfs_conservados.csv"
archivo_fasta_arroz = "oryza_sativa.fasta"

df = pd.read_csv(archivo_csv, sep=";")

descripciones = {}
for record in SeqIO.parse(archivo_fasta_arroz, "fasta"):
    descripciones[record.id] = record.description

df["Anotacion_Funcional"] = df["Gen_Arroz_ID"].map(descripciones)

palabras_estres = ["expansin", "stress", "water", "osmotic", "dehydration", "cell wall", "probable"]
patron_filtro = "|".join(palabras_estres)

df_filtrado = df[df["Anotacion_Funcional"].str.contains(patron_filtro, case=False, na=False)]

df_filtrado.to_csv("orfs_estres_hidrico.csv", index=False, sep=";")

print("Archivo guardado como 'orfs_estres_hidrico.csv'")
print(df_filtrado[["Gen_Arroz_ID", "Gen_Maiz_ID", "Anotacion_Funcional"]])