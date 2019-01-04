# -*- coding: utf-8 -*-
import numpy as np
from skimage import filters
from skimage.measure import label, regionprops
from skimage import morphology
from skimage import draw
import matplotlib.pyplot as plt


def count_holes(s):
    s = np.logical_not(s).astype('uint8')
    
    ss = np.ones((s.shape[0] + 2, s.shape[1] + 2))
    ss[1:-1, 1:-1] = s
    
    LBs = label(ss)
    LBs[LBs == 1] = 0
    
    return len(np.unique(LBs))-1

def half_hole(s):
    s = np.logical_not(s).astype('uint8')
    y = s.shape[0] // 3
    x = s.shape[1] // 3
    ss = s[y:-y, x:-x]
    if s[0, 0] in ss:
        return True
    else:
        return False

def has_vline(s):
    line = np.sum(s, 0) // s.shape[0]
    return 1 in line

# Считает кол-во штрихов
def count_hatch(s):
    up = s[0, :]
    upe = np.zeros(len(up) + 2)
    upe[1: -1] = up
    upe = np.abs(np.diff(upe))
    
    intervals = np.where(upe > 0)[0]
    points_up = []
    
    for p1, p2 in zip( intervals[::2], intervals[1::2]):
        points_up.append((p2+p1) // 2)
#    print(points_up)
    
    down = s[-1, :]
    downe = np.zeros(len(down) + 2)
    downe[1: -1] = down
    downe = np.abs(np.diff(downe))
    
    intervals = np.where(downe > 0)[0]
    points_down = []
    
    for p1, p2 in zip( intervals[::2], intervals[1::2]):
        points_down.append((p2+p1) // 2)
#    print(points_down)

    
    h = 0 # Кол-во штрихов.
    for p1 in points_up:
        for p2 in points_down:
            line = draw.line(0, p1, s.shape[0] - 1, p2)
            if np.all(s[line] == 1):
                h += 1
#    print (h)
    if (h == 0):
        h = has_vline(s)
    return h

def recognite(s):
#   Смотрим кол-во отверстий в букве.
    holes = count_holes(s)
    if holes == 2:
#        Считаем штрихи
        hatches = count_hatch(s)
        if hatches == 1:
            return "B"
        else:
            return "8"
    elif holes == 1:
        ss = morphology.binary_closing(s)
        hatches = count_hatch(ss)
        if hatches == 2:
            return "A"
        elif hatches:
            if half_hole(s):
                return "P"
            else: 
                return "D"
        else:
            return "0"
    else:
        hatches = count_hatch(s)
#        print(hatches)
        ratio = s.shape[0] / s.shape[1] # Соотношение (процентное) высоты к ширине
#        print("Ratio = ", ratio)
        if (3 <= hatches <= 4 ):
            return "W"
        elif hatches == 2 and (0.9 < ratio < 1.1):
            return "*"
        elif hatches == 2:
            return "X"
        elif has_vline(s) and ratio > 1:
            return "1"
        elif (0.9 < ratio <= 1.1):
            return "*"
        elif (hatches == 1) and (1.9 < ratio < 2.16):
            return "/"
        elif (hatches == 1) and (ratio < 0.5):
            return "-"
    return ""
    
if __name__ == "__main__":
    alphabet = plt.imread("symbols.png")
    
    alphabet = np.mean(alphabet, 2)
    thresh = filters.threshold_otsu(alphabet)
    
    alphabet[alphabet < thresh] = 0
    alphabet[alphabet >= thresh] = 1
    
    b_alpha = np.zeros_like(alphabet)
    b_alpha[alphabet < thresh] = 1
    b_alpha[alphabet >= thresh] = 0
    
    LB = label(alphabet)
    props = regionprops(LB)
    
    count_symbols = {}
    symbols = {}
    index = 0
    indexes = []
    while (True):
        try:
           s = props[index].image 
           sym = recognite(s)
           if count_symbols.get(sym):
               count_symbols[recognite(s)] = count_symbols[recognite(s)] + 1
           else:
               count_symbols[recognite(s)] = 1
           index += 1
        except IndexError:
            print(index)
            break

    recognized = 0
    for key in count_symbols:
        recognized += count_symbols[key]
    print("распознаваемость:", recognized / index * 100)
    
    plt.figure()
#    plt.subplot(121)
    plt.imshow(props[29].image, cmap = 'gray')
#    plt.imshow(props[127].image, cmap = 'gray')
#    plt.subplot(122)
#    plt.plot(props[7].image)
#    plt.plot(props[127].image)
    plt.show()
    
