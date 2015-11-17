# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from bs4 import BeautifulSoup
import urllib2
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(450, 250)
        Dialog.setSizeGripEnabled(True)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 20, 500, 281))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 5, 300, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.widget)
        self.plainTextEdit.setGeometry(QtCore.QRect(90, 5, 261, 80))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(170, 150, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        # 保存路径标签
        self.browseLabel = QtGui.QLabel(self.widget)
        self.browseLabel.setGeometry(QtCore.QRect(10, 100, 300, 20))
        self.browseLabel.setObjectName(_fromUtf8("label"))

        # 路径显示输入框
        self.directoryComboBox = QtGui.QComboBox(self.widget)
        self.directoryComboBox.setEditable(True)
        self.directoryComboBox.setGeometry(QtCore.QRect(90, 100, 260, 20))
        self.directoryComboBox.addItem(QtCore.QDir.currentPath())
        self.directoryComboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Preferred)
        self.directoryComboBox.setObjectName(_fromUtf8("comboBox"))

        # 浏览文件按钮
        self.browseButton = QtGui.QPushButton(self.widget)
        self.browseButton.setGeometry(QtCore.QRect(355, 100, 80, 23))
        self.browseButton.setObjectName(_fromUtf8("pushButton"))
        self.browseButton.clicked.connect(self.browse)

        # 事件
        self.pushButton.clicked.connect(self.test)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "91助手游戏资料获取工具", None))
        self.label.setText(_translate("Dialog", '下载地址：', None))
        self.pushButton.setText(_translate("Dialog", "确定", None))
        self.browseLabel.setText(_translate("Dialog", "保存路径：", None))
        self.browseButton.setText(_translate("Dialog", "浏览", None))

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Find Files",
                                                           QtCore.QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))

    def test(self):
        url = self.plainTextEdit.toPlainText()
        # print unicode(QtCore.QString(url))
        self.parseUrl(post_url=url)

    def parseUrl(self, post_url):
        url = unicode(QtCore.QString(post_url))
        save_path = unicode(QtCore.QString(self.directoryComboBox.currentText()))
        response = urllib2.urlopen(url.encode('utf-8'))
        html = BeautifulSoup(response.read())
        game_logo = html.findAll(attrs={"class": "s-intro-img"})[0].get('src')
        game_name = html.select('.s-h1')[0].get_text()
        game_about1 = html.select('.offcanvas p')
        game_about2 = html.select('.offcanvas .o-content')
        game_about3 = html.select('.offcanvas span')
        game_scroll = html.select('.screen-scroll img')
        game_other = html.select('.o-tip')


        # 解决元素多样性问题
        game_about = ''  # 游戏简介
        if len(game_about1) > 0:  # 有p标签的
            for val in game_about1:
                game_about += val.get_text()
        elif len(game_about2) > 0:  # 直接在o-content标签内
            game_about = game_about2[0].get_text()
        elif len(game_about3) > 0:
            game_about = game_about3[0].get_text()

        # 创建游戏名称目录
        if os.path.exists(save_path + '/' + game_name) == False:
            os.mkdir(save_path + '/' + game_name, 777)

        # 游戏简介
        game_about_file_name = "游戏简介.txt"
        file_obj = open(save_path + '/' + game_name + '/' + game_about_file_name.decode('utf-8'), 'wb')
        file_obj.write(bytes(game_about.strip().encode('utf-8')))
        file_obj.close()

        # 游戏logo
        f = urllib2.urlopen(game_logo.encode('utf-8'))
        with open(save_path + '/' + game_name + '/' + "logo.png", "wb") as code:
            code.write(f.read())

        # 游戏截图
        for img_url in game_scroll:
            img_down_url = img_url.get('src')
            img_name = os.path.basename(img_down_url)
            f = urllib2.urlopen(img_down_url.encode('utf-8'))
            code = open(save_path + '/' + game_name + '/' + img_name, "wb")
            code.write(f.read())

        # 其他信息
        game_other_file_name = "其他信息.txt"
        file_obj = open(save_path + '/' + game_name + '/' + game_other_file_name.decode('utf-8'), 'wb')
        file_obj.write(
            bytes(game_other[0].get_text().replace('\t', '').replace('\n', '').replace(' ', '').encode('utf-8')))
        file_obj.close()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Window()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())






