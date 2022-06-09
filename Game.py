# Joel Wisdom (2005295)
# Occurrence: UM1
# Title: CNS1001 Final Project - Snakes and Ladders Program
# About: This snake and ladder game is coded using the pygame module, one of a few ways in 
#        in which we can implement our game in a GUI form.

import pygame
from pygame.locals import *
import random
import sys

clock = pygame.time

# initialize pygame, set window surface size, caption and icon
pygame.init()

# load background and board images
icon = pygame.image.load("game images/icon.png")
bg = pygame.image.load("game images/forest.png")
board = pygame.image.load("game images/board.png")
title_image = pygame.image.load("game images/title image.png")

# load button images
start = pygame.image.load("buttons/start.png")
end = pygame.image.load("buttons/exit.png")
playAgain = pygame.image.load("buttons/play again.png")
roll = pygame.image.load("buttons/roll.png")
onePlayer = pygame.image.load("buttons/1player.png")
twoPlayer = pygame.image.load("buttons/2player.png")
threePlayer = pygame.image.load("buttons/3player.png")
fourPlayer = pygame.image.load("buttons/4player.png")

# load player icons
p1 = pygame.image.load("player icons/blue.png")
p2 = pygame.image.load("player icons/red.png")
p3 = pygame.image.load("player icons/yellow.png")
p4 = pygame.image.load("player icons/green.png")

# load dice face images
d1 = pygame.image.load("dice/d1.png")
d2 = pygame.image.load("dice/d2.png")
d3 = pygame.image.load("dice/d3.png")
d4 = pygame.image.load("dice/d4.png")
d5 = pygame.image.load("dice/d5.png")
d6 = pygame.image.load("dice/d6.png")
dice_img = [d1, d2, d3, d4, d5, d6]

# load sounds
ladder_sound = pygame.mixer.Sound("audio/ladder.wav")
snake_sound = pygame.mixer.Sound("audio/rattlesnake.wav")

# set display mode (window size), window title and icon
win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Snake and Ladder")
pygame.display.set_icon(icon)


class Message:
    """A class to represent a message displayed on the screen.

    Attributes:
        text (str): message text
        font (pygame.font): message font
        font_size (int): size of message text
        x_position (int): message x position on screen
        y_position (int): message y position on screen

    """

    def __init__(self, text, font_size, x, y):
        """initializes Message object.

        Args:
            text: text to be displayed
            font_size: size of text
            x: message x position on screen
            y: message y position on screen
        """
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font("font/FreeSansBold.ttf", self.font_size)  #: pygame font object
        self.x_position = x
        self.y_position = y

    def draw(self):
        """creates pygame surface from text and renders it on screen"""
        text_surface = self.font.render(self.text, True, "white")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x_position, self.y_position)
        win.blit(text_surface, text_rect)


class Button:
    """A class to represent an onscreen button.

    Attributes:
        width (int): button width
        height (int): button height
        x_position (int): button x position on screen
        y_position (int): button y position on screen
        image (pygame.image): button image, what the button displays

    """

    def __init__(self, x, y, image, scale):
        """initializes Button object.

        Args:
            x: message x position on screen
            y: message y position on screen
            image: button image
            scale: scale to size the button image

        """
        self.width = image.get_width()
        self.height = image.get_height()
        self.x_position = x
        self.y_position = y
        self.image = pygame.transform.scale(image, (int(self.width * scale), (int(self.height * scale))))
        self.rect = 0

    def draw(self):
        """Creates the button surface and then renders it on screen"""
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_position, self.y_position)
        win.blit(self.image, (self.rect.x, self.rect.y))

    def check_click(self, event):
        """Checks if the button is clicked.

        Args:
            event (pygame.event): pygame event is whatever is happening in the game window.

        Returns:
            True if button clicked, False if not

        """
        mouse_position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        # selection to check if the event was a mouse button press
        if event.type == MOUSEBUTTONDOWN:
            # check if the press was within the button bounds
            if self.rect.collidepoint((mouse_position[0], mouse_position[1])):
                if click:
                    return True
        return False


