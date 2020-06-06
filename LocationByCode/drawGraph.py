import openpyxl
from PointCalculation import pointCalculation


if __name__ == "__main__":
    anchor_x = [0,-75,75,-75,75]
    anchor_y = [0,-75,-75,75,75]
    pc = pointCalculation(anchor_x,anchor_y)
    pc.get_group(5)


