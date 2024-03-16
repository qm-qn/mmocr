import os
from PIL import Image
from tqdm import tqdm


def find_black(width, height, x, y, line_y):
    global is_black
    global to_white
    global connect
    global is_find

    # 和下面连上了，不删，停止所有递归
    if connect == 1:
        return
    if y == line_y:
        connect = 1
        return

    # 找周围八个点
    for m in range(-1, 2):
        for n in range(-1, 2):
            if 0 <= x + m < width and 0 <= y + n < height:
                if is_find[x + m][y + n] == 0 and is_black[x + m][y + n] == 1:
                    is_find[x + m][y + n] = 1
                    to_white.append((x + m, y + n))
                    find_black(width, height, x + m, y + n, line_y)


def delete_stroke(editable_pixels, width, height, line_y, top_y_end, white_color):
    global top_black
    global is_black
    global to_white
    global connect
    global is_find

    # 遍历顶部所有黑点
    for x, y in top_black:
        is_find = [[0 for j in range(height)] for i in range(width)]
        connect = 0
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

    for y in range(top_y_end):
        for x in range(width):
            editable_pixels[x, y] = white_color


def delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color):
    # 笔画黑点
    last_word_black = []

    for y in range(height):
        for delete_y in line_to_white:
            if y == delete_y:
                for current_line_x in range(width):
                    # 记录这个横线黑点上方有无笔画黑点
                    find_black = 0
                    for last_word_x in last_word_black:
                        # 有相邻黑色
                        if abs(current_line_x - last_word_x) <= 0:
                            find_black = 1
                            break
                    if find_black == 0:
                        editable_pixels[current_line_x, y] = white_color

        last_word_black.clear()
        for x in range(width):
            if editable_pixels[x, y] < word_black_color:
                last_word_black.append(x)


def crop_image(image_path, file_save_folder, file_view_folder):
    # 打开图像
    img = Image.open(image_path)

    # 将图像转换为可编辑模式
    editable_image = img.copy()
    editable_pixels = editable_image.load()

    # 获取图像尺寸
    width, height = img.size

    line_black_color = 220
    word_black_color = 100
    row_color_threshold = 0.4
    white_color = 255
    top_y_end = 3

    # 横线黑点
    current_line_black = []
    # 最上方三行黑点坐标
    global top_black
    top_black = []
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
            if editable_pixels[x, y] < line_black_color:
                current_line_black.append(x)
                is_black[x][y] = 1
                if y in range(top_y_end):
                    top_black.append((x, y))
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
        print("error: no line_y  img_path: " + image_path)

    delete_stroke(editable_pixels, width, height, line_y, top_y_end, white_color)
    delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color)

    editable_image.save(file_save_folder)

    # 拼接处理前后的图片
    concatenated_image = Image.new('RGB', (width * 2, height))
    concatenated_image.paste(img, (0, 0))
    # 在处理后的图片右侧拼接处理后的图片
    concatenated_image.paste(editable_image, (width, 0))
    # 保存拼接后的图片
    concatenated_image.save(file_view_folder)


def process_images_in_folder(folderIn_path, folder_save_folder, folder_view_folder):
    if not os.path.exists(folder_save_folder):
        os.makedirs(folder_save_folder)
    if not os.path.exists(folder_view_folder):
        os.makedirs(folder_view_folder)

    # 获取总图片数量
    total_images = count_images_in_folder(folderIn_path)

    # 使用总图片数量初始化进度条
    progress_bar = tqdm(total=total_images, desc='Processing images')

    # 开始处理图片
    for filename in os.listdir(folderIn_path):
        fileInpath = os.path.join(folderIn_path, filename)
        file_save_folder = os.path.join(folder_save_folder, filename)
        file_view_folder = os.path.join(folder_view_folder, filename)
        if os.path.isdir(fileInpath):
            # 如果是文件夹，则递归处理其中的图片
            process_images_in_folder(fileInpath, file_save_folder, file_view_folder)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # 如果是图片文件，则进行处理
            crop_image(fileInpath, file_save_folder, file_view_folder)
            # 更新进度条
            progress_bar.update(1)

    # 关闭进度条
    progress_bar.close()


# 计算指定文件夹中图片文件的数量
def count_images_in_folder(folder_path):
    image_count = 0
    for filename in os.listdir(folder_path):
        fileInpath = os.path.join(folder_path, filename)
        if os.path.isdir(fileInpath):
            image_count += count_images_in_folder(fileInpath)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            image_count += 1
    return image_count


if __name__ == "__main__":
    input_folder = "m_testout/testin"  # 输入文件夹路径
    folder_path = os.path.dirname(input_folder)
    save_folder = os.path.join("m_testout", "save")  # 处理后的文件夹路径
    view_folder = os.path.join("m_testout", "view")  # 拼接图片文件夹路径
    process_images_in_folder(input_folder, save_folder, view_folder)
