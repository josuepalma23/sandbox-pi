# laboratorio_cafe.py — Laboratorio integrador CaféAndino (VERSIÓN CON TODOs)
# Ejecuta desde la raíz del repositorio:
#   python scripts/laboratorio_cafe.py
#
# Requiere: pandas, numpy, scipy, matplotlib.
#
# CaféAndino es una cadena de cafeterías en Ecuador. Este laboratorio reúne
# los temas de los laboratorios 2, 3 y 4:
#   Parte A: clasificación de variables           (data/clientes_cafe.csv)
#   Parte B: población vs. muestra                (data/clientes_500.csv)
#   Parte C: experimento pareado + IC + prueba t  (data/registro_experimento_cafe.csv)
#   Parte D: gráficos de barras y pastel          (data/ventas_diarias_cafe.csv)

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
RAIZ = Path(__file__).resolve().parent.parent   # Sesgos_IC_Estadistica (aquí queda figuras/)
DATOS = Path(__file__).resolve().parent         # practica_examen_esPro (aquí están los CSV)
AZUL, ORO = "#205080", "#8a6d1f"
SALIDA = RAIZ / "figuras"
SALIDA.mkdir(exist_ok=True)


# ===========================================================================
# PARTE A — CLASIFICACIÓN DE VARIABLES
# ===========================================================================
# data/clientes_cafe.csv tiene 12 clientes y 10 columnas. Objetivo: clasificar
# cada variable (numérica continua/discreta, categórica binaria/ordinal/nominal)
# y verificar la clasificación en código.
# Regla: el dtype es una pista, no la clasificación; decide el criterio
# (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?).
def parte_a():
    print("\n" + "=" * 70 + "\nPARTE A — Clasificación de variables\n" + "=" * 70)

    # TODO 1: carga data/clientes_cafe.csv en `clientes` e imprime sus
    #         dimensiones y la tabla completa.
    #         Pista: pd.read_csv(RAIZ / "data" / "..."), .shape, .to_string(index=False)
    clientes = pd.read_csv(DATOS / "clientes_cafe.csv")
    print(clientes.to_string(index=False))
    print(clientes.shape)

    # TODO 2: imprime los tipos inferidos (dtype). Anota en el informe qué
    #         columnas llegan como número y cuáles como texto. Ojo con
    #         calificacion_servicio: llega como número (1 a 5), pero ¿es una
    #         cantidad medible? ("4 no es el doble de 2").
    #         Pista: clientes.dtypes
    print(clientes.dtypes)

    # TODO 3: recorre las columnas e imprime cuántos valores únicos tiene cada
    #         una y cuáles son. ¿Cuántas categorías tiene genero? ¿Y suscrito?
    #         Pista: for columna in clientes.columns: ...  .unique().tolist() y len()
    for columna in clientes.columns:
        valores_unicos = clientes[columna].unique().tolist()
        numero = len(valores_unicos)
        # CORREGIDO: el print va DENTRO del bucle (antes solo salía la última columna)
        print(f"{columna}: {numero} valores distintos -> {valores_unicos}")

    # TODO 4: convierte nivel_estudios a categoría ordenada
    #         (Bachillerato < Tecnico < Grado < Maestria). Comprueba con .min()
    #         y .max(). Antes de convertir, guarda una copia del texto original
    #         en `nivel_texto` (la necesitas para la prueba extra).
    #         Pista: CategoricalDtype(categories=[...], ordered=True) y .astype(...)
    # CORREGIDO: nivel_texto es una COPIA del texto original, tomada ANTES de convertir
    nivel_texto = clientes["nivel_estudios"].copy()

    orden_estudios = CategoricalDtype(
        categories=["Bachillerato", "Tecnico", "Grado", "Maestria"],
        ordered=True
    )
    clientes["nivel_estudios"] = clientes["nivel_estudios"].astype(orden_estudios)
    print(clientes["nivel_estudios"].min())
    print(clientes["nivel_estudios"].max())

    # TODO 5: haz lo mismo con frecuencia_visita (Ocasional < Semanal < Diaria)
    #         y con calificacion_servicio (escala 1–5). ¿Qué devuelve .min() en
    #         calificacion_servicio y por qué no es 1?
    #
    #         Prueba extra: crea el tipo de nivel_estudios escribiendo "Maestría"
    #         (con tilde) en la lista de categorías y aplícalo sobre nivel_texto.
    #         Cuenta los faltantes con .isna().sum(): ¿qué pasó y por qué no hubo
    #         ningún error? (Si pandas muestra una advertencia, es lo esperado.)
    orden_frecuencia = CategoricalDtype(
        categories=["Ocasional", "Semanal", "Diaria"],
        ordered=True
    )
    clientes["frecuencia_visita"] = clientes["frecuencia_visita"].astype(orden_frecuencia)
    print(clientes["frecuencia_visita"].min())
    print(clientes["frecuencia_visita"].max())

    print("Faltantes: ", clientes["frecuencia_visita"].isna().sum())

    # CORREGIDO: faltaba calificacion_servicio
    orden_calificacion = CategoricalDtype(categories=[1, 2, 3, 4, 5], ordered=True)
    clientes["calificacion_servicio"] = clientes["calificacion_servicio"].astype(orden_calificacion)
    print(clientes["calificacion_servicio"].min())   # 2: nadie puso 1
    print(clientes["calificacion_servicio"].max())   # 5

    # CORREGIDO: faltaba la prueba extra del typo "Maestría" (con tilde)
    orden_con_typo = CategoricalDtype(
        categories=["Bachillerato", "Tecnico", "Grado", "Maestría"],
        ordered=True
    )
    nivel_con_typo = nivel_texto.astype(orden_con_typo)
    print("Faltantes con typo:", nivel_con_typo.isna().sum())   # 3

    # TODO 6: completa el resumen con el tipo de cada variable (el criterio que
    #         justifica cada clasificación va en el informe).
    # CORREGIDO: el resumen pide el TIPO DE VARIABLE, no el dtype
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
    print("Resumen de la clasificación (para el informe):")
    for variable, tipo in clasificacion.items():
        print(f"  {variable:22s} {tipo}")


