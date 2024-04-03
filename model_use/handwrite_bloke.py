import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, \
    QColorDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QGridLayout, QTextEdit, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRect
from PIL import ImageGrab
from connect_Rec import Rec
import sys


class show_window(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.window = QWidget()


class mylable(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def __init__(self, parent):
        super(mylable, self).__init__(parent)
        self.pixmap = QPixmap(747, 647)  # 考虑边框的间距 减去px 597, 497
        self.pixmap.fill(Qt.white)
        self.setStyleSheet("border: 2px solid red")
        self.Color = Qt.black  # pen color: defult:blue
        self.penwidth = 5  # pen width : default:4
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, event):
        Label_painter = QPainter(self)
        Label_painter.drawPixmap(2, 2, self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.pixmap)
            painter.setPen(QPen(self.Color, self.penwidth, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def clear_canvas(self):
        self.pixmap.fill(Qt.white)
        self.update()


class cb(QMainWindow):
    def __init__(self):
        super(cb, self).__init__()
        self.initUi()

    def initUi(self):
        self.resize(1000, 800)  # 800, 600
        vbox = QVBoxLayout()
        # 橡皮
        self.button_erase = QPushButton(self)
        self.button_erase.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_erase.setGeometry(810, 40, 180, 75)
        self.button_erase.setText("Erase")
        self.button_erase.setFont(QFont("Tahoma", 20))
        vbox.addWidget(self.button_erase)
        vbox.addStretch()
        # 选择画笔颜色 按钮
        self.button_color = QPushButton(self)
        self.button_color.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_color.setGeometry(810, 460, 180, 75)
        self.button_color.setText("Color")
        self.button_color.setFont(QFont("Tahoma", 20))
        vbox.addWidget(self.button_color)
        vbox.addStretch()
        # 选择画笔粗细 按钮
        self.button_width = QPushButton(self)
        self.button_width.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_width.setGeometry(810, 320, 180, 75)
        self.button_width.setText("Width")
        self.button_width.setFont(QFont("Tahoma", 20))
        vbox.addWidget(self.button_width)
        vbox.addStretch()
        # 设置画板
        self.lb = mylable(self)
        self.lb.setGeometry(20, 40, 751, 651)  # 20, 40, 601, 501
        # 工具栏
        self.menubar = self.addToolBar("ToolBar")
        # 写
        self.button_write = QPushButton(self)
        self.button_write.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_write.setGeometry(810, 180, 180, 75)
        self.button_write.setText("Write")
        self.button_write.setFont(QFont("Tahoma", 20))
        vbox.addWidget(self.button_write)
        # 识别
        self.button_recognize = QPushButton(self)
        self.button_recognize.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_recognize.setGeometry(200, 700, 400, 60)
        self.button_recognize.setText("Recognize")
        self.button_recognize.setFont(QFont("Tahoma", 20))
        vbox.addWidget(self.button_recognize)
        # clear
        self.button_clear = QPushButton(self)
        self.button_clear.setStyleSheet("color: #12c2f5;background-color: white")
        self.button_clear.setGeometry(810, 600, 180, 75)
        self.button_clear.setText("Clear")
        self.button_clear.setFont(QFont("Tahoma", 24))
        vbox.addWidget(self.button_clear)
        # 主页面
        self.setWindowIcon(QIcon(r"D:\exp_recognize\logo.png"))
        self.setWindowTitle("Drawing Board")
        self.button_erase.clicked.connect(self.erase)
        self.button_color.clicked.connect(self.choose_color)
        self.button_width.clicked.connect(self.choose_width)
        self.button_write.clicked.connect(self.write)
        self.button_recognize.clicked.connect(self.recognize)
        self.button_clear.clicked.connect(self.lb.clear_canvas)

    def back(self):
        self.show_win.close()

    def write(self):
        self.lb.penwidth = 5
        self.lb.Color = Qt.black
        self.lb.setCursor(Qt.CrossCursor)

    def choose_color(self):
        Color = QColorDialog.getColor()  # color是Qcolor
        if Color.isValid():
            self.lb.Color = Color
        self.lb.penwidth = 5
        self.lb.setCursor(Qt.CrossCursor)

    def erase(self):
        self.lb.Color = Qt.white
        self.lb.setCursor(Qt.ForbiddenCursor)
        self.lb.penwidth = self.lb.penwidth * 5

    def choose_width(self):
        width, ok = QInputDialog.getInt(self, 'Choose width', 'Please input width:', min=5, step=1)
        if ok:
            self.lb.penwidth = width
        self.lb.Color = Qt.black
        self.lb.setCursor(Qt.CrossCursor)

    def recognize(self):
        img_ready = ImageGrab.grab((486, 160, 1227, 800))
        filename = 'model_use/connect_in.jpg'
        img_ready.save(filename)
        pre = pre_img(filename)
        vbox = QVBoxLayout()
        # 识别结果展示界面
        self.show_win = show_window()
        self.show_win.setGeometry(486, 180, 741, 640)  # 起始点坐标、组件大小
        self.show_win.setWindowTitle('Result')
        # self.show_win.setWindowIcon(QIcon(r'D:\exp_recognize\logo.png'))

        # 识别结果
        self.label = QLabel(pre, self.show_win)
        grid_layout = QGridLayout()
        self.label.setFont(QFont("Tahoma", 30))
        self.label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.label)
        self.show_win.setLayout(grid_layout)

        # 返回按钮
        self.button_back = QPushButton(self.show_win)
        self.button_back.setStyleSheet("color: white;background-color: #99CCCC")
        self.button_back.setGeometry(0, 0, 50, 30)
        self.button_back.setText("Back")
        self.button_back.setFont(QFont("Tahoma", 12))
        vbox.addWidget(self.button_back)
        self.button_back.clicked.connect(self.back)

        # 显示识别过程
        self.button_att = QPushButton(self.show_win)
        self.button_att.setStyleSheet("color: white;background-color: #99CCCC")
        self.button_att.setGeometry(610, 0, 130, 30)
        self.button_att.setText("Attention Map")
        self.button_att.setFont(QFont("Tahoma", 12))
        vbox.addWidget(self.button_att)
        self.button_att.clicked.connect(Rec)

        # 图片展示
        self.button_show = QPushButton(self.show_win)
        self.button_show.setStyleSheet("color: white;background-color: #99CCCC")
        self.button_show.setGeometry(210, 600, 320, 50)
        self.button_show.setText("Show")
        self.button_show.setFont(QFont("Tahoma", 16))
        self.button_show.clicked.connect(show)
        self.show_win.show()
        self.show_win.exec_()


def show():
    img = cv2.imread(r'D:\exp_recognize\result.png')
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    rate = img.shape[0] / img.shape[1]
    r_rate = img.shape[1] / img.shape[0]
    if img.shape[1] > 300:
        cv2.resizeWindow("result", 900, int(900 * rate))
    elif img.shape[0] >= img.shape[1]:
        cv2.resizeWindow("result", 200, int(200 * r_rate))
    else:
        cv2.resizeWindow("result", 250, int(350 * rate))

    cv2.moveWindow("result", 900, 300)
    # cv2.namedWindow('result', 0)
    # cv2.resizeWindow('result', 500, 500)
    cv2.imshow('result', img)
    cv2.waitKey(0)
    try:
        cv2.destroyWindow('result')
    except Exception as e:
        print(e)


# from predict_gui import pre_img

app = QApplication(sys.argv)
mainwindow = cb()
mainwindow.show()
app.exec_()
