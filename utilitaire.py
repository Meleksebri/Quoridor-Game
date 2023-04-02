"""Module de fonctions utilitaires pour le jeu jeu Quoridor

Functions:
    * analyser_commande - Génère un interpréteur de commande.
"""

import argparse


def analyser_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par `parser.parse_args()`.
                    Cet objet a trois attributs: « idul » représentant l'idul
                    du joueur, « parties » qui est un booléen `True`/`False`
                    et « local » qui est un booléen `True`/`False`.
    """
    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase 3")
    parser.add_argument('-a', '--automatique',
                        dest='automatique',
                        action='store_true',
                        help="Activer le mode automatique.")
    parser.add_argument('-x', '--graphique',
                        dest='graphique',
                        action='store_true',
                        help="Activer le mode graphique.")
    parser.add_argument('-p', '--parties',
                        action='store_true',
                        help="Lister les parties existantes")
    parser.add_argument('-l', '--local',
                        action='store_true',
                        help="Jouer localement")
    parser.add_argument('idul',
                        default='nom_du_joueur',
                        help="IDUL du joueur.")
    return parser.parse_args()


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
        res += f"{i+1:<2}: {j['date']}, {j['joueurs'][0]} vs {j['joueurs'][1]}%s" \
             %(", gagnant: "+j["gagnant"] if j["gagnant"] is not None else "\n")
    return res
