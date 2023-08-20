import sys , asyncio , math , os , random
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QMainWindow ,QApplication, QWidget, QLabel,QAction,qApp
from PyQt5.QtCore import QEvent, QObject, Qt,QRect,QSize,QTimer,QPoint
from PyQt5.QtGui import QMouseEvent, QCursor, QPixmap , QMovie

            


class Sticker(QMainWindow):
    def __init__(self,imgPath):
        super(Sticker,self).__init__()
        self.sizeUp = False
        self.imgPath = imgPath
        self.setContextMenu()
        self.stickerInit()
        self.timerInit()

    
    def stickerInit(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_NoSystemBackground , True)
        self.setAttribute(Qt.WA_TranslucentBackground,True)

        self.label = QLabel(self.centralwidget)

        self.movie = QMovie(self.imgPath)

        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()

        self.w = int(self.movie.frameRect().size().width())
        self.h = int(self.movie.frameRect().size().height())

        print(self.w , self.h)
        
        self.movie.setScaledSize(QSize(self.w , self.h))

        self.movie.start()

        # 등장 위치는 랜덤
        screen_rect = app.desktop().screenGeometry()
        x = random.randrange(0,screen_rect.width() - self.w)
        y = random.randrange(0,screen_rect.height() - self.h)

        self.setGeometry(x,y,self.w , self.h)

        self.show()


    def setContextMenu(self):
        
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        timer_start_action = QAction('마우스 따라가기', self,checkable= True)
        
        quit_action = QAction('잘가 ㅠㅠ',self)
        self.addAction(timer_start_action)
        
        self.addAction(quit_action)

        timer_start_action.triggered.connect(self.handlerTimerThread)
        
        quit_action.triggered.connect(self.quitApp)


    def timerInit(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.__workHandler)
        

    def __workHandler(self):
        #중앙 위치 계산
        centerPos = QPoint(self.pos().x() + self.w // 2 , self.pos().y() + self.h //2) if not self.sizeUp else QPoint(self.pos().x() + self.w, self.pos().y() + self.h )
        vector = QPoint(QCursor.pos() - centerPos)
        # print(self.pt.x(),self.pt.y())

        #벡터 정규화 (단위벡터로 만들어줌)
        vector /= math.sqrt(vector.x()**2 + vector.y()**2)
        
        # 적당히 벡터의 크기를 늘려줌
        vector *= 2
        # print(vector.x() , vector.y())

        # 해당 방향으로 이동
        self.move(self.pos() + vector)

    # timerThread 시작 및 종료
    def handlerTimerThread(self,state):
        if state:
            self.timer.start(10)
        else:
            self.timer.stop()

    # 프로그램 종료
    def quitApp(self):
        qApp.quit()

    # 마우스 드래그 오버라이딩
    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position=event.globalPos()-self.pos()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.LeftButton and self.m_flag:  
            self.move(event.globalPos()-self.m_Position)
            event.accept()

    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        QApplication.restoreOverrideCursor()
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        print('call double click')
        if self.sizeUp:
            self.sizeUp = False
            
            self.setFixedSize(self.w, self.h)

            self.label.setFixedSize(self.w , self.h)
            
            self.movie.setScaledSize(QSize(self.w , self.h))
            
            print(self.movie.frameRect().size().width() , self.movie.frameRect().size().height())
            
        else :
            self.sizeUp = True
            
            self.setFixedSize(self.w * 2 , self.h * 2)

            #라벨의 크기를 바꿔야 함 (라벨이 도화지임)
            self.label.setFixedSize(self.w * 2 , self.h * 2)
            
            self.movie.setScaledSize(QSize(self.w * 2, self.h * 2))
            
            print(self.movie.frameRect().size().width() , self.movie.frameRect().size().height())
            
            
            

    # mouse hover event
    def enterEvent(self, event: QEvent) -> None:
        # print(QCursor.pos() - self.pos())
        QApplication.setOverrideCursor(Qt.CursorShape.CustomCursor)
    
    def leaveEvent(self, event: QEvent) -> None:
        QApplication.restoreOverrideCursor()

if __name__ == '__main__':
    path_dir = 'image'
    file_list = os.listdir(path_dir)
    
    app = QApplication(sys.argv)
    
    #폴더에 있는 모든 이미지를 생성
    ex = []
    for file in file_list:
        ex.append( Sticker("image/" + file))
    

    sys.exit(app.exec_())