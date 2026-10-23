# Hypertexte bidimensionnel

Série d'articles de Pierre Gradit sur une version bidimensionnelle de l'hypertexte
de Ted Nelson (Xanadu), construite sur les pavages de Truchet–Smith.

| Papier | Sujet | Source | Animation |
| --- | --- | --- | --- |
| 0. Messagerie | langage de messagerie au caractère, transclusion 2D, hashes, opérateurs `@>` et `@>>`, Akoma Ntoso | [`papier-0-messagerie/messagerie.tex`](papier-0-messagerie/messagerie.tex) | — |
| I. Arbres | XML, version graphe, dualité par (pa)(pin), disque de Poincaré, déformation continue | [`papier-I-arbres/arbres.tex`](papier-I-arbres/arbres.tex) | [`deformation.html`](papier-I-arbres/deformation.html) |
| II. (à venir) | géodésiques extérieures, double disque, cartes planaires | — | — |

## Organisation

```
papier-0-messagerie/
  messagerie.tex   le papier compagnon : langage de messagerie (pdfLaTeX)
  reference/
    expansion.py   interpréteur de référence, vérifie rendus et hashes
commun/
  smith.sty        tuiles en TikZ, spin du vide, notation (pa)(pin)
  pavage.py        lecture par les coins : arbre -> pavage, contrôles
papier-I-arbres/
  arbres.tex       le papier
  latexmkrc        compilation XeLaTeX
  figures/
    genfig.py      génère toutes les figures fig-*.tex depuis l'arbre
  deformation.html animation autonome (un seul fichier, sans dépendance)
```

## Compiler

Il faut une distribution TeX récente (XeLaTeX ou LuaLaTeX, `polyglossia`,
`tikz`) et Python 3.

```sh
cd papier-I-arbres
python3 figures/genfig.py   # régénère les figures et vérifie 7 boucles / 1 boucle
latexmk                     # produit arbres.pdf
```

Les figures ne se dessinent pas à la main : on modifie l'arbre dans
`commun/pavage.py`, puis on relance `genfig.py`.

## Animation

`papier-I-arbres/deformation.html` s'ouvre directement dans un navigateur. Le
papier y renvoie par l'adresse GitHub Pages
`https://pgradit.github.io/2DHypertext/papier-I-arbres/deformation.html`, active
une fois Pages activé sur ce dépôt (Settings → Pages → branche `main`, racine).
