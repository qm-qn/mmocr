import os
from PIL import Image, ImageDraw
from tqdm import tqdm


def delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color):
    # 笔画黑点
    last_word_black = []

    # 要变回来的点
    change_spot = []
    for y in range(height):
        for delete_y in line_to_white:
            if y == delete_y:
                for current_line_x in range(width):
                    change_spot.append((current_line_x, y, editable_pixels[current_line_x, y]))
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

    return change_spot


def find_black_line(editable_pixels, width, height):
    line_black_color = 220
    word_black_color = 130
    row_color_threshold = 0.4
    white_color = 255

    # 横线黑点
    current_line_black = []
    # 要调整的横线
    line_to_white = []

    for y in range(height):
        current_line_black.clear()
        find_line = 0
        # 统计当前行的黑色像素数
        for x in range(width):
            if editable_pixels[x, y] < line_black_color:
                current_line_black.append(x)
        black_pixel_count = len(current_line_black)

        if black_pixel_count > width * row_color_threshold:
            # 找到了横线
            find_line = 1

        if find_line == 1 and y > height * 0.5:
            for i in range(-1, 2):
                if 0 <= y + i < height:
                    no_add = 0
                    for delete_line in line_to_white:
                        if y + i == delete_line:
                            no_add = 1
                            break
                    if no_add == 0:
                        # 添加相邻黑线
                        line_to_white.append(y + i)

    return delete_bottom_lines(editable_pixels, width, height, line_to_white, white_color, word_black_color)


def crop_image(image_path, output_path, bad_img):
    global paths
    # 打开图像
    img = Image.open(image_path)
    # print(image_path)

    # 将图像转换为可编辑模式
    editable_image = img.copy()
    editable_pixels = editable_image.load()

    # 获取图像尺寸
    width, height = img.size

    black_color = 180
    row_color_threshold = 0.005
    column_color_threshold = 0.03
    # blank_distance = 0.013

    # 检测是否是空白图
    is_blank = 1
    for x in range(width):
        # 统计当前列的黑色像素数
        is_blank_black_pixel_count = sum(1 for y in range(height) if editable_pixels[x, y] < black_color)
        if is_blank_black_pixel_count > height * column_color_threshold:
            is_blank = 0
            break

    if is_blank == 1:
        paths.append(image_path)
    else:
        # 把下方黑线变白，避免影响
        change_spot = find_black_line(editable_pixels, width, height)
        # 左右
        find = 0
        left_boundary = []
        right_boundary = []
        left_bound = -1
        right_bound = -1
        black_pixel_count2 = 0
        for x in range(width):
            # 统计当前列的黑色像素数
            black_pixel_count1 = black_pixel_count2
            black_pixel_count2 = sum(1 for y in range(height) if editable_pixels[x, y] < black_color)
            # print("x=" + str(x) + ", count=" + str(black_pixel_count1))
            # 左白右黑，左边界
            if find == 0 and black_pixel_count1 > height * column_color_threshold and black_pixel_count2 > height * column_color_threshold:
                find = 1
                left_boundary.append(x - 1)
            # 左黑右白，右边界
            if find == 1 and black_pixel_count1 <= height * column_color_threshold and black_pixel_count2 <= height * column_color_threshold:
                find = 0
                right_boundary.append(x)

        # 左右边界一一对应
        if len(left_boundary) == len(right_boundary) + 1:
            right_boundary.append(width - 1)

        if len(left_boundary) == 0:
            bad_img.append(image_path)
            return
        else:
            left_bound = left_boundary[0]
            right_bound = right_boundary[-1]

        # 变白的部分还原
        for (change_x, change_y, color) in change_spot:
            editable_pixels[change_x, change_y] = color

        top_bound = -1
        bottom_bound = -1
        # 寻找上边界
        for y in range(height):
            # 统计当前行的黑色像素数
            top_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if editable_pixels[x, y] < black_color)
            if top_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                top_bound = y
                break

        # 寻找下边界
        for y in range(height - 1, 0, -1):
            # 统计当前行的黑色像素数
            bottom_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if editable_pixels[x, y] < black_color)
            if bottom_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                bottom_bound = y
                break

        if top_bound == -1 or bottom_bound == -1:
            print(image_path)

        # 绘制矩形
        draw = ImageDraw.Draw(editable_image)
        if top_bound >= bottom_bound:
            print("top_bound >= bottom_bound  " + image_path)
            return
        draw.rectangle([left_bound, top_bound, right_bound, bottom_bound], outline='red')
        editable_image.save(output_path)

        # # 裁剪图片
        # cropped_img = editable_image.crop((left_bound, top_bound, right_bound, bottom_bound))
        # cropped_img.save(output_path)


def process_images_in_folder(folderIn_path, folder_save_folder, bad_img):
    if not os.path.exists(folder_save_folder):
        os.makedirs(folder_save_folder)

    # 获取总图片数量
    total_images = count_images_in_folder(folderIn_path)

    # 使用总图片数量初始化进度条
    progress_bar = tqdm(total=total_images, desc='Processing images')

    # 开始处理图片
    for filename in os.listdir(folderIn_path):
        fileInpath = os.path.join(folderIn_path, filename)
        file_save_folder = os.path.join(folder_save_folder, filename)
        if os.path.isdir(fileInpath):
            # 如果是文件夹，则递归处理其中的图片
            process_images_in_folder(fileInpath, file_save_folder)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # 如果是图片文件，则进行处理
            crop_image(fileInpath, file_save_folder, bad_img)
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
    input_folder = "m_testout/delete_stroke"  # 输入文件夹路径
    output_folder = "m_testout/m_image"  # 输出文件夹路径
    global paths
    bad_img = []
    process_images_in_folder(input_folder, output_folder, bad_img)
    with open("m_testout/badimg.txt", 'w') as file:
        for img in bad_img:
            file.write(img + '\n')
