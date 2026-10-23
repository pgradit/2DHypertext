# Contexte du dépôt — à lire avant toute modification

Série « Pavages de Smith et hypertexte bidimensionnel » (P. Gradit), en français.
Papier I (arbres) rédigé ; papier II (double disque, cartes planaires) à venir.
Le texte des éléments est délégué au papier compagnon sur le langage de messagerie.

## Conventions fixées (ne pas les réinventer)

- **Neuf tuiles de Wang** : CONNECT (2 rotations), VIRAGE (4), DROIT (2), VIDE (1).
  Couleur d'un côté = traversé ou non par une courbe rouge.
- **CONNECT** = tuile de Smith + barre noire courte sur la diagonale des centres
  des arcs ; la barre chevauche les deux arcs et **n'atteint pas les coins**.
- **Lecture par les coins** : coins « dedans »/« dehors » ; 0/4 → VIDE, 1/3 → VIRAGE,
  2 adjacents → DROIT, 2 opposés → CONNECT. Seule l'orientation des CONNECT reste libre.
- **Version graphe** (dessin spontané d'un humain) : arcs de CONNECT autour des coins
  « dedans » ; une boucle par nœud, barre = lien parent→enfant, nommée par l'enfant.
- **Version disque** : arcs autour des coins « dehors » ; une seule boucle = horizon.
- **(pa)(pin)** : retourne une CONNECT ; agit comme σ ↦ σ∘(x y) ; appliquée à toutes
  les CONNECT = passage au dual (σ ↦ φ = σ∘α). Nom : robinet de **Denis** Papin ;
  « p » est le nom générique de la barre.
- **Spin du vide** : ⥁ (U+2941), sens horaire, posé dans une tuile VIDE extérieure ;
  (pa)(pin) ne le touche pas, l'orientation est conservée par dualité.
- **Disque de Poincaré** : positions 0..11 depuis le haut dans le sens de ⥁ ;
  géodésiques intérieures injectives, qui débordent légèrement de l'horizon.
- **Étiquettes** : parallèles aux barres (±45° dans le pavage), lisibles, à écart
  constant ; sur le disque, du côté de la région que l'élément délimite.
- Abandonné : l'alphabet `[()01 ]*` (rôle de 0 et 1).

## Fabrication

- Figures générées par `papier-I-arbres/figures/genfig.py` depuis `commun/pavage.py`
  — jamais retouchées à la main. Le script vérifie 7 boucles (graphe) et 1 (disque).
- `deformation.html` recalcule tout depuis l'arbre, même algorithme ; fichier unique.
- Compilation : `latexmk` dans le dossier du papier (XeLaTeX, polyglossia).

## Points ouverts

- Références « à vérifier » en fin de papier I, dont celle de l'isotopie à l'identité.
