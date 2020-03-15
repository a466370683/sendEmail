# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication,  QMainWindow, QMessageBox,QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore,QtWidgets, QtGui
import time
from threading import Thread
import logging
import coloredlogs
import pkgutil
import importlib
import plugins

def load_plugins(namespace):
    """
    加载命名控件下所有的子模块
    :param namespace:
    :type namespace: Any
    namespace.__path__: 命名空间绝对路径
    namespace.__name__: 命名控件前缀
    :return:
    """
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules(namespace.__path__, namespace.__name__ + '.')
    }

"""
执行加载子模块
plugins.模块名 即可调用
"""
load_plugins(plugins)

def setup_logger(name,use_colors=True,verbose_count=0):
    """
    初始化日志~
    :param name: 日志名
    :type name: str
    :param use_colors:
    :type use_colors: bool
    :param verbose_count:
    :type verbose_count: int
    :return:
    """
    fmt = '[%(levelname).8s %(asctime)s %(name)s:%(lineno)d] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    fh = logging.FileHandler('test.log')
    level = max(5 - verbose_count, 0) * 10
    logger = logging.getLogger(name)

    """控制器中显示log日志"""
    if use_colors:
        coloredlogs.install(logger=logger, level=logging.INFO, fmt=fmt, datefmt=datefmt)
    else:
        logging.basicConfig(level=level, format=fmt, datefmt=datefmt)

    formatter = logging.Formatter(fmt, datefmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

"""
    App类说明
    :param Diaoyu: 软件窗口
    :type Diaoyu: object
    :param QMainWindow:所有窗口继承的基类
    :type QMainWindow: object
"""
class App(plugins.diaoyu.Diaoyu,QMainWindow):
    """创建信号，使用信号触发table刷新,避免刷新异常"""
    signal = pyqtSignal()

    def __init__(self):

        super(App,self).__init__()
        self.setupUi(self)
        self.label = False
        self.logger = setup_logger("diaoyu.log")
        self.logger.info("开始使用")

        """窗口控件的事件"""
        self.pushButton.clicked.connect(self.sendEmail)
        self.pushButton_2.clicked.connect(self.getData)
        self.pushButton_3.clicked.connect(self.licenseData)
        self.pushButton_4.clicked.connect(self.stopLicense)
        self.signal.connect(self.getData)

    def stopLicense(self):
        self.logger.info("暂停监听")
        self.label = True

    def licenseData(self):
        self.label = False
        thread = Thread(target=self.license)
        thread.start()

    def license(self):
        _translate = QtCore.QCoreApplication.translate
        while True:
            if(self.label):
                break
            self.signal.emit()
            time.sleep(3)

    def getData(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget.clear()
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(181)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "账号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "密码"))
        try:
            self.model = plugins.mysqlcurd.Model(db="rxjh")
            table = "rxjhapp_user"
            datalist = self.model.selectData(table)
            for index,data in enumerate(datalist):
                item = QTableWidgetItem(data[1])
                self.tableWidget.setItem(index, 0, item)
                item = QTableWidgetItem(data[2])
                self.tableWidget.setItem(index, 1, item)
            self.logger.info("查看数据库")
        except Exception as e:
            self.logger.error(e)

    def sendEmail(self):
        """方法为发送邮件"""
        reply = QMessageBox.question(self, '确认', '确认发送吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if (self.lineEdit.text() == ""):
                return False
            self.email = plugins.sendmessage.EmailSina(receivers=[self.lineEdit.text()],price=self.lineEdit_2.text(),sender_mail=self.lineEdit_3.text(),sender_pass=self.lineEdit_4.text())
            try:
                self.email.sendEmail()
            except Exception as e:
                self.logger.error(e)
        else:
            pass

    def __del__(self):
        self.label = True

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '确认退出吗？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logger.info("关闭应用")
            self.logger.removeHandler()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    resultapp = App()
    resultapp.show()
    sys.exit(app.exec_())