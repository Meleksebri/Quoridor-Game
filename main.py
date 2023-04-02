"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.
"""
import time
from api import débuter_partie, jouer_coup
from quoridor import Quoridor
from utilitaire import analyser_commande
from quoridorx import QuoridorX


# Mettre ici votre secret récupéré depuis le site de PAX
SECRET = "4892f0cc-7a64-46e3-8fa5-e5d2d0c9cef3"

def mode_manuel(arggg):
    """
    fonction pour jouer en mode manuel
    """
    id_partie, état = débuter_partie(arggg.idul, SECRET)
    game = Quoridor(état["joueurs"], état["murs"])
    while True:
        try:
            print(game)
            typecoup, position = game.récupérer_le_coup(1)
            id_partie, état = jouer_coup(id_partie, typecoup, position, arggg.idul, SECRET)
            game.état = état
        except StopIteration as err:
            print("Winner is: " + err)

def mode_manuel_graphique(arggg):
    """
    fonction pour jouer en mode manuel graphique
    """
    id_partie, état = débuter_partie(arggg.idul, SECRET)
    game = QuoridorX(état["joueurs"], état["murs"])
    game.afficher()
    while True:
        try:
            game.afficher()
            typecoup, position = game.demander_coup()
            id_partie, état = jouer_coup(id_partie, typecoup, position, arggg.idul, SECRET)
            game.état = état
        except StopIteration as err:
            game.afficher()
            game.terminé(err)

def mode_automatique(arggg):
    """
    fonction pour jouer en mode automatique
    """
    id_partie, état = débuter_partie(arggg.idul, SECRET)
    game = Quoridor(état['joueurs'], état['murs'])
    print(game)
    while True:
        try:
            type_coup, position = game.jouer_le_coup(1)
            id_partie, état = jouer_coup(id_partie, type_coup, position, arggg.idul, SECRET)
            time.sleep(1)
            game.état = état
            print(game)
        except StopIteration as err:
            print(game)
            print("Winner is :" + str(err))
            break

def mode_automatique_graphique(arggg):
    """
    fonction pour jouer en mode automatique graphique
    """
    id_partie, état = débuter_partie(arggg.idul, SECRET)
    game = QuoridorX(état["joueurs"], état["murs"])
    game.afficher()
    while True:
        try:
            typecoup, position = game.jouer_le_coup(1)
            game.afficher()
            time.sleep(1)
            id_partie, état = jouer_coup(id_partie, typecoup, position, arggg.idul, SECRET)
            game.état = état
            print(game)
        except StopIteration as err:
            game.afficher()
            game.terminé(err)
            break

if __name__ == "__main__":
    args = analyser_commande()
    if args.automatique and args.graphique:
        mode_automatique_graphique(args)
    elif args.graphique:
        mode_manuel_graphique(args)
    elif args.automatique:
        mode_automatique(args)
    else:
        mode_manuel(args)
