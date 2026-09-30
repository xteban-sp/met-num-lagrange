"""
Análisis Numérico · Unidad 2 · Sesión 8
Interpolación de Lagrange — latencia media de un microservicio según la RAM asignada.

Datos de las pruebas de carga (stress testing):
    x (GB)  :   2     4     8    12
    y (ms)  : 150    85    50    70

Objetivo: estimar la latencia cuando el contenedor se escala a x = 6 GB.

Fernando Istaña Flores · Universidad Peruana Unión
"""

from fractions import Fraction


# --------------------------------------------------------------------------
# Motor de cálculo: polinomios base de Lagrange con bucles anidados O(n^2)
# --------------------------------------------------------------------------
def base_lagrange(xs, k, x):
    """
    L_k(x) = producto_{i != k} (x - x_i) / (x_k - x_i)
    Un solo bucle por base; llamado para cada k queda O(n^2).
    """
    Lk = 1.0
    for i in range(len(xs)):
        if i != k:
            Lk *= (x - xs[i]) / (xs[k] - xs[i])
    return Lk


def interpolar(xs, ys, x):
    """P_n(x) = suma_k y_k * L_k(x).  Devuelve el valor y la lista de L_k(x)."""
    bases = [base_lagrange(xs, k, x) for k in range(len(xs))]
    return sum(ys[k] * bases[k] for k in range(len(xs))), bases


# --------------------------------------------------------------------------
# Coeficientes exactos de P_n en forma estándar (aritmética racional)
# --------------------------------------------------------------------------
def coeficientes(xs, ys):
    """Expande la suma de Lagrange y devuelve [a_n, ..., a_1, a_0] como fracciones."""
    n = len(xs)
    total = [Fraction(0)] * n
    for k in range(n):
        num = [Fraction(1)]                       # polinomio (x - x_i) acumulado
        den = Fraction(1)
        for i in range(n):
            if i == k:
                continue
            nuevo = [Fraction(0)] * (len(num) + 1)
            for j, c in enumerate(num):
                nuevo[j] += c                     # término x * num
                nuevo[j + 1] -= c * xs[i]         # término -x_i * num
            num = nuevo
            den *= Fraction(xs[k] - xs[i])
        for j, c in enumerate(num):
            total[j] += Fraction(ys[k]) * c / den
    return total


def polinomio_texto(coef):
    grados = len(coef) - 1
    partes = []
    for j, c in enumerate(coef):
        g = grados - j
        if c == 0:
            continue
        signo = " + " if c > 0 and partes else (" - " if c < 0 and partes else ("-" if c < 0 else ""))
        val = abs(c)
        term = "%s" % val if g == 0 else ("%s·x" % val if g == 1 else "%s·x^%d" % (val, g))
        partes.append(signo + term)
    return "".join(partes)


if __name__ == "__main__":
    xs = [2, 4, 8, 12]
    ys = [150, 85, 50, 70]
    x_eval = 6

    print("=" * 74)
    print("DATOS EXPERIMENTALES")
    print("=" * 74)
    print("   k     x_k (GB)     y_k (ms)")
    for k, (a, b) in enumerate(zip(xs, ys)):
        print("  %2d   %8.2f   %10.2f" % (k, a, b))

    print()
    print("=" * 74)
    print("POLINOMIOS BASE EVALUADOS EN x = %g" % x_eval)
    print("=" * 74)
    p, bases = interpolar(xs, ys, x_eval)
    for k, Lk in enumerate(bases):
        print("  L%d(%g) = %+10.6f     y%d · L%d = %+12.6f" % (k, x_eval, Lk, k, k, ys[k] * Lk))
    print("  suma de las bases = %.6f   (debe ser 1)" % sum(bases))

    print()
    print("=" * 74)
    print("POLINOMIO INTERPOLADOR EN FORMA ESTÁNDAR")
    print("=" * 74)
    coef = coeficientes(xs, ys)
    print("  P3(x) = " + polinomio_texto(coef))
    print("  coeficientes decimales: " + ", ".join("%+.6f" % float(c) for c in coef))

    print()
    print("=" * 74)
    print("RESULTADO")
    print("=" * 74)
    print("  P3(%g) = %.4f ms" % (x_eval, p))
    print()
    print("  Verificación en los nodos:")
    for a, b in zip(xs, ys):
        v, _ = interpolar(xs, ys, a)
        print("    P3(%2g) = %8.4f   (dato: %g)   error = %.2e" % (a, v, b, abs(v - b)))

    # ----------------------------------------------------------------------
    # Gráfica: 4 puntos experimentales, curva de P3 en [2, 12] y el punto x=6
    # ----------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        malla = [2 + i * (12 - 2) / 400 for i in range(401)]
        curva = [interpolar(xs, ys, t)[0] for t in malla]

        fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=200)
        ax.plot(malla, curva, color="#14366b", linewidth=2, label="P₃(x) interpolante", zorder=2)
        ax.scatter(xs, ys, s=48, color="#101c33", zorder=3, label="puntos medidos")
        ax.scatter([x_eval], [p], s=90, color="#c8890a", zorder=4,
                   edgecolor="white", linewidth=1.4, label="P₃(6) = %.2f ms" % p)
        ax.vlines(x_eval, min(curva) - 6, p, color="#c8890a", linestyle=":", linewidth=1.2, zorder=1)
        ax.annotate("6 GB → %.2f ms" % p, (x_eval, p), textcoords="offset points",
                    xytext=(10, 10), color="#8a6a12", fontsize=9)
        for a, b in zip(xs, ys):
            ax.annotate("(%g, %g)" % (a, b), (a, b), textcoords="offset points",
                        xytext=(6, -14), color="#3c4a63", fontsize=8)
        ax.set_xlabel("Memoria asignada x (GB)")
        ax.set_ylabel("Latencia media y (ms)")
        ax.set_title("Interpolación de Lagrange de la latencia frente a la RAM")
        ax.grid(color="#dfe5ef", linewidth=0.8)
        ax.set_axisbelow(True)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        ax.legend(frameon=False, fontsize=9)
        fig.tight_layout()
        fig.savefig("interpolacion_s8.png")
        print()
        print("  Gráfica guardada en interpolacion_s8.png")
    except ImportError:
        print()
        print("  (matplotlib no está instalado: se omitió la gráfica)")
