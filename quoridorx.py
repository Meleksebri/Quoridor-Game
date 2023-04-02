"""Module de la classe QuoridorX

Classes:
    * QuoridorX - Classe pour encapsuler le jeu Quoridor avec affichage graphique
"""

import turtle
from quoridor import Quoridor



class QuoridorX(Quoridor):
    """
    Classe pour encapsuler le jeu QuoridorX.
    """
    def __init__(self, joueur, murs=None):
        """
        constructeur de la classe QuoridorX
        """
        super().__init__(joueur, murs)
        self.board = turtle.Screen()
        self.board.title("Quoridor Game")
        self.sebri = turtle.Turtle(visible=False)
        self.afficher()

    def aff_mur_h(self):
        """
        méthode pour afficher mur
        """
        for i in range(1, 11):
            self.sebri.penup()
            self.sebri.forward(i * self.board_w // 10)
            self.sebri.setheading(90)
            self.sebri.pendown()
            self.sebri.forward(self.board_h)
            self.sebri.penup()
            self.sebri.goto(self.origin)
            self.sebri.setheading(0)
            self.sebri.pendown()

    def aff_mur_v(self):
        """
        méthode pour afficher mur
        """
        for i in range(1, 11):
            self.sebri.penup()
            self.sebri.setheading(90)
            self.sebri.forward(i * self.board_h // 10)
            self.sebri.pendown()
            self.sebri.setheading(0)
            self.sebri.forward(self.board_w)
            self.sebri.penup()
            self.sebri.goto(self.origin)
            self.sebri.pendown()

    def draw_mur_v(self):
        """
        méthode pour dessiner mur
        """
        position_murs_verticaux = self.état["murs"]['verticaux']
        self.sebri.pensize(10)

        for i, _ in enumerate(position_murs_verticaux):
            self.sebri.pencolor("black")
            self.sebri.goto(self.origin)
            self.sebri.setheading(0)
            self.sebri.forward(position_murs_verticaux[i][0] * self.board_w // 10)
            self.sebri.setheading(90)
            self.sebri.forward(position_murs_verticaux[i][1] * self.board_h // 10)
            self.sebri.pendown()
            self.sebri.forward(2 * self.board_h // 10)
            self.sebri.penup()

    def draw_mur_h(self):
        """
        méthode pour dessiner mur
        """
        position_murs_horizontaux = self.état["murs"]['horizontaux']

        self.sebri.setheading(0)

        for i, _ in enumerate(position_murs_horizontaux):
            self.sebri.pencolor("grey")
            self.sebri.goto(self.origin)
            self.sebri.forward(position_murs_horizontaux[i][0] * self.board_w // 10)
            self.sebri.setheading(90)
            self.sebri.forward(position_murs_horizontaux[i][1] * self.board_h // 10)
            self.sebri.setheading(0)
            self.sebri.pendown()
            self.sebri.forward(2 * self.board_w // 10)
            self.sebri.penup()

    def légende(self):
        """
        méthode pour afficher légende sur board
        """
        position_joueur = (self.état["joueurs"][0]['pos'], self.état["joueurs"][1]['pos'])
        self.sebri.pensize(1)
        for i in range(0, 2):
            firstletter = self.état["joueurs"][i]['nom'][0]
            color = "green" if i == 0 else "red"
            self.sebri.goto(self.origin_x + self.board_w //20, self.origin_y + self.board_h //40)
            self.sebri.forward(position_joueur[i][0] * self.board_w // 10)
            self.sebri.setheading(90)
            self.sebri.forward(position_joueur[i][1] * self.board_h //10)
            self.sebri.pencolor(color)
            self.sebri.write(firstletter, align='center', font=('Arial', '15', 'bold'))
            self.sebri.setheading(0)

    def afficher(self):
        """
        méthode pour afficher le jeu
        """
        width = 800
        height = 800

        self.board_w = int(width * 0.60)
        self.board_h = int(height * 0.60)

        self.origin_x = -self.board_w/2
        self.origin_y = -self.board_h/2
        self.origin = (self.origin_x, self.origin_y)

        self.board.setup(width, height)

        self.board.tracer(False)
        self.sebri.hideturtle()

        self.sebri.pencolor("black")
        self.board.bgcolor("light green")

        self.sebri.clear()

        self.sebri.penup()
        self.sebri.goto(self.origin)
        self.sebri.pensize(2)
        self.sebri.pendown()

        self.aff_mur_h()

        self.aff_mur_v()

        self.sebri.penup()
        self.sebri.forward(self.board_w // 20)
        self.sebri.setheading(90)
        self.sebri.forward(self.board_h // 40 + self.board_h //10)
        for i in range(1, 10):
            self.sebri.write(str(i), align='center', font=('Arial', '15', 'normal'))
            self.sebri.forward(self.board_h // 10)

        self.sebri.goto(self.origin)
        self.sebri.forward(self.board_h // 40)
        self.sebri.setheading(0)
        self.sebri.forward(self.board_w // 20 + self.board_w //10)
        for i in range(1, 10):
            self.sebri.write(str(i), align='center', font=('Arial', '15', 'normal'))
            self.sebri.forward(self.board_w // 10)

        self.sebri.goto(self.origin)

        self.sebri.penup()
        self.sebri.setheading(90)
        self.sebri.forward(self.board_h + self.board_h//20 * 5)
        self.sebri.write("Légende: ", font=('Courier', '20', 'italic'))
        self.sebri.backward(self.board_h //20)
        self.sebri.write("1. " + str(self.état["joueurs"][0]['nom']) + ' (green): '\
            + str(self.état["joueurs"][0]['murs']), font=('Arial', '10', 'normal'))

        self.sebri.backward(self.board_h //20)
        self.sebri.write("2. " + str(self.état["joueurs"][1]['nom']) + ' (red): '\
            + str(self.état["joueurs"][1]['murs']), font=('Arial', '10', 'normal'))

        self.draw_mur_v()

        self.draw_mur_h()

        self.légende()

        self.sebri.goto(self.origin)
        self.sebri.pencolor("black")

    def terminé(self, winner):
        """
        méthode pour afficher une fenetre si le jeu est fini
        """
        self.sebri.clear()
        self.sebri.goto((0,80))
        self.sebri.write("Game is over", align="center", font=("Cooper Black", 50, "italic"))
        self.sebri.goto((0,-30))
        self.sebri.write("The Winner is: " + str(winner), align="center",
        font=("Arial", 20, "normal"))
        self.sebri.pencolor("grey")
        self.sebri.goto((0,-120))
        self.sebri.write("To quit the game, please click the left mouse button",
        align="center", font=("Arial", 15, "normal"))
        self.board.exitonclick()

    def demander_coup(self):
        """
        méthode pour demander le coup graphiquement
        """
        move = self.board.textinput("Quel type de coup voulez-vous jouer : ", "(D, MH, MV)")
        position2 = []
        if move in ('D', 'MH', 'MV'):
            position1 = self.board.textinput("À quelle position voulez-vous jouer : ", "(x, y)")
            position2.append(int(position1[0]))
            position2.append(int(position1[2]))
        return (move, position2)