# ===========================================================================
# PARTE B — POBLACIÓN VS. MUESTRA
# ===========================================================================
# La población es la base completa de clientes: data/clientes_500.csv (N = 500).
# Pregunta de negocio: ¿cuál es el gasto mensual promedio de los clientes?
# Se estima con tres diseños de muestreo (n = 30 en cada uno) y se compara con
# el parámetro real, que aquí sí se conoce.
def reporte(nombre, muestra, parametro):
    """Imprime n, media estimada y composición por ciudad de una muestra.

    La composición por ciudad es la pista que delata un sesgo de selección.
    """
    n = len(muestra)
    media = muestra["gasto_mensual"].mean()
    comp = muestra["ciudad"].value_counts().to_dict()
    print(f"[{nombre}] n={n}  media={media:.2f} USD  "
          f"(parámetro {parametro:.2f}, diferencia {media - parametro:+.2f})")
    print(f"    composición por ciudad: {comp}")


def parte_b():
    print("\n" + "=" * 70 + "\nPARTE B — Población vs. muestra\n" + "=" * 70)

    # TODO 1: carga la población en `poblacion` y calcula el `parametro`
    #         (media de gasto_mensual). Imprime sus dimensiones, el parámetro y
    #         el conteo de clientes por ciudad.
    #         Pista: .mean(), .value_counts().to_dict()
    poblacion = pd.read_csv(DATOS / "clientes_500.csv")
    parametro = poblacion["gasto_mensual"].mean()
    print(f"El dataset tiene {poblacion.shape[0]} filas x {poblacion.shape[1]} columnas.")
    # CORREGIDO: faltaba imprimir el parámetro y contar por la columna "ciudad"
    print(f"Parámetro poblacional: {parametro:.2f} USD")
    print(f"Conteo de clientes por ciudad: {poblacion['ciudad'].value_counts().to_dict()}")

    # TODO 2: muestra por conveniencia: las primeras 30 filas de la población.
    #         Mira la composición por ciudad: ¿es un corte al azar? ¿Qué ciudades
    #         faltan por completo? ¿Por qué ocurre (mira cómo está ordenado el archivo)?
    #         Pista: .head(30)
    muestra_conv = poblacion.head(30)
    print(muestra_conv)

    # TODO 3: muestra aleatoria simple de 30 clientes (6 %) con random_state=1.
    #         Luego repite el sorteo con las semillas 1 a 5 e imprime, por cada
    #         una, la media de gasto_mensual y de calificacion_servicio. La
    #         variabilidad entre semillas es parte de la lección.
    #         Pista: .sample(30, random_state=semilla) dentro de un for
    # CORREGIDO: faltaba el 30 (sin él, sample() devuelve 1 sola fila)
    muestra_aas = poblacion.sample(30, random_state=1)

    for semilla in range(1, 6):
        m = poblacion.sample(30, random_state=semilla)
        # CORREGIDO: comillas simples dentro del f-string (con dobles falla en Python < 3.12)
        print(f"Semilla {semilla}, media de gasto mensual: {m['gasto_mensual'].mean():.2f}, "
              f"media de calificacion servicio: {m['calificacion_servicio'].mean():.2f}")
        print()

    # TODO 4: muestra estratificada: 6 % dentro de cada ciudad (15 de Quito,
    #         9 de Guayaquil y 6 de Cuenca). ¿Qué garantiza este diseño que el
    #         sorteo simple no garantiza?
    #         Pista: .groupby("ciudad", group_keys=False).sample(frac=0.06, random_state=1)
    muestra_est = poblacion.groupby("ciudad", group_keys=False).sample(frac=0.06, random_state=1)
    print("Muestra estratificada", muestra_est["ciudad"].value_counts())

    # TODO 5: comparación final con reporte() y una tabla resumen (DataFrame con
    #         columnas diseño, n y media estimada).
    #         Pista: pd.DataFrame([{...}, {...}, {...}]) y .to_string(index=False)
    # CORREGIDO: faltaba todo el TODO 5
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
# CaféAndino probó en 8 tiendas dos formatos de carta: menu_digital y
# menu_impreso. Cada tienda probó AMBOS (diseño cruzado), alternando por semana
# durante 4 semanas. La variable de resultado es ventas_combo (combos vendidos).
def parte_c():
    print("\n" + "=" * 70 + "\nPARTE C — Experimento pareado: menú digital vs. impreso\n" + "=" * 70)

    # TODO 1: carga data/registro_experimento_cafe.csv en `df`. Imprime las
    #         primeras filas, la venta media por formato_menu y el conteo de
    #         registros por formato_menu. ¿Está balanceado el diseño?
    #         Pista: .head(), .groupby("formato_menu")["ventas_combo"].mean(), .value_counts()
    df = pd.read_csv(DATOS / "registro_experimento_cafe.csv")
    # CORREGIDO: faltaba imprimir lo que pide el TODO
    print(df.head(), "\n")
    print(df.groupby("formato_menu")["ventas_combo"].mean(), "\n")
    print(df["formato_menu"].value_counts(), "\n")

    # TODO 2: diseña un experimento NUEVO para otras 6 tiendas:
    #         tiendas = Riobamba, Ibarra, Esmeraldas, Portoviejo, Babahoyo, Tulcan
    #         semanas = 1, 2, 3, 4
    #         a) sortea con un generador reproducible (semilla 2027) la condición
    #            con la que EMPIEZA cada tienda (menu_digital o menu_impreso);
    #         b) arma una lista de diccionarios {tienda, semana, formato_menu}
    #            alternando la condición: semanas impares = la inicial, pares = la otra;
    #         c) conviértela en el DataFrame `diseno`.
    #         Pista: np.random.default_rng(...), rng.choice([...], size=...),
    #                zip(tiendas, primera), s % 2 == 1, pd.DataFrame(filas)
    tiendas = ["Riobamba", "Ibarra", "Esmeraldas", "Portoviejo", "Babahoyo", "Tulcan"]
    semanas = [1, 2, 3, 4]

    rng = np.random.default_rng(2027)
    primera = rng.choice(["menu_digital", "menu_impreso"], size=len(tiendas))
    print("Condicion inicial por tienda: ", primera)

    filas = []

    for tienda, cond in zip(tiendas, primera):
        if cond == "menu_digital":
            contraria = "menu_impreso"
        else:
            contraria = "menu_digital"
        for s in semanas:
            if s == 1 or s == 3:
                ubicacion = cond
            else:
                ubicacion = contraria
            # CORREGIDO: la clave debe llamarse "formato_menu" (antes "ubicacion"
            # y el TODO 3 fallaba con KeyError al buscar diseno["formato_menu"])
            fila = {"tienda": tienda, "semana": s, "formato_menu": ubicacion}
            filas.append(fila)

    diseno = pd.DataFrame(filas)

    print(diseno)

    # TODO 3: simula las ventas del diseño nuevo (semilla 2028) en la columna
    #         ventas_combo, sumando: un nivel base por tienda ~ Normal(850, 90)
    #         + un efecto de semana {1: 0, 2: 20, 3: 40, 4: 60}
    #         + 150 si el formato es menu_digital
    #         + ruido ~ Normal(0, 60). Redondea y convierte a entero.
    #         Pista: dict(zip(tiendas, rng.normal(...))), .map(),
    #                (diseno["formato_menu"] == "menu_digital") * 150, .round(0).astype(int)
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
# Reglas del buen gráfico que se aplican:
#   - título que diga qué se muestra
#   - ejes con unidades ("Días registrados", "Ventas (USD)")
#   - escala desde cero en las barras
#   - barras ordenadas por magnitud y horizontales para etiquetas largas
#   - pastel solo con 2–4 categorías y mensaje de proporción
#   - gráficos guardados como archivo en figuras/
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

    # TODO 1: carga data/ventas_diarias_cafe.csv en `ventas`
    #         (columnas: fecha, region, sucursal, ventas).
    ventas = pd.read_csv(DATOS / "ventas_diarias_cafe.csv")

    # TODO 2: tablas de frecuencia absoluta y relativa de region y de sucursal
    #         (dias_region, dias_region_rel, dias_sucursal, dias_sucursal_rel).
    #         Imprime las sumas: las absolutas deben dar 300 y las relativas 1.0.
    #         Pista: .value_counts() y .value_counts(normalize=True)
    dias_region = ventas["region"].value_counts()  # frecuencia absoluta
    dias_region_rel = ventas["region"].value_counts(normalize=True)  # frecuencia relativa
    dias_sucursal = ventas["sucursal"].value_counts()
    dias_sucursal_rel = ventas["sucursal"].value_counts(normalize=True)

    # CORREGIDO: faltaba imprimir las sumas de comprobación
    print("Suma de días por región:", dias_region.sum())           # debe dar 300
    print("Suma relativa por región:", dias_region_rel.sum())      # debe dar 1.0
    print("Suma de días por sucursal:", dias_sucursal.sum())       # debe dar 300
    print("Suma relativa por sucursal:", dias_sucursal_rel.sum())  # debe dar 1.0

    # TODO 3: barras VERTICALES de días por región, desde cero.
    #         Guarda como "barras_dias_region".
    #         Pista: fig, ax = plt.subplots(figsize=(6, 4)); serie.plot(kind="bar", ax=ax, color=AZUL);
    #                ax.set_title / set_xlabel / set_ylabel / set_ylim;
    #                ax.tick_params(axis="x", rotation=0); guardar(fig, "...")
    fig, ax = plt.subplots(figsize=(6, 4))
    dias_region.plot(kind="bar", ax=ax, color=AZUL)

    ax.set_title("Dias registrados por region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Dias Registrados")
    ax.set_ylim(0, dias_region.max() * 1.1)
    ax.tick_params(axis="x", rotation=0)
    guardar(fig, "barras_dias_region")

    # TODO 4: barras HORIZONTALES de días por sucursal, ordenadas (la mayor arriba).
    #         Guarda como "barras_dias_sucursal".
    #         Pista: .sort_values() y kind="barh" (la última barra queda arriba)
    # CORREGIDO: figsize más alto, faltaba .sort_values() y en barras horizontales
    # el eje de valores es el x, por eso va set_xlim (no set_ylim)
    fig, ax = plt.subplots(figsize=(7, 4))
    dias_sucursal.sort_values().plot(kind="barh", ax=ax, color=AZUL)

    ax.set_title("Dias registrados por sucursal")
    ax.set_xlabel("Dias Registrados")
    ax.set_ylabel("Sucursal")
    ax.set_xlim(0, dias_sucursal.max() * 1.1)
    guardar(fig, "barras_dias_sucursal")

    # TODO 5: volumen de ventas (suma) por región y por sucursal, y venta media
    #         por día (volumen / días) para cada una.
    #         Pista: ventas.groupby("region")["ventas"].sum()  y la división entre Series
    volumen_region = ventas.groupby("region")["ventas"].sum()
    volumen_sucursal = ventas.groupby("sucursal")["ventas"].sum()

    media_region = volumen_region / dias_region
    media_sucursal = volumen_sucursal / dias_sucursal

    # TODO 6: barras de volumen: por región (verticales) y por sucursal
    #         (horizontales y ordenadas). Eje con "Ventas (USD)" y separador de
    #         miles. Guarda "barras_volumen_region" y "barras_volumen_sucursal".
    #         Pista: ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))
    #                (en las horizontales el eje de valores es el x)
    fig, ax = plt.subplots(figsize=(6, 4))
    volumen_region.plot(kind="bar", ax=ax, color=AZUL)
    ax.set_title("Volumen de ventas por region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Ventas USD")
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

    # TODO 7: pastel de proporción de días por región (2 categorías), con
    #         porcentajes y colores [AZUL, ORO]. Guarda "pastel_dias_region".
    #         Pista: serie.plot(kind="pie", ax=ax, autopct="%.1f%%", startangle=90,
    #                colors=[AZUL, ORO]); ax.set_ylabel("")
    fig, ax = plt.subplots(figsize=(5, 5))
    dias_region.plot(kind="pie", ax=ax, autopct="%.1f%%", startangle=90, colors=[AZUL, ORO])
    ax.set_ylabel("")
    ax.set_title("Proporción de días por región")
    guardar(fig, "pastel_dias_region")

    # TODO 8: pastel de participación de cada sucursal en el volumen de ventas
    #         (5 categorías, ordenadas de mayor a menor). Guarda
    #         "pastel_volumen_sucursal". ¿Por qué 5 categorías ya es el límite
    #         razonable para un pastel?
    fig, ax = plt.subplots(figsize=(6, 6))
    volumen_sucursal.sort_values(ascending=False).plot(
        kind="pie", ax=ax, autopct="%.1f%%", startangle=90
    )
    ax.set_ylabel("")
    ax.set_title("Participación de cada sucursal en el volumen de ventas")
    guardar(fig, "pastel_volumen_sucursal")

    # TODO 9: arma e imprime dos tablas de referencia (por región y por
    #         sucursal) con columnas dias, proporcion_dias, ventas_usd y
    #         media_por_dia, y confirma que se generaron 6 gráficos.
    #         Pista: pd.DataFrame({"dias": ..., "proporcion_dias": ..., ...})
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