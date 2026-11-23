## GRAFICOS AIDAN

import pandas as  pd 
import matplotlib.pyplot as plt 
from matplotlib.ticker import FuncFormatter 

Azul, Oro = "#205080", "#8a6d1f"
ventas = pd.read_csv('practica_examen_esPro/ventas_diarias.csv')

# Calculo de frecuencias Absolutas 
region_frec_abs = ventas['region'].value_counts()
sucursal_frec_abs = ventas['sucursal'].value_counts()

#Frecuencia relativa
region_frec_relativa = ventas['region'].value_counts(normalize=True)
sucursal_frec_relativa = ventas['sucursal'].value_counts(normalize=True)

#Grafico de barras de Ventas por dias en region y sucursales
fig, ax = plt.subplots(figsize=(5,4))
region_frec_abs.plot(
    kind="bar",
    ax=ax,
    color=Azul,
    rot=False
)
ax.set_title("Ventas por Region")
ax.set_xlabel("Region")
ax.set_ylabel("Ventas")
ax.set_ylim(0,200)
fig.tight_layout()
plt.show()

#Grafico de ventas por sucursal 
fig,ax = plt.subplots(figsize=(6,8))
sucursal_frec_abs.sort_values(ascending=True).plot(
    kind="barh",
    ax=ax,
    color=Azul
)
ax.set_title("Ventas por sucursales")
ax.set_ylabel("sucursales")
ax.set_xlabel("Ventas")
ax.set_xlim(0, 60)
fig.tight_layout()
plt.show()

# Volumenes de sucursales
volumen_region = ventas.groupby('region')['ventas'].sum()
volumen_sucursal = ventas.groupby('sucursal')['ventas'].sum()

#Porcentaje de aporte de region y sucursal en las ventas 
pct_vol_region = volumen_region / region_frec_abs.sum()
pct_vol_sucursal = volumen_sucursal / sucursal_frec_abs.sum()

#Grafico de pastel de Ventas de los dias por region 
fig, ax = plt.subplots(figsize=(6,7))
region_frec_abs.plot(
        kind="pie",
        autopct="%.1f%%",
        startangle=90,
        colors=[Azul, Oro],
        wedgeprops={"edgecolor": "white"},
        ax=ax,
    )
for texto in ax.texts:
    if "%" in texto.get_text():
            texto.set_color("white")
            texto.set_fontweight("bold")
    ax.set_title("Proporción de días por región")
    ax.set_ylabel("")
    ax.set_aspect("equal")
    fig.tight_layout()
    plt.show()
    
