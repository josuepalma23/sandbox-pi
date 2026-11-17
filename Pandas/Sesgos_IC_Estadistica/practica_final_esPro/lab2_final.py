import warnings
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from scipy import stats

pd.set_option("display.width", 120)

# =====================================================
# Practica Lab 2 - Universidad Andina: clasificacion de variables y muestreo
# Completa cada TODO. Imprime siempre el resultado (print) y anota la interpretacion.
# =====================================================
#
# CONTEXTO
# La Universidad Andina quiere conocer los habitos de estudio de sus 600 estudiantes.
# Antes de analizar, el equipo de datos debe (A) clasificar cada variable del archivo y
# (B) decidir como tomar una muestra para estimar las horas de estudio semanales,
# porque encuestar a todos es caro. Tu rol: analista de datos.
#
# ARCHIVO: estudiantes_600.csv (600 filas y 12 columnas)
#   estudiante_id            codigo del estudiante (E0001...)
#   edad                     anos cumplidos
#   facultad                 Artes, Derecho, Salud, Administracion, Ingenieria
#   semestre                 semestre que cursa (1 a 10)
#   nivel_ingles             A1, A2, B1, B2, C1, C2 (de menor a mayor)
#   promedio                 promedio de notas (escala 0 a 10, con decimales)
#   horas_estudio_semana     horas de estudio por semana (con decimales)  <- se quiere estimar su media
#   numero_hermanos          cantidad de hermanos
#   vive_con_familia         Si / No
#   beca                     Si / No
#   satisfaccion_biblioteca  escala de opinion 1 a 5
#   codigo_postal            codigo postal de 6 digitos
# OJO: el archivo esta ordenado por facultad (asi se fue inscribiendo cada una).

# =====================================================
# PARTE A. Clasificacion de variables
# =====================================================
# ---------- Paso A1. Cargar y revisar ----------
estudiantes = pd.read_csv("estudiantes_600.csv")
# TODO A1 Imprime las dimensiones (filas y columnas) y las primeras filas
#print(f"El dataset tiene {estudiantes.shape[0]} filas x {estudiantes.shape[1]} columnas.")


# ---------- Paso A2. Tipos inferidos ----------
# TODO A2 Imprime los tipos de dato (dtypes). Anota en un comentario: que columnas llegan
#         como NUMERO sin ser variables numericas? (hay dos y debes justificar cada una)

#print(estudiantes.dtypes, f"\n")

'''
satisfaccion_biblioteca: llega como int64 y es un nivel de satisfaccion (variable categorica ordinal)
codigo_postal: llega como int y es una categorica nominal.
'''


# ---------- Paso A3. Valores unicos ----------
# TODO A3 Con un bucle for sobre las columnas, imprime cuantos valores unicos hay en cada
#         una y cuales son (muestra solo los primeros 8). Cuantas categorias tiene facultad?
for columna in estudiantes.columns:
    valores_unicos = estudiantes[columna].unique().tolist()

#print(f"\nHay {len(valores_unicos)} valores unicos y son:\n {valores_unicos[:8]}")

# ---------- Paso A5. nivel_ingles ordinal ----------
# TODO A5.1 Declara el orden A1 < A2 < B1 < B2 < C1 < C2 con CategoricalDtype(ordered=True)

orden_ingles = CategoricalDtype(
    categories=["A1", "A2", "B1", "B2", "C1", "C2"],
    ordered=True
)
estudiantes["nivel_ingles"] = estudiantes["nivel_ingles"].astype(orden_ingles)

# TODO A5.2 Imprime el nivel minimo y el maximo

#print(f"Nivel minimo de ingles:\n {estudiantes['nivel_ingles'].min()}")
#print(f"Nivel maximo de ingles:\n {estudiantes['nivel_ingles'].max()}")

# TODO A5.3 Cuenta cuantos estudiantes tienen nivel B2 o superior (una comparacion con >=)
#print(f"Numero de estudiantes con nivel B2 o superior: \n", int((estudiantes["nivel_ingles"] >= "B2").sum()))


# =====================================================
# PARTE B. Muestreo
# =====================================================
muestras = {}   # aqui guardaras cada muestra para el reporte final (nombre -> DataFrame)

# ---------- Paso B1. Poblacion y parametro ----------
poblacion = pd.read_csv("estudiantes_600.csv")
# TODO B1.1 Calcula el parametro: media de horas_estudio_semana de TODA la poblacion
parametro = poblacion["horas_estudio_semana"].mean()
print(parametro)


# TODO B1.2 Imprime cuantos estudiantes hay por facultad y el porcentaje que representa cada una

estudiantes_por_facultad = poblacion["facultad"].value_counts()
print(estudiantes_por_facultad)

#porcentaje
porcentaje_por_facu = pd.DataFrame({"Estudiantes": estudiantes_por_facultad, "Porcentaje": (estudiantes_por_facultad / len(poblacion)*100).round(1)})
print(porcentaje_por_facu)


# ---------- Paso B2. Muestreo por conveniencia ----------
# TODO B2.1 Toma los primeros 30 estudiantes (head) y guardalos en muestras["Conveniencia"]
muestra_conv = poblacion.head(30)

# TODO B2.2 Imprime su composicion por facultad, su media y su error frente al parametro

