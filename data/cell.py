import pygame


class cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.occupied = False

    def draw(self, surface):
        if self.occupied:
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(
                self.x-(self.size/2), self.y-(self.size/2), self.size, self.size))
        else:
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(
                self.x-(self.size/2), self.y-(self.size/2), self.size, self.size))

    def handleClick(self, x, y):
        if (x >= (self.x-(self.size/2))) and (x <= (self.x+(self.size/2))):
            if (y >= (self.y-(self.size/2))) and (y <= (self.y+(self.size/2))):
                self.occupied = not self.occupied

    def isHovering(self, x, y):
        if (x >= (self.x-(self.size/2))) and (x <= (self.x+(self.size/2))):
            if (y >= (self.y-(self.size/2))) and (y <= (self.y+(self.size/2))):
                return True
        return False


class material:
    def __init__(self, color=tuple, intensity=float, rate=float):
        self.color = color
        self.intensity = intensity
        self.rate = rate


class cellGradiant:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.intensity = 0
        self.rate = 0
        # This will hold the next intensity value after update
        self.nextValue = (0, 0, (0, 0, 0))
        self.materialColor = (0, 0, 0)

    def draw(self, surface):
        r = int(self.materialColor[0]*(self.intensity))
        g = int(self.materialColor[1]*(self.intensity))
        b = int(self.materialColor[2]*(self.intensity))
        if self.intensity <= 0:
            self.addMaterial(material((0, 0, 0), 0, 0))
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        pygame.draw.rect(surface, (r, g, b), pygame.Rect(
            self.x-(self.size/2), self.y-(self.size/2), self.size, self.size))

    def handleClick(self, x, y):
        if (x >= (self.x-(self.size/2))) and (x <= (self.x+(self.size/2))):
            if (y >= (self.y-(self.size/2))) and (y <= (self.y+(self.size/2))):
                self.addMaterial(material((0, 0, 255), 1, 0.1))

    def addMaterial(self, material):
        self.intensity += material.intensity
        if self.intensity > 1:
            self.intensity = 1
        self.rate = material.rate
        self.materialColor = material.color

    def setIntensity(self, intensity):
        self.intensity = intensity

    def evaporate(self):
        if self.intensity > 0:
            self.intensity = self.intensity-self.rate

    def diffuse(self, rowIndex, columnIndex, cell_gradiant_grid):
        count = 0
        averageValue = 0
        averageRate = 0
        r = 0
        g = 0
        b = 0
        # Check Left
        if columnIndex > 0:
            averageValue = averageValue + \
                cell_gradiant_grid.grid[rowIndex][columnIndex-1].intensity
            averageRate = averageRate + \
                cell_gradiant_grid.grid[rowIndex][columnIndex-1].rate
            r += cell_gradiant_grid.grid[rowIndex][columnIndex -
                                                   1].materialColor[0]
            g += cell_gradiant_grid.grid[rowIndex][columnIndex -
                                                   1].materialColor[1]
            b += cell_gradiant_grid.grid[rowIndex][columnIndex -
                                                   1].materialColor[2]
            count += 1
        # Check Right
        if columnIndex < cell_gradiant_grid.columnCount-1:
            averageValue = averageValue + \
                cell_gradiant_grid.grid[rowIndex][columnIndex+1].intensity
            averageRate = averageRate + \
                cell_gradiant_grid.grid[rowIndex][columnIndex+1].rate

            r += cell_gradiant_grid.grid[rowIndex][columnIndex +
                                                   1].materialColor[0]
            g += cell_gradiant_grid.grid[rowIndex][columnIndex +
                                                   1].materialColor[1]
            b += cell_gradiant_grid.grid[rowIndex][columnIndex +
                                                   1].materialColor[2]
            count += 1
        # Check Up
        if rowIndex > 0:
            averageValue = averageValue + \
                cell_gradiant_grid.grid[rowIndex-1][columnIndex].intensity
            averageRate = averageRate + \
                cell_gradiant_grid.grid[rowIndex-1][columnIndex].rate

            r += cell_gradiant_grid.grid[rowIndex -
                                         1][columnIndex].materialColor[0]
            g += cell_gradiant_grid.grid[rowIndex -
                                         1][columnIndex].materialColor[1]
            b += cell_gradiant_grid.grid[rowIndex -
                                         1][columnIndex].materialColor[2]
            count += 1
            # Check Up Left
            if columnIndex > 0:
                averageValue = averageValue + \
                    cell_gradiant_grid.grid[rowIndex -
                                            1][columnIndex-1].intensity
                averageRate = averageRate + \
                    cell_gradiant_grid.grid[rowIndex-1][columnIndex-1].rate

                r += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex-1].materialColor[0]
                g += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex-1].materialColor[1]
                b += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex-1].materialColor[2]
                count += 1
            # Check Up Right
            if columnIndex < cell_gradiant_grid.columnCount-1:
                averageValue = averageValue + \
                    cell_gradiant_grid.grid[rowIndex -
                                            1][columnIndex+1].intensity
                averageRate = averageRate + \
                    cell_gradiant_grid.grid[rowIndex -
                                            1][columnIndex+1].rate
                r += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex+1].materialColor[0]
                g += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex+1].materialColor[1]
                b += cell_gradiant_grid.grid[rowIndex -
                                             1][columnIndex+1].materialColor[2]
                count += 1
        # Check Down
        if rowIndex < cell_gradiant_grid.rowCount-1:
            averageValue = averageValue + \
                cell_gradiant_grid.grid[rowIndex+1][columnIndex].intensity
            averageRate = averageRate + \
                cell_gradiant_grid.grid[rowIndex+1][columnIndex].rate

            r += cell_gradiant_grid.grid[rowIndex +
                                         1][columnIndex].materialColor[0]
            g += cell_gradiant_grid.grid[rowIndex +
                                         1][columnIndex].materialColor[1]
            b += cell_gradiant_grid.grid[rowIndex +
                                         1][columnIndex].materialColor[2]
            count += 1
            # Check Down Left
            if columnIndex > 0:
                averageValue = averageValue + \
                    cell_gradiant_grid.grid[rowIndex +
                                            1][columnIndex-1].intensity
                averageRate = averageRate + \
                    cell_gradiant_grid.grid[rowIndex +
                                            1][columnIndex-1].rate

                r += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex-1].materialColor[0]
                g += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex-1].materialColor[1]
                b += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex-1].materialColor[2]
                count += 1
            # Check Down Right
            if columnIndex < cell_gradiant_grid.columnCount-1:
                averageValue = averageValue + \
                    cell_gradiant_grid.grid[rowIndex +
                                            1][columnIndex+1].intensity
                averageRate = averageRate + \
                    cell_gradiant_grid.grid[rowIndex +
                                            1][columnIndex+1].rate

                r += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex+1].materialColor[0]
                g += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex+1].materialColor[1]
                b += cell_gradiant_grid.grid[rowIndex +
                                             1][columnIndex+1].materialColor[2]
                count += 1

        averageValue = (averageValue)/count
        averageRate = (averageRate)/count
        r = r/count
        g = g/count
        b = b/count
        self.nextValue = (averageValue, averageRate, (r, g, b))

    def update(self, surface):
        self.intensity = self.nextValue[0]
        self.rate = self.nextValue[1]
        self.materialColor = self.nextValue[2]
        self.evaporate()

    def stepWithGrid(self, rowIndex, columnIndex, cell_gradiant_grid):
        self.diffuse(rowIndex, columnIndex, cell_gradiant_grid)

    def updateWithGrid(self):
        self.intensity = self.nextValue[0]
        self.rate = self.nextValue[1]
        self.materialColor = self.nextValue[2]
        self.evaporate()
