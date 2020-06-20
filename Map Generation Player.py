from noise import snoise2
import pygame

width = 1280
height = 720
window = pygame.display.set_mode((width, height))


class GameMap(object):
    def __init__(self, map_width, map_height):
        self.block_size = 32
        self.map_height = map_height * 2 // self.block_size
        self.map_width = map_width * 2 // self.block_size
        self.scl = 0.1
        self.px = 0
        self.py = 0

    def create(self):
        f = open('game.txt', 'w')
        xcor = 0
        for x in range(self.map_width):
            ycor = 0
            for y in range(self.map_height):
                val = int(abs(snoise2(x * self.scl, y * self.scl) * 10))
                f.write(str(val))
                ycor += self.block_size
            xcor += self.block_size
            f.write(str('\n'))
        f.close()

    def load_game(self):
        f = open('game.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        load = []
        for xcor in data:
            col = []
            for ycor in xcor:
                col.append(ycor)
            load.append(col)
        return load

    def draw(self, g_arr):
        window.fill([15, 50, 125])
        xcor = 0
        for x in g_arr:
            ycor = 0
            for y in x:
                if 0 <= int(y) <= 2:  # water
                    pygame.draw.rect(window, (0, 0, 255),
                                     (self.px + xcor, self.py + ycor, self.block_size, self.block_size))
                elif 2 < int(y) <= 4:  # sand
                    pygame.draw.rect(window, (255, 255, 154),
                                     (self.px + xcor, self.py + ycor, self.block_size, self.block_size))
                elif 4 < int(y) <= 6:  # grass
                    pygame.draw.rect(window, (0, 255, 0),
                                     (self.px + xcor, self.py + ycor, self.block_size, self.block_size))
                elif 6 < int(y) <= 8:  # stone
                    pygame.draw.rect(window, (int(y) * 25, int(y) * 25, int(y) * 25),
                                     (self.px + xcor, self.py + ycor, self.block_size, self.block_size))
                elif 8 < int(y) <= 10:  # snow
                    pygame.draw.rect(window, (255, 255, 255),
                                     (self.px + xcor, self.py + ycor, self.block_size, self.block_size))
                ycor += self.block_size
            xcor += self.block_size


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(window, (159, 75, 255), (self.x, self.y), 25, 25)


player = Player(width // 2, height // 2)
game_map = GameMap(height, width)
game_map.create()
gmap = game_map.load_game()

game = True
while game:
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()
            quit()
        if pressed[pygame.K_a]:
            game_map.px += game_map.block_size
        if pressed[pygame.K_w]:
            game_map.py += game_map.block_size
        if pressed[pygame.K_d]:
            game_map.px -= game_map.block_size
        if pressed[pygame.K_s]:
            game_map.py -= game_map.block_size

    game_map.draw(gmap)
    player.draw()
    pygame.display.update()
