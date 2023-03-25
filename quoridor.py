"""Module Quoridor

Functions:
    * analyser_commande - Génère un interpréteur de commande.
    * formater_légende - Formater la représentation graphique du damier.
    * formater_damier - Formater la représentation graphique de la légende.
    * formater_jeu - Formater la représentation graphique d'un jeu.
    * formater_les_parties - Formater la liste des dernières parties.
    * récupérer_le_coup - Demander le prochain coup à jouer au joueur.
"""
import argparse


def analyser_commande():
    """Génère un interpréteur de commande.
    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut «idul» représentant l'idul du joueur
                   et l'attribut «parties» qui est un booléen True/False.
    """
    parser = argparse.ArgumentParser(description="Quoridor")
    parser.add_argument('-p', '--parties',
                        action='store_true',
                        help="Lister les parties existantes")
    parser.add_argument('idul',
                        default='nom_du_joueur',
                        help="IDUL du joueur.")
    return parser.parse_args()


def formater_légende(joueurs):
    """Formater la représentation graphique de la légende.
    Args:
        joueurs (list): Liste de dictionnaires représentant les joueurs.
    Returns:
        str: Chaîne de caractères représentant la légende.
    """
    m = max([len(v["nom"]) for v in joueurs])
    res = "Légende:\n"
    for i , j in enumerate(joueurs):
        nom = j['nom']+","
        res += f"   {i+1}={nom:<{m+1}} murs={'|'*j['murs']}\n"
    return res


def formater_damier(joueurs, murs):
    """Formater la représentation graphique du damier.
    Args:
        joueurs (list): Liste de dictionnaires représentant les joueurs.
        murs (dict): Dictionnaire représentant l'emplacement des murs.
    Returns:
        str: Chaîne de caractères représentant le damier.
    """
    tab = []
    for i in range(9):
        tab += [[' . ', ' '] * 8 + [' . ']]
        if i != 8:
            tab += [['   ', ' '] * 8 + ['   ']]

    tab[(9 - joueurs[0]["pos"][1]) *2][(joueurs[0]["pos"][0]-1) * 2] = ' 1 '
    tab[(9-joueurs[1]["pos"][1]) *2][(joueurs[1]["pos"][0]-1) * 2] = ' 2 '

    for i in murs["verticaux"]:
        tab[(9 - i[1]) * 2][(i[0] - 1) * 2 - 1] = '|'
        tab[(9 - i[1]) * 2 - 1][(i[0] - 1) * 2 - 1] = '|'
        tab[(9 - i[1] - 1) * 2][(i[0] - 1) * 2 - 1] = '|'

    for i in murs["horizontaux"]:
        tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2] = '---'
        tab[(9 - i[1]) * 2 + 1][(i[0] - 1) * 2 + 1] = '-'
        tab[(9 - i[1]) * 2 + 1][(i[0]) * 2] = '---'

    damier = '   ' + '-' * 35 + '\n'
    debut2 = '  |'
    ligne_f = '--|' + '-' * 35 + '\n  | 1   2   3   4   5   6   7   8   9' + "\n"

    for i in range(9):
        debut1 = f'{9 - i} |'
        ligne1 = debut1 + ''.join(tab[2 * i]) + '|\n'
        if i != 8:
            ligne2 = debut2 + ''.join(tab[2 * i + 1]) + '|\n'
        else:
            ligne2 = ''
        damier += ligne1 + ligne2

    damier += ligne_f
    return damier


def formater_jeu(état):
    """Formater la représentation graphique d'un jeu.
    Doit faire usage des fonctions formater_légende et formater_damier.
    Args:
        état (dict): Dictionnaire représentant l'état du jeu.
    Returns:
        str: Chaîne de caractères représentant le jeu.
    """
    res = formater_légende(état["joueurs"]) + formater_damier(état["joueurs"], état["murs"])
    return res


def formater_les_parties(parties):
    """Formater une liste de parties
    L'ordre rester exactement la même que ce qui est passé en paramètre.
    Args:
        parties (list): Liste des parties
    Returns:
        str: Représentation des parties
    """
    res = ""
    for i,j in enumerate(parties):
        res += f"{i+1:<2}: {j['date']}, {j['joueurs'][0]} vs {j['joueurs'][0]}%s" \
             %(", gagnant: "+j["gagnant"] if j["gagnant"] is not None else "\n")
    return res


def récupérer_le_coup():
    """Récupérer le coup
    Returns:
        tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
    Examples:
        Quel type de coup voulez-vous jouer? ('D', 'MH', 'MV'):
        Donnez la position où appliquer ce coup (x,y): 2,6
    """
    coup = input("Quel type de coup voulez-vous jouer? ('D', 'MH', 'MV'): ")
    pos = input("Donnez la position où appliquer ce coup (x,y): ")
    return (coup, [int(s) for s in pos.split(',')])
