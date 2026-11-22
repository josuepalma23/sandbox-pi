# laboratorio_cafe_solucion.py — Laboratorio integrador CaféAndino (SOLUCIÓN)
# Ejecuta desde la raíz del repositorio:
#   python scripts/laboratorio_cafe_solucion.py
#
# Requiere: pandas, numpy, scipy, matplotlib.
#
# Contenido (solo temas de los laboratorios 2, 3 y 4):
#   Parte A: clasificación de variables           (clientes_cafe.csv)
#   Parte B: población vs. muestra                (clientes_500.csv)
#   Parte C: experimento pareado + IC + prueba t  (registro_experimento_cafe.csv)
#   Parte D: gráficos de barras y pastel          (ventas_diarias_cafe.csv)

import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # permite ejecutar sin pantalla

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from pandas.api.types import CategoricalDtype
from scipy import stats

pd.set_option("display.width", 100)

# Rutas relativas a la raíz del repositorio (este script vive en scripts/)
RAIZ = Path(__file__).resolve().parent.parent
AZUL, ORO = "#205080", "#8a6d1f"
SALIDA = RAIZ / "figuras"
SALIDA.mkdir(exist_ok=True)


# ===========================================================================
# PARTE A — CLASIFICACIÓN DE VARIABLES
# ===========================================================================
def parte_a():
    print("\n" + "=" * 70 + "\nPARTE A — Clasificación de variables\n" + "=" * 70)

    # TODO 1: cargar y mirar la estructura
    clientes = pd.read_csv(RAIZ / "data" / "clientes_cafe.csv")
    print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas\n")
    print(clientes.to_string(index=False), "\n")

    # TODO 2: tipos inferidos (dtype) — solo una pista
    print("Tipos inferidos (dtype):")
    print(clientes.dtypes, "\n")
    # Llegan como número: cliente_id, edad, num_mascotas, gasto_mensual (float)
    # y calificacion_servicio (int, pero es ORDINAL: "4 no es el doble de 2").
    # Llegan como texto: genero, nivel_estudios, ciudad, frecuencia_visita, suscrito.

    # TODO 3: valores únicos por columna
    for columna in clientes.columns:
        valores = clientes[columna].unique().tolist()
        print(f"{columna}: {len(valores)} valores distintos -> {valores}")
    print()
    # genero tiene 3 categorías (F, M, Otro); suscrito tiene 2 (binaria).

    # TODO 4: nivel_estudios como categoría ordenada
    nivel_texto = clientes["nivel_estudios"].copy()  # copia para la prueba del typo
    orden_estudios = CategoricalDtype(
        categories=["Bachillerato", "Tecnico", "Grado", "Maestria"], ordered=True
    )
    clientes["nivel_estudios"] = clientes["nivel_estudios"].astype(orden_estudios)
    print("Estudios mínimo:", clientes["nivel_estudios"].min())  # Bachillerato
    print("Estudios máximo:", clientes["nivel_estudios"].max())  # Maestria

    # TODO 5: frecuencia_visita y calificacion_servicio también son ordinales
    orden_frecuencia = CategoricalDtype(
        categories=["Ocasional", "Semanal", "Diaria"], ordered=True
    )
    clientes["frecuencia_visita"] = clientes["frecuencia_visita"].astype(orden_frecuencia)

    orden_calificacion = CategoricalDtype(categories=[1, 2, 3, 4, 5], ordered=True)
    clientes["calificacion_servicio"] = clientes["calificacion_servicio"].astype(
        orden_calificacion
    )
    print("Frecuencia mínima:", clientes["frecuencia_visita"].min())  # Ocasional
    print("Calificación mínima:", clientes["calificacion_servicio"].min())  # 2 (nadie puso 1)
    print("Calificación máxima:", clientes["calificacion_servicio"].max())  # 5

    # Prueba extra: el typo silencioso ("Maestría" con tilde no coincide con "Maestria")
    # Las versiones nuevas de pandas ya avisan de este caso con una advertencia
    # (y en el futuro lanzarán error); la silenciamos aquí para ver el efecto.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        con_typo = nivel_texto.astype(
            CategoricalDtype(
                categories=["Bachillerato", "Tecnico", "Grado", "Maestría"], ordered=True
            )
        )
    print("Faltantes por el typo 'Maestría':", con_typo.isna().sum())  # 3, sin ningún error

    # TODO 6: resumen de la clasificación
    clasificacion = {
        "cliente_id": "Identificador",
        "edad": "Numérica discreta",
        "num_mascotas": "Numérica discreta",
        "genero": "Categórica nominal",
        "nivel_estudios": "Categórica ordinal",
        "ciudad": "Categórica nominal",
        "gasto_mensual": "Numérica continua",
        "frecuencia_visita": "Categórica ordinal",
        "suscrito": "Categórica binaria",
        "calificacion_servicio": "Categórica ordinal",
    }
    print("\nResumen de la clasificación (para el informe):")
    for variable, tipo in clasificacion.items():
        print(f"  {variable:22s} {tipo}")


