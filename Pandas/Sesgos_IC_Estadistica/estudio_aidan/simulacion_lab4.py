import pandas as pd 
from scipy import stats
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

# Cargamos las sucursales y semanas
sucursales = [
    'cuenca_norte', 'cuenca_sur', 'guayaquil_norte', 'guayaquil_sur', 
    'quito_norte', 'quito_sur', 'loja_norte', 'loja_sur', 
    'manabi_norte', 'manabi_sur', 'santa_elena_norte', 'santa_elena_sur'
]
semanas = [1,2,3,4]

# Elegimos la primera condición de manera aleatoria
rng = np.random.default_rng(1234598)
primera = rng.choice(['movida', 'relajante'], len(sucursales))

filas = []
for sucursal, cond in zip(sucursales, primera):
    otra = 'relajante' if cond == 'movida' else 'movida'
    for s in semanas:
        filas.append({
            'sucursal': sucursal, 
            'semana': s, 
            'musica': cond if s % 2 == 1 else otra
        })

diseno = pd.DataFrame(filas)

# Simulación de ventas
rng = np.random.default_rng(123443569)
efecto_tienda = dict(zip(sucursales, rng.normal(1001, 120, len(sucursales))))
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}


diseno['ventas'] = (
    diseno['sucursal'].map(efecto_tienda) 
    + diseno['semana'].map(efecto_semana)
    + (diseno['musica'] == 'relajante') * 202 
    + rng.normal(0, 90, len(diseno))
).round(0).astype(int)


diseno['promocion_simultanea'] = 'no'
diseno.loc[(diseno['sucursal'] == 'quito_sur') & (diseno['semana'] == 1), 'promocion_simultanea'] = 'si'
diseno.loc[diseno['promocion_simultanea'] == 'si', 'ventas'] += 180

print(diseno.head(10))


piv = diseno.groupby(['sucursal', 'musica'])['ventas'].mean().unstack()
piv['diferencia'] = piv['relajante'] - piv['movida']

print(piv['diferencia'])
media = piv['diferencia'].mean()
dev = piv['diferencia'].std()
#Intervalo de confianza
n = len(piv)

t_crict = stats.t.ppf(0.975, df=n-1 )
ic_inf = media - (t_crict*dev/n**0.5)
ic_sup = media + (t_crict*dev/n**0.5)
print(f"{ic_inf}, {ic_sup}")
#pvalue 
prueba = stats.ttest_rel(piv['relajante'], piv['movida'])
print(f"{prueba.pvalue: .10}")


#grafico

plt.figure(figsize=(10, 5))
sns.lineplot(data=diseno, x='semana', y='ventas', hue='musica', style='promocion_simultanea', markers=True)

plt.title('Evolución de ventas por semana y tipo de música')
plt.xticks([1, 2, 3, 4])
plt.ylabel('Ventas')
plt.xlabel('Semana del experimento')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