class Menu:
    """A class to represent a Menu.

    Attributes:
        start (Button): button to start the game
        exit (Button): button to exit the program
        P1 (Button): button to start game with one player
        P2 (Button): button to start game with two players
        P3 (Button): button to start game with three players
        P4 (Button): button to start game with four players
        play_again (Button): button to play the game again

    """

    def __init__(self):
        """initialize Menu object"""
        self.start = Button(225, 400, start, .5)
        self.exit = Button(475, 400, end, .5)
        self.P1 = Button(350, 100, onePlayer, 1)
        self.P2 = Button(350, 200, twoPlayer, 1)
        self.P3 = Button(350, 300, threePlayer, 1)
        self.P4 = Button(350, 400, fourPlayer, 1)
        self.play_again = Button(350, 400, playAgain, 1)

        # call main_menu once Menu class is instantiated
        self.pSelect = self.main_menu()

    def main_menu(self):
        """Displays the main menu where the user can choose to Start or to Exit.

        Returns:
            True is start button is clicked, False if exit button is clicked.
        """
        win.blit(bg, (0, 0))
        win.blit(title_image, (100, 0))
        self.start.draw()
        self.exit.draw()
        show_menu = True
        while show_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                continue_game = self.start.check_click(event)
                end_game = self.exit.check_click(event)
                if continue_game:
                    return True
                if end_game:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def player_select(self):
        """Displays the player options menu where the number of players can be selected.

        Returns:
            number of players
        """

        # Draw background and player select buttons on screen
        win.blit(bg, (0, 0))
        self.P1.draw()
        self.P2.draw()
        self.P3.draw()
        self.P4.draw()

        player_selection = True
        while player_selection:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                one_p = self.P1.check_click(event)
                two_p = self.P2.check_click(event)
                three_p = self.P3.check_click(event)
                four_p = self.P4.check_click(event)
                if one_p:
                    return 1
                elif two_p:
                    return 2
                elif three_p:
                    return 3
                elif four_p:
                    return 4
            pygame.display.update()

    def end_screen(self, winner):
        win.blit(bg, (0, 0))
        win_message = Message(f"{winner.color.upper()} WINS!", 30, 350, 250)
        win_message.draw()
        self.play_again.draw()

        ending = True
        while ending:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                go_again = self.play_again.check_click(event)
                end_game = self.exit.check_click(event)
                if go_again:
                    clock.wait(1000)
                    return
                if end_game:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


class Player:
    """A class to used to represent a player.

    Attributes:
        icon (pygame.image): image to represent player on screen
        color (str): color of the player
        square (int): player square on the game board
        x (int): player x position on screen
        y (int): player y position on screen
    """

    def __init__(self, color):
        """initializes Player object"""
        self.icon = pygame.image.load("player icons/" + color + ".png")
        self.color = color
        self.square = 0
        self.x = 150
        self.y = 500

    def turn(self):
        """Handles a players turn to roll dice and move.

        Returns:
            new_square: player new square after dice roll and checking for snakes/ladders
            new_position: player new on-screen position based on new_square
            six: True if player rolled a six, False if not

        """
        dice, six = self.roll_dice()
        new_square = self.square + dice

        # Display messages to user with previous and dice roll
        Message(f"Was on {self.square}", 20, 100, 220).draw()
        Message(f"Rolled {dice}", 20, 100, 245).draw()

        # If new_square after roll is greater than 100, make it 100
        if new_square >= 100:
            new_square = 100

        # Display message with square the player landed on
        Message(f"Landed on {new_square}", 20, 100, 270).draw()

        # check for snakes and ladder and get the player onscreen position for the new square
        new_square = Board().check_snake(new_square)
        new_square = Board().check_ladder(new_square)
        new_position = Board().positions[new_square]

        return new_square, new_position, six

    def draw(self):
        """Render the player on screen"""
        win.blit(self.icon, (self.x, self.y))

    @staticmethod
    def roll_dice():
        """Dice roll

        Returns:
            dice: the dice number rolled
            six: True if six is rolled, False if not
        """
        six = False
        dice = random.randint(1, 6)
        if dice == 6:
            six = True

        # Render dice face image based on dice rolled
        win.blit(dice_img[dice - 1], (68, 100))

        return dice, six


class Game:
    """A class to represent a snake and ladder Game.

    Attributes:
        num_players (int): number of players in the game
        player1 (Player): player 1
        player2 (Player): player 2
        player3 (Player):player 3
        player4 (Player): player 4
        players (list): list of which players are playing based on num_players
        board (Board): game board
        roll (Button): button for player to roll dice

    """

    def __init__(self, players):
        """initialize the Game.

        Arg:
            players (int): the amount of players in the game

        """
        self.num_players = players
        self.roll = Button(100, 50, roll, 1)
        self.board = Board()
        self.player1 = Player("blue")
        self.player2 = Player("red")
        self.player3 = Player("yellow")
        self.player4 = Player("green")

        # if statements to create Player instances based on the number of players
        if self.num_players > 0:
            self.players = [self.player1]
        if 5 > self.num_players > 1:
            self.players.append(self.player2)
        if 5 > self.num_players > 2:
            self.players.append(self.player3)
        if 5 > self.num_players > 3:
            self.players.append(self.player4)

    def draw(self):
        """Displays the game board, player icons and dice roll button"""
        win.blit(bg, (0, 0))
        self.roll.draw()
        self.board.draw()

    def draw_players_onboard(self):
        """Renders all players in game on screen"""
        if self.num_players > 0:
            self.player1.draw()
        if 5 > self.num_players > 1:
            self.player2.draw()
        if 5 > self.num_players > 2:
            self.player3.draw()
        if 5 > self.num_players > 3:
            self.player4.draw()

    def in_game(self):
        """Contains the logic of Snake and Ladder which handles the playing of the game.

        Returns:
            True if a player reaches square 100
            player that got to 100

        """
        roll_num = 1
        turn = False
        in_game = True
        while in_game:
            self.draw_players_onboard()  # draw all players on board to show previous positions

            # Pygame event handler loop to get events that happen in the game window.
            for event in pygame.event.get():
                # check for pygame QUIT event which is when player closes the program window
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # check if roll button is clicked
                if self.roll.check_click(event):
                    turn = True
                    self.draw()
            if turn:
                player = self.players[roll_num - 1]
                Message(f"{player.color.upper()}'s Turn", 25, 100, 190).draw()
                new_square, new_position, six = player.turn()
                player.square = new_square
                player.x, player.y = new_position[0], new_position[1]

                # Draw circle of player color to show its their turn
                pygame.draw.circle(win, player.color, (100, 420), 50)

                self.draw_players_onboard()  # draw all players on board with new positions

                if new_square == 100:
                    player.draw()
                    pygame.display.flip()
                    pygame.event.pump()
                    clock.wait(2000)
                    return True, player

                if six:
                    roll_num = roll_num
                    Message(f"Roll Again.", 20, 100, 345).draw()
                elif not six:
                    roll_num += 1
                    if roll_num == 2 and self.num_players == 1:
                        roll_num = 1
                    elif roll_num == 3 and self.num_players == 2:
                        roll_num = 1
                    elif roll_num == 4 and self.num_players == 3:
                        roll_num = 1
                    elif roll_num == 5 and self.num_players == 4:
                        roll_num = 1

                turn = False
                pygame.display.update()
            pygame.display.update()


