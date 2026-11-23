## SNIPPET 1


import matplotlib

'''
Pasos del diseño de un experimento
a) Definir poblacion objetivo y tratamientos
b) establecer un grupo de control
c) Aplicar la aleatorizacion
d) Implementar cegamiento
e) Analisis estadistico y conclusion
'''



matplotlib.use("Agg")  # permite ejecutar sin pantalla

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from pandas.api.types import CategoricalDtype
from scipy import stats

pd.set_option("display.width", 100)

# ===========================================================================
# LAB 2A — CLASIFICACIÓN DE VARIABLES
# ===========================================================================
clientes = pd.read_csv("data/clientes.csv")

print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas")
print(clientes.to_string(index=False))

# Tipos inferidos (dtype)
print(clientes.dtypes)

# Valores únicos por columna
for columna in clientes.columns:
    valores = clientes[columna].unique().tolist()
    cantidad = len(valores)
    print(f"{columna}: {cantidad} categorias -> {valores}")
    print()

# Variable ordinal como categoría ordenada
orden_niveles = CategoricalDtype(
    categories=["Primaria", "Secundaria", "Universidad", "Posgrado"],
    ordered=True
)
clientes["nivel_educacion"] = clientes["nivel_educacion"].astype(orden_niveles)
print(clientes["nivel_educacion"].min())
print(clientes["nivel_educacion"].max())

# Escala numérica como categoría ordenada
orden_satisfaccion = CategoricalDtype(
    categories=[1, 2, 3, 4, 5],
    ordered=True
)
clientes["satisfaccion"] = clientes["satisfaccion"].astype(orden_satisfaccion)
print(clientes["satisfaccion"].min())
print(clientes["satisfaccion"].max())

# Prueba del typo: una categoría mal escrita no da error, da NaN
print(clientes["nivel_educacion"].isna().sum())

# Resumen de la clasificación
clasificacion = {
    "cliente_id": "Identificador",
    "edad": "Numerica Discreta",
    "numero_hijos": "Numerica Discreta",
    "genero": "Categorica Nominal",
    "nivel_educacion": "Categorica Ordinal",
    "ciudad": "Categorica nominal",
    "ingresos_mensuales": "Numerica continua",
    "satisfaccion": "Categorica Ordinal",
}
print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")

# ===========================================================================
# LAB 2B — POBLACIÓN VS. MUESTRA
# ===========================================================================
def reporte(nombre, muestra, parametro):
    """Imprime n, media estimada y composición por ciudad de una muestra."""
    n = len(muestra)
    media = muestra["ingresos_mensuales"].mean()
    comp = muestra["ciudad"].value_counts().to_dict()
    print(f"[{nombre}] n={n}  media={media:.2f} USD  "
          f"(parámetro {parametro:.2f}, diferencia {media - parametro:+.2f})")
    print(f"    composición por ciudad: {comp}")


# La población y su parámetro
poblacion = pd.read_csv("data/clientes_400.csv")
parametro = poblacion["ingresos_mensuales"].mean()
print(f"Población: {poblacion.shape[0]} clientes × {poblacion.shape[1]} columnas")
print(f"Parámetro poblacional — ingreso medio: {parametro:.2f} USD")
print("Ciudades en la población:", poblacion["ciudad"].value_counts().to_dict())
print()

# Muestra por conveniencia
muestra_conv = poblacion.head(20)
print(muestra_conv)

# Muestra aleatoria simple
muestra_aas = poblacion.sample(20, random_state=1)
print(muestra_aas)

# Variabilidad entre semillas
for semilla in range(1, 6):
    muestra = poblacion.sample(20, random_state=semilla)
    media_ingresos = muestra["ingresos_mensuales"].mean()
    media_satisfaccion = muestra["satisfaccion"].mean()
    print(f"Semilla {semilla}: media de ingresos = {media_ingresos:.2f}\n")
    print(f"Semilla {semilla}: media de satisfaccion = {media_satisfaccion:.2f}\n")

# Muestra estratificada
muestra_est = poblacion.groupby("ciudad", group_keys=False).sample(frac=0.05, random_state=1)
print(muestra_est["ciudad"].value_counts())

# Comparación final
reporte("Conveniencia", muestra_conv, parametro)
reporte("Aleatorio simple", muestra_aas, parametro)
reporte("Estratificado", muestra_est, parametro)
print()

