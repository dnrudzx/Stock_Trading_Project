import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import pandas_datareader.data as web
import matplotlib.pyplot as plt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('키움 API 테스터')
        self.setGeometry(300,300,300,700)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        '''UI처리'''
        #로그인 박스
        box_setting = QGroupBox('셋팅',self)
        box_setting.setGeometry(20,20,260,60)

        self.btn_login = QPushButton('Login',box_setting)
        self.btn_login.move(20,20)
        self.edit_login = QLineEdit('Not Connect', box_setting)
        self.edit_login.setGeometry(140,20,100,30)
        self.edit_login.setEnabled(False)
        # 전체조회[종목코드 : 종목명]
        self.box_allList = QGroupBox('전체종목', self)
        self.box_allList.setGeometry(20, 90, 260, 300)
        self.box_allList.setEnabled(False)

        self.list_All = QListWidget(self.box_allList)
        self.list_All.setGeometry(0, 20, 260, 250)
        btn_show_item = QPushButton('조    회', self.box_allList)
        btn_show_item.setGeometry(0,271,260,29)
        #단일종목 검색 박스
        self.box_single_find = QGroupBox('단일종목 조회',self)
        self.box_single_find.setGeometry(20,400,260,190)
        self.box_single_find.setEnabled(False)

        label_singleCode = QLabel('종목코드 : ',self.box_single_find)
        label_singleCode.move(20,30)
        self.edit_singleCode = QLineEdit(self.box_single_find)
        self.edit_singleCode.setGeometry(100,27,140,25)
        btn_single_find = QPushButton('조    회', self.box_single_find)
        btn_single_find.setGeometry(20,60,220,30)
        self.edit_singleResult = QTextEdit(self.box_single_find)
        self.edit_singleResult.setGeometry(20,110,220,65)
        self.edit_singleResult.setEnabled(False)
        #조건검색명
        self.box_condition = QGroupBox('조건', self)
        self.box_condition.setGeometry(20,600,260,70)
        self.box_condition.setEnabled(False)

        label_condition_name = QLabel('조건검색명 : ', self.box_condition)
        label_condition_name.move(20,20)
        self.select_condition = QComboBox(self.box_condition)
        self.select_condition.setGeometry(100,17,140,25)

        '''이벤트 처리'''
        self.kiwoom.OnEventConnect.connect(self.login_event)
        self.kiwoom.OnReceiveTrData.connect(self.single_find_event)
        self.kiwoom.OnReceiveConditionVer.connect(self.receive_condition)

        '''메소드 처리'''
        self.btn_login.clicked.connect(self.login)
        btn_single_find.clicked.connect(self.single_find)
        btn_show_item.clicked.connect(self.show_item)

    '''메소드 연결'''
    def login(self):
        ret = self.kiwoom.dynamicCall('CommConnect()')

    def single_find(self):
        code = self.edit_singleCode.text()
        self.edit_singleResult.append('종목코드 : ' + code)
        self.kiwoom.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)
        self.kiwoom.dynamicCall('CommRqData(QString, QString, int, QString)', 'opt10001_req', 'opt10001', 0, '0101')

    def show_item(self):
        item = self.list_All.currentItem().text()[:6]
        item = web.DataReader(item+'.KS', 'yahoo')
        plt.plot(item.index, item['Adj Close'])
        plt.show()

    '''이벤트 연결'''
    def login_event(self,err_code):
        if err_code == 0:
            self.edit_login.setText('Connect')

            self.btn_login.setEnabled(False)
            self.box_single_find.setEnabled(True)
            self.box_allList.setEnabled(True)
            self.box_condition.setEnabled(True)

            self.kiwoom.dynamicCall('GetConditionLoad()')

            ret = self.kiwoom.dynamicCall('GetCodeListByMarket(QString)', ['0'])
            code_list = ret.split(';')
            items = []
            for code in code_list:
                items.append(code + ':' + self.kiwoom.dynamicCall('GetMasterCodeName(QString)', [code]))
            self.list_All.addItems(items)
        else: self.edit_login.setText('Not Connect')

    def single_find_event(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == 'opt10001_req':
            self.edit_singleResult.append('종목명 : ' + self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString', trcode, '', rqname, 0, '종목명').strip())
            self.edit_singleResult.append('거래량 : ' + self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString', trcode, '',rqname, 0, '거래량').strip())

    def receive_condition(self):
        conditions = self.kiwoom.dynamicCall('GetConditionNameList()')
        conditions = conditions.rstrip(';').split(';')
        self.select_condition.addItems(conditions)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
