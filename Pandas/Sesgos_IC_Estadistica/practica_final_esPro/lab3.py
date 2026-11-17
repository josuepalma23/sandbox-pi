#lab3
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("registro_experimento.csv")
#print(df["ubicacion"].value_counts()) # contar los registros por ubicacion
#print()

#print(df.groupby("ubicacion")["ventas_producto"].mean())

##Simulacion de la cantidad de tiendas por franquicia
tiendas = ["Quito_Norte", "Quito_Sur", "Guayaquil_Centro", "Guayaquil_Norte", 
            "Cuenca_Norte", "Cuenca_Sur", "Ambato_Centro", "Loja", "Machala"]
semanas = [1,2,3,4]

## Sorteo de la condicion inicial (habitual o pasillo entre todas esas ciudades)
rng = np.random.default_rng(1234567)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))
#print(primera)

filas = []

for tienda, cond in zip(tiendas, primera):
    if cond == "pasillo_principal":
        otra = "habitual"
    else:
        otra = "pasillo_principal"
    for s in semanas:
        if s == 1 or s == 3: #son 4 semanas, basicamente es repartir la condicion
            ubicacion = cond
        else:
            ubicacion = otra
        fila = {"tienda": tienda, "semana": s, "ubicacion": ubicacion}
        filas.append(fila)

diseno = pd.DataFrame(filas)

# print(diseno.to_string(index=False))

## generar las ventas (simular)
rng = np.random.default_rng(1525252)
efecto_tienda = dict(zip(tiendas, rng.normal(1100, 120, len(tiendas)))) # centro, desviacion est, cuantos numeros generar
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90} #tendencia

## nuevos datos de ventas
diseno['ventas_producto'] = (diseno['tienda'].map(efecto_tienda) # suma de el efecto de la tienda base
                                + diseno['semana'].map(efecto_semana) # el efecto de la semana (semana 1: 0, semana 2: 30...)
                                + (diseno['ubicacion'] == "pasillo_principal") * 220 #se añade 220 si esta en pasillo, nada si esta en habitual
                                + rng.normal(0,90, len(diseno))).round(0).astype(int) # ruido de otros factores incontrolables

# print(diseno)

diseno['promocion_simultanea'] = 'no'
diseno.loc[(diseno['tienda'] == 'Guayaquil_Centro') & (diseno['semana'] == 1), 'promocion_simultanea'] = "si" ## en cada fila de guayaquil centro y que sea semana 1, poner 'si' en promocion_simultanea
diseno.loc[diseno['promocion_simultanea'] == 'si', 'ventas_producto'] += 180 # en la fila donde la promocion simultanea sea 'si', añadir 180 USD a las ventas


## Analisis pareado
piv = diseno.groupby(['tienda', 'ubicacion'])['ventas_producto'].mean().unstack() #ubico las parejas de cada tienda con ambas condiciones, producto en habitual y producto en pasillo principal
piv['diferencia'] = piv['pasillo_principal'] - piv['habitual'] # calculo la diferencia de ventas entre ambos pasillos

print(f"{piv}\n")

# calculamos las medidas que nos van a devolver si el tratamiento (cambiar el producto de ubicacion) dio efecto

media = round(piv['diferencia'].mean(), 2)
std_dev = round(piv['diferencia'].std(ddof=1), 2)

print("Medidas para evaluar la efectividad del tratamiento: \n")
print(f"En promedio, se vendio {media} USD mas al cambiar la ubicacion del producto.")
print()
print(f"Desviacion estandar: {std_dev}")


#Evaluacion del tratamiento con pruebas estadisticas
n = len(piv)
t_crict = stats.t.ppf(0.975, df=9) # uso de distribucion t, con 95% en el centro y 9 grados de libertad

# intervalo de confianza
ic_inf = media - (t_crict*std_dev/n**0.5)
ic_sup = media + (t_crict*std_dev/n**0.5)

## el efecto de mover el producto al pasillo esta con un 95% de confianza entre unos 173 y 297 dolares semanales
print(f"\nIntervalo de Confianza: {round(ic_inf, 2)} - {round(ic_sup, 2)}")


# prueba p-value

## la probabilidad de que ocurran estos datos si la ubicacion del producto en el pasillo no tuviera un efecto seria de 0.0000260644
prueba = stats.ttest_rel(piv['pasillo_principal'], piv['habitual'])
print(f"\nPrueba p-value: {prueba.pvalue:.10f}")


#diseno.to_csv("experimento_realizado.csv")
#piv.to_csv("diseno_pareado.csv")