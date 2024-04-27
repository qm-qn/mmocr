import argparse
from Strokes import strokes
from Blank import blank
from Recog import recog
from datetime import datetime

current_time = datetime.now()
print("Current time:", current_time)


parser = argparse.ArgumentParser(description='Recognization')
parser.add_argument('input_folder', type=str, help='The path to the image')
args = parser.parse_args()

strokes(args.input_folder)
blank()
recog()
current_time = datetime.now()
print("Current time:", current_time)