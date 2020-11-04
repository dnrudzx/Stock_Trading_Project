import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 500)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        '''로그인 버튼 처리'''
        btn1 = QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)
        self.btn1_edit = QTextEdit('Not Connect',self)
        self.btn1_edit.move(170, 20)
        self.btn1_edit.setEnabled(False)
        self.kiwoom.OnEventConnect.connect(self.login_event_connect)

        '''단일 종목 조회'''#키움증권 : 039490
        label1 = QLabel('종목코드 : ', self)
        label1.move(20,70)
        self.code_edit = QLineEdit(self)
        self.code_edit.move(80,70)
        btn2 = QPushButton('종목조회', self)
        btn2.move(190,70)
        btn2.clicked.connect(self.btn2_clicked)
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10,120,280,80)
        self.text_edit.setEnabled(False)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

        '''전체조회[종목코드 : 종목명]'''
        btn3 = QPushButton('전체조회',self)
        btn3.setGeometry(10,220,280,30)
        btn3.clicked.connect(self.btn3_clicked)
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10,270,280,150)

    '''로그인 버튼 처리'''
    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
    def login_event_connect(self, err_code):
        if err_code == 0: self.btn1_edit.setText('Connect')
        else: self.btn1_edit.setText('Not Connect')

    '''단일 종목 조회'''
    def btn2_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append('종목코드 : '+code)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', "종목코드", code)
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())

    '''전체조회[종목코드 : 종목명]'''
    def btn3_clicked(self):
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        code_list = ret.split(';')
        result = []
        for code in code_list:
            #result.append(code + ':' + self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [code]))
            result.append(code + ':' + self.kiwoom.dynamicCall("GetMasterLastPrice(QString)", [code]))
        self.listWidget.addItems(result)
        print(len(result))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()