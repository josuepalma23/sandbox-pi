#ej1
import pandas as pd
import numpy as np
from scipy import stats

# =====================================================
# Ejercicio 1 - PanDelValle: croissant en vitrina frontal vs vitrina habitual
# Completa cada TODO. Imprime siempre el resultado (print) y anota la interpretacion.
# =====================================================

# ---------- Paso 1. Cargar y revisar ----------
df = pd.read_csv("panaderias_experimento.csv")

# TODO 1.1 Imprime las dimensiones (filas x columnas) y las primeras filas
print(f"El dataset tiene {df.shape[0]} filas x {df.shape[1]} columnas\n")

# TODO 1.2 Imprime los tipos de dato (dtypes)
print(f"Tipos de datos inferidos por pandas:\n", df.dtypes)

# TODO 1.3 Cuenta cuantas tiendas y cuantas semanas distintas hay
for columna in df.columns:
    tiendas_unicas = df["tienda"].unique().tolist()
    semanas_unicas = df["semana"].unique().tolist()
    cantidad_t = len(tiendas_unicas)
    cantidad_s = len(semanas_unicas)

print(f"\nHay {cantidad_t} tiendas distintas y {cantidad_s} semanas distintas.\n")

# TODO 1.4 Cuenta cuantas filas hay en cada ubicacion
filas_ubi = df["ubicacion"].value_counts()
print(f"\n{filas_ubi}\n")

# ---------- Paso 2. Reproducir el sorteo ----------
tiendas = list(df["tienda"].unique())   # mismo orden que se uso en el sorteo
# TODO 2.1 Crea el generador con semilla 2026 (np.random.default_rng)
rng = np.random.default_rng(2026)

# TODO 2.2 Sortea la condicion inicial con una lista de 4 "vitrina_frontal" y
#          4 "vitrina_habitual" usando rng.permutation (reparto exacto 4 y 4)
lista_ubicaciones = ["vitrina_frontal"] * 4 + ["vitrina_habitual"] * 4
sorteo_ci = rng.permutation(lista_ubicaciones)

'''
## sorteo con choice (de forma independiente):
sorteo_ci = rng.choice(["vitrina_frontal", "vitrina_habitual"], size=8)
'''

# TODO 2.3 Imprime cada tienda con su condicion inicial sorteada

'''
# una manera de hacerlo
for tienda, cond_in in zip(tiendas, sorteo_ci):
    print(tienda, cond_in)
'''

tienda_y_ci = pd.DataFrame({"Tienda": tiendas, "Ubicacion inicial": sorteo_ci})
print(f"\n\{tienda_y_ci}\n")

# TODO 2.4 Compara tu sorteo con la ubicacion de la semana 1 del CSV:
#          deben coincidir tienda por tienda
sem1 = df[df["semana"] == 1]
#print((sem1["ubicacion"].values == sorteo_ci).all())

# ---------- Paso 4. Promedio simple por ubicacion (sin emparejar) ----------
# TODO 4.1 Calcula el promedio de ventas_producto por ubicacion
promedio_ventas = df.groupby("ubicacion")["ventas_producto"].mean()
print(round(promedio_ventas, 2))

# TODO 4.2 Calcula la diferencia entre los dos promedios
diferencia = promedio_ventas["vitrina_frontal"] - promedio_ventas["vitrina_habitual"]
print(f"\nLa diferencia entre el promedio de ventas en vitrina y ventas en ubicacion habitual es: {round(diferencia, 2)}\n")

# ---------- Paso 5. El confusor ----------
# TODO 5.1 Filtra las filas con promocion_simultanea == "si" y muestralas
prom_si = df[df["promocion_simultanea"] == "si"]
print(f"\nRegistros con promocion simultanea:\n {prom_si.to_string(index=False)}", f"\n")

# TODO 5.2 Anota: en que tienda, en que semana y en que ubicacion cayo la promocion

'''
En Cuenca_centro, en la semana 3, con la ubicacion de vitrina_frontal.
'''

# ---------- Paso 6. Tabla pareada: una fila por tienda ----------
# TODO 6.1 Agrupa por tienda y ubicacion, promedia ventas_producto y pasa la
#          ubicacion a columnas con unstack()  -> tabla "piv"

piv = round(df.groupby(["tienda", "ubicacion"])["ventas_producto"].mean(), 2).unstack()

# TODO 6.2 Crea la columna "diferencia" = vitrina_frontal - vitrina_habitual
piv["diferencia"] = piv["vitrina_frontal"] - piv["vitrina_habitual"]

# TODO 6.3 Imprime piv
print(piv)

# ---------- Paso 7. Media, desviacion y n de las diferencias ----------
# TODO 7.1 media de la columna diferencia
avg_dif = piv["diferencia"].mean()


# TODO 7.2 desviacion estandar muestral (ddof=1)
std_dev = round(piv["diferencia"].std(ddof=1), 2)

# TODO 7.3 n = numero de tiendas, y error estandar = dev / raiz(n)
n = len(piv)
error = (std_dev/np.sqrt(n))

print("Medidas para evaluar la efectividad del tratamiento: \n")
print(f"En promedio, se vendio {avg_dif} USD mas al cambiar la ubicacion del producto.")
print()
print(f"Desviacion estandar: {std_dev}")

# ---------- Paso 8. Intervalo de confianza del 95% ----------
# TODO 8.1 Valor critico t con stats.t.ppf(0.975, df=n-1)
t_critico = stats.t.ppf(0.975, df = n-1)
# TODO 8.2 Margen = t_critico * error estandar
margen_error = t_critico * error 
print(f"Margen de error {margen_error}")

# TODO 8.3 Limites inferior y superior = media -/+ margen
lim_sup = avg_dif + margen_error
lim_inf = avg_dif - margen_error

print(f"Intervalo de confianza: {lim_inf} - {lim_sup}")

# ---------- Paso 9. Prueba t pareada ----------
# TODO 9.1 stats.ttest_rel entre vitrina_frontal y vitrina_habitual de piv
prueba = stats.ttest_rel(piv["vitrina_frontal"], piv["vitrina_habitual"])
# TODO 9.2 Imprime estadistico t y p-valor
t = (avg_dif / error)
print(f"\nEstadistico t: {prueba.statistic:.2f}, P-valor: {prueba.pvalue:.10f}\n")
# TODO 9.3 Verifica a mano: estadistico t = media / error estandar
print(t)
