from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import re
import serial
import serial.tools.list_ports

import global_var

class Serialwindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()


    def initUI(self):

        self.port = ''
        self.bps = 0
        self.timeout = 0.0

        self.senddata=bytes()

        self.read_data=''
        
        self.btn_plist=QPushButton('获取可用串口',self)
        self.btn_plist.setGeometry(20,20,170,40)
        self.btn_plist.clicked.connect(self.get_serial_info)
        
        self.btn_ser_init=QPushButton('初始化',self)
        self.btn_ser_init.setGeometry(20,70,170,40)
        self.btn_ser_init.clicked.connect(self.serial_init)

        self.btn_open=QPushButton('打开串口',self)
        self.btn_open.setGeometry(20,120,170,40)
        self.btn_open.clicked.connect(self.open_serial)

        self.btn_close=QPushButton('关闭串口',self)
        self.btn_close.setGeometry(20,170,170,40)
        self.btn_close.clicked.connect(self.close_serial)

        self.btn_read_data=QPushButton('读取数据',self)
        self.btn_read_data.setGeometry(20,220,170,40)
        self.btn_read_data.clicked.connect(self.read_data_size)

        self.port_set=QComboBox(self)
        self.port_set.setGeometry(140,270,120,40)
        self.lbl_port_set=QLabel(self)
        self.lbl_port_set.setGeometry(20,270,120,40)
        self.lbl_port_set.setText('串口号:')

        self.baud_set=QComboBox(self)
        self.baud_set.setGeometry(140,320,120,40)
        self.baud_set.addItems(['9600','19200','38400','115200'])
        self.lbl_baud_set=QLabel(self)
        self.lbl_baud_set.setGeometry(20,320,120,40)
        self.lbl_baud_set.setText('波特率:')

        self.stopbit_set=QComboBox(self)
        self.stopbit_set.setGeometry(140,370,120,40)
        self.stopbit_set.addItems(['0','1'])
        self.lbl_stopbit_set = QLabel(self)
        self.lbl_stopbit_set.setGeometry(20,370,120,40)
        self.lbl_stopbit_set.setText('停止位:')

        self.parity_set=QComboBox(self)
        self.parity_set.setGeometry(140,420,120,40)
        self.parity_set.addItems(['无','奇校验','偶校验'])
        self.lbl_parity_set = QLabel(self)
        self.lbl_parity_set.setGeometry(20,420,120,40)
        self.lbl_parity_set.setText('校验位:')

        self.databit_set=QComboBox(self)
        self.databit_set.setGeometry(140,470,120,40)
        self.databit_set.addItems(['8','7'])
        self.lbl_databit_set=QLabel(self)
        self.lbl_databit_set.setGeometry(20,470,120,40)
        self.lbl_databit_set.setText('数据位:')

        self.timeout_set=QLineEdit(self)
        self.timeout_set.setGeometry(140,520,120,40)
        self.timeout_set.setText('1000')
        self.lbl_timeout_set=QLabel(self)
        self.lbl_timeout_set.setGeometry(20,520,120,40)
        self.lbl_timeout_set.setText('超时设置:')

        self.le_recdata=QTextEdit(self)
        self.le_recdata.setGeometry(300,20,600,540)

        self.setGeometry(100,100,920,600)
        self.setWindowTitle('串口调试助手')
        self.show()


    def Qcombo(self):
        print(self.port_set.currentText())
        print(self.baud_set.currentText())
        print(self.stopbit_set.currentText())
        print(self.parity_set.currentText())
        print(self.databit_set.currentText())
        print(self.timeout_set.text())


    def get_serial_info(self):
        self.plist = list(serial.tools.list_ports.comports())
        if len(self.plist) <= 0:
            self.le_recdata.append('[SPU Error]: Port Not Found')
        else:
            for i in list(self.plist):
                self.port_set.addItem(i.name)


    def serial_init(self):
        self.port = self.port_set.currentText()
        self.bps = int(self.baud_set.currentText())
        self.timeout = float(self.timeout_set.text())
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.bps, bytesize=8, parity='N', stopbits=1)
            print(self.ser)
            if self.ser.is_open:
                self.le_recdata.append('串口正常')
        except Exception as e:
            self.le_recdata.append('[SPU Error]: Port Not Found')
            print('异常：', e)


    def open_serial(self):
        try:
            self.ser.open()
        except Exception as e:
            self.le_recdata.append('[SPU Error]: Port Not Found')
            print('异常：', e)


    def close_serial(self):
        try:
            self.ser.close()
        except Exception as e:
            self.le_recdata.append('[SPU Error]: Port Not Found')
            print('异常：', e)


    def read_data_size(self):
        ct=datetime.datetime.now()
        ct_str=ct.strftime("%Y-%m-%d %H:%M:%S")
        try:
            #self.size=10
            self.read_data=self.ser.read_all()
            #print(self.read_data)
            self.read_data_str=self.read_data.hex()   #字节转成16进制字符显示
            #re.findall(r'.{3}',self.read_data_str)
            self.read_data_str_fg=self.str_separate(self.read_data_str)
            #print(self.read_data_str)
            self.le_recdata.append('\n'+'['+ct_str+']'+' '+self.read_data_str_fg+'\n')
        except Exception as e:
            self.le_recdata.append('[SPU Error]: Port Not Found')
        # return self.read_data


    def read_data_line(self):
        self.read_data=self.ser.readline()
        return self.read_data


    def read_data_alway(self, way):
        print('开始接受数据：')
        while True:
            try:
                if self.ser.inWaiting:
                    if (way == 0):
                        for i in range(self.ser.inWaiting):
                            print('接收ascII数据：'+str(self.read_data_size(1)))
                            data1 = self.read_data_size(1).hex()
                            data2 = int(data1, 16)
                            print('接收到16进制数据：'+data1+'接收到10进制数据：'+str(data2))
                    if (way == 1):
                        data = self.ser.read_all()
            except Exception as e:
                self.le_recdata.append('[SPU Error]: Port Not Found')
                print('异常：', e)


    def str_separate(self, A):
        '''
        对字符串进行按长度分割，并在中间加入其他字符，如空格、短横等
        '''
        b = re.findall(r'.{2}', A)
        c = ' '.join(b)
        #print(c)
        return c