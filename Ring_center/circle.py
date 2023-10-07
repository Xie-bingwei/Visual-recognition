import sensor
import image
import time
import lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_hmirror(0)
lcd.init()

# 中值滤波
def median_filter(values):
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 1:     # 列表是奇数，返回中间值
        return sorted_values[n // 2]    
    else:    # 列表是偶数，取中间两个的平均值
        index1 = n // 2
        index2 = index1 - 1
        return (sorted_values[index1] + sorted_values[index2]) / 2

def fabs(values):
    a = values
    if a < 0:
        return -a
    else:
        return a

sum_x = 0; sum_y = 0
i = 0
aravage_x = 0; aravage_y = 0
last_x = 0; last_y = 0

while True:
    img = sensor.snapshot()

    img_gray = img.to_grayscale()

    # 圆检测
    circles = img_gray.find_circles(
       roi = (36, 22, 227, 208),
        x_margin = 0, y_margin = 0,
        r_margin = 0, r_min = 40, r_max = 45
    )

    if circles:
       
        center_x_list = []   # 初始化目标滤波数组
        center_y_list = []
       
        circles.sort(key=lambda c: c.r())  # 半径从小到大排序
        #smallest_circle = circles[0]   # 获取最小的圆

        for c in circles:
            center_x = c.x()       # 获取圆心坐标
            center_y = c.y()

            center_x_list.append(center_x)  # 圆心坐标添加到目标数组
            center_y_list.append(center_y)

        center_x_median = median_filter(center_x_list)
        center_y_median = median_filter(center_y_list)

        sum_x += center_x_median; sum_y += center_y_median
        if sum_x != 0 and sum_y != 0:
            i += 1
            if i == 10:
                last_x = aravage_x
                last_y = aravage_y
                aravage_x = int(sum_x / 10)
                aravage_y = int(sum_y / 10)
                if fabs(aravage_x - last_x) <= 1 and fabs(aravage_y - last_y) <= 1:
                    aravage_x = last_x
                    aravage_y = last_y
                sum_x = 0; sum_y = 0
                i = 0
  
        img.draw_cross(aravage_x, aravage_y, color=(0, 0, 255), thickness=2)
        print("Median Circle center:({}, {})".format(aravage_x, aravage_y))

    lcd.display(img)
