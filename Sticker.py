import sys , asyncio , math
from PyQt5 import QtGui

from PyQt5.QtWidgets import QMainWindow ,QApplication, QWidget, QLabel,QAction,qApp
from PyQt5.QtCore import Qt,QRect,QSize,QTimer,QPoint
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap , QMovie

            


class Sticker(QMainWindow):
    def __init__(self):
        super(Sticker,self).__init__()
        self.imgPath = "image/sticker.gif"
        self.positionInit()
        self.setContextMenu()
        self.stickerInit()
        self.timerInit()

    #각종 위치의 초기값을 설정
    def positionInit(self):
        #마우스 위치 벡터
        self.pt = QPoint(0,0)
        
        

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

        self.w = int(self.movie.frameRect().size().width() * 0.5)
        self.h = int(self.movie.frameRect().size().height() * 0.5)

        print(self.w , self.h)
        self.movie.setScaledSize(QSize(self.w , self.h))

        self.movie.start()

        self.setGeometry(0,0,self.w , self.h)

        self.show()


    def setContextMenu(self):
        
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        quit_action = QAction('잘가 ㅠㅠ',self)
        self.addAction(quit_action)

        quit_action.triggered.connect(self.quitApp)


    def timerInit(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.__workHandler)
        self.timer.start(10)

    def __workHandler(self):
        #중앙 위치 계산
        centerPos = QPoint(self.pos().x() + self.w // 2 , self.pos().y() + self.h //2)
        vector = QPoint(QCursor.pos() - centerPos)
        # print(self.pt.x(),self.pt.y())

        #벡터 정규화 (단위벡터로 만들어줌)
        vector /= math.sqrt(vector.x()**2 + vector.y()**2)
        
        # 적당히 벡터의 크기를 늘려줌
        vector *= 2
        print(vector.x() , vector.y())

        # 해당 방향으로 이동
        self.move(self.pos() + vector)

    def quitApp(self):
        qApp.quit()

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