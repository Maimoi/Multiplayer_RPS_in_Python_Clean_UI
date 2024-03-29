import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player")

paper = pygame.image.load("paper.png") 
rock = pygame.image.load("rock.png") 
scisor = pygame.image.load("scisor.png") 
bg = pygame.image.load("bg.jpg")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("aria", 30)
        text = font.render(self.text, 1, (0,0, 0))
        win.blit(text, (self.x + round(self.width/3) - round(text.get_width()/3), self.y + round(self.height/3) - round(text.get_height()/2)))
     

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((0,0,0))
    win.blit(rock, (50,400))
    win.blit(scisor, (250,400))
    win.blit(paper, (450,400))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/3, height/2 - text.get_height()/3))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 150))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (300, 150))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (255, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (255, 0, 0))

        if p == 1:
            win.blit(text2, (100, 200))
            win.blit(text1, (300, 300))
        else:
            win.blit(text1, (100,200))
            win.blit(text2, (300, 300))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 600, (0,0,255)), Button("Scissors", 250, 600, (255,0,0)), Button("Paper", 450, 600, (0,255,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        #win.fill((0,0,0))
        font = pygame.font.SysFont("comicsans", 70)
        font1 = pygame.font.SysFont("monospace", 40, bold = True)
        text1 = font1.render("ROCK PAPER SCISORS", 1, (0,0,255))
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(bg, (0,0))
        win.blit(text, (180,450))
        win.blit(text1, (270, 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
