from connect_Det_Blank import delete_blank
from connect_Det_strokes import delete_strokes
import os


current_folder = os.path.dirname(__file__)
delete_strokes(os.path.join(current_folder, 'files/image/1.jpg'), os.path.join(current_folder, 'files/nostroke/1.jpg'))
delete_blank(os.path.join(current_folder, 'files/nostroke/1.jpg'), os.path.join(current_folder, 'files/noblank/1.jpg'))
delete_strokes(os.path.join(current_folder, 'files/image/2.jpg'), os.path.join(current_folder, 'files/nostroke/2.jpg'))
delete_blank(os.path.join(current_folder, 'files/nostroke/2.jpg'), os.path.join(current_folder, 'files/noblank/2.jpg'))
delete_strokes(os.path.join(current_folder, 'files/image/3.jpg'), os.path.join(current_folder, 'files/nostroke/3.jpg'))
delete_blank(os.path.join(current_folder, 'files/nostroke/3.jpg'), os.path.join(current_folder, 'files/noblank/3.jpg'))
