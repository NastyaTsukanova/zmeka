import pygame
import random

pygame.init()
window = pygame.display.set_mode((402, 402))
pygame.display.set_caption("Game Artur&Lesha&Vika")
screen = pygame.Surface((402, 402))

q = True  # для главного цикла


# рисуем сетку
def draw_setka():
    x = 0
    x_x = 400
    y = 0
    y_y = 400
    for i in range(11):
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y_y), 2)
        x += 40
    x = 0
    for i2 in range(11):
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x_x, y), 2)
        y += 40
    # класс героя, элемента хвоста, яблока


class Zmeika:
    def __init__(self, xpos, ypos, filename):
        self.xpos = xpos
        self.ypos = ypos
        self.bitmap = pygame.image.load(filename)

    def render(self):
        screen.blit(self.bitmap, (self.xpos * 40 + 2, self.ypos * 40 + 2))


# движение хвоста
def going_hv():
    x = 2
    y = len(coordinaty)
    for i in reversed(coordinaty[1:]):
        i.xpos, i.ypos = coordinaty[y - x].xpos, coordinaty[
            y - x].ypos  # каждый кубик (элемент хвоста) получает координаты стоящего перед ним (ближе к голове змейки)
        x += 1


counter = 0  # для будущего счёта
hvost = Zmeika(4, 5, 'golova1.png')
golova = Zmeika(4, 4, 'golova2.png')
going = ''  # для клавиш
coordinaty = [golova, hvost]  # тут хранится змейка
apple = Zmeika(10, 10, 'apple.png')


# движение головы змейки
def do_going():
    if going == 'left':
        going_hv()
        coordinaty[0].xpos -= 1
        if (coordinaty[0].ypos and coordinaty[0].xpos) not in coordinaty:
            if coordinaty[0].xpos < 0:
                coordinaty[0].xpos = 9
    if going == 'right':
        going_hv()
        coordinaty[0].xpos += 1
        if (coordinaty[0].ypos and coordinaty[0].xpos) not in coordinaty:
            if coordinaty[0].xpos > 9:
                coordinaty[0].xpos = 0
    if going == 'up':
        going_hv()
        coordinaty[0].ypos -= 1
        if (coordinaty[0].ypos and coordinaty[0].xpos) not in coordinaty:
            if coordinaty[0].ypos < 0:
                coordinaty[0].ypos = 9
    if going == 'down':
        going_hv()
        coordinaty[0].ypos += 1
        if (coordinaty[0].ypos and coordinaty[0].xpos) not in coordinaty:
            if coordinaty[0].ypos > 9:
                coordinaty[0].ypos = 0
    w = False
    for i in coordinaty[1:]:
        if (i.xpos, i.ypos) == (coordinaty[0].xpos, coordinaty[0].ypos):
            w = True
            break
        else:
            continue
    return w


# генерация яблока
def apple_gen():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    for i in coordinaty:
        if (i.xpos, i.ypos) == (x, y):
            x, y = apple_gen()
        else:
            continue
    return x, y


apple.xpos, apple.ypos = apple_gen()  # начальное положение яблока
# pygame.mixer.init()
# pygame.mixer.music.load('music.ogg')
# pygame.mixer.music.play(loops=-1)
while q:
    some_x = coordinaty[-1].xpos  # если бедет захвачено яблоко, добавленной части хвоста передаётся это значение по Х
    some_y = coordinaty[-1].ypos  # --//-- по У
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q = False
        if event.type == pygame.KEYDOWN:
            # Выясняем какая именно кнопка была нажата
            if event.key == pygame.K_LEFT and going != 'right':
                going = 'left'
            if event.key == pygame.K_RIGHT and going != 'left':
                going = 'right'
            if event.key == pygame.K_UP and going != 'down':
                going = 'up'
            if event.key == pygame.K_DOWN and going != 'up':
                going = 'down'
    s = do_going()  # передаем новые координаты змейки
    if s:
        q = False
        window.blit(pygame.image.load('Game-Over.png'), (0, 0))
        pygame.display.flip()
        pygame.mixer.music.stop()
        # ToDO: Вставить сюда музыку
        pygame.mixer.music.load('Say What Again.ogg')
        pygame.mixer.music.play(loops=-1)
        pygame.time.delay(7500)
    else:
        # если съедено яблоко
        if coordinaty[0].xpos == apple.xpos and coordinaty[0].ypos == apple.ypos:
            counter += 1
            coordinaty.append(Zmeika(some_x, some_y, 'golova1.png'))
            apple.xpos, apple.ypos = apple_gen()
        screen.fill((0, 0, 0))
        draw_setka()
        # отрисовка змейки через цикл
        for i in coordinaty:
            i.render()
        apple.render()
        window.blit(screen, (0, 0))
        pygame.display.flip()
        pygame.time.delay(300)
pygame.quit()
