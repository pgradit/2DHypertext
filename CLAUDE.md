# Contexte du dépôt — à lire avant toute modification

Série de Pierre Gradit sur un hypertexte bidimensionnel, en français.
Trois papiers, dont deux rédigés :

| Papier | Statut | Objet |
| --- | --- | --- |
| 0. Messagerie (`papier-0-messagerie/`) | rédigé | réécrire un document **au caractère** par messages hachés |
| I. Arbres (`papier-I-arbres/`) | rédigé | XML ↔ pavage de Smith ↔ disque de Poincaré, dualité par (pa)(pin) |
| II. (à créer, `papier-II-…/`) | **en cours** | géodésiques extérieures, double disque, cartes planaires |

Titre de série : « Pavages de Smith et hypertexte bidimensionnel » (numérotation I/II
à la manière de de Bruijn sur Penrose). Le papier 0 est le « papier compagnon ».

## L'argument qui tient la série

**Sans intérieur, pas de sécurité.** Xanadu pensait la transclusion en 3D, où une
courbe fermée ne sépare rien. En 2D, Jordan donne un dedans et un dehors.
Les deux papiers rédigés déclinent ce même slogan à deux niveaux :

- papier 0 : 2D = (position du caractère, couche). On n'écrit jamais *dans* un
  message, seulement *au-dessus* d'une copie ; l'intérieur d'une transclusion est
  adressable mais jamais modifié.
- papier I : 2D = le plan. Une boucle rouge (courbe de Jordan) sépare les coins
  « dedans » des coins « dehors ».

Attention : « 2D » n'a pas le même sens dans les deux papiers. Le papier II doit
garder le sens topologique du papier I, et ne faire le pont vers le papier 0 que
par la phrase déjà fixée : *le texte des éléments est porté par la courbe rouge*.

---

## Papier 0 — fondamentaux (ne pas redéfinir)

- **Coupure `<m:i>`** : position entre deux caractères du message `m`. En ouverture,
  garde le préfixe jusqu'à `i` inclus ; en fermeture, le suffixe après `i`.
  **Compte pour un caractère**, quelle que soit sa longueur écrite.
- **Transclusion `<X>`** : insère le bloc X ; **compte pour la longueur** de ce
  qu'elle marque ; son intérieur reste adressable.
- Références vers l'antérieur seulement → l'expansion termine ; historique = **DAG**.
- Distribution : numéros remplacés par **SHA-256** du brut sérialisé UTF-8 ;
  offsets invariants (pur renommage, α-conversion) → **DAG de Merkle**.
  Abréviation `749a...986b` (4 + 4 caractères).