class Board:
    """A class to represent a snake and ladder board.

    Attributes:
        positions (list): list holding screen position coordinates for squares on the board.
        snakes (dict): dictionary storing snake squares, snake mouth:snake tail
        ladders (dict): dictionary storing ladder squares, ladder bottom:ladder top

    """
    def __init__(self):
        self.positions = [[150, 500],
                          [200, 450], [250, 450], [300, 450], [350, 450], [400, 450], [450, 450],
                          [500, 450], [550, 450], [600, 450], [650, 450],
                          [650, 400], [600, 400], [550, 400], [500, 400], [450, 400], [400, 400], [350, 400],
                          [300, 400], [250, 400], [200, 400],
                          [200, 350], [250, 350], [300, 350], [350, 350], [400, 350], [450, 350], [500, 350],
                          [550, 350], [600, 350], [650, 350],
                          [650, 300], [600, 300], [550, 300], [500, 300], [450, 300], [400, 300], [350, 300],
                          [300, 300], [250, 300], [200, 300],
                          [200, 250], [250, 250], [300, 250], [350, 250], [400, 250], [450, 250], [500, 250],
                          [550, 250], [600, 250], [650, 250],
                          [650, 200], [600, 200], [550, 200], [500, 200], [450, 200], [400, 200], [350, 200],
                          [300, 200], [250, 200], [200, 200],
                          [200, 150], [250, 150], [300, 150], [350, 150], [400, 150], [450, 150], [500, 150],
                          [550, 150], [600, 150], [650, 150],
                          [650, 100], [600, 100], [550, 100], [500, 100], [450, 100], [400, 100], [350, 100],
                          [300, 100], [250, 100], [200, 100],
                          [200, 50], [250, 50], [300, 50], [350, 50], [400, 50], [450, 50], [500, 50], [550, 50],
                          [600, 50], [650, 50],
                          [650, 0], [600, 0], [550, 0], [500, 0], [450, 0], [400, 0], [350, 0], [300, 0], [250, 0],
                          [200, 0]]
        self.snakes = {32: 10, 36: 6, 48: 26, 62: 18, 88: 24, 95: 56, 97: 78}
        self.ladders = {1: 38, 4: 14, 8: 30, 21: 42, 28: 76, 50: 67, 71: 92, 80: 99}

    @staticmethod
    def draw():
        """Render the board on screen"""
        win.blit(board, (200, 0))

    def check_snake(self, square):
        """Checks if player landed on a square with a snake and updates the square

        Args:
            square (int): player square on game board

        Returns:
            square

        """
        # loop through snake dictionary to check if square is in it. If yes, update square
        for snake in self.snakes:
            if square == snake:
                snake = snake
                square = self.snakes[snake]

                # Display to player they were bit a snake and play snake sound
                Message(f"Got bit by a Snake", 20, 100, 295).draw()
                Message(f"Ended up on {square}", 20, 100, 320).draw()
                pygame.mixer.Sound.play(snake_sound)
        return square

    def check_ladder(self, square):
        for ladder in self.ladders:
            if square == ladder:
                ladder = ladder
                square = self.ladders[ladder]
                Message(f"Went up a Ladder", 20, 100, 295).draw()
                Message(f"Ended up on {square}", 20, 100, 320).draw()
                pygame.mixer.Sound.play(ladder_sound)
        return square


def main():
    win.blit(bg, (0, 0))
    # load and play background music
    pygame.mixer.music.load("audio/forestwalk.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    run = True
    while run:
        # Pygame event handler loop to get events that happen in the game window.
        for event in pygame.event.get():
            # check for pygame QUIT event which is when player closes the program window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        menu = Menu()
        if menu.pSelect:
            players = menu.player_select()
            game = Game(players)
            game.draw()
            game_end, winner = game.in_game()
            if game_end:
                menu.end_screen(winner)
        pygame.display.update()


if __name__ == "__main__":
    main()
