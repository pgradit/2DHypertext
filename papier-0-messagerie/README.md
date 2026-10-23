# Papier 0. Réécrire au caractère : un langage de messagerie à transclusion 2D

Papier compagnon de la série : il fixe le langage de messagerie auquel le
papier I délègue le texte des éléments.

| Fichier | Rôle |
| --- | --- |
| `messagerie.tex` | le papier (version de travail) |
| `messagerie.pdf` | le papier compilé |
| `latexmkrc` | compilation pdfLaTeX |
| `reference/expansion.py` | interpréteur de référence : rendus, longueurs, hashes SHA-256 |

## Compiler

```sh
cd papier-0-messagerie
latexmk                          # produit messagerie.pdf (pdfLaTeX)
```

Le préambule utilise `babel` en français et Latin Modern s'ils sont installés,
et se replie sinon sur l'anglais et Times.

## Vérifier les exemples

```sh
python3 reference/expansion.py
```

Le script recalcule les messages A, B, C, 4, 5 et 6 du papier, et vérifie leurs
rendus, leurs longueurs brutes et leurs hashes abrégés (`749a...986b`, etc.).
Toute modification d'un exemple du papier doit passer par ce script.

## Notation

- coupure `<m:i>` : compte pour un caractère ; transclusion `<X>` : compte pour
  la longueur de ce qu'elle marque ;
- règle `<X> → ⟦X⟧` : nom à gauche (le hash), valeur à droite ;
- opérateurs à la ELAN, `@` étant l'emplacement d'argument : `@>` (relation
  décontextualisée, appliquée en `X>`) et `@>>` (relation en contexte, à la
  manière d'un Journal officiel, appliquée en `X>>`).

## Points ouverts

- Références à vérifier avant soumission (notamment Borovanský et al., TCS 2002).
- Choix de la lecture de la double dépense : par coupure ou par message entier.
- Collisions de notation avec les IRI Akoma Ntoso (`@` de version, `->` de plage).
