import math
fileName = input("Input file name: ")
fileName = "figure1.txt"

def add_coords(j, i, coords):
    lst = []
    lst.append(j)
    lst.append(i)
    if not lst in coords:
        coords.append(lst)
    return coords

def find_dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def find_max(coords):
    mx = 0.0
    for i in range(len(coords) - 1):
        for j in range(i, len(coords) - 1):
            cur = find_dist(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            if mx < cur:
                mx = cur
    return mx

def read_N():
    with open(fileName, "r") as file:
        N = float(file.readline())
    return N

def read_circuit():
    with open(fileName, "r") as file:
        N = float(file.readline())
        row_old = file.readline().strip().split()
        coords = []
        for i, row in enumerate(file):
            row = row.strip().split()
            for j in range(len(row) - 1):
                try:
                    if (row[j-1] == '0' and row[j] == '1'):
                        coords = add_coords(j, i, coords)
                    elif (row[j] == '1' and row[j + 1] == '0'):
                        coords = add_coords(j, i, coords)
                    elif (row_old[j] == '0' and row[j] == '1'):
                        coords = add_coords(j, i, coords)
                    elif (row[j] == '0' and row_old[j] == '1'):
                        coords = add_coords(j, i, coords)
                except IndexError:
                    pass
            row_old = row
    return coords

N = read_N()
coords = read_circuit()
print(find_max(coords)/N)

