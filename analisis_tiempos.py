import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF

# Cargar datos
df = pd.read_csv("data/tiempos_completitud.csv")

# Agregar columna de desviación en duración
df["Desviacion_Duracion"] = df["Duracion_Real_min"] - df["Duracion_Estimada_min"]

# Boxplot de desviación por tipo de contenido
plt.figure(figsize=(8, 5))
sns.boxplot(x="Tipo_Contenido", y="Desviacion_Duracion", data=df)
plt.title("Desviación de Duración por Tipo de Contenido")
plt.axhline(0, color="gray", linestyle="--")
plt.tight_layout()
plt.savefig("images/grafico_desviacion_duracion.png")
plt.close()

# PDF de resumen por tipo de contenido
resumen = df.groupby("Tipo_Contenido").agg({
    "Duracion_Estimada_min": "mean",
    "Duracion_Real_min": "mean",
    "Completitud_%": "mean"
}).round(2)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "Informe de Tiempos y Completitud – Formación Online", ln=True, align="C")
pdf.ln(10)

for tipo in resumen.index:
    r = resumen.loc[tipo]
    pdf.cell(200, 10, f"{tipo}:", ln=True)
    pdf.cell(200, 10, f"- Duración estimada media: {r['Duracion_Estimada_min']} min", ln=True)
    pdf.cell(200, 10, f"- Duración real media: {r['Duracion_Real_min']} min", ln=True)
    pdf.cell(200, 10, f"- Completitud promedio: {r['Completitud_%']}%", ln=True)
    pdf.ln(5)

pdf.output("output/resumen_tiempos.pdf")
print("Análisis finalizado.")
