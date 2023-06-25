# -*- coding: utf-8 -*-

import sys
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import ui_uart_tools
from tool import Tool
import serial
import serial.tools.list_ports


class myMainwindow(qw.QMainWindow, ui_uart_tools.Ui_MainWindow):
    signal_recv_data = qc.pyqtSignal(str)
    signal_recv_data1 = qc.pyqtSignal(int)
    signal_recv_data2 = qc.pyqtSignal()

    def __init__(self):
        super().__init__()
        # ui = ui_uart_tools.Ui_MainWindow()
        self.setupUi(self)
        # 获取串口列表
        self.comList = list(serial.tools.list_ports.comports())
        self.portlist = []
        for com in range(0, len(self.comList)):
            self.portlist.append(self.comList[com][0])
        # 加载配置文件
        self.settings = qc.QSettings("config.ini", qc.QSettings.IniFormat)
        self.settings.setIniCodec("UTF-8")
        self.config_uartbaud = self.settings.value("setup/UART_BAUD", 0, type=int)
        self.uart_port = self.settings.value("setup/UART_PORT")
        # print(self.config_uartbaud)
        # 初始化窗口
        self.statusbar.showMessage("status:ok")
        # 初始化界面
        self.comboBox_uart.addItems(self.portlist)
        self.radioButton_recvascii.setChecked(True)
        self.radioButton_sendascii.setChecked(True)
        self.spinBox.setRange(100, 30 * 1000)
        self.spinBox.setSingleStep(100)
        self.spinBox.setWrapping(True)
        self.spinBox.setValue(1000)
        self.comboBox_baud.setCurrentText(str(self.config_uartbaud))
        self.comboBox_uart.setCurrentText(self.uart_port)
        # 绑定信号与槽
        self.comboBox_baud.currentIndexChanged.connect(self.comboBox_baud_cb)
        self.comboBox_uart.currentIndexChanged.connect(self.comboBox_uart_cb)
        self.btn_send.clicked.connect(self.btn_send_cb)
        self.actionstart.triggered.connect(self.actionstart_cb)
        self.actionpause.triggered.connect(self.actionpause_cb)
        self.actionstop.triggered.connect(self.actionstop_cb)
        self.actionqingsao.triggered.connect(self.actionqingsao_cb)
        self.radioButton_recvascii.toggled.connect(self.radioButton_recvascii_cb)
        self.radioButton_sendascii.toggled.connect(self.radioButton_sendascii_cb)
        self.radioButton_sendhex.toggled.connect(self.radioButton_sendhex_cb)
        self.radioButton_recvhex.toggled.connect(self.radioButton_recvhex_cb)
        self.checkBox_autoline.toggled.connect(self.checkBox_autoline_cb)
        self.checkBox_showsend.toggled.connect(self.checkBox_showsend_cb)
        self.checkBox_showtime.toggled.connect(self.checkBox_showtime_cb)
        self.checkBox_repeatsend.toggled.connect(self.checkBox_repeatsend_cb)
        self.spinBox.valueChanged.connect(self.spinBox_cb)
        # 自定义信号
        self.signal_recv_data.connect(self.textBrowser_show_data_cb)
        # 实例化tool,tool为中间层
        self.tool = Tool(self)

    def textBrowser_show_data_cb(self, data):
        self.textBrowser.insertPlainText(data)
        cursor = self.textBrowser.textCursor().End
        self.textBrowser.moveCursor(cursor)

    def comboBox_baud_cb(self):
        content = self.comboBox_baud.currentText()
        text = f"您当前选中了{content}"
        qw.QMessageBox.information(self, "提示", text, qw.QMessageBox.Ok | qw.QMessageBox.Cancel)

    def comboBox_uart_cb(self):
        content = self.comboBox_uart.currentText()
        self.settings.setValue("setup/UART_PORT", content)

    def btn_send_cb(self):
        # print("you click btn_send")
        send_data = self.textEdit_get.toPlainText()
        self.tool.uart.send_uart_data(send_data)

    def actionstart_cb(self):
        pass

    def actionpause_cb(self):
        pass

    def actionstop_cb(self):
        pass

    def actionqingsao_cb(self):
        pass

    def radioButton_recvascii_cb(self):
        pass

    def radioButton_sendascii_cb(self):
        pass

    def radioButton_recvhex_cb(self):
        pass

    def radioButton_sendhex_cb(self):
        pass

    def checkBox_autoline_cb(self):
        res_auto_line = self.checkBox_autoline.isChecked()
        print("res_auto_line is ", res_auto_line)
        res_show_send = self.checkBox_showsend.isChecked()
        print("res_show_send is ", res_show_send)
        res_show_time = self.checkBox_showtime.isChecked()
        print("res_show_time is ", res_show_time)
        res_repeat_send = self.checkBox_repeatsend.isChecked()
        print("res_repeat_send is ", res_repeat_send)

    def checkBox_showsend_cb(self):
        pass

    def checkBox_showtime_cb(self):
        pass

    def checkBox_repeatsend_cb(self):
        pass

    def spinBox_cb(self, value):
        # res_spinbox=self.spinBox.value()
        print("spinbox value is:", value)


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    print(sys.argv)
    w = myMainwindow()
    w.show()
    sys.exit(app.exec_())
