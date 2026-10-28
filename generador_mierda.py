# Este script genera el archivo Markdown con el formato correcto de ecuaciones
# Al ejecutarlo, se creará un archivo "memoria_calculos_exportable.md" en tu directorio actual.

def generar_documento():
    # Utilizamos raw strings (r"...") para evitar problemas con los caracteres de escape de LaTeX como \n o \t
    markdown_content = r"""<div align="center">

# Aparato medidor de flujo
## Memoria de cálculos

</div>

### 1 Datos y constantes

* Volumen de llenado: $V = 28\text{ L} = 0,028\text{ m}^{3}$; $\delta V = 0,5\text{ L} = 5,0\times10^{-4}\text{ m}^{3}$
* Densidad adoptada: $\rho = 1000\text{ kg/m}^{3}$ (sin considerar temperaturas).
* Incertidumbres de instrumentos: $\delta h = 1\text{ mm} = 1,0\times10^{-3}\text{ m}$; $\delta t_{lect} = 0,01\text{ s}$; $\delta R = 0,05\text{ cm}$.
* Constantes del fabricante: $\dot{m}_{v} = 0,962(h_{A}-h_{B})^{1/2}$, $\dot{m}_{po} = 0,846(h_{E}-h_{F})^{1/2}$ (con $\Delta h$ en m y $\dot{m}$ en kg/s).

**Datos medidos**

| R [cm] | $h_{A}$ [mm] | $h_{B}$ [mm] | $h_{E}$ [mm] | $h_{F}$ [mm] | $t_{1}$ [s] | $t_{2}$ [s] | $t_{3}$ [s] |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 5,3 | 231 | 203 | 227 | 193 | 106 | 106 | 106 |
| 10,4 | 213 | 146 | 208 | 134 | 66 | 66 | 66 |
| 17,0 | 280 | 126 | 277 | 93 | 41 | 40 | 40 |

### 2 Criterios de cifras significativas y redondeo

1. Datos medidos: se conservan con las cifras con que se leyeron ($h$ en mm enteros, $t$ en s, $V = 28\text{ L}$, $R$ con un decimal). Las constantes del fabricante ($0,962$ y $0,846$) tienen 3 cifras significativas y $\rho = 1000\text{ kg/m}^{3}$ se toma como valor exacto.
2. Cifras de guarda: en los cálculos intermedios se conservan al menos dos cifras más que en el resultado final y no se redondea hasta el final, para evitar acumular error de redondeo.
3. Resta de alturas: $\Delta h = h_{A}-h_{B}$ se expresa con la posición decimal de la lectura menos precisa (mm enteros); por ejemplo, $28\text{ mm} = 0,028\text{ m}$ tiene 2 cifras significativas.
4. Incertidumbre: se redondea a 1 cifra significativa, o a 2 si la primera cifra es 1 (criterio de Taylor, ref. [4] del reporte).
5. Valor medido o calculado: se redondea a la misma posición decimal que su incertidumbre, y se escribe como $(x \pm \delta x)$ con la misma unidad.
6. Error porcentual: se reporta con 3 cifras significativas.
7. Al redondear se aplica el criterio habitual (5 o más sube la última cifra retenida).

### 3 Fórmulas

$$
\dot{m}_{v} = 0,962(h_{A}-h_{B})^{1/2}
$$

$$
\dot{m}_{po} = 0,846(h_{E}-h_{F})^{1/2}
$$

$$
\overline{t} = \frac{1}{N}\sum t_{i}
$$

$$
Q = \frac{V}{\overline{t}}
$$

$$
\dot{m}_{bh} = \rho Q
$$

$$
\dot{m}_{cc} = aR^{2} + bR + c
$$

$$
EP = \frac{|\dot{m}_{cc}-\dot{m}_{exp}|}{\dot{m}_{cc}} \times 100\%
$$

$$
\delta\dot{m}_{v} = \frac{0,962}{2\sqrt{h_{A}-h_{B}}}\sqrt{\delta h_{A}^{2} + \delta h_{B}^{2}}
$$

$$
\delta\dot{m}_{po} = \frac{0,846}{2\sqrt{h_{E}-h_{F}}}\sqrt{\delta h_{E}^{2} + \delta h_{F}^{2}}
$$

$$
s = \sqrt{\frac{\sum(t_{i}-\overline{t})^{2}}{N-1}}
$$

$$
\delta t = \sqrt{s^{2} + \delta t_{lect}^{2}}
$$

$$
\delta\dot{m}_{bh} = \dot{m}_{bh}\sqrt{\left(\frac{\delta V}{V}\right)^{2} + \left(\frac{\delta t}{\overline{t}}\right)^{2}}
$$

$$
\delta\dot{m}_{cc} = \left|\frac{d\dot{m}_{cc}}{dR}\right|\delta R = |2aR+b|\delta R
$$

$$
\delta_{comb} = \sqrt{\delta\dot{m}_{exp}^{2} + \delta\dot{m}_{cc}^{2}}
$$

### 4 Curva de calibración (digitalizada)

La Figura 3 de la guía se digitalizó (775 puntos) y se ajustó un polinomio de segundo grado ($\sigma_{res} = 3\times10^{-4}\text{ kg/s}$):

$$
\dot{m}_{cc} = 0,0001063 R^{2} + 0,01692 R + 0,05025 \quad (\text{R en cm, }\dot{m}\text{ en kg/s})
$$

### 5 Posición $R = 5,3\text{ cm}$

**Venturi**

$$
\Delta h = h_{A}-h_{B} = (231-203)\text{ mm} = 28\text{ mm} = 0,028\text{ m}
$$

$$
\dot{m}_{v} = 0,962(0,028)^{1/2} = 0,1610\text{ kg/s}
$$

$$
\delta\dot{m}_{v} = \frac{0,962}{2\sqrt{0,028}}\sqrt{(10^{-3})^{2}+(10^{-3})^{2}} = 2,8745\times0,00141 = 4,07\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{v} = (0,161 \pm 0,004)\text{ kg/s}$

**Placa orificio**

$$
\Delta h = h_{E}-h_{F} = (227-193)\text{ mm} = 0,034\text{ m}
$$

$$
\dot{m}_{po} = 0,846(0,034)^{1/2} = 0,1560\text{ kg/s}
$$

$$
\delta\dot{m}_{po} = \frac{0,846}{2\sqrt{0,034}}\sqrt{2}(10^{-3}) = 2,2940\times0,00141 = 3,24\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{po} = (0,156 \pm 0,003)\text{ kg/s}$

**Banco hidráulico**

$$
\overline{t} = \frac{106+106+106}{3} = 106,00\text{ s}
$$

$$
s = \sqrt{\frac{(106-106,00)^{2}+(106-106,00)^{2}+(106-106,00)^{2}}{2}} = 0,000\text{ s}
$$

$$
\delta t = \sqrt{0,000^{2}+0,01^{2}} = 0,010\text{ s}
$$

$$
Q = \frac{0,028}{106,00} = 2,642\times10^{-4}\text{ m}^{3}\text{/s}
$$

$$
\dot{m}_{bh} = 1000 \times 2,642\times10^{-4} = 0,2642\text{ kg/s}
$$

$$
\delta\dot{m}_{bh} = 0,2642\sqrt{\left(\frac{0,0005}{0,028}\right)^{2}+\left(\frac{0,010}{106,00}\right)^{2}} = 0,2642\sqrt{3,189\times10^{-4}+8,900\times10^{-9}} = 0,0047\text{ kg/s}
$$

Resultado: $\overline{t} = (106,000 \pm 0,010)\text{ s}$; $\dot{m}_{bh} = (0,264 \pm 0,005)\text{ kg/s}$

**Curva de calibración y comparación**

$$
\dot{m}_{cc} = 0,0001063(5,3)^{2} + 0,01692(5,3) + 0,05025 = 0,1429\text{ kg/s}
$$

$$
\frac{d\dot{m}_{cc}}{dR} = 2(0,0001063)(5,3) + 0,01692 = 0,01804\text{ kg/(s}\cdot\text{cm)}
$$

$$
\delta\dot{m}_{cc} = 0,01804 \times 0,05 = 0,00090\text{ kg/s}
$$

Resultado: $\dot{m}_{cc} = (0,1429 \pm 0,0009)\text{ kg/s}$

$$
EP_{v} = \frac{|0,1429 - 0,1610|}{0,1429} \times 100 = 12,7\%
$$

$$
EP_{po} = \frac{|0,1429 - 0,1560|}{0,1429} \times 100 = 9,17\%
$$

$$
EP_{bh} = \frac{|0,1429 - 0,2642|}{0,1429} \times 100 = 84,9\%
$$

Incertidumbre combinada: $\delta_{comb,v} = 0,004$; $\delta_{comb,po} = 0,003$; $\delta_{comb,bh} = 0,005\text{ kg/s}$.

Constante efectiva: $K_{ef,v} = \dot{m}_{cc}/\sqrt{\Delta h} = 0,854$; $K_{ef,po} = 0,775$.

Volumen que reproduce la curva: $V_{cc} = \dot{m}_{cc}\overline{t}/\rho = 0,1429\times106,00/1000 = 15,1\text{ L}$; $\dot{m}_{bh}/\dot{m}_{cc} = 1,85$.

Número de Reynolds ($\mu = 1,0\times10^{-3}\text{ Pa}\cdot\text{s}$ supuesta): $Re_{v} = 4\dot{m}_{v}/(\pi D\mu) = 7883$ ($D = 26\text{ mm}$); $Re_{po} = 3894$ ($D = 51\text{ mm}$).

### 6 Posición $R = 10,4\text{ cm}$

**Venturi**

$$
\Delta h = h_{A}-h_{B} = (213-146)\text{ mm} = 67\text{ mm} = 0,067\text{ m}
$$

$$
\dot{m}_{v} = 0,962(0,067)^{1/2} = 0,2490\text{ kg/s}
$$

$$
\delta\dot{m}_{v} = \frac{0,962}{2\sqrt{0,067}}\sqrt{(10^{-3})^{2}+(10^{-3})^{2}} = 1,8583\times0,00141 = 2,63\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{v} = (0,249 \pm 0,003)\text{ kg/s}$

**Placa orificio**

$$
\Delta h = h_{E}-h_{F} = (208-134)\text{ mm} = 0,074\text{ m}
$$

$$
\dot{m}_{po} = 0,846(0,074)^{1/2} = 0,2301\text{ kg/s}
$$

$$
\delta\dot{m}_{po} = \frac{0,846}{2\sqrt{0,074}}\sqrt{2}(10^{-3}) = 1,5550\times0,00141 = 2,20\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{po} = (0,230 \pm 0,002)\text{ kg/s}$

**Banco hidráulico**

$$
\overline{t} = \frac{66+66+66}{3} = 66,00\text{ s}
$$

$$
s = \sqrt{\frac{(66-66,00)^{2}+(66-66,00)^{2}+(66-66,00)^{2}}{2}} = 0,000\text{ s}
$$

$$
\delta t = \sqrt{0,000^{2}+0,01^{2}} = 0,010\text{ s}
$$

$$
Q = \frac{0,028}{66,00} = 4,242\times10^{-4}\text{ m}^{3}\text{/s}
$$

$$
\dot{m}_{bh} = 1000 \times 4,242\times10^{-4} = 0,4242\text{ kg/s}
$$

$$
\delta\dot{m}_{bh} = 0,4242\sqrt{\left(\frac{0,0005}{0,028}\right)^{2}+\left(\frac{0,010}{66,00}\right)^{2}} = 0,4242\sqrt{3,189\times10^{-4}+2,296\times10^{-8}} = 0,0076\text{ kg/s}
$$

Resultado: $\overline{t} = (66,000 \pm 0,010)\text{ s}$; $\dot{m}_{bh} = (0,424 \pm 0,008)\text{ kg/s}$

**Curva de calibración y comparación**

$$
\dot{m}_{cc} = 0,0001063(10,4)^{2} + 0,01692(10,4) + 0,05025 = 0,2377\text{ kg/s}
$$

$$
\frac{d\dot{m}_{cc}}{dR} = 2(0,0001063)(10,4) + 0,01692 = 0,01913\text{ kg/(s}\cdot\text{cm)}
$$

$$
\delta\dot{m}_{cc} = 0,01913 \times 0,05 = 0,00096\text{ kg/s}
$$

Resultado: $\dot{m}_{cc} = (0,238 \pm 0,001)\text{ kg/s}$

$$
EP_{v} = \frac{|0,2377 - 0,2490|}{0,2377} \times 100 = 4,76\%
$$

$$
EP_{po} = \frac{|0,2377 - 0,2301|}{0,2377} \times 100 = 3,18\%
$$

$$
EP_{bh} = \frac{|0,2377 - 0,4242|}{0,2377} \times 100 = 78,5\%
$$

Incertidumbre combinada: $\delta_{comb,v} = 0,003$; $\delta_{comb,po} = 0,002$; $\delta_{comb,bh} = 0,008\text{ kg/s}$.

Constante efectiva: $K_{ef,v} = \dot{m}_{cc}/\sqrt{\Delta h} = 0,918$; $K_{ef,po} = 0,874$.

Volumen que reproduce la curva: $V_{cc} = \dot{m}_{cc}\overline{t}/\rho = 0,2377\times66,00/1000 = 15,7\text{ L}$; $\dot{m}_{bh}/\dot{m}_{cc} = 1,78$.

Número de Reynolds ($\mu = 1,0\times10^{-3}\text{ Pa}\cdot\text{s}$ supuesta): $Re_{v} = 4\dot{m}_{v}/(\pi D\mu) = 12194$ ($D = 26\text{ mm}$); $Re_{po} = 5745$ ($D = 51\text{ mm}$).

### 7 Posición $R = 17,0\text{ cm}$

**Venturi**

$$
\Delta h = h_{A}-h_{B} = (280-126)\text{ mm} = 154\text{ mm} = 0,154\text{ m}
$$

$$
\dot{m}_{v} = 0,962(0,154)^{1/2} = 0,3775\text{ kg/s}
$$

$$
\delta\dot{m}_{v} = \frac{0,962}{2\sqrt{0,154}}\sqrt{(10^{-3})^{2}+(10^{-3})^{2}} = 1,2257\times0,00141 = 1,73\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{v} = (0,3775 \pm 0,0017)\text{ kg/s}$

**Placa orificio**

$$
\Delta h = h_{E}-h_{F} = (277-93)\text{ mm} = 0,184\text{ m}
$$

$$
\dot{m}_{po} = 0,846(0,184)^{1/2} = 0,3629\text{ kg/s}
$$

$$
\delta\dot{m}_{po} = \frac{0,846}{2\sqrt{0,184}}\sqrt{2}(10^{-3}) = 0,9861\times0,00141 = 1,39\times10^{-3}\text{ kg/s}
$$

Resultado: $\dot{m}_{po} = (0,3629 \pm 0,0014)\text{ kg/s}$

**Banco hidráulico**

$$
\overline{t} = \frac{41+40+40}{3} = 40,33\text{ s}
$$

$$
s = \sqrt{\frac{(41-40,33)^{2}+(40-40,33)^{2}+(40-40,33)^{2}}{2}} = 0,577\text{ s}
$$

$$
\delta t = \sqrt{0,577^{2}+0,01^{2}} = 0,577\text{ s}
$$

$$
Q = \frac{0,028}{40,33} = 6,942\times10^{-4}\text{ m}^{3}\text{/s}
$$

$$
\dot{m}_{bh} = 1000 \times 6,942\times10^{-4} = 0,6942\text{ kg/s}
$$

$$
\delta\dot{m}_{bh} = 0,6942\sqrt{\left(\frac{0,0005}{0,028}\right)^{2}+\left(\frac{0,577}{40,33}\right)^{2}} = 0,6942\sqrt{3,189\times10^{-4}+2,050\times10^{-4}} = 0,0159\text{ kg/s}
$$

Resultado: $\overline{t} = (40,3 \pm 0,6)\text{ s}$; $\dot{m}_{bh} = (0,694 \pm 0,016)\text{ kg/s}$

**Curva de calibración y comparación**

$$
\dot{m}_{cc} = 0,0001063(17,0)^{2} + 0,01692(17,0) + 0,05025 = 0,3686\text{ kg/s}
$$

$$
\frac{d\dot{m}_{cc}}{dR} = 2(0,0001063)(17,0) + 0,01692 = 0,02053\text{ kg/(s}\cdot\text{cm)}
$$

$$
\delta\dot{m}_{cc} = 0,02053 \times 0,05 = 0,00103\text{ kg/s}
$$

Resultado: $\dot{m}_{cc} = (0,3686 \pm 0,0010)\text{ kg/s}$

$$
EP_{v} = \frac{|0,3686 - 0,3775|}{0,3686} \times 100 = 2,43\%
$$

$$
EP_{po} = \frac{|0,3686 - 0,3629|}{0,3686} \times 100 = 1,54\%
$$

$$
EP_{bh} = \frac{|0,3686 - 0,6942|}{0,3686} \times 100 = 88,4\%
$$

Incertidumbre combinada: $\delta_{comb,v} = 0,002$; $\delta_{comb,po} = 0,0017$; $\delta_{comb,bh} = 0,016\text{ kg/s}$.

Constante efectiva: $K_{ef,v} = \dot{m}_{cc}/\sqrt{\Delta h} = 0,939$; $K_{ef,po} = 0,859$.

Volumen que reproduce la curva: $V_{cc} = \dot{m}_{cc}\overline{t}/\rho = 0,3686\times40,33/1000 = 14,9\text{ L}$; $\dot{m}_{bh}/\dot{m}_{cc} = 1,88$.

Número de Reynolds ($\mu = 1,0\times10^{-3}\text{ Pa}\cdot\text{s}$ supuesta): $Re_{v} = 4\dot{m}_{v}/(\pi D\mu) = 18487$ ($D = 26\text{ mm}$); $Re_{po} = 9060$ ($D = 51\text{ mm}$).

### 8 Resumen de resultados

| R [cm] | $\dot{m}_{v} \pm \delta\dot{m}_{v}\text{ [kg/s]}$ | $\dot{m}_{po} \pm \delta\dot{m}_{po}\text{ [kg/s]}$ | $\dot{m}_{bh} \pm \delta\dot{m}_{bh}\text{ [kg/s]}$ | $\dot{m}_{cc} \pm \delta\dot{m}_{cc}\text{ [kg/s]}$ |
| :---: | :---: | :---: | :---: | :---: |
| 5,3 | $0,161 \pm 0,004$ | $0,156 \pm 0,003$ | $0,264 \pm 0,005$ | $0,1429 \pm 0,0009$ |
| 10,4 | $0,249 \pm 0,003$ | $0,230 \pm 0,002$ | $0,424 \pm 0,008$ | $0,238 \pm 0,001$ |
| 17,0 | $0,3775 \pm 0,0017$ | $0,3629 \pm 0,0014$ | $0,694 \pm 0,016$ | $0,3686 \pm 0,0010$ |

| R [cm] | $EP_{v}\text{ [\%]}$ | $EP_{po}\text{ [\%]}$ | $EP_{bh}\text{ [\%]}$ |
| :---: | :---: | :---: | :---: |
| 5,3 | 12,7 | 9,17 | 84,9 |
| 10,4 | 4,76 | 3,18 | 78,5 |
| 17,0 | 2,43 | 1,54 | 88,4 |

### 9 Ajustes lineales $\dot{m} = aR + b$ (3 puntos)

| Método | $a\text{ [kg/(s}\cdot\text{cm)]}$ | $b\text{ [kg/s]}$ | $R^{2}$ |
| :--- | :---: | :---: | :---: |
| Venturi | 0,0186 | 0,0603 | 0,9989 |
| Placa orificio | 0,0178 | 0,0557 | 0,9922 |
| Banco hidráulico | 0,0370 | 0,0580 | 0,9947 |
| Curva de calibración | 0,0193 | 0,0392 | 0,9997 |
"""

    nombre_archivo = "memoria_calculos_exportable.md"
    
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(markdown_content)
        
    print(f"Éxito: Se ha generado el archivo '{nombre_archivo}' correctamente.")
    print("Este archivo contiene los saltos de línea requeridos en los bloques $$ para ser procesado sin errores en Google Docs.")

if __name__ == "__main__":
    generar_documento()