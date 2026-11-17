#ej2
import pandas as pd
import numpy as np
from scipy import stats

# =====================================================
# Ejercicio 3 - CafeAltura: cartel del combo en la caja vs sin cartel
# Completa cada TODO. Imprime siempre el resultado (print) y anota la interpretacion.
# Los TODO ESPECIALES (E1 a E8) piden SIMULAR las filas del CSV en vez de recibirlas.
# =====================================================
#
# CONTEXTO
# CafeAltura es una cadena de cafeterias. Quiere saber si colocar un cartel del combo
# desayuno junto a la caja aumenta los combos vendidos por semana, comparado con no
# tener cartel (su situacion habitual). Se hara un experimento CRUZADO en 10 cafeterias
# durante 4 semanas: cada cafeteria alterna semana a semana entre "con_cartel" y
# "sin_cartel", y con cual empieza se sortea (5 y 5).
# Todavia no hay datos reales: primero los vas a SIMULAR y despues los vas a analizar.
#
# ESPECIFICACION DE LA SIMULACION (sigue estos valores EXACTOS para que tu CSV sea
# identico al archivo de referencia cafeterias_referencia.csv)
#
#   Tiendas (en este orden): Quito_Norte, Quito_Sur, Guayaquil_Centro, Guayaquil_Norte,
#                            Cuenca_Centro, Cuenca_Sur, Ambato_Centro, Manta, Loja, Machala
#   Semanas: 1, 2, 3, 4
#   Sorteo: semilla 3030, rng.permutation sobre 5 "con_cartel" y 5 "sin_cartel"
#   Calendario: semanas 1 y 3 = condicion inicial; semanas 2 y 4 = la otra condicion
#   Ventas (combos_vendidos) = efecto de tienda + efecto de semana
#                              + 45 si la condicion es "con_cartel" + ruido
#       efecto de tienda: normal(media 300, desviacion 40), una por cafeteria
#       efecto de semana: {1: 0, 2: 5, 3: 10, 4: 15}
#       ruido: normal(media 0, desviacion 25), uno por fila
#       Se usa UN SOLO generador nuevo con semilla 3031: primero se generan los 10
#       efectos de tienda y DESPUES (con el mismo generador) los 40 ruidos.
#       Se redondea al entero mas cercano (round(0).astype(int)).
#   Confusor: en Guayaquil_Norte, semana 3 hubo una promocion simultanea:
#       promocion_simultanea = "si" en esa fila (y "no" en las demas) y +100 combos.
#   Columnas del CSV: tienda, semana, condicion, combos_vendidos, promocion_simultanea

# ---------- Paso 0. Protocolo (responde en comentarios) ----------
# TODO 0.1 Escribe H1 (variable, direccion y periodo) y H0

'''
H1: durante 4 semanas en 10 cafeterias se venden mas combos de desayuno con el cartel 
cerca de la caja que sin el cartel (condicion habitual) 
H2: no influye en nada ubicar el cartel cerca de la caja
'''

# TODO 0.2 Unidad experimental y cuantas hay en total

'''
Unidad experimental: la cafeteria, son 10
'''

# TODO 0.3 Factor, niveles y tratamiento
'''
Factor: combo de desayuno
NIveles: con cartel, sin cartel

'''

# TODO 0.4 Grupo de control y su rol
'''
la cafeteria sin el cartel, se usa para saber si ubicar el cartel influye en algo
(comprobar si el tratamiento funciona)
'''

# TODO 0.5 Que se sortea exactamente y por que sortear reparte los factores desconocidos

'''
basicamente se sortea la condicion inicial (con que condicion comienza cada sucursal)
reparte los factores desconocidos porque puede que tener o no el cartel influya por fuera a la cafeteria
al estar en un lugar con mas clientela, con un clima favorable al negocio o mas cercania, cosas que no se pueden controlar.
'''
# TODO 0.6 Variable respuesta
'''
combos vendidos por semana
'''

# TODO 0.7 Dos factores a controlar y como se controlan

'''
promociones simultaneas, eventos locales, etc.
'''

# ---------- Paso 1. TODOs ESPECIALES: simulacion del experimento ----------
# TODO ESPECIAL E1 Crea las listas "tiendas" y "semanas" segun la especificacion


## se nos piden 10 tiendas por 4 semanas
tiendas = ["Quito_Norte", "Quito_Sur", "Guayaquil_Centro", "Guayaquil_Norte", "Cuenca_Centro",
            "Cuenca_Sur", "Ambato_Centro", "Manta", "Loja", "Machala"]
