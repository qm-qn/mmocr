from PIL import Image


def find_black(width, height, x, y, line_y):
    global is_black
    global to_white
    global connect
    global is_find
    global count

    # 和横线连上了，不删，停止所有递归
    if connect == 1:
        return
    if y == line_y:
        connect = 1
        return
    if count > 900:
        connect = 1
        return

    # 找周围八个点
    for m in range(-1, 2):
        for n in range(-1, 2):
            if 0 <= x + m < width and 0 <= y + n < height:
                if is_find[x + m][y + n] == 0 and is_black[x + m][y + n] == 1:
                    is_find[x + m][y + n] = 1
                    to_white.append((x + m, y + n))
                    count = count + 1
                    find_black(width, height, x + m, y + n, line_y)


def delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color):
    global is_black
    global to_white
    global connect
    global is_find
    global count

    # 遍历顶部所有黑点
    for x, y in top_black:
        is_find = [[0 for j in range(height)] for i in range(width)]
        connect = 0
        count = 0
        find_black(width, height, x, y, line_y)
        # 如果没和下面连上，说明是杂笔画，删除
        if connect == 0:
            # 变白
            for m, n in to_white:
                is_black[m][n] = 0
                # 顶部黑点列表去掉要去除的黑点
                if n < top_y_end:
                    for i in range(len(top_black)):
                        if top_black[i] == (m, n):
                            top_black.pop(i)
                            break
                editable_pixels[m, n] = white_color
        to_white.clear()


def delete_strokes(image_path, file_save_folder):
    # 打开图像
    img = Image.open(image_path)
    # print(image_path)

    # 将图像转换为可编辑模式
    editable_image = img.copy()
    editable_pixels = editable_image.load()

    # 获取图像尺寸
    width, height = img.size

    line_black_color = 200
    row_color_threshold = 0.4
    white_color = (255, 255, 255)
    top_y_end = 1
    bottom_y_end = 1

    # 横线黑点
    current_line_black = []
    # 最上方三行黑点坐标
    top_black = []
    # 最下方三行黑点坐标
    bottom_black = []
    # 全图黑色点
    global is_black
    is_black = [[0 for j in range(height)] for i in range(width)]
    # 要变白的点
    global to_white
    to_white = []
    # 要调整的横线
    line_to_white = []

    find_top_line_y = 0
    line_y = -1
    for y in range(height):
        current_line_black.clear()
        find_line = 0
        # 统计当前行的黑色像素数
        for x in range(width):
            gray_value = int(sum(editable_pixels[x, y]) / 3)
            if gray_value < line_black_color:
                current_line_black.append(x)
                is_black[x][y] = 1
                if y < top_y_end:
                    top_black.append((x, y))
                if y > height - 1 - bottom_y_end:
                    bottom_black.append((x, y))
        black_pixel_count = len(current_line_black)

        if black_pixel_count > width * row_color_threshold:
            # 找到了横线
            find_line = 1

        if find_line == 1 and y > height * 0.5 and find_top_line_y == 0:
            line_y = y
            find_top_line_y = 1

        if find_line == 1 and y > height * 0.5:
            for i in range(-1, 2):
                if 0 <= y + i < height:
                    no_add = 0
                    for delete_line in line_to_white:
                        if y + i == delete_line:
                            no_add = 1
                            break
                    if no_add == 0:
                        line_to_white.append(y + i)

    # print(image_path)
    if line_y == -1:
        line_y = height / 2
        print("no line")

    delete_stroke(editable_pixels, width, height, line_y, top_y_end, top_black, white_color)

    editable_image.save(file_save_folder)
