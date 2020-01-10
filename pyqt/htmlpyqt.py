import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class CallHandler(QObject):
    @pyqtSlot(result=str)
    def myHello(self):
        print('call received')
        return 'hello, Python'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QWebEngineView()
    channel = QWebChannel()
    handler = CallHandler()
    channel.registerObject('pyjs', handler)
    view.page().setWebChannel(channel)
    url_string = 'http://192.168.0.165:8080/index' #"file:///F:/数据/lsat/index.html"
    view.load(QUrl(url_string))
    view.show()
    sys.exit(app.exec_())
