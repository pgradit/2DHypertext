"""Construction d'un pavage de Smith à partir d'un arbre (XML).

Lecture par les coins (papier I, section 1) : chaque coin de tuile est
marqué « dedans » ou « dehors » ; le type et la rotation de chaque tuile
s'en déduisent, sauf l'orientation des tuiles CONNECT, fixée par la version :
  - « graphe » : les arcs de CONNECT entourent les coins « dedans » ;
  - « disque » : les arcs de CONNECT entourent les coins « dehors »
    (après application de (pa)(pin) à toutes les CONNECT).

Coordonnées : coin (c, r), colonne c vers la droite, ligne r vers le bas.
La tuile (c, r) a pour coin haut-gauche (c, r).
"""

from math import atan2, cos, sin, pi, hypot

# --- L'exemple jouet ---------------------------------------------------------
LARGEUR, HAUTEUR = 5, 6           # en tuiles
NOEUDS = {                        # nœud -> coin « dedans »
    "document": (1, 2),
    "html": (2, 3),
    "head": (3, 2),
    "title": (4, 1),
    "body": (3, 4),
    "h1": (4, 5),
    "p": (2, 5),
}
ARETES = [                        # (parent, enfant) ; l'arête porte le nom de l'enfant
    ("document", "html"),
    ("html", "head"),
    ("head", "title"),
    ("html", "body"),
    ("body", "h1"),
    ("body", "p"),
]
# Balises dans l'ordre du document : paires (ouvrante, fermante)
PAIRES = {"html": (0, 11), "head": (1, 4), "title": (2, 3),
          "body": (5, 10), "h1": (6, 7), "p": (8, 9)}
TUILE_SPIN = (0, 0)               # tuile VIDE extérieure portant le spin

TL, TR, BL, BR = "TL", "TR", "BL", "BR"


def coins_tuile(c, r):
    return {TL: (c, r), TR: (c + 1, r), BL: (c, r + 1), BR: (c + 1, r + 1)}


def classer(c, r, dedans, version):
    """Renvoie (type, rotation, centres_des_arcs) pour la tuile (c, r)."""
    k = coins_tuile(c, r)
    ins = {n for n, p in k.items() if p in dedans}
    if len(ins) in (0, 4):
        return "vide", 0, []
    if len(ins) in (1, 3):
        special = next(iter(ins)) if len(ins) == 1 else next(iter(set(k) - ins))
        rot = {TL: 0, BL: 90, BR: 180, TR: 270}[special]
        return "virage", rot, [k[special]]
    if ins in ({TL, TR}, {BL, BR}):
        return "droit", 0, []
    if ins in ({TL, BL}, {TR, BR}):
        return "droit", 90, []
    # deux coins opposés : CONNECT
    centres = ins if version == "graphe" else set(k) - ins
    rot = 0 if centres == {TL, BR} else 90
    return "connect", rot, [k[n] for n in sorted(centres)]


def construire(version):
    dedans = set(NOEUDS.values())
    # Contrôles de la construction (section 2) : coins « dedans » voisins
    # uniquement en diagonale, et seulement le long d'une arête.
    arete_de = {}
    for parent, enfant in ARETES:
        a, b = NOEUDS[parent], NOEUDS[enfant]
        assert abs(a[0] - b[0]) == 1 and abs(a[1] - b[1]) == 1, (parent, enfant)
        arete_de[frozenset((a, b))] = enfant
    pts = sorted(dedans)
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            d = (abs(a[0] - b[0]), abs(a[1] - b[1]))
            assert d not in ((1, 0), (0, 1)), ("coins dedans adjacents", a, b)
            if d == (1, 1):
                assert frozenset((a, b)) in arete_de, ("diagonale sans arête", a, b)
    for (c, r) in pts:   # le bord reste « dehors »
        assert 0 < c < LARGEUR and 0 < r < HAUTEUR

    tuiles = {}
    for r in range(HAUTEUR):
        for c in range(LARGEUR):
            typ, rot, centres = classer(c, r, dedans, version)
            nom = None
            if typ == "connect":
                k = coins_tuile(c, r)
                diag = frozenset(p for p in k.values() if p in dedans)
                nom = arete_de[diag]
            tuiles[(c, r)] = (typ, rot, centres, nom)
    return tuiles


# --- Courbes rouges : segments entre milieux de côtés -------------------------
def segments(c, r, typ, rot, centres):
    """Segments rouges de la tuile : liste de (milieu_a, milieu_b, centre|None).
    Les milieux sont en demi-unités entières (pour servir de clés)."""
    m = {"N": (2 * c + 1, 2 * r), "S": (2 * c + 1, 2 * r + 2),
         "O": (2 * c, 2 * r + 1), "E": (2 * c + 2, 2 * r + 1)}
    cotes = {TL: ("N", "O"), TR: ("N", "E"), BL: ("S", "O"), BR: ("S", "E")}
    k = coins_tuile(c, r)
    nom = {v: n for n, v in k.items()}
    if typ == "vide":
        return []
    if typ == "droit":
        a, b = ("O", "E") if rot == 0 else ("N", "S")
        return [(m[a], m[b], None)]
    out = []
    for ctr in centres:
        a, b = cotes[nom[ctr]]
        out.append((m[a], m[b], ctr))
    return out


def compter_boucles(tuiles):
    """Nombre de courbes rouges fermées (toutes le sont : bord « dehors »)."""
    voisins = {}
    for (c, r), (typ, rot, centres, _) in tuiles.items():
        for a, b, _ in segments(c, r, typ, rot, centres):
            voisins.setdefault(a, []).append(b)
            voisins.setdefault(b, []).append(a)
    assert all(len(v) == 2 for v in voisins.values()), "courbe ouverte"
    vus, n = set(), 0
    for s in voisins:
        if s in vus:
            continue
        n += 1
        pile = [s]
        while pile:
            x = pile.pop()
            if x in vus:
                continue
            vus.add(x)
            pile.extend(voisins[x])
    return n


# --- Disque de Poincaré -------------------------------------------------------
def point_horizon(i, n=12):
    """Position i sur l'horizon : 0 en haut, sens horaire (repère y vers le haut)."""
    a = pi / 2 - 2 * pi * i / n
    return (cos(a), sin(a))


def geodesique(i, j, n=12, pas=40):
    a, b = point_horizon(i, n), point_horizon(j, n)
    d = a[0] * b[0] + a[1] * b[1]
    if abs(d + 1) < 1e-9:
        return [(a[0] + (b[0] - a[0]) * t / pas, a[1] + (b[1] - a[1]) * t / pas)
                for t in range(pas + 1)]
    cx, cy = (a[0] + b[0]) / (1 + d), (a[1] + b[1]) / (1 + d)
    rr = hypot(a[0] - cx, a[1] - cy)
    t1, t2 = atan2(a[1] - cy, a[0] - cx), atan2(b[1] - cy, b[0] - cx)
    dt = (t2 - t1 + pi) % (2 * pi) - pi           # arc court = arc intérieur
    return [(cx + rr * cos(t1 + dt * k / pas), cy + rr * sin(t1 + dt * k / pas))
            for k in range(pas + 1)]