# TODO B2.3 Anota: hacia donde esta sesgada la media y por que? (mira la composicion)

# ---------- Paso B3. Muestreo aleatorio simple (MAS) ----------
# TODO B3 Toma una MAS de 30 estudiantes con random_state=2026, guardala en muestras["MAS"] e
#         imprime composicion, media y error

muestra_aas = poblacion.sample(30, random_state=2026)
muestras["MAS"] = muestra_aas
print(f"Muestreo aleatorio simple: \n {muestra_aas['facultad'].value_counts().to_dict()}")
print(f"Media: \n {muestra_aas['horas_estudio_semana'].mean():.2f}")
print(f"Error: \n {muestra_aas['horas_estudio_semana'].mean() - parametro:.2f}")
# ---------- Paso B4. Variabilidad muestral ----------
# TODO B4.1 Con un bucle, toma una MAS de 30 con las semillas 1 a 5 e imprime la media de cada una

medias_semillas = []
for semilla in range(1,6):
    m = poblacion.sample(30, random_state=semilla)["horas_estudio_semana"].mean()
    medias_semillas.append(m)
    print("-" * 30)
    print(f"Media con semilla {semilla} -> {round(m, 2)}")
    if semilla == 5:
        print("-" * 30)




# TODO B4.2 Imprime el rango (minimo y maximo) de esas 5 medias. Que te dice sobre sacar
#           conclusiones con una sola muestra?
print(f"Minimo: {min(medias_semillas):.2f}, Maximo: {max(medias_semillas):.2f}")


# ---------- Paso B5. Estratificada proporcional (5 %) ----------
# TODO B5.1 Toma el 5 % de cada facultad (groupby + sample con frac y random_state=1) y guardala
#           en muestras["Estratificada 5 %"]

muestra_estrato = poblacion.groupby("faciltad", group_keys=False).sample(frac=0.05, random_state=1)
muestras["Estratificada 5%"] = muestra_estrato


# TODO B5.2 Arma una tabla que compare el % de cada facultad en la poblacion con su % en la muestra




# ---------- Paso B6. Un estrato que desaparece ----------
# TODO B6.1 Repite con frac=0.02 e imprime cuantas filas salen de cada facultad. Que facultad
#           desaparece y por que? (calcula 0.02 por el tamano de esa facultad)
# TODO B6.2 Corrigelo garantizando al menos 1 estudiante por facultad (pista: un bucle con
#           poblacion.groupby("facultad") y grupo.sample(n=...); cupos 1, 1, 2, 3 y 5 segun
#           Artes, Derecho, Salud, Administracion, Ingenieria; usa un solo
#           np.random.RandomState(1) como random_state compartido)

# ---------- Paso B7. Estratificada con n fijo ----------
# TODO B7.1 Calcula la cuota proporcional de cada facultad para una muestra TOTAL de 40
#           (cuota = tamano de la facultad / 600 * 40) y muestrala con decimales
# TODO B7.2 Reparte esas cuotas en numeros enteros que sumen EXACTAMENTE 40 (pista: parte
#           entera con np.floor y entrega las filas que faltan a las facultades con mayor
#           parte decimal) e imprime la suma para comprobarlo
# TODO B7.3 Toma la muestra con esos cupos (mismo patron de bucle del B6.2)
# TODO B7.4 Extra: repite la cuota para n=50 usando round(). Suma 50? Por que no?

# ---------- Paso B8. Sobremuestreo y media ponderada ----------
# TODO B8.1 Toma 10 estudiantes de CADA facultad (mismo cupo para todas)
# TODO B8.2 Calcula la media simple de esa muestra y la media ponderada por el tamano real de
#           cada facultad (media de cada facultad x su tamano / 600, sumadas)
# TODO B8.3 Anota: cual de las dos esta mas cerca del parametro y por que hay que ponderar?

# ---------- Paso B9. Sesgo vs variabilidad ----------
# TODO B9.1 Repite 1000 veces (semillas 0 a 999) una MAS de 30 y una estratificada al 5 %, y guarda
#           la media de cada repeticion en dos listas
# TODO B9.2 Para cada diseno imprime el sesgo (media de las medias - parametro) y la variabilidad
#           (desviacion estandar de las medias, ddof=1). Compara con el sesgo de la conveniencia
# TODO B9.3 Anota: cual diseno es mas preciso (menos variabilidad) y por que, tomando en cuenta
#           que las facultades difieren mucho en horas de estudio

# ---------- Paso B10. Intervalo de confianza ----------
# TODO B10.1 Con la MAS del B3 calcula el IC del 95 % de la media: media -/+ t * (desv / raiz(n)),
#            con stats.t.ppf(0.975, df=n-1)
# TODO B10.2 Comprueba si el intervalo contiene el parametro del B1. Como se lee ese 95 %?

# ---------- Paso B11. Reporte final ----------
# TODO B11.1 Con un bucle sobre el diccionario "muestras" imprime para cada una: n, media,
#            diferencia con el parametro y composicion por facultad
# TODO B11.2 Escribe una conclusion de 4 lineas: que diseno recomiendas, que sesgo tuvo la
#            conveniencia, que ventaja dio estratificar y que limitacion queda
