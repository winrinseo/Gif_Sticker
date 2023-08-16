import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt,QRect
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap , QMovie

class Sticker(QWidget):
    def __init__(self):
        super(Sticker,self).__init__()
        self.imgPath = "image/image.gif"
        self.stickerInit()

    def stickerInit(self):
        self.centralwidget = QWidget(self)
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground , True)
        self.setAttribute(Qt.WA_TranslucentBackgroud,True)

        self.label = QLabel(self.centralwidget)

        self.movie = QMovie(self.imgPath)

        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()

        w = int(self.movie.frameRect().size().width())
        h = int(self.movie.frameRect().size().height())

        self.movie.setScaledSize(w,h)

        self.movie.start()


    # 마우스 드래그 오버라이딩
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        return super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        return super().mouseMoveEvent(a0)
    
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        return super().mouseReleaseEvent(a0)
        

if __name__ == '__main__':
    print("실행")
    app = QApplication(sys.argv)
    ex = Sticker()
    sys.exit(app.exec_())