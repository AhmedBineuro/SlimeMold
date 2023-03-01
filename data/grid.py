from data.cell import cellGradiant


class cellGradiantGrid:
    def __init__(self, x, y, rowCount, columnCount, cellSize):
        self.cellSize = cellSize
        self.x = x
        self.y = y
        self.rowCount = rowCount
        self.columnCount = columnCount
        self.grid = []

        self.halfWidth = columnCount*cellSize/2
        self.halfHeight = rowCount*cellSize/2
        for j in range(rowCount):
            row = []
            for i in range(columnCount):
                row.append(cellGradiant(
                    (x+(i*cellSize)), y+(j*cellSize), cellSize))
            self.grid.append(row)

    def update(self):
        for i in range(self.rowCount-1, 0, -1):
            for j in range(self.columnCount):
                self.grid[i][j].updateWithGrid()

    def step(self):
        for i in range(self.rowCount):
            for j in range(self.columnCount):
                self.grid[i][j].stepWithGrid(i, j, self)

    def draw(self, surface):
        for i in range(self.rowCount):
            for j in range(self.columnCount):
                self.grid[i][j].draw(surface)

    def handleClick(self, x, y):
        for j in range(self.rowCount):
            for i in range(self.columnCount):
                self.grid[i][j].handleClick(x, y)

    def translateIndex(self, x, y):
        rowIndex = int((y-self.y)/self.cellSize)
        columnIndex = int((x-self.x)/self.cellSize)
        return (rowIndex, columnIndex)
