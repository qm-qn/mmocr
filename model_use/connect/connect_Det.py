from connect_Det_Blank import delete_blank
from connect_Det_strokes import delete_strokes
import os


current_folder = os.path.dirname(__file__)
delete_strokes(os.path.join(current_folder, 'files/image.jpg'), os.path.join(current_folder, 'files/nostroke.jpg'))
delete_blank(os.path.join(current_folder, 'files/nostroke.jpg'), os.path.join(current_folder, 'files/noblank.jpg'))
