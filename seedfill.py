import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

np.set_printoptions(threshold=np.inf)

# 初始化200*200的矩阵为零/initialize 200 * 200 matrix to zero
# 值：0 空白点，1 填充点，2 边界点/value：0 blank spot，1 filled spot，2 boundary spot
a = np.zeros((200, 200))


# 用类模拟栈/Simulate stack with class
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


s = Stack()


def scanline_seedfill(x, y):
    s.push([x, y])
    while not s.is_empty():
        [seed_x, seed_y] = s.pop()
        x_right = seed_x + 1
        x_left = seed_x - 1
        # 向右填充/fill right
        while a[x_right][seed_y] == 0:
            a[x_right][seed_y] = 1
            x_right += 1
        x_right -= 1
        # 向左填充/fill left
        while a[x_left][seed_y] == 0:
            a[x_left][seed_y] = 1
            x_left -= 1
        x_left += 1
        # 填充种子点/fill seed
        a[seed_x][seed_y] = 1
        # 寻找新的种子点/find new seeds
        search_newseed(x_left, x_right, seed_y + 1)
        search_newseed(x_left, x_right, seed_y - 1)


def search_newseed(x_left, x_right, y):
    find_newseed = False
    temp_x = x_left
    # 从左往右寻找种子点/Search for seed points from left to right
    # 两个相同的while是为了处理同一条扫描线上有多个种子点的情况/Two identical while
    # are used to handle the case of multiple seed points on the same scan line
    while temp_x <= x_right:
        while temp_x <= x_right:
            while a[temp_x][y] == 0:
                temp_x += 1
                find_newseed = True
                if temp_x > x_right:
                    break
            if find_newseed:
                seed_x = temp_x - 1
                s.push([seed_x, y])
                find_newseed = False
                break
            temp_x += 1


# Bresenham直线算法，用于绘制多边形的边界
# Bresenham line algorithm, used to draw the boundary of polygon
def bresenham_line(x1, y1, x2, y2):
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    s1 = 1 if x2 > x1 else -1
    s2 = 1 if y2 > y1 else -1
    interchange = False
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        interchange = True
    e = 2 * dy - dx
    x, y = x1, y1
    # 网格线
    plt.grid()
    # x轴y轴数值取整/rounding the value of x-axis and y-axis
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    # 绘点并将矩阵对应的值设置为2/Draw points and set the value corresponding to the matrix to 2
    for i in range(0, int(abs(dx) + 1)):
        plt.plot(x, y, 'r.', markersize=4)
        a[x][y] = 2
        if e >= 0:
            if not interchange:
                y += s2
            else:
                x += s1
            e -= 2 * dx
        if not interchange:
            x += s1
        else:
            y += s2
        e += 2 * dy


# 绘制多边形的边/Draw polygon edges
def draw(polygon):
    length = len(polygon)
    for i, element in enumerate(polygon):
        [x1, y1] = polygon[i]
        [x2, y2] = polygon[(i + 1) % length]
        bresenham_line(x1, y1, x2, y2)


# 填充多边形内部点/Fill polygon interior points
def fill(xlim, ylim):
    [x_min, x_max] = xlim
    [y_min, y_max] = ylim
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            if a[i][j] == 1:
                plt.plot(i, j, '.', color='orange', markersize=2)


def x_lim(polygon):
    [x_min, x_max] = polygon[0]
    for i, element in enumerate(polygon):
        p = polygon[i]
        if p[0] < x_min:
            x_min = p[0]
        if p[0] > x_max:
            x_max = p[0]
    return [x_min, x_max]


def y_lim(polygon):
    [y_min, y_max] = polygon[0]
    for i, element in enumerate(polygon):
        p = polygon[i]
        if p[1] < y_min:
            y_min = p[1]
        if p[1] > y_max:
            y_max = p[1]
    return [y_min, y_max]
