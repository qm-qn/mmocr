import argparse
from Strokes import strokes
from Blank import blank
from Recog import recog


# parser = argparse.ArgumentParser(description='Recognizationrecog')
# parser.add_argument('input_folder', type=str, help='The path to the image')
# args = parser.parse_args()

strokes('model_use/final/image')  # args.input_folder
blank()
recog()
