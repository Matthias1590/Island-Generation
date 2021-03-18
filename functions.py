import random, os, copy, sys
import numpy as np
from PIL import Image, ImageEnhance
os.system("cls")

def generateLine(size: int = 10):
    line = []
    for i in range(size):
        line.append(random.randint(0, 1))
    return line

def generateGrid(size: tuple = (10, 10)):
    grid = []
    for y in range(size[1]):
        grid.append(generateLine(size[0]))
    return grid

def smoothGrid(grid: list, iterations: int = 1, smoothSize: int = 3):
    if iterations == 0:
        return grid

    smoothedGrid = copy.deepcopy(grid)
    start = (smoothSize - 1, smoothSize - 1)
    end = (len(grid) - smoothSize - 1, len(grid[0]) - smoothSize - 1)
    current = list(start)
    for i in range((end[0] * end[1]) - (start[0] * start[1])):
        neighbors = [grid[current[0]][current[1]]]
        for i in range(1, smoothSize):
            # print(current, end)
            neighbors.append(grid[current[0] + i][current[1]])
            neighbors.append(grid[current[0] - i][current[1]])
            neighbors.append(grid[current[0]][current[1] + i])
            neighbors.append(grid[current[0]][current[1] - i])
        smoothedGrid[current[0]][current[1]] = sum(neighbors) / len(neighbors)
        current[0] += 1
        if current[0] > end[0]:
            current[0] = start[0]
            current[1] += 1
        if current[1] > end[1]:
            current[1] = start[1]
            current[0] += 1
    
    return smoothGrid(smoothedGrid, iterations - 1, smoothSize)

def amplifyGrid(grid: list, amplifier: float = 1.75):
    amplifiedGrid = grid
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x] = grid[y][x] ** amplifier

    return amplifiedGrid

def saveGrid(grid: list, path: str):
    img = Image.new("L", (len(grid[0]), len(grid)))
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            img.putpixel((x, y), int(grid[x][y] * 255))
    img.save(path)

def removeSmall(grid: list, minValue: float = 0.3, replaceFactor: float = 0):
    newGrid = grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] < minValue:
                newGrid[y][x] = grid[y][x] * replaceFactor
    return newGrid

def islandColors(island: Image, replaceColors: list):
    img = island.convert("RGB")
    data = np.array(img)
    for colors in replaceColors:
        data[(data == colors[0]).all(axis=-1)] = colors[1]
    img = Image.fromarray(data, mode="RGB")
    return img

def generateIsland(size: tuple = (10, 10), smooth: bool = True, smoothSize: int = 1, smoothIterations: int = 2, amplify: bool = True, amplifyMultiplier: float = 1.45, borderColor: float = 0.75, customEdits: bool = False, save: bool = True, contrastFactor: float = 1.65, sharpness: float = 0.2, shadowFactor: float = 0.35, waterOffset: float = 0.35):
    island = [] # [borderColor]
    for i in range(smoothSize):
        island.append([borderColor] * (size[0] + smoothSize * 2))
    island.extend(generateGrid(size))
    for i in range(smoothSize):
        island.append([borderColor] * (size[0] + smoothSize * 2))
    newIsland = []
    for i in range(len(island)):
        line = island[i]
        if i > smoothSize - 1 and i < len(island) - smoothSize:
            line = [borderColor] * (smoothSize)
            line.extend(island[i])
            line.extend([borderColor] * (smoothSize))
        newIsland.append(line)
    island = newIsland
    if customEdits:
        if smooth:
            island = smoothGrid(island, smoothIterations, smoothSize)
            island = removeSmall(island, waterOffset, 0)
        if amplify:
            island = amplifyGrid(island, amplifyMultiplier)
    else:
        island = smoothGrid(island, 2, smoothSize)
        island = removeSmall(island, waterOffset, 0)
        island = amplifyGrid(island, 2.65)
        island = smoothGrid(island, 3, smoothSize)
        island = removeSmall(island, sharpness, 0)
        darkenMap = island

    img = Image.new("L", (len(island[0]), len(island)))
    for y in range(len(island)):
        for x in range(len(island[0])):
            img.putpixel((x, y), int(island[y][x] * 255))
    img2 = Image.new("L", (len(darkenMap[0]), len(darkenMap)))
    for y in range(len(darkenMap)):
        for x in range(len(darkenMap[0])):
            img2.putpixel((x, y), int(darkenMap[y][x] * 255))
    img2 = img2.convert("RGB")

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrastFactor)

    grassColor = (103, 217, 59)
    sandColor = (222, 195, 60)
    waterColor = (37, 108, 168)
    # Replace color A with color B
    colorList = [
        [(0, 0, 0), grassColor]
    ]
    for i in range(256):
        old = (i, i, i)
        new = sandColor if i > 0 and i < 120 else waterColor if i > 0 else (i, i, i)
        color = [old, new]
        colorList.append(color)
    img = islandColors(img, colorList)

    img = Image.blend(img, img2, shadowFactor)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrastFactor * 0.65)
    
    # STRIP RIGHT AND BOTTOM COLUMN
    return img

def showGrid(grid: list):
    for line in grid:
        print(line)