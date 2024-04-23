import argparse
from Strokes import strokes
from Blank import blank
from Recog import recog


# # 设置 ArgumentParser
# parser = argparse.ArgumentParser(description='Recognizationrecog')
# parser.add_argument('input_folder', type=str, help='The path to the image')

# # 解析命令行参数
# args = parser.parse_args()

strokes('model_use/test/image')  # args.input_folder
blank()
recog()
