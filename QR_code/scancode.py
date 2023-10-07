import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_hmirror(0)
#sensor.set_auto_gain(False)

clock = time.clock()
num_list = []
while(True):
    clock.tick()
    img = sensor.snapshot()
    for code in img.find_qrcodes():
        img.draw_rectangle(code.rect(), color = (255, 0, 0))
        # print(code.payload())
        if code.payload() is not None:
            code_str = code.payload().strip()  # 去除字符串两端的空格和换行符
            code_str = code.payload()
            code_list = code_str.split("+")
            print(code_list)
            if len(code_list) == 2:
                #code_int = [int(digit) for num in code_list for digit in num]
                code_int = [int(digit) for num in code_list for digit in num if digit.isdigit()]
                num_list = code_int
                print(num_list[0], num_list[1], num_list[2], num_list[3], num_list[4], num_list[5])
