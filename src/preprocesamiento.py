import os


def generar_consulta_ncbi(archivo_entrada, organismo):
    if not os.path.exists(archivo_entrada): return None

    with open(archivo_entrada, "r") as f:
        ids = [line.strip() for line in f if line.strip()]

    if not ids: return None

    ids_unidos = " OR ".join(ids)

    consulta_final = f"({ids_unidos}) AND \"{organismo}\"[Organism]"

    return consulta_final


consulta_arroz = generar_consulta_ncbi("ids_oryza_sativa.txt", "Oryza sativa")
consulta_maiz = generar_consulta_ncbi("ids_zea_mays.txt", "Zea mays")
with open("consultas_listas_ncbi.txt", "w") as salida:
    if consulta_arroz:
        salida.write(consulta_arroz + "\n\n")
    if consulta_maiz:
        salida.write(consulta_maiz + "\n")
print("\n'consultas_listas_ncbi.txt")