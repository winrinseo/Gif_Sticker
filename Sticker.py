import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMainWindow ,QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt,QRect,QSize
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap , QMovie

class Sticker(QMainWindow):
    def __init__(self):
        super(Sticker,self).__init__()
        self.imgPath = "image/sticker.gif"
        self.stickerInit()
        # self.setContextMenu()

    def stickerInit(self):
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)

        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_NoSystemBackground , True)
        self.setAttribute(Qt.WA_TranslucentBackground,True)

        self.label = QLabel(centralwidget)

        self.movie = QMovie(self.imgPath)
        print(self.movie)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()

        w = int(self.movie.frameRect().size().width())
        h = int(self.movie.frameRect().size().height())

        print(w , h)
        self.movie.setScaledSize(QSize(w,h))

        self.movie.start()

        self.setGeometry(0,0,w,h)

        self.show()


    # def setContextMenu():




    # 마우스 드래그 오버라이딩
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position=event.globalPos()-self.pos()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton and self.m_flag:  
            self.move(event.globalPos()-self.m_Position)
            event.accept()

    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
        

if __name__ == '__main__':
    print("실행")
    app = QApplication(sys.argv)
    ex = Sticker()
    sys.exit(app.exec_())