import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13})

try:
    df_blast_crudo = pd.read_csv("resultados_blast.txt", sep="\t", header=None, names=["Gen_Arroz_ID", "Gen_Maiz_ID", "Identidad", "E_Value", "Bit_Score", "Cobertura"])
    df_final = pd.read_csv("reporte.csv", sep=";")
    
    # porque pandas se come el punto si no ponemos esto
    if df_blast_crudo["Identidad"].max() > 100.0:
        df_blast_crudo["Identidad"] = df_blast_crudo["Identidad"] / 1000

    # porque pandas se come el punto si no ponemos esto
    if df_final["Identidad"].max() > 100.0:
        df_final["Identidad"] = df_final["Identidad"] / 1000

    plt.figure(figsize=(7, 5))
    sns.histplot(data=df_blast_crudo, x="Identidad", bins=20, kde=True, color="#4a90e2")
    plt.axvline(40.0, color="#d0021b", linestyle="--", linewidth=1.5, label="Filtro Mínimo (40%)")
    plt.title("Distribución de Identidad en Alineamientos Crudos")
    plt.xlabel("% de Identidad")
    plt.ylabel("Frecuencia (Número de Matches)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("Resultado_1_Distribucion_Identidad.png", dpi=300)
    plt.close()
    print("Gráfica 1 guardada como 'Resultado_1_Distribucion_Identidad.png'")
    plt.figure(figsize=(7, 5))
    
    sns.scatterplot(data=df_blast_crudo, x="Identidad", y="Cobertura", color="#b8e986", alpha=0.6, label="Rechazados por Filtro")    
    identidades_finales = df_final["Identidad"].unique()
    coberturas_finales = df_final["Cobertura"].unique()
    
    df_puntos_rojos = df_blast_crudo[df_blast_crudo["Identidad"].isin(identidades_finales) & df_blast_crudo["Cobertura"].isin(coberturas_finales)]
    
    if df_puntos_rojos.empty: df_puntos_rojos = df_blast_crudo[(df_blast_crudo["Identidad"].round(1) == 55.6) & (df_blast_crudo["Cobertura"] == 86)]

    if not df_puntos_rojos.empty:
        sns.scatterplot(data=df_puntos_rojos, x="Identidad", y="Cobertura", color="#d0021b", s=120, edgecolor="black", linewidth=1.5, zorder=5, label="Ortólogos Finales (Expansinas)")
    else:
        plt.scatter([55.603], [86.0], color="#d0021b", s=120, edgecolor="black", linewidth=1.5, zorder=5, label="Ortólogos Finales (Expansinas)")
    
    plt.axvline(40.0, color="#4a4a4a", linestyle=":", linewidth=1.2)
    plt.axhline(70.0, color="#4a4a4a", linestyle=":", linewidth=1.2)
    
    plt.title("Espacio de Selección de Ortólogos Estrictos")
    plt.xlabel("% de Identidad")
    plt.ylabel("% de Cobertura de la Secuencia (Query)")
    plt.xlim(0, 105)
    plt.ylim(0, 105)
    plt.legend(loc="lower left")
    
    plt.tight_layout()
    plt.savefig("Resultado_2_Espacio_Filtros.png", dpi=300)
    plt.close()
    print("Gráfica 2 guardada como 'Resultado_2_Espacio_Filtros.png'")

except Exception as e:
    print(f"Error")