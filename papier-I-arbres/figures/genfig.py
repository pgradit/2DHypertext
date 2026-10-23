#!/usr/bin/env python3
"""Génère les figures TikZ du papier I depuis l'arbre de l'exemple jouet.

    python3 figures/genfig.py      (depuis papier-I-arbres/)

Les figures ne sont jamais dessinées à la main : elles découlent du marquage
des coins (commun/pavage.py), ce qui garantit leur cohérence avec le texte.
Le script vérifie aussi les comptes annoncés : 7 boucles en version graphe,
1 boucle en version disque.
"""
import sys
from math import atan2, degrees, hypot, sqrt
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent.parent / "commun"))
import pavage as P  # noqa: E402

ECART = 0.17      # écart entre barre et nom, en tuiles (identique partout)
R_DISQUE = 2.7    # rayon de l'horizon, en tuiles
DEBORD = 0.10     # débord des géodésiques au-delà de l'horizon


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".") if abs(x) > 5e-4 else "0"


def lisible(angle):
    """Ramène un angle (degrés) dans ]-90, 90] pour que le texte se lise."""
    while angle > 90:
        angle -= 180
    while angle <= -90:
        angle += 180
    return angle


def tuile(typ, x, y, rot=0):
    """Pose une tuile centrée en (x, y), tournée autour de son centre."""
    r = f", rotate={rot}" if rot else ""
    return rf"  \begin{{scope}}[shift={{({f(x)},{f(y)})}}{r}] \tuile{typ} \end{{scope}}"


def ecrire(nom, corps):
    (ICI / nom).write_text(corps)
    print("écrit", nom)


# --- Pavages -----------------------------------------------------------------
def pavage_tikz(version, grille=True):
    tuiles = P.construire(version)
    lignes = [f"% Généré par genfig.py — version {version}. Ne pas modifier à la main.",
              r"\begin{tikzpicture}[scale=.85]"]
    if grille:
        lignes.append(rf"  \draw[smith/grille] (0,0) grid ({P.LARGEUR},{-P.HAUTEUR});")
    etiquettes = []
    for (c, r), (typ, rot, _, nom) in sorted(tuiles.items(), key=lambda t: (t[0][1], t[0][0])):
        if typ == "vide":
            continue
        x, y = c + .5, -r - .5
        lignes.append(tuile(typ, x, y, rot))
        if typ == "connect":
            if rot == 0:   # barre vers le bas-droite
                ang, (ox, oy) = -45, (ECART / sqrt(2), ECART / sqrt(2))
            else:          # barre vers le haut-droite
                ang, (ox, oy) = 45, (-ECART / sqrt(2), ECART / sqrt(2))
            etiquettes.append(
                rf"  \node[smith/etiquette, font=\tiny\sffamily, rotate={ang}] at ({f(x + ox)},{f(y + oy)}) {{{nom}}};")
    lignes += etiquettes
    sx, sy = P.TUILE_SPIN
    assert tuiles[(sx, sy)][0] == "vide"
    lignes.append(rf"  \spinpic[1.1]{{({f(sx + .5)},{f(-sy - .5)})}}")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes) + "\n", P.compter_boucles(tuiles)


# --- Les neuf tuiles ---------------------------------------------------------
def tuiles_tikz():
    rangee1 = [("connect", 0), ("connect", 90), None,
               ("droit", 0), ("droit", 90), None, ("vide", 0)]
    rangee2 = [("virage", 0), ("virage", 90), ("virage", 180), ("virage", 270)]
    L = ["% Généré par genfig.py. Ne pas modifier à la main.",
         r"\begin{tikzpicture}[scale=.8]"]

    def rangee(items, y):
        x = 0.5
        for it in items:
            if it is None:
                x += .6
                continue
            typ, rot = it
            L.append(tuile("cadre", x, y))
            L.append(tuile(typ, x, y, rot))
            x += 1.25
    rangee(rangee1, 0)
    rangee(rangee2, -2)
    leg = r"\node[font=\small] at"
    L += [rf"  {leg} (1.125,-.95) {{\CONNECT}};",
          rf"  {leg} (4.475,-.95) {{\DROIT}};",
          rf"  {leg} (7.2,-.95) {{\VIDE}};",
          rf"  {leg} (2.375,-2.95) {{\VIRAGE}};",
          r"\end{tikzpicture}"]
    return "\n".join(L) + "\n"


# --- (pa)(pin) sur une tuile -------------------------------------------------
def papin_tikz():
    e = ECART / sqrt(2)
    return "\n".join([
        "% Généré par genfig.py. Ne pas modifier à la main.",
        r"\begin{tikzpicture}[scale=1.3]",
        tuile("cadre", 0, 0), tuile("connect", 0, 0),
        rf"  \node[smith/etiquette, font=\small\itshape, rotate=-45] at ({f(e)},{f(e)}) {{p}};",
        tuile("cadre", 2.6, 0), tuile("connect", 2.6, 0, 90),
        rf"  \node[smith/etiquette, font=\small\itshape, rotate=45] at ({f(2.6 - e)},{f(e)}) {{p}};",
        r"  \draw[{Stealth}-{Stealth}, smithnoir!70] (.75,0) -- node[above, font=\small] {\papin} (1.85,0);",
        r"\end{tikzpicture}"]) + "\n"


# --- Disque de Poincaré ------------------------------------------------------
def poincare_tikz():
    L = ["% Généré par genfig.py. Ne pas modifier à la main.",
         r"\begin{tikzpicture}[scale=.85]",
         rf"  \draw[smith/horizon] (0,0) circle ({R_DISQUE});"]
    et = []
    for nom, (i, j) in P.PAIRES.items():
        pts = [(R_DISQUE * x, R_DISQUE * y) for x, y in P.geodesique(i, j)]
        a, b = P.point_horizon(i), P.point_horizon(j)
        s = R_DISQUE + DEBORD          # débord radial = perpendiculaire à l'horizon
        d0, d1 = (s * a[0], s * a[1]), (s * b[0], s * b[1])
        chemin = " -- ".join(f"({f(x)},{f(y)})" for x, y in [d0] + pts + [d1])
        L.append(rf"  \draw[smith/barre, line join=round] {chemin};")
        # étiquette : au milieu, du côté de la région que l'élément délimite
        k = len(pts) // 2
        m, av, ap = pts[k], pts[k - 1], pts[k + 1]
        tx, ty = ap[0] - av[0], ap[1] - av[1]
        nt = hypot(tx, ty)
        nx, ny = -ty / nt, tx / nt
        h = P.point_horizon((i + j) / 2)
        if nx * (h[0] * R_DISQUE - m[0]) + ny * (h[1] * R_DISQUE - m[1]) < 0:
            nx, ny = -nx, -ny
        ang = lisible(degrees(atan2(ty, tx)))
        et.append(rf"  \node[smith/etiquette, rotate={f(ang)}] at "
                  rf"({f(m[0] + ECART * nx)},{f(m[1] + ECART * ny)}) {{{nom}}};")
    L += et
    L.append(rf"  \spinpic[1.1]{{({f(-R_DISQUE - .6)},{f(R_DISQUE - .4)})}}")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    g, ng = pavage_tikz("graphe")
    d, nd = pavage_tikz("disque")
    assert (ng, nd) == (7, 1), (ng, nd)
    print(f"boucles : version graphe {ng}, version disque {nd}")
    ecrire("fig-graphe.tex", g)
    ecrire("fig-disque-pavage.tex", d)
    ecrire("fig-tuiles.tex", tuiles_tikz())
    ecrire("fig-papin.tex", papin_tikz())
    ecrire("fig-poincare.tex", poincare_tikz())