resumen = pd.DataFrame([
    {"diseño": "Conveniencia (head)", "n": len(muestra_conv),
     "media estimada": round(muestra_conv["ingresos_mensuales"].mean(), 2)},
    {"diseño": "Aleatorio simple (sample)", "n": len(muestra_aas),
     "media estimada": round(muestra_aas["ingresos_mensuales"].mean(), 2)},
    {"diseño": "Estratificado (groupby + frac)", "n": len(muestra_est),
     "media estimada": round(muestra_est["ingresos_mensuales"].mean(), 2)},
])
print(f"Parámetro poblacional: {parametro:.2f} USD")
print(resumen.to_string(index=False))

# ===========================================================================
# LAB 3 — EXPERIMENTO PAREADO
# ===========================================================================
df = pd.read_csv("plantillas/registro_experimento.csv")

print(df.head())
# Promedio por ubicacion
print(df.groupby("ubicacion")["ventas_producto"].mean())
print("")
# Contar los registros de cada ubicacion
print(df["ubicacion"].value_counts())

# Simulación de la cantidad de tiendas
tiendas = ["Quito_Norte", "Quito_Sur", "Guayaquil_Centro", "Guayaquil_Norte", "Cuenca_Norte", "Cuenca_Sur", "Ambato_Centro", "Loja", "Machala"]
semanas = [1, 2, 3, 4]

# Sorteo de la condicion inicial
rng = np.random.default_rng(1234597)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))
print(primera)
filas = []

for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond == "pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({"tienda": tienda, "semana": s, "ubicacion": cond if s % 2 == 1 else otra})

diseno = pd.DataFrame(filas)

# Simulación de la ejecución
rng = np.random.default_rng(1234598)
efecto_tienda = dict(zip(tiendas, rng.normal(1100, 120, len(tiendas))))
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}
diseno['ventas_producto'] = (diseno['tienda'].map(efecto_tienda) + diseno['semana'].map(efecto_semana)
                             + (diseno['ubicacion'] == "pasillo_principal") * 220
                             + rng.normal(0, 90, len(diseno))
                             ).round(0).astype(int)

diseno['promocion_simultanea'] = 'no'

# El loc hace que se cumpla una condicion; despues de la coma va la columna en la que se asigna
diseno.loc[(diseno['tienda'] == 'Guayaquil_Centro') & (diseno['semana'] == 1), 'promocion_simultanea'] = 'si'
diseno.loc[diseno['promocion_simultanea'] == 'si', 'ventas_producto'] += 180

print(diseno)

# Análisis pareado: una fila por tienda con sus condiciones
piv = diseno.groupby(['tienda', 'ubicacion'])['ventas_producto'].mean().unstack()
piv['diferencia'] = piv['pasillo_principal'] - piv['habitual']

media = round(piv['diferencia'].mean(), 2)
dev = round(piv['diferencia'].std(ddof=1), 2)
print(media)
print(dev)
print(piv)
n = len(piv)
t_crict = stats.t.ppf(0.975, df=n - 1)
ic_inf = media - (t_crict * dev / n ** 0.5)
ic_sup = media + (t_crict * dev / n ** 0.5)
print(round(ic_sup, 2))
print(round(t_crict, 2))

# Con 95% de confianza la diferencia promedio entre pasillo principal y habitual cae en este rango
print(f"{ic_inf:.5f} - {ic_sup:.5f}")

# Prueba p-value
prueba = stats.ttest_rel(piv["pasillo_principal"], piv["habitual"])

print(f" Prueba P-value:  {prueba.pvalue:.10f}")

# ===========================================================================
# LAB 4 — GRÁFICOS DE BARRAS Y PASTEL
# ===========================================================================

##GRAFICOS
AZUL, ORO = "#205080", "#8a6d1f"


