import matplotlib.pyplot as plt
import seedfill

# 多边形的点（逆时针）/points of polygon (counterclockwise)
polygon = [
    [10, 30],
    [50, 48],
    [90, 30],
    [75, 65],
    [60, 60],
    [50, 80],
    [40, 60],
    [25, 65]
]
seedfill.draw(polygon)
xlim = seedfill.x_lim(polygon)
ylim = seedfill.y_lim(polygon)

# 网格线
plt.grid()
# 选取(30，40)作为种子起始点/Select (30, 40) as the first seed  point
seedfill.scanline_seedfill(30, 40)
seedfill.fill(xlim, ylim)
plt.show()