semanas = [1, 2, 3, 4]

# TODO ESPECIAL E2 Sortea la condicion inicial de cada tienda (semilla 3030, reparto 5 y 5).
#                  Imprime cada tienda con su condicion inicial en una tabla

#condicion inicial
rng = np.random.default_rng(3030)
tienda_ci = rng.permutation(["con_cartel"] * 5 + ["sin_cartel"] * 5)

tiendas_y_ci = pd.DataFrame({"tienda": tiendas, "condicion_inicial": tienda_ci})
print(tiendas_y_ci)


# TODO ESPECIAL E3 Construye el calendario con dos bucles (tiendas y semanas) y guardalo
#                  en un DataFrame llamado "diseno" con las columnas tienda, semana y
#                  condicion. Comprueba que tiene 40 filas y que cada tienda tiene
#                  2 semanas en cada condicion (groupby + size)

filas = []

for tienda, cond in zip(tiendas, tienda_ci):
    if cond == "con_cartel":
        contraria = "sin_cartel"
    else:
        contraria = "con_cartel"
    for s in semanas:
        if s == 1 or s == 3:
            condicion = cond
        else: 
            condicion = contraria
        filas.append({"tienda": tienda, "semana": s, "condicion": condicion})

diseno = pd.DataFrame(filas)
print(diseno.shape)
print(diseno.groupby(["tienda", "condicion"]).size().unstack())


# TODO ESPECIAL E4 Agrega la columna combos_vendidos con la formula de la especificacion
#                  (usa map para llevar el efecto de tienda y el de semana a cada fila,
#                  y recuerda que True vale 1 y False vale 0 al multiplicar)

rng2 = np.random.default_rng(3031)
efecto_tienda = dict(zip(tiendas, rng2.normal(300, 40, len(tiendas))))
efecto_semana = {1: 0, 2: 5, 3: 10, 4: 15}
diseno["combos_vendidos"] = (diseno["tienda"].map(efecto_tienda)
                                + diseno["semana"].map(efecto_semana)
                                + (diseno["condicion"] == "con_cartel") * 45
                                + rng2.normal(0, 25, len(diseno))).round(0).astype(int)


# TODO ESPECIAL E5 Agrega la columna promocion_simultanea (todo "no") y marca "si" solo en
#                  Guayaquil_Norte semana 3 con .loc; luego suma 100 combos a esa fila

diseno["promocion_simultanea"] = "no"
marca = (diseno["tienda"] == "Guayaquil_Norte") & (diseno["semana"] == 3)
diseno.loc[marca, "promocion_simultanea"] = "si"
diseno.loc[diseno["promocion_simultanea"] == "si", "combos_vendidos"] += 100
print(diseno[diseno["promocion_simultanea"] == "si"])

# TODO ESPECIAL E6 Guarda el DataFrame como "cafeterias_simulado.csv" sin la columna indice
#                  (to_csv con index=False), vuelve a leerlo en "df" e imprime dimensiones
#                  y tipos de dato

diseno.to_csv("cafeterias_simulado.csv", index=False)
df = pd.read_csv("cafeterias_simulado.csv")
print(df.shape)
print(df.dtypes)


# TODO ESPECIAL E7 Lee "cafeterias_referencia.csv" y comprueba que tu archivo es identico
#                  (df.equals). Si da False, revisa semillas, orden de las tiendas y el
#                  orden en que generas los numeros aleatorios

ref = pd.read_csv("cafeterias_referencia.csv")
print("¿Mi simulacion es identica a la referencia?", df.equals(ref))

# TODO ESPECIAL E8 (opcional) Encapsula la simulacion en una funcion simular(semilla_sim,
#                  con_promo) que devuelva el DataFrame. Repite con las semillas 3031 a
#                  3035, con y sin promocion, y para cada una imprime la media de las
#                  diferencias y su IC del 95 %. Cuenta en cuantos casos el IC contiene
#                  el efecto real (45). Pista: te conviene una segunda funcion que
#                  reciba un DataFrame y devuelva media y limites del IC

# ---------- Paso 2. Revisar el CSV simulado ----------
# TODO 2.1 Imprime las dimensiones (filas x columnas) y las primeras filas de df
print(f"El dataset tiene {df.shape[0]} filas x {df.shape[1]} columnas.")
print(df.head())
# TODO 2.2 Imprime los tipos de dato (dtypes)
print(df.dtypes)
# TODO 2.3 Cuenta cuantas tiendas y cuantas semanas distintas hay (nunique)
for columna in df.columns:
    tiendas_diferentes = df["tienda"].unique()
    semanas_diferentes = df["semana"].unique()
    cantidad_t = len(tiendas_diferentes)
    cantidad_s = len(semanas_diferentes)