- **Sémantique** : chaque message X est une règle positionnée `<X> → ⟦X⟧`
  (à gauche le nom/hash et ce qu'il recouvre, à droite la valeur posée au-dessus).
  **Repentir** : le recouvert reste désignable ; rien n'est détruit.
- **Opérateurs** (notation mixfixe ELAN, `@` = place d'argument) :
  `@>` relation décontextualisée (preuve, perd l'emplacement et les effets de bord) ;
  `@>>` relation en contexte, « à la manière d'un Journal officiel ».
- **Double dépense** : une coupure ne sert qu'une fois (UTXO, logique linéaire).
  Les messages 5 et 6 dépensent tous deux `<4:23>` → conflit au caractère malgré
  des emprises disjointes. Un **message de titre** (`7. Titre<6`) rend une version
  exécutoire.
- **Légistique / Akoma Ntoso** : `@>>` se projette en `<mod>` + `<textualMod>`
  (`source`, `destination`, `old`, `new`). Écart restant : AKN adresse à l'alinéa,
  pas au caractère.
- Exemples canoniques A, B, C, 4, 5, 6 : **toute modification passe par
  `reference/expansion.py`**, qui revérifie rendus, longueurs et hashes.
- Compilation pdfLaTeX (babel, repli anglais/Times).

## Papier I — fondamentaux (ne pas redéfinir)

### Tuiles
- **Neuf tuiles de Wang** : CONNECT (2 rotations), VIRAGE (4), DROIT (2), VIDE (1).
  Couleur d'un côté = traversé ou non par une courbe rouge. Les courbes rouges sont
  donc simples, lisses, disjointes, fermées ou finissant au bord.
- **CONNECT** = tuile de Smith + barre noire courte sur la diagonale des centres des
  arcs ; la barre chevauche les deux arcs et **n'atteint pas les coins**.
- **Lecture par les coins** (« dedans »/« dehors ») : 0/4 → VIDE, 1/3 → VIRAGE,
  2 adjacents → DROIT, 2 opposés → CONNECT. Le marquage fixe tout **sauf
  l'orientation des CONNECT** — ce bit porte la dualité.

### Les deux versions
- **Version graphe** (dessin spontané d'un humain) : un coin « dedans » par nœud,
  arcs de CONNECT autour des coins « dedans » ; une boucle par nœud ; barre = lien
  parent→enfant, **nommée par l'enfant**.
- **Version disque** : arcs autour des coins « dehors » ; une seule boucle = horizon ;
  les barres deviennent des cordes intérieures.

### Carte combinatoire
- Carte `(D, σ, α)` : σ sommets, α arêtes (involution sans point fixe),
  **φ = σ∘α** faces. Euler `V − E + F = 2 − 2g`. Lienhardt/CGAL : β₁ = φ, β₂ = α.
- Lecture : sommet = boucle rouge ; brin = extrémité de barre sur une boucle ;
  α = deux extrémités d'une barre ; σ = ordre le long d'une boucle dans le sens du spin.
- **Spin du vide** ⥁ (U+2941), horaire, dans une tuile VIDE extérieure
  (`TUILE_SPIN = (0,0)`). (pa)(pin) ne le touche pas → orientation conservée.

### Dualité et (pa)(pin)
- Duale de `(D,σ,α)` = `(D,φ,α)` ; involutive car φ∘α = σ.
- **(pa)(pin)** retourne une CONNECT (arcs et barre changent de diagonale),
  préserve la règle de Wang, agit comme **σ ↦ σ∘(x y)** : fusionne deux boucles ou
  en coupe une (±1 cycle). Appliquée à toutes les CONNECT (transpositions disjointes
  qui commutent) : σ ↦ σ∘α = φ, **passage au dual**.
  Nom : robinet de **Denis** Papin ; « p » = nom générique de la barre.

### Exemple jouet (à réutiliser, ne pas en changer)
`<html><head><title/></head><body><h1/><p/></body></html>`, 7 nœuds (document
implicite compris), 6 arêtes, pavage 5×6 = 30 tuiles (6 CONNECT, 16 VIRAGE, 8 VIDE).
```
α   = (0 11)(1 4)(2 3)(5 10)(6 7)(8 9)
σ_g = (0)(1 5 11)(2 4)(3)(6 8 10)(7)(9)      φ_g = (0 1 2 … 11)
σ_d = φ_g                                    φ_d = σ_g
```
Graphe : 7−6+1 = 2. Duale : 1−6+7 = 2.

### Disque de Poincaré
- 2n points sur l'horizon, positions 0..2n−1 **depuis le haut dans le sens de ⥁** ;
  σ_d = ordre de lecture des balises, α = ouvrante ↔ fermante.
- **Géodésiques intérieures injectives** (ni croisement, ni contact hors extrémités),
  qui débordent légèrement de l'horizon pour figurer le chevauchement des barres.
- Clé : carte à un sommet planaire ⇔ cordes non croisées ⇔ mot bien parenthésé ⇔
  XML bien formé. Comptage : Catalan C_n (C₆ = 132).
- Régions = faces φ_d = nœuds ; la région entre 11 et 0 (côté horizon) est le document.

### Théorème de déformation
Isotopie du plan envoyant la boucle Γ sur l'horizon et chaque barre sur sa
géodésique, orientation préservée. Preuve : Jordan–Schoenflies (arrondir Γ) →
répartir les extrémités → **lemme de redressement** (récurrence sur une corde à
extrémités consécutives, Schoenflies de chaque côté) → isotopie à l'identité
(référence encore à fixer). Corollaire : à isotopie près, **le dessin ne dépend
que de (σ_d, α)**. L'animation interpole linéairement ; elle illustre, ne prouve pas.

### Étiquettes
Parallèles aux barres (±45° dans le pavage), lisibles, écart constant (`ECART=0.17`) ;
sur le disque, du côté de la région que l'élément délimite.

### Abandonné
L'alphabet `[()01 ]*` (rôle de 0 et 1). On attaque par l'exemple XML.

---

## Papier II — ce que les papiers précédents ont promis

Engagement écrit dans la conclusion de I : le pavage admet des CONNECT **dont la
bande est extérieure à l'horizon** → géodésiques extérieures → **double disque** →
**mots à deux types de parenthèses** → **cartes planaires générales**.

Ce qui découle mécaniquement de I (à exploiter, pas à redémontrer) :
- Intérieur et extérieur de l'horizon sont deux disques (sphère = deux disques
  recollés). Cordes intérieures non croisées entre elles, cordes extérieures non
  croisées entre elles, et une intérieure ne coupe jamais une extérieure.
  Donc un double disque = **entrelacement (shuffle) de deux mots bien parenthésés
  indépendants**, un type par côté.
- Le lemme de redressement s'applique tel quel de chaque côté (le côté extérieur
  est un disque sur la sphère, ou via inversion dans le plan).
- (pa)(pin) reste σ ↦ σ∘(x y) ; il faut dire ce qu'il fait sur une CONNECT
  extérieure et vérifier qu'il préserve toujours Wang et le spin.
- La formule d'Euler reste l'invariant de contrôle ; planarité = g = 0.

Pistes de littérature **à vérifier avant de citer** (ne rien inventer) :
- Mullin (1967) sur les cartes enracinées munies d'un arbre couvrant, comptées par
  C_n·C_{n+1}, et codage par entrelacement de deux mots de Dyck ;
- Bernardi (2007), bijection pour ces cartes ;
- Walsh–Lehman, Tutte, pour le comptage des cartes planaires ;
- le lien avec les plongements en livre à deux pages, si le double disque y mène.

Questions à trancher avec Pierre, ne pas les décider seul :
- Ce que représente l'horizon dans le cas général (contour d'un arbre couvrant ?).
- Le sens XML du second type de parenthèse (liens, transclusions, IDREF ?).
- L'exemple jouet du papier II : prolonger celui de I, ou un nouveau minimal.
- Où vont les étiquettes des géodésiques extérieures.

## Fabrication

- Figures générées par `figures/genfig.py` depuis `commun/pavage.py`, **jamais
  retouchées à la main**. Le script vérifie 7 boucles (graphe) et 1 (disque).
- `commun/pavage.py` est **câblé sur l'exemple jouet** (`NOEUDS`, `ARETES`, `PAIRES`,
  `n=12` dans `point_horizon`/`geodesique`) : le papier II exigera de le généraliser
  sans casser les figures de I (relancer `genfig.py` de I après toute modification).
