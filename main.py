from functions import *

def main(xSize: int, ySize: int):
    island = generateIsland(
        size = (xSize, ySize),
        smoothIterations = 2, # 3-4
        amplifyMultiplier = 3, # 3
        contrastFactor = 2.15, # 1.85-2.75
        sharpness = 0.215, # 0.185-0.225
        borderColor = 0.75, # 0.75
        shadowFactor = 0.315, # 0.315
        smoothSize = 2 # 2 = default
    )

    island = island.resize((xSize * 100, ySize * 100), resample=Image.BOX)
    island.show()

if __name__ == "__main__":
    try:
        main(int(sys.argv[1]), int(sys.argv[2]))
    except:
        main(int(input("X: ")), int(input("Y: ")))