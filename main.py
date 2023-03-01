import random
import pygame
from data.grid import cellGradiantGrid
from data.agent import agent
pygame.init()
WIDTH = 1400
HEIGHT = 700
TICKS = 300
font = pygame.font.Font("data/Font/big_noodle_titling.ttf", 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
W, A, S, D, U, D, R, L = False, False, False, False, False, False, False, False


STEP_TIME = 0
AGENT_COUNT = 8000
PAUSED = True
HOLDING = False
RC = 90
CC = 150
CS = 4
SA = 15
SD = 1
TC = 30
RA = 20
plane = cellGradiantGrid(130, 100, RC, CC, CS)
particles = []
# for i in range(AGENT_COUNT):
#     particles.append(agent(plane.x+random.random()*(plane.halfWidth*2),
#                      plane.y+random.random()*(plane.halfHeight*2), CS/CS, plane))
for i in range(AGENT_COUNT):
    particles.append(agent(plane.x+random.randint(CS, CS*CC),
                     plane.y+random.randint(CS, CS*RC), CS, SD, SA, TC, RA, plane))


timer = STEP_TIME

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            HOLDING = True
        if event.type == pygame.MOUSEBUTTONUP:
            HOLDING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PAUSED = not PAUSED
            if event.key == pygame.K_UP:
                for single in particles:
                    single.increaseSensorDistance()
                SD += 1
            if event.key == pygame.K_DOWN:
                for single in particles:
                    single.decreaseSensorDistance()
                if SD > 0:
                    SD -= 1
            if event.key == pygame.K_RIGHT:
                for single in particles:
                    single.increaseSensorAngle()
                if SA < 360:
                    SA += 5
            if event.key == pygame.K_LEFT:
                for single in particles:
                    single.decreaseSensorAngle()
                if SA > 0:
                    SA -= 5

            if event.key == pygame.K_w:
                for single in particles:
                    single.increaseRandomAngle()
                if RA < 360:
                    RA += 10
            if event.key == pygame.K_s:
                for single in particles:
                    single.decreaseRandomAngle()
                if RA > 0:
                    RA -= 10
            if event.key == pygame.K_d:
                for single in particles:
                    single.increaseTurnChance()
                if TC < 100:
                    TC += 10
            if event.key == pygame.K_a:
                for single in particles:
                    single.decreaseTurnChance()
                if TC > 0:
                    TC -= 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                U = False
            if event.key == pygame.K_DOWN:
                D = False
            if event.key == pygame.K_RIGHT:
                R = False
            if event.key == pygame.K_LEFT:
                L = False
            if event.key == pygame.K_w:
                W = False
            if event.key == pygame.K_s:
                A = False
            if event.key == pygame.K_d:
                D = False
            if event.key == pygame.K_a:
                S = False
    if HOLDING:
        mousePos = pygame.mouse.get_pos()
        plane.handleClick(mousePos[0], mousePos[1])
    if not PAUSED:
        if timer <= 0:
            timer = STEP_TIME
            plane.step()
            plane.update()
            for i in range(AGENT_COUNT):
                particles[i].move()
        else:
            timer = timer-1

    screen.fill((100, 100, 100))
    plane.draw(screen)
    clock.tick(TICKS)
    FPS = font.render(
        "FPS:  "+str(round(clock.get_fps(), 2)), True, (0, 255, 0))
    screen.blit(FPS, (40, 100))
    status = ""
    c = (0, 255, 0)
    if PAUSED:
        status = "Paused"
        c = (255, 0, 0)
    else:
        status = "Running"
    # for single in particles:
    #     single.draw(screen)
    FPS = font.render(status, True, c)
    screen.blit(FPS, (40, 150))

    SDString = "Sensor Distance:  "+str(SD)
    FPS = font.render(SDString, True, c)
    screen.blit(FPS, ((CS*CC)+150, 110))

    SAString = "Sensor Angle:  "+str(SA)
    FPS = font.render(SAString, True, c)
    screen.blit(FPS, ((CS*CC)+150, 130))

    TCString = "Turn Chance:  "+str(TC)
    FPS = font.render(TCString, True, c)
    screen.blit(FPS, ((CS*CC)+150, 150))

    RAString = "Random Angle:  "+str(RA)
    FPS = font.render(RAString, True, c)
    screen.blit(FPS, ((CS*CC)+150, 170))

    pygame.display.update()
