# Interpolación de Lagrange · Sesión 8

Aplicativo que automatiza la interpolación polinómica de Lagrange, en web y en Python.

Universidad Peruana Unión · Ingeniería de Sistemas · Fernando Istaña Flores
Curso: Análisis Numérico / Métodos Numéricos

---

## Qué hay aquí

| Archivo | Contenido |
|---|---|
| `index.html` | La app web. Un solo archivo, sin dependencias: se abre con doble clic o desde GitHub Pages |
| `python/lagrange.py` | Motor de cálculo con bucles anidados O(n²), coeficientes exactos y gráfica con matplotlib |
| `python/salida.txt` | La salida del programa, para pegarla en el informe |
| `python/interpolacion_s8.png` | La gráfica generada |
| `informes/` | El informe de la GAA de la Sesión 8 en PDF |

## La app web

- **Nodos editables** (2 a 8 puntos) y punto `x` a evaluar: todo se recalcula al tipear.
- **Pasos del reemplazo numérico**: cada base `L_k` con su producto de numeradores y denominadores
  ya sustituidos, su valor, el producto `y_k · L_k` y la suma final.
- **Control de la partición de la unidad**: la suma de las bases debe dar 1; la app la muestra siempre.
- **Tabla de bases evaluadas en los nodos**: hace visible la propiedad `L_k(x_j) = 1 si k = j, 0 si no`.
- **Polinomio en forma estándar**: en fracciones exactas cuando los datos son enteros, y en decimales.
- **Gráfica**: curva de `P_n(x)`, los puntos medidos y el punto interpolado resaltado, con
  crosshair y tooltip al pasar el cursor.
- **Aviso de extrapolación**: si el punto cae fuera del rango de los nodos, la app lo advierte.

## Ejecutar la versión en Python

```bash
python python/lagrange.py
```

Solo necesita `matplotlib` para la gráfica; el resto es biblioteca estándar (`fractions`).

## Caso resuelto — latencia vs. RAM

Cuatro mediciones de una prueba de carga sobre un microservicio:

| x (GB) | 2 | 4 | 8 | 12 |
|---|---|---|---|---|
| y (ms) | 150 | 85 | 50 | 70 |

Bases evaluadas en x = 6: L₀ = −0.20, L₁ = 0.75, L₂ = 0.50, L₃ = −0.05 (suman 1).

```
P3(x) = -43/192·x^3 + 227/32·x^2 - 1651/24·x + 261
P3(6) = 55.25 ms
```

El mínimo de la curva está cerca de los 7.5 GB: más memoria que eso empeora la latencia.
