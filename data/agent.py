import pygame
import random
import math
from data.cell import material
from data.grid import cellGradiantGrid


class agent:
    def __init__(self, x, y, size, sensorDistance, sensorAngle, turnChance, randomAngle, gradiantGrid=cellGradiantGrid):
        self.x = x
        self.y = y
        self.size = size
        self.chemGrid = gradiantGrid
        self.xVel = random.randint(-size, size)
        self.yVel = random.randint(-size, size)
        self.normalize()
        self.sensorAngle = sensorAngle
        self.sensorDistance = sensorDistance
        self.turnChance = turnChance
        self.randomAngle = randomAngle

    def move(self):
        self.sense()
        if (self.x+self.xVel <= (self.chemGrid.x)) or (self.x+self.xVel >= self.chemGrid.x+(self.chemGrid.halfWidth*2)):
            self.xVel *= -1
        if (self.y+self.yVel <= (self.chemGrid.y)) or (self.y+self.yVel >= (self.chemGrid.y+(self.chemGrid.halfHeight*2))):
            self.yVel *= -1
        self.x += self.xVel
        self.y += self.yVel
        translated = self.chemGrid.translateIndex(self.x, self.y)
        if translated[0] < self.chemGrid.rowCount and translated[0] >= 0 and translated[1] >= 0 and translated[1] < self.chemGrid.columnCount:
            self.chemGrid.grid[translated[0]
                               ][translated[1]].addMaterial(material((255, 255, 0), 0.16, 0.08))

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0),
                           (self.x, self.y), self.size/2)

    def sense(self):
        mag = self.size
        self.normalize()
        forward = (self.xVel, self.yVel)
        rotatedLeft = self.rotate(self.radians(-self.sensorAngle))
        rotatedRight = self.rotate(self.radians(self.sensorAngle))
        forwardPos = (self.x+self.xVel, self.y+self.yVel)
        rightPos = (self.x+rotatedRight[0], self.y+rotatedRight[1])
        leftPos = (self.x+rotatedLeft[0], self.y+rotatedLeft[1])
        maxChem = 0
        direction = 'f'
        if (forwardPos[0] > (self.chemGrid.x)) and (forwardPos[0] < self.chemGrid.x+(self.chemGrid.halfWidth*2)) and (forwardPos[1] > (self.chemGrid.y)) and (forwardPos[1] < self.chemGrid.y+(self.chemGrid.halfHeight*2)):
            index = self.chemGrid.translateIndex(forwardPos[0], forwardPos[1])
            maxChem = self.chemGrid.grid[index[0]][index[1]].intensity
        if (rightPos[0] > (self.chemGrid.x)) and (rightPos[0] < self.chemGrid.x+(self.chemGrid.halfWidth*2)) and (rightPos[1] > (self.chemGrid.y)) and (rightPos[1] < self.chemGrid.y+(self.chemGrid.halfHeight*2)):
            index = self.chemGrid.translateIndex(rightPos[0], rightPos[1])
            chem = self.chemGrid.grid[index[0]][index[1]].intensity
            if maxChem < chem:
                maxChem = chem
                direction = 'r'
        if (leftPos[0] > (self.chemGrid.x)) and (leftPos[0] < self.chemGrid.x+(self.chemGrid.halfWidth*2)) and (leftPos[1] > (self.chemGrid.y)) and (leftPos[1] < self.chemGrid.y+(self.chemGrid.halfHeight*2)):
            index = self.chemGrid.translateIndex(leftPos[0], leftPos[1])
            chem = self.chemGrid.grid[index[0]][index[1]].intensity
            if maxChem < chem:
                maxChem = chem
                direction = 'l'
        if (direction == 'l'):
            self.xVel = rotatedLeft[0]
            self.yVel = rotatedLeft[1]
        elif (direction == 'r'):
            self.xVel = rotatedRight[0]
            self.yVel = rotatedRight[1]
        else:
            self.xVel = forward[0]
            self.yVel = forward[1]
        if random.random() <= (self.turnChance/100):
            temp = self.rotate(
                self.radians(-self.randomAngle*(random.random()*self.randomAngle*2)))
            self.xVel = temp[0]
            self.yVel = temp[1]
        self.normalize()
        if self.mag() > 0:
            self.xVel *= mag
            self.yVel *= mag
        else:
            self.xVel = 1
            self.yVel = 1
            self.normalizeNScale(self.size)

    # Rotation Matrix values
    # x=x*cos(angle)-ysin(angle)
    # y=x*sin(angle)-ycos(angle)

    def rotate(self, angle):
        xPrime = (-self.xVel*math.cos(angle))-(-self.yVel*math.sin(angle))
        yPrime = (-self.xVel*math.sin(angle))-(-self.yVel*math.cos(angle))
        return (xPrime, yPrime)

    def normalize(self):
        mag = self.mag()
        if (mag > 0):
            self.xVel /= mag
            self.yVel /= mag

    def normalizeNScale(self, scalar):
        mag = self.mag()
        if (mag > 0):
            self.xVel /= mag
            self.yVel /= mag
            self.xVel *= scalar
            self.yVel *= scalar

    def mag(self):
        return math.sqrt(pow(self.xVel, 2)+pow(self.yVel, 2))

    def getAngle(self):
        return math.atan2(self.yVel, self.xVel)

    def degrees(self, radians=float):
        return (radians*180/math.pi)

    def radians(self, degrees=float):
        return (degrees*math.pi/180)

    def increaseSensorDistance(self):
        self.sensorDistance += 1

    def decreaseSensorDistance(self):
        if self.sensorDistance > 0:
            self.sensorDistance -= 1

    def increaseSensorAngle(self):
        if self.sensorAngle < 360:
            self.sensorAngle += 5

    def decreaseSensorAngle(self):
        if self.sensorAngle > 0:
            self.sensorAngle -= 5

    def increaseRandomAngle(self):
        if self.randomAngle < 360:
            self.randomAngle += 10

    def decreaseRandomAngle(self):
        if self.randomAngle > 0:
            self.randomAngle -= 10

    def increaseTurnChance(self):
        if self.turnChance < 100:
            self.turnChance += 10

    def decreaseTurnChance(self):
        if self.turnChance > 0:
            self.turnChance -= 10