- `commun/smith.sty` : macros `\tuileconnect`, `\tuilevirage`, `\tuiledroit`,
  `\tuilevide`, `\spin`, `\papin`, `\CONNECT`… — à réutiliser, pas à dupliquer.
- `deformation.html` : fichier unique sans dépendance, recalcule depuis l'arbre ;
  publié via GitHub Pages.
- Compilation : `latexmk` dans le dossier du papier. Papier 0 en pdfLaTeX,
  papier I (et II) en **XeLaTeX + polyglossia**. Un dossier par papier, `.tex` +
  `latexmkrc` + `figures/`.

## Méthode de travail

- Tout calcul de permutation, de cycle ou de comptage est **vérifié par script**
  avant d'entrer dans le texte. Toute figure se déduit des données.
- Notations figées : φ = σ∘α (pas α∘σ), composition de droite à gauche,
  positions comptées depuis le haut dans le sens horaire.
- Style : français, « nous », phrases courtes, une idée par paragraphe ; chaque
  section s'ouvre par une phrase qui dit ce qu'elle établit. Pas de jargon non défini.
- Références : jamais inventées. Ce qui n'est pas vérifié est marqué « à vérifier ».

## Points ouverts hérités

- Papier I : références « à vérifier », dont l'isotopie à l'identité des
  homéomorphismes du plan préservant l'orientation.
- Papier 0 : Borovanský et al. (TCS 2002) à vérifier ; lecture de la double dépense
  (par coupure ou par message entier) ; collisions de notation avec les IRI Akoma
  Ntoso (`@` de version, `->` de plage).
