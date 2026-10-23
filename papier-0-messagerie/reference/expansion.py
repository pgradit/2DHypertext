"""Interpréteur de référence du langage de messagerie (papier 0).

Un message brut est une suite de caractères, de coupures et de transclusions :
  - texte : écrit tel quel ;
  - coupure <h:n> : compte pour UN caractère dans le message qui la contient ;
    en ouverture (première coupure du message, non finale), elle conserve le
    préfixe de h jusqu'à l'unité n incluse ; sinon le suffixe après l'unité n ;
  - transclusion <h> : compte pour autant d'unités que le rendu de h, et son
    intérieur reste adressable par un message ultérieur.

Le message est sérialisé en UTF-8, hash complet en hexadécimal dans les balises,
puis haché en SHA-256. Les hashes sont affichés sous la forme 749a...986b.

Lancer :  python3 expansion.py   (vérifie les rendus et les hashes du papier)
"""

import hashlib
import re

MAGASIN = {}                                   # hash -> message brut
BALISE = re.compile(r"<([0-9a-f]{64})(?::(\d+))?>")


def publier(brut):
    """Range un message et renvoie son hash SHA-256."""
    h = hashlib.sha256(brut.encode("utf-8")).hexdigest()
    MAGASIN[h] = brut
    return h


def court(h):
    return f"{h[:4]}...{h[-4:]}"


def jetons(brut):
    """Découpe un message brut en texte, coupures et transclusions."""
    sortie, pos = [], 0
    for m in BALISE.finditer(brut):
        sortie += [("texte", c) for c in brut[pos:m.start()]]
        if m.group(2) is None:
            sortie.append(("transclusion", m.group(1)))
        else:
            sortie.append(("coupure", m.group(1), int(m.group(2))))
        pos = m.end()
    sortie += [("texte", c) for c in brut[pos:]]
    return sortie


def unites(h):
    """Liste des unités adressables d'un message ; chacune se rend en une chaîne."""
    js = jetons(MAGASIN[h])
    coupures = [i for i, j in enumerate(js) if j[0] == "coupure"]
    sortie = []
    for i, j in enumerate(js):
        if j[0] == "texte":
            sortie.append(j[1])
        elif j[0] == "transclusion":
            sortie.extend(rendu(j[1]))           # une unité par caractère
        else:
            base, n = unites(j[1]), j[2]
            ouverture = i == coupures[0] and i != len(js) - 1
            sortie.append("".join(base[:n] if ouverture else base[n:]))
    return sortie


def rendu(h):
    return "".join(unites(h))


if __name__ == "__main__":
    A = publier("Ceci est un paragraphe.")
    B = publier(f"<{A}:12>texte réécrit<{A}:22>")
    C = publier(f"<{B}:7>avec un repentir non trivial. Pour continuer :<{A}:23>")
    M4 = publier(f"<{A}:0><{A}>, et aussi<{A}:4>")
    M5 = publier(f"<{M4}:23><{M4}:24>")
    M6 = publier(f"<{M4}:13>chapitre<{M4}:23>")

    attendus = [
        ("A", A, "749a...986b", 23, "Ceci est un paragraphe."),
        ("B", B, "0631...7a3c", 15, "Ceci est un texte réécrit."),
        ("C", C, "70fd...3c77", 48,
         "Ceci est un texte avec un repentir non trivial. Pour continuer :"),
        ("4", M4, None, 35, "Ceci est un paragraphe., et aussi est un paragraphe."),
        ("5", M5, "d807...29f7", 2, "Ceci est un paragraphe, et aussi est un paragraphe."),
        ("6", M6, None, 10, "Ceci est un chapitre., et aussi est un paragraphe."),
    ]
    for nom, h, hash_attendu, longueur, texte in attendus:
        assert rendu(h) == texte, (nom, rendu(h))
        assert len(unites(h)) == longueur, (nom, len(unites(h)))
        if hash_attendu:
            assert court(h) == hash_attendu, (nom, court(h))
        print(f"{nom}  {court(h)}  {len(unites(h)):>2}  {rendu(h)}")
    print("Tous les rendus et hashes du papier sont vérifiés.")