print(f"Hay {cantidad_t} tiendas diferentes y {cantidad_s} semanas diferentes")

# TODO 2.4 Cuenta cuantas filas hay en cada condicion
print(df["condicion"].value_counts())


# ---------- Paso 3. Promedio simple por condicion (sin emparejar) ----------
# TODO 3.1 Calcula el promedio de combos_vendidos por condicion
avg_combos = df.groupby("condicion")["combos_vendidos"].mean()
print(avg_combos)


# TODO 3.2 Calcula la diferencia entre los dos promedios (con_cartel - sin_cartel)
diferencia_avgs = avg_combos["con_cartel"] - avg_combos["sin_cartel"]
print(f"La diferencia entre los promedios simples sin emparejar es: {diferencia_avgs}")

# ---------- Paso 4. El confusor ----------
# TODO 4.1 Filtra las filas con promocion_simultanea == "si" y muestralas
print(df[df["promocion_simultanea"] == "si"].to_string(index=False))

# TODO 4.2 Anota: en que tienda, semana y condicion cayo la promocion, y hacia donde
#          sesga el efecto estimado (lo sube o lo baja) y por que

'''
Cae en Guayaquil_norte, semana 3, sin_cartel
'''

# ---------- Paso 5. Tabla pareada: una fila por tienda ----------
# TODO 5.1 Agrupa por tienda y condicion, promedia combos_vendidos y pasa la condicion
#          a columnas con unstack()  -> tabla "piv"

piv = round(df.groupby(["tienda", "condicion"])["combos_vendidos"].mean(), 2).unstack()

# TODO 5.2 Crea la columna "diferencia" = con_cartel - sin_cartel

piv["diferencia"] = piv["con_cartel"] - piv["sin_cartel"]

# TODO 5.3 Imprime piv
print(piv)

# ---------- Paso 6. Media, desviacion y n de las diferencias ----------
# TODO 6.1 media de la columna diferencia
avg_dif = round(piv["diferencia"].mean(), 2)
print(avg_dif)

# TODO 6.2 desviacion estandar muestral (ddof=1)
std_dev = round(piv["diferencia"].std(ddof=1), 2)
print(std_dev)

# TODO 6.3 n = numero de tiendas, y error estandar = dev / raiz(n)
n = len(piv)
error = (std_dev / np.sqrt(n))

# ---------- Paso 7. Intervalo de confianza del 95% ----------
# TODO 7.1 Valor critico t con stats.t.ppf(0.975, df=n-1)
t_critico = stats.t.ppf(0.975, df = n-1)

# TODO 7.2 Margen = t_critico * error estandar
margen = t_critico * error
# TODO 7.3 Limites inferior y superior = media -/+ margen
#          Anota: contiene el IC el efecto real (45)?
lim_inf = avg_dif - margen
lim_sup = avg_dif + margen

print(f"Intervalo de confianza al 95%: {lim_inf} - {lim_sup}")


# ---------- Paso 8. Prueba t pareada ----------
# TODO 8.1 stats.ttest_rel entre con_cartel y sin_cartel de piv
prueba = stats.ttest_rel(piv["con_cartel"], piv["sin_cartel"])

# TODO 8.2 Imprime estadistico t y p-valor (cuida el formato: el p-valor no debe
#          mostrarse como 0.00)
print(f"Estadistico: {prueba.statistic:.2f}, P-valor: {prueba.pvalue:.8f}")
# TODO 8.3 Verifica a mano: estadistico t = media / error estandar (compara con scipy)
t = avg_dif / error


# ---------- Paso 9. Comparar con el analisis sin emparejar ----------
# TODO 9.1 stats.ttest_ind sobre las mismas dos columnas de piv
# TODO 9.2 Compara los dos p-valores y las desviaciones (columnas vs diferencia)

# ---------- Paso 10. Analisis de sensibilidad ----------
# TODO 10.1 Repite los pasos 5 a 9 sin las filas con promocion_simultanea == "si"
#           (pista: encapsula el analisis en una funcion que reciba un DataFrame)
# TODO 10.2 Compara media, intervalo y p-valor con el analisis completo. Esta vez la
#           promocion cayo en el control: ¿el efecto sube o baja al quitarla?
