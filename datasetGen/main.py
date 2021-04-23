from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

from utils.VerifyCode import VeifyCode
class Window:
    def __init__(self):
        self.ui = uic.loadUi("main.ui")
        self.firstStart = True
        # 信号处理
        self.ui.edt_input.returnPressed.connect(self.returnPressed)

        self.img_components = [self.ui.lbl_pic_code_1, self.ui.lbl_pic_code_2,
                          self.ui.lbl_pic_code_3, self.ui.lbl_pic_code_4]
        self.text_components = [self.ui.lbl_code_1, self.ui.lbl_code_2, self.ui.lbl_code_3, self.ui.lbl_code_4]
        self.ui.lbl_dataset_size.setText(VeifyCode.getDatasetSize().__str__())
        self.next()

    def next(self):
        self.getAndSetPic()
        filename = VeifyCode.divide("tmp/img.jpg")
        while filename is None:
            self.getAndSetPic()
            filename = VeifyCode.divide("tmp/img.jpg")
        for idx, fn in enumerate(filename):
            img = QPixmap(fn)
            self.img_components[idx].setPixmap(img)


    def returnPressed(self):
        '''
        按下回车键处理
        :return:
        '''



        text = self.ui.edt_input.text()
        if len(text) != 4:
            return
        for idx,char in enumerate(text):
            self.text_components[idx].setText(char)
        # save file
        VeifyCode.save(text)
        self.next()
        self.ui.edt_input.setText("")
        self.ui.lbl_dataset_size.setText(VeifyCode.getDatasetSize().__str__())



    def getAndSetPic(self):
        filename = VeifyCode.getVerifyCode()
        img_code = QPixmap(filename)
        self.ui.lbl_verify_code.setPixmap(img_code)


'''
    程序需要连接学校内网才可以使用
    文件存进训练数据集中
'''
app = QApplication([])
window = Window()
window.ui.show()
app.exec_()
