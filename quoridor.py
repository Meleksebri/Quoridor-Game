"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
"""
from copy import deepcopy

from quoridor_error import QuoridorError

from graphe import construire_graphe

import networkx as nx


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        état (dict): état du jeu tenu à jour.
    """

    def __init__(self, joueurs, murs=None):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Appel la méthode `vérification` pour valider les données et assigne
        ce qu'elle retourne à l'attribut `self.état`.

        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
        """
        self.état = deepcopy(self.vérification(joueurs, murs))

    def erreur_vérification(self, joueurs, murs):
        """
        fonction pour vérifier les erreurs du focntion vérification
        """
        if not hasattr(joueurs, '__iter__'):
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux.")
        if isinstance(joueurs[0],dict):
            for joueur in joueurs:
                if not 1 <= joueur['pos'][0] <= 9 or not 1 <= joueur['pos'][1] <= 9:
                    raise QuoridorError("La position d'un joueur est invalide.")
        if murs is not None and not isinstance(murs, dict):
            raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
        if murs is not None and isinstance(joueurs[0],dict):
            if len(murs["horizontaux"]) + len(murs["verticaux"]) + \
                joueurs[0]["murs"] + joueurs[1]["murs"] != 20:
                raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20.")

    def vérification(self, joueurs, murs):
        """Vérification d'initialisation d'une instance de la classe Quoridor.

        Valide les données arguments de construction de l'instance et retourne
        l'état si valide.

        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de list [x, y] uniquement.
        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """
        msg = "Le nombre de murs qu'un joueur peut placer est plus grand que 10, ou négatif."
        self.erreur_vérification(joueurs, murs)
        if isinstance(joueurs[0],dict):
            if joueurs[0]["murs"] not in range(0,11) or joueurs[1]["murs"] not in range(0,11):
                raise QuoridorError(msg)
        if murs is not None:
            # itérer sur chaque mur horizontal
            for mur in murs['horizontaux']:
                # Vérifier si la position du mur est valide
                if not 1 <= mur[0] <= 8 or not 2 <= mur[1] <= 9:
                    raise QuoridorError("La position d'un mur est invalide.")
            # itérer sur chaque mur vertical
            for mur in murs['verticaux']:
                if not 2 <= mur[0] <= 9 or not 1 <= mur[1] <= 8:
                    raise QuoridorError("La position d'un mur est invalide.")
        if murs is None and isinstance(joueurs[0], str):
            return deepcopy({"joueurs" : [{"nom": joueurs[0], "murs": 10, "pos": [5, 1]},
            {"nom": joueurs[1], "murs": 10, "pos": [5, 9]}],
            "murs" : {
            "horizontaux": [],
            "verticaux": [],
        }})
        if murs is None:
            return deepcopy({"joueurs" : joueurs, "murs" : {
            "horizontaux": [],
            "verticaux": [],
        }})
        return deepcopy({"joueurs" : joueurs, "murs" : murs})

    def formater_légende(self):
        """Formater la représentation graphique de la légende.

        Returns:
            str: Chaîne de caractères représentant la légende.
        """
        m = max([len(v["nom"]) for v in self.état["joueurs"]])
        res = "Légende:\n"
        for i , j in enumerate(self.état["joueurs"]):
            nom = j['nom']+","
            res += f"   {i+1}={nom:<{m+1}} murs={'|'*j['murs']}\n"
        return res

    def formater_damier(self):
        """Formater la représentation graphique du damier.

        Returns:
            str: Chaîne de caractères représentant le damier.
        """
        joueurs = self.état["joueurs"]
        murs = self.état["murs"]
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

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        res = self.formater_légende() + self.formater_damier()
        return res

    def état_courant(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(self.état)

    def est_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        joueur1, joueur2 = (self.état["joueurs"][i] for i in (0, 1))
        pos1 = joueur1["pos"]
        pos2 = joueur2["pos"]
        if pos1[1] == 9:
            return joueur1["nom"]
        if pos2[1] == 1:
            return joueur2["nom"]
        return False

    def récupérer_le_coup(self, joueur):
        """Récupérer le coup

        Notez que seul 2 questions devrait être posée à l'utilisateur.

        Notez aussi que cette méthode ne devrait pas modifier l'état du jeu.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La position est invalide (en dehors du damier).

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        coup = input("Quel type de coup voulez-vous jouer? ('D', 'MH', 'MV'): ")
        if coup not in ["D", "MH", "MV"]:
            raise QuoridorError("Le type de coup est invalide.")
        pos = input("Donnez la position où appliquer ce coup (x,y): ")
        position = [int(s) for s in pos.split(',')]
        if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
            raise QuoridorError("La position est invalide (en dehors du damier).")
        return (coup, position)

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (List[int, int]): La liste [x, y] de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        if not 1 <= position[0] <= 9 or not 1 <= position[1] <= 9:
            raise QuoridorError("La position est invalide (en dehors du damier).")
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.état["joueurs"]],
            self.état['murs']['horizontaux'],
            self.état['murs']['verticaux']
        )
        # vérifier si le mouvement est valide
        if tuple(position) not in \
        list(graphe.successors(tuple(self.état['joueurs'][joueur - 1]['pos']))):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        # Changer la position du joueur
        self.état["joueurs"][(joueur - 1)]['pos'] = position

    def erreur_placer_un_mur(self, joueur, position, orientation):
        """
        fonction pour vérifier les erreurs de placer_un_mur
        """
        ortn = ("horizontal", "vertical")
        msg = "La position est invalide pour cette orientation."
        orientations = "horizontaux" if orientation == "horizontal" else "verticaux"
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        if self.état["joueurs"][(joueur-1)]["murs"] <= 0:
            raise QuoridorError("Le joueur a déjà placé tous ses murs.")
        if position in self.état["murs"][orientations]:
            raise QuoridorError("Un mur occupe déjà cette position.")
        if orientation not in ortn:
            raise QuoridorError(msg)

    def vérifier_enfermé(self, position, orientation):
        """
        fonction pour vérifier si le mur enferme le joueur
        """
        objectif = ['B1', 'B2']
        msg = "La position est invalide pour cette orientation."
        if orientation == "horizontal":
            graphe = construire_graphe(
            [joueur['pos'] for joueur in self.état["joueurs"]],
            self.état['murs']['horizontaux'] + [position],
            self.état['murs']['verticaux']
            )
            # vérifier si placer ce mur enfermerais un joueur
            for i in range(2):
                if not nx.has_path(graphe, tuple(self.état["joueurs"][i]['pos']), objectif[i]):
                    raise QuoridorError(msg)
        if orientation == "vertical":
            graphe = construire_graphe(
            [joueur['pos'] for joueur in self.état["joueurs"]],
            self.état['murs']['horizontaux'],
            self.état['murs']['verticaux'] + [position]
            )
            # vérifier si placer ce mur enfermerais un joueur
            for i in range(2):
                if not nx.has_path(graphe, tuple(self.état["joueurs"][i]['pos']), objectif[i]):
                    raise QuoridorError(msg)

    def placer_un_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (List[int, int]): la liste [x, y] de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        self.erreur_placer_un_mur(joueur, position, orientation)
        self.vérifier_enfermé(position, orientation)
        msg = "La position est invalide pour cette orientation."
        cd = position
        if orientation == "horizontal":
            if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
                raise QuoridorError(msg)
            for pos in self.état["murs"]["horizontaux"]:
                if (cd[0] == pos[0]-1 or cd[0] == pos[0] or cd[0] == pos[0]+1) and cd[1] == pos[1]:
                    raise QuoridorError(msg)
            self.état["joueurs"][joueur-1]["murs"] -= 1
            self.état["murs"]["horizontaux"].append(position)
        elif orientation == "vertical":
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError(msg)
            for pos in self.état["murs"]["verticaux"]:
                if (cd[1] == pos[1]-1 or cd[1] == pos[1] or cd[1] == pos[1]+1) and cd[0] == pos[0]:
                    raise QuoridorError(msg)
            self.état["joueurs"][joueur-1]["murs"] -= 1
            self.état["murs"]["verticaux"].append(position)
        for vert in self.état["murs"]["verticaux"]:
            for hori in self.état["murs"]["horizontaux"]:
                if vert == [hori[0]+1, hori[1]-1]:
                    raise QuoridorError(msg)

    def jouer_le_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).

        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.

        Returns:
            Tuple[str, List[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")
        if self.est_terminée() is not False:
            raise QuoridorError("La partie est déjà terminée.")
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.état["joueurs"]],
            self.état['murs']['horizontaux'],
            self.état['murs']['verticaux']
        )
        goal = "B1" if joueur == 1 else "B2"
        path = nx.shortest_path(graphe, tuple(self.état["joueurs"][(joueur-1)]["pos"]), goal)
        nextmove = list(path[1])
        self.déplacer_jeton(joueur, nextmove)
        return ("D", nextmove)