def guardar(fig, nombre):
    """Guarda la figura como PNG y libera la memoria."""
    fig.tight_layout()
    fig.savefig(f"{nombre}.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def formato_miles(valor, posicion):
    """Escribe los números con separador de miles (ej. 12,000)."""
    return f"{valor:,.0f}"


ventas = pd.read_csv("data/ventas_diarias.csv")

# Tablas de frecuencia (absoluta y relativa)
dias_region = ventas["region"].value_counts()
dias_region_rel = ventas["region"].value_counts(normalize=True)

dias_sucursal = ventas["sucursal"].value_counts()
dias_sucursal_rel = ventas["sucursal"].value_counts(normalize=True)

print("Suma de días por región:", dias_region.sum())
print("Suma relativa por región:", dias_region_rel.sum())
print("Suma de días por sucursal:", dias_sucursal.sum())
print("Suma relativa por sucursal:", dias_sucursal_rel.sum())

# Barras de días por región
fig, ax = plt.subplots(figsize=(6, 4))
dias_region.plot(kind="bar", ax=ax, color=AZUL)
ax.set_title("Días registrados por región")
ax.set_xlabel("Región")
ax.set_ylabel("Días registrados")
ax.set_ylim(0, dias_region.max() * 1.1)
ax.tick_params(axis="x", rotation=0)
guardar(fig, "barras_dias_region")

# Barras de días por sucursal (horizontales, ordenadas)
dias_sucursal_ordenado = dias_sucursal.sort_values()
fig, ax = plt.subplots(figsize=(7, 4))
dias_sucursal_ordenado.plot(kind="barh", ax=ax, color=AZUL)
ax.set_title("Días registrados por sucursal")
ax.set_xlabel("Días registrados")
ax.set_ylabel("Sucursal")
ax.set_xlim(0, dias_sucursal.max() * 1.1)
guardar(fig, "barras_dias_sucursal")

# Volumen por región y por sucursal, y venta media por día
volumen_region = ventas.groupby("region")["ventas"].sum()
volumen_sucursal = ventas.groupby("sucursal")["ventas"].sum()

media_region = volumen_region / dias_region
media_sucursal = volumen_sucursal / dias_sucursal

# Barras de volumen por región
fig, ax = plt.subplots(figsize=(6, 4))
volumen_region.plot(kind="bar", ax=ax, color=AZUL)
ax.set_title("Volumen de ventas por región")
ax.set_xlabel("Región")
ax.set_ylabel("Ventas (USD)")
ax.set_ylim(0, volumen_region.max() * 1.1)
ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
ax.tick_params(axis="x", rotation=0)
guardar(fig, "barras_volumen_region")

# Barras de volumen por sucursal (horizontales, ordenadas por magnitud)
volumen_sucursal_ordenado = volumen_sucursal.sort_values()
fig, ax = plt.subplots(figsize=(7, 4))
volumen_sucursal_ordenado.plot(kind="barh", ax=ax, color=AZUL)
ax.set_title("Volumen de ventas por sucursal")
ax.set_xlabel("Ventas (USD)")
ax.set_ylabel("Sucursal")
ax.set_xlim(0, volumen_sucursal.max() * 1.1)
ax.xaxis.set_major_formatter(FuncFormatter(formato_miles))
guardar(fig, "barras_volumen_sucursal")

# Pastel de región (2 categorías)
fig, ax = plt.subplots(figsize=(5, 5))
dias_region.plot(kind="pie", ax=ax, autopct="%.1f%%", startangle=90, colors=[AZUL, ORO])
ax.set_ylabel("")
ax.set_title("Proporción de días por región")
guardar(fig, "pastel_dias_region")

# Pastel de sucursal (participación por volumen)
volumen_sucursal_mayor = volumen_sucursal.sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(6, 6))
volumen_sucursal_mayor.plot(kind="pie", ax=ax, autopct="%.1f%%", startangle=90)
ax.set_ylabel("")
ax.set_title("Participación de cada sucursal en el volumen de ventas")
guardar(fig, "pastel_volumen_sucursal")

# Tablas de referencia
tabla_region = pd.DataFrame(
    {
        "dias": dias_region,
        "proporcion_dias": dias_region_rel,
        "ventas_usd": volumen_region,
        "media_por_dia": media_region,
    }
)
tabla_sucursal = pd.DataFrame(
    {
        "dias": dias_sucursal,
        "proporcion_dias": dias_sucursal_rel,
        "ventas_usd": volumen_sucursal,
        "media_por_dia": media_sucursal,
    }
)

print("\nTabla por región:")
print(tabla_region)
print("\nTabla por sucursal:")
print(tabla_sucursal)