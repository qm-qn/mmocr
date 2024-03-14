import os
import json
from PIL import Image, ImageDraw


def crop_image(image_path, output_path):
    global paths
    # 打开图像
    img = Image.open(image_path)

    print(image_path)

    # 将图像转换为灰度图
    img_gray = img.convert('L')

    # 获取图像尺寸
    width, height = img_gray.size
    print("width: " + str(width))
    print("height: " + str(height))

    black_color = 150
    row_color_threshold = 0.005
    column_color_threshold = 0.05
    blank_distance = 0.08

    # 检测是否是空白图
    is_blank = 1
    for x in range(width):
        # 统计当前列的黑色像素数
        is_blank_black_pixel_count = sum(1 for y in range(height) if img_gray.getpixel((x, y)) < black_color)
        if is_blank_black_pixel_count > height * column_color_threshold:
            is_blank = 0
            break

    if is_blank == 1:
        paths.append(image_path)
    else:
        # 左右
        find = 0
        left_boundary = []
        right_boundary = []
        for x in range(width):
            # 统计当前列的黑色像素数
            left_black_pixel_count = sum(1 for y in range(height) if img_gray.getpixel((x, y)) < black_color)
            # 左白右黑，左边界
            if find == 0 and left_black_pixel_count > height * column_color_threshold:
                find = 1
                left_boundary.append(x)
                # 右边界列表非空
                if right_boundary:
                    # 空白距离过小
                    if left_boundary[-1] - right_boundary[-1] < width * blank_distance:
                        left_boundary.pop(-1)
                        right_boundary.pop(-1)
            # 左黑右白，右边界
            if find == 1 and left_black_pixel_count <= height * column_color_threshold:
                find = 0
                right_boundary.append(x)

        # 左右边界一一对应
        if len(left_boundary) == len(right_boundary) + 1:
            right_boundary.append(width - 1)

        if len(left_boundary) == 0:
            print("error: len(left_boundary)=0")
        else:
            max_distance = 0
            for i in range(len(left_boundary)):
                if right_boundary[i] - left_boundary[i] > max_distance:
                    max_distance = right_boundary[i] - left_boundary[i]
                    right_bound = right_boundary[i]
                    left_bound = left_boundary[i]

        # 寻找上边界
        for y in range(height):
            # 统计当前行的黑色像素数
            top_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if img_gray.getpixel((x, y)) < black_color)
            if top_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                top_bound = y
                break

        # 寻找下边界
        for y in range(height - 1, 0, -1):
            # 统计当前行的黑色像素数
            bottom_black_pixel_count = sum(1 for x in range(left_bound, right_bound + 1) if img_gray.getpixel((x, y)) < black_color)
            if bottom_black_pixel_count > (right_bound - left_bound + 1) * row_color_threshold:
                bottom_bound = y
                break

        # 裁剪图片
        cropped_img = img.crop((left_bound, top_bound, right_bound, bottom_bound))
        cropped_img.save(output_path)

        # # 绘制矩形
        # draw = ImageDraw.Draw(img)
        # draw.rectangle([left_bound, top_bound, right_bound, bottom_bound])
        # img.save(output_path)


def batch_process_images(folderIn_path, folderOut_path):
    if not os.path.exists(folderOut_path):
        os.makedirs(folderOut_path)
    for filename in os.listdir(folderIn_path):
        fileInpath = os.path.join(folderIn_path, filename)
        fileOutpath = os.path.join(folderOut_path, filename)
        if os.path.isdir(fileInpath):
            # 如果是文件夹，则递归处理其中的图片
            batch_process_images(fileInpath, fileOutpath)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            # 如果是图片文件，则进行处理
            crop_image(fileInpath, fileOutpath)


if __name__ == "__main__":
    input_folder = "ocren_test0304/save"  # 输入文件夹路径
    output_folder = "ocren_test0309"  # 输出文件夹路径
    batch_process_images(input_folder, output_folder)
    global paths
    paths = []
    # 将路径列表写入到 JSON 文件中
    with open(os.path.join(output_folder, "blankImg.json"), "w") as f:
        json.dump(paths, f)
