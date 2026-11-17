#Muestreo en poblacion vs muestra (tipos de muestreo)
import pandas as pd

pd.set_option("display.width", 100)

def reporte(nombre, muestra, parametro):
    """Imprime n, media estimada y composición por ciudad de una muestra.

    Composición por ciudad: es la pista que delata un sesgo de selección.
    """
    if muestra is None:
        print(f"[{nombre}] pendiente de completar (TODO)")
        return
    n = len(muestra)
    media = muestra["ingresos_mensuales"].mean()
    comp = muestra["ciudad"].value_counts().to_dict()
    print(f"[{nombre}] n={n}  media={media:.2f} USD  "
          f"(parámetro {parametro:.2f}, diferencia {media - parametro:+.2f})")
    print(f"    composición por ciudad: {comp}")

## Poblacion y parametro
poblacion = pd.read_csv("estudio_inicial/clientes_400.csv")
poblacion["ingresos_mensuales"] = poblacion["ingresos_mensuales"].astype(float)
parametro = poblacion["ingresos_mensuales"].mean()
print(f"El dataset tiene {poblacion.shape[0]} filas x {poblacion.shape[1]} columnas")
print(f"Parametro poblacional: media de ingresos {parametro:.2f} USD")
print(f"Ciudades en la poblacion: ", poblacion["ciudad"].value_counts().to_dict())
print()
print("-" * 30)


## Tipo 1: Muestreo por conveniencia (causa sesgo de seleccion)
muestra_conv = poblacion.head(20) ## se agarran los primeros 20 que llegan
print("Muestra por conveniencia (causa un sesgo de seleccion)")
print(muestra_conv)
print()
print("-" * 30)

## Tipo 2: Muestreo aleatorio simple (MAS)
muestra_aas = poblacion.sample(20, random_state=47)
print("Muestra aleatoria (MAS)")
print(muestra_aas)

for semilla in range(1, 6):
    muestra = poblacion.sample(20, random_state=semilla)
    media_ingresos = muestra["ingresos_mensuales"].mean()
    media_satisfaccion = muestra["satisfaccion"].mean()
    print("--" * 20)
    print(f"Semilla {semilla}: media de ingresos = {media_ingresos:.2f}\n")
    print(f"Semilla {semilla}: media de satisfaccion = {media_satisfaccion:.2f}")


## Muestra estratificada
muestra_estratificada = poblacion.groupby("ciudad", group_keys=False).sample(frac=0.05, random_state=1)
print()
print(muestra_estratificada["ciudad"].value_counts())

##Comparacion final
reporte("Muestreo por conveniencia: ", muestra_conv, parametro)
reporte("Muestreo aleatorio simple (MAS): ", muestra_aas, parametro)
reporte("Muestreo estratificado: ", muestra_estratificada, parametro)
print()