# ===========================================================================
# PARTE B — POBLACIÓN VS. MUESTRA
# ===========================================================================
def reporte(nombre, muestra, parametro):
    """Imprime n, media estimada y composición por ciudad de una muestra."""
    n = len(muestra)
    media = muestra["gasto_mensual"].mean()
    comp = muestra["ciudad"].value_counts().to_dict()
    print(f"[{nombre}] n={n}  media={media:.2f} USD  "
          f"(parámetro {parametro:.2f}, diferencia {media - parametro:+.2f})")
    print(f"    composición por ciudad: {comp}")


def parte_b():
    print("\n" + "=" * 70 + "\nPARTE B — Población vs. muestra\n" + "=" * 70)

    # TODO 1: la población (N = 500) y su parámetro
    poblacion = pd.read_csv(RAIZ / "data" / "clientes_500.csv")
    parametro = poblacion["gasto_mensual"].mean()
    print(f"Población: {poblacion.shape[0]} clientes × {poblacion.shape[1]} columnas")
    print(f"Parámetro poblacional — gasto medio: {parametro:.2f} USD")
    print("Ciudades:", poblacion["ciudad"].value_counts().to_dict(), "\n")

    # TODO 2: muestra por conveniencia (30 primeras filas)
    muestra_conv = poblacion.head(30)
    # Sesgo de selección: el archivo está ordenado por ciudad, así que head(30)
    # solo trae clientes de Quito; Guayaquil y Cuenca no aparecen.

    # TODO 3: muestra aleatoria simple de 30 (6 %) y variabilidad entre semillas
    muestra_aas = poblacion.sample(30, random_state=1)
    for semilla in range(1, 6):
        m = poblacion.sample(30, random_state=semilla)
        print(f"Semilla {semilla}: gasto medio = {m['gasto_mensual'].mean():.2f} | "
              f"calificación media = {m['calificacion_servicio'].mean():.2f}")
    print()

    # TODO 4: muestra estratificada, 6 % por ciudad (15 Quito, 9 Guayaquil, 6 Cuenca)
    muestra_est = poblacion.groupby("ciudad", group_keys=False).sample(
        frac=0.06, random_state=1
    )
    print(muestra_est["ciudad"].value_counts(), "\n")
    # Garantiza que la muestra respete las proporciones reales de cada estrato.

    # TODO 5: comparación final
    reporte("Conveniencia", muestra_conv, parametro)
    reporte("Aleatorio simple", muestra_aas, parametro)
    reporte("Estratificado", muestra_est, parametro)
    print()

    resumen = pd.DataFrame([
        {"diseño": "Conveniencia (head)", "n": len(muestra_conv),
         "media estimada": round(muestra_conv["gasto_mensual"].mean(), 2)},
        {"diseño": "Aleatorio simple (sample)", "n": len(muestra_aas),
         "media estimada": round(muestra_aas["gasto_mensual"].mean(), 2)},
        {"diseño": "Estratificado (groupby + frac)", "n": len(muestra_est),
         "media estimada": round(muestra_est["gasto_mensual"].mean(), 2)},
    ])
    print(f"Parámetro poblacional: {parametro:.2f} USD")
    print(resumen.to_string(index=False))


# ===========================================================================
# PARTE C — EXPERIMENTO PAREADO
# ===========================================================================
def parte_c():
    print("\n" + "=" * 70 + "\nPARTE C — Experimento pareado: menú digital vs. impreso\n" + "=" * 70)

    # TODO 1: cargar el registro y explorarlo
    df = pd.read_csv(RAIZ / "data" / "registro_experimento_cafe.csv")
    print(df.head(), "\n")
    print(df.groupby("formato_menu")["ventas_combo"].mean(), "\n")
    print(df["formato_menu"].value_counts(), "\n")  # 16 y 16: diseño balanceado

    # TODO 2: diseñar un experimento NUEVO para otras 6 tiendas (sorteo + alternancia)
    tiendas = ["Riobamba", "Ibarra", "Esmeraldas", "Portoviejo", "Babahoyo", "Tulcan"]
    semanas = [1, 2, 3, 4]

    rng = np.random.default_rng(2027)
    primera = rng.choice(["menu_digital", "menu_impreso"], size=len(tiendas))
    print("Condición inicial por tienda:", primera)

    filas = []
    for tienda, cond in zip(tiendas, primera):
        otra = "menu_impreso" if cond == "menu_digital" else "menu_digital"
        for s in semanas:
            filas.append({"tienda": tienda, "semana": s,
                          "formato_menu": cond if s % 2 == 1 else otra})
    diseno = pd.DataFrame(filas)

    # TODO 3: simular las ventas del diseño nuevo
    rng = np.random.default_rng(2028)
    efecto_tienda = dict(zip(tiendas, rng.normal(850, 90, len(tiendas))))
    efecto_semana = {1: 0, 2: 20, 3: 40, 4: 60}
    diseno["ventas_combo"] = (
        diseno["tienda"].map(efecto_tienda)
        + diseno["semana"].map(efecto_semana)
        + (diseno["formato_menu"] == "menu_digital") * 150
        + rng.normal(0, 60, len(diseno))
    ).round(0).astype(int)

    # TODO 4: una promoción simultánea en una tienda y semana (variable de confusión)
    diseno["promocion_simultanea"] = "no"
    diseno.loc[(diseno["tienda"] == "Ibarra") & (diseno["semana"] == 2),
               "promocion_simultanea"] = "si"
    diseno.loc[diseno["promocion_simultanea"] == "si", "ventas_combo"] += 140
    print("\nDiseño simulado (primeras filas):")
    print(diseno.head(8), "\n")

    # TODO 5: análisis pareado SOBRE EL REGISTRO REAL (df): una fila por tienda
    piv = df.groupby(["tienda", "formato_menu"])["ventas_combo"].mean().unstack()
    piv["diferencia"] = piv["menu_digital"] - piv["menu_impreso"]
    print(piv.round(1), "\n")

    media = piv["diferencia"].mean()
    dev = piv["diferencia"].std(ddof=1)
    n = len(piv)
    print(f"Diferencia media: {media:.2f} | desviación: {dev:.2f} | n = {n}")

    # TODO 6: intervalo de confianza del 95 %
    t_crit = stats.t.ppf(0.975, df=n - 1)
    error = dev / n ** 0.5
    ic_inf, ic_sup = media - t_crit * error, media + t_crit * error
    print(f"IC 95 %: ({ic_inf:.2f}, {ic_sup:.2f})")

    # TODO 7: prueba t pareada
    prueba = stats.ttest_rel(piv["menu_digital"], piv["menu_impreso"])
    print(f"t = {prueba.statistic:.3f} | p-value = {prueba.pvalue:.8f}")


