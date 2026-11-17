#Clasificacion de variables
import pandas as pd
from pandas.api.types import CategoricalDtype

empleados = pd.read_csv("empleados_practica.csv")

#Dimensiones del dataset
print()
print(f"El dataset esta formado por {empleados.shape[0]} filas y {empleados.shape[1]} columnas")
print()

## Imprimir las filas y columnas
#print(empleados.to_string(index=False))
#print(empleados)

#Tipos inferidos por pandas
print("Tipos de datos inferidos.")
print(empleados.dtypes)
print()

## Cuantos valores unicos hay y cuales son
print("Cuantos valores unicos hay y cuales son? (bucle)")
for columna in empleados.columns:
    valores_unicos = empleados[columna].unique().tolist() #lista de valores unicos
    cantidad_vu = len(valores_unicos)
    print(f"{columna}: {cantidad_vu} categorias -> {valores_unicos}")

## Declarar orden en variables ordinales

##Orden para el nivel_educacion
orden_cargos = CategoricalDtype(
    categories=["Junior", "Semisenior", "Senior", "Gerente"],
    ordered=True
)
empleados["nivel_cargo"] = empleados["nivel_cargo"].astype(orden_cargos)

print()
print("Orden de variable categorica ordinal establecido con CategoricalDtypes")
print(f"Cargo minimo en la empresa segun lo establecido: {empleados['nivel_cargo'].min()}")
print(f"Cargo maximo en la empresa segun lo establecido: {empleados['nivel_cargo'].max()}")


##Orden para la evaluacion
orden_evaluacion = CategoricalDtype(
    categories=[1, 2, 3, 4, 5],
    ordered=True
)

empleados["evaluacion"] = empleados["evaluacion"].astype(orden_evaluacion)

print()
print("Orden de variable categorica ordinal establecido con CategoricalDtypes")
print(f"Evaluacion minima de un empleado en la empresa segun lo establecido: {empleados['evaluacion'].min()}")
print(f"Evaluacion maxima de un empleado en la empresa segun lo establecido: {empleados['evaluacion'].max()}")

print()
print(empleados.dtypes)
