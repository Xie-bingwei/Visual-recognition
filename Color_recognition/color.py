import sensor
import image
import lcd

# 初始化摄像头和LCD显示
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.skip_frames(time = 2000)
lcd.init()

# 阈值设置
red_threshold = (54, 29, 3, 74, -36, 36)
blue_threshold = (5, 100, 48, 1, -9, -128)
green_threshold = (30, 71, -52, -6, 3, 127)

roi = (74, 49, 186, 179)

while True:
    img = sensor.snapshot()

    img = img.crop(roi)
    blobs_red = img.find_blobs([red_threshold])
    blobs_blue = img.find_blobs([blue_threshold])
    blobs_green = img.find_blobs([green_threshold])

    if blobs_red:
        max_blob_red = max(blobs_red, key=lambda b: b.pixels())  # 找到最大的红色物体
      
        center_x = max_blob_red.cx()  # 得到中心点x坐标
        center_y = max_blob_red.cy()

        img.draw_rectangle(max_blob_red.rect())  # 绘制边框
        img.draw_cross(center_x, center_y)       # 绘制中心点

        text = "Red"
        img.draw_string(max_blob_red.x(), max_blob_red.y() - 10, text)

        print("x: " + str(center_x) + "  " + "y: " + str(center_y))

    if blobs_blue:
        max_blob_blue = max(blobs_blue, key= lambda b: b.pixels())

        center_x = max_blob_blue.cx()
        center_y = max_blob_blue.cy()

        img.draw_rectangle(max_blob_blue.rect())
        img.draw_cross(center_x, center_y)

        text = "Blue"
        img.draw_string(max_blob_blue.x(), max_blob_blue.y() - 10, text)

        print("x: " + str(center_x) + "  " + "y: " + str(center_y))

    if blobs_green:
        max_blob_green = max(blobs_green, key= lambda b: b.pixels())

        center_x = max_blob_green.cx()
        center_y = max_blob_green.cy()

        img.draw_rectangle(max_blob_green.rect())
        img.draw_cross(center_x, center_y)

        text = "Green"
        img.draw_string(max_blob_green.x(), max_blob_green.y() - 10, text)

        print("x: " + str(center_x) + "  " + "y: " + str(center_y))

    lcd.display(img)
