"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.
"""
from api import débuter_partie, jouer_coup, lister_parties
from quoridor import (analyser_commande, formater_jeu, formater_les_parties,
                      récupérer_le_coup)

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "4892f0cc-7a64-46e3-8fa5-e5d2d0c9cef3"


if __name__ == "__main__":
    args = analyser_commande()
    if args.parties:
        parties = lister_parties(args.idul, SECRET)
        print(formater_les_parties(parties))
    else:
        id_partie, état = débuter_partie(args.idul, SECRET)
        while True:
            # Afficher la partie
            print(formater_jeu(état))
            # Demander au joueur de choisir son prochain coup
            type_coup, position = récupérer_le_coup()
            # Envoyez le coup au serveur
            id_partie, état = jouer_coup(
                id_partie,
                type_coup,
                position,
                args.idul,
                SECRET,
            )