# ===========================================================================
# PARTE D — GRÁFICOS DE BARRAS Y PASTEL
# ===========================================================================
def guardar(fig, nombre):
    """Guarda la figura como PNG y libera la memoria."""
    fig.tight_layout()
    fig.savefig(SALIDA / f"{nombre}.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def formato_miles(valor, posicion):
    """Escribe los números con separador de miles (ej. 12,000)."""
    return f"{valor:,.0f}"


def parte_d():
    print("\n" + "=" * 70 + "\nPARTE D — Gráficos de barras y pastel\n" + "=" * 70)

    # TODO 1: cargar los datos
    ventas = pd.read_csv(RAIZ / "data" / "ventas_diarias_cafe.csv")

    # TODO 2: tablas de frecuencia (absoluta y relativa)
    dias_region = ventas["region"].value_counts()
    dias_region_rel = ventas["region"].value_counts(normalize=True)
    dias_sucursal = ventas["sucursal"].value_counts()
    dias_sucursal_rel = ventas["sucursal"].value_counts(normalize=True)

    print("Suma de días por región:", dias_region.sum())           # debe dar 300
    print("Suma relativa por región:", dias_region_rel.sum())      # debe dar 1.0
    print("Suma de días por sucursal:", dias_sucursal.sum())       # debe dar 300
    print("Suma relativa por sucursal:", dias_sucursal_rel.sum())  # debe dar 1.0

    # TODO 3: barras de días por región (verticales, desde cero)
    fig, ax = plt.subplots(figsize=(6, 4))
    dias_region.plot(kind="bar", ax=ax, color=AZUL)
    ax.set_title("Días registrados por región")
    ax.set_xlabel("Región")
    ax.set_ylabel("Días registrados")
    ax.set_ylim(0, dias_region.max() * 1.1)
    ax.tick_params(axis="x", rotation=0)
    guardar(fig, "barras_dias_region")

    # TODO 4: barras de días por sucursal (horizontales, ordenadas)
    fig, ax = plt.subplots(figsize=(7, 4))
    dias_sucursal.sort_values().plot(kind="barh", ax=ax, color=AZUL)  # mayor arriba
    ax.set_title("Días registrados por sucursal")
    ax.set_xlabel("Días registrados")
    ax.set_ylabel("Sucursal")
    ax.set_xlim(0, dias_sucursal.max() * 1.1)
    guardar(fig, "barras_dias_sucursal")

    # TODO 5: volumen por región y por sucursal, y venta media por día
    volumen_region = ventas.groupby("region")["ventas"].sum()
    volumen_sucursal = ventas.groupby("sucursal")["ventas"].sum()
    media_region = volumen_region / dias_region
    media_sucursal = volumen_sucursal / dias_sucursal

    # TODO 6: barras de volumen
    fig, ax = plt.subplots(figsize=(6, 4))
    volumen_region.plot(kind="bar", ax=ax, color=AZUL)
    ax.set_title("Volumen de ventas por región")
    ax.set_xlabel("Región")
    ax.set_ylabel("Ventas (USD)")
    ax.set_ylim(0, volumen_region.max() * 1.1)
    ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    ax.tick_params(axis="x", rotation=0)
    guardar(fig, "barras_volumen_region")

    fig, ax = plt.subplots(figsize=(7, 4))
    volumen_sucursal.sort_values().plot(kind="barh", ax=ax, color=AZUL)
    ax.set_title("Volumen de ventas por sucursal")
    ax.set_xlabel("Ventas (USD)")
    ax.set_ylabel("Sucursal")
    ax.set_xlim(0, volumen_sucursal.max() * 1.1)
    ax.xaxis.set_major_formatter(FuncFormatter(formato_miles))
    guardar(fig, "barras_volumen_sucursal")

    # TODO 7: pastel de región (2 categorías)
    fig, ax = plt.subplots(figsize=(5, 5))
    dias_region.plot(kind="pie", ax=ax, autopct="%.1f%%", startangle=90, colors=[AZUL, ORO])
    ax.set_ylabel("")
    ax.set_title("Proporción de días por región")
    guardar(fig, "pastel_dias_region")

    # TODO 8: pastel de sucursal (5 categorías, participación por volumen)
    fig, ax = plt.subplots(figsize=(6, 6))
    volumen_sucursal.sort_values(ascending=False).plot(
        kind="pie", ax=ax, autopct="%.1f%%", startangle=90
    )
    ax.set_ylabel("")
    ax.set_title("Participación de cada sucursal en el volumen de ventas")
    guardar(fig, "pastel_volumen_sucursal")

    # TODO 9: tablas de referencia y confirmación de los 6 gráficos
    tabla_region = pd.DataFrame({
        "dias": dias_region,
        "proporcion_dias": dias_region_rel,
        "ventas_usd": volumen_region,
        "media_por_dia": media_region,
    })
    tabla_sucursal = pd.DataFrame({
        "dias": dias_sucursal,
        "proporcion_dias": dias_sucursal_rel,
        "ventas_usd": volumen_sucursal,
        "media_por_dia": media_sucursal,
    })
    print("\nTabla por región:")
    print(tabla_region)
    print("\nTabla por sucursal:")
    print(tabla_sucursal)
    print("\nGráficos generados: 6")
    print(f"Listo: revisa los gráficos en {SALIDA}/")


def main():
    parte_a()
    parte_b()
    parte_c()
    parte_d()


if __name__ == "__main__":
    main()
