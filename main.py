import sys
import cv2
import os
import numpy as np
import PySide6.QtCore as Qc
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox, QFileDialog, QStatusBar)
from PySide6.QtGui import QAction, QPixmap

import img_effect as IE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("画像処理ソフト")
        self.setGeometry(100, 100, 1600, 820)
        self.setFixedSize(1600, 820)
        self.is_open = False
        self.output = False

        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        wholeLayout = QHBoxLayout()

        wholeLayout.addLayout(self.leftLayout)
        wholeLayout.addLayout(self.rightLayout)
        self.setLayout(wholeLayout)
        
        # ステータスバー
        self.sb_status = QStatusBar()
        self.setStatusBar(self.sb_status)
        self.sb_status.setSizeGripEnabled(False)
        # left_Layout
        self.lb_img1 = QLabel(self)

        self.lb_I_01 = QLabel(self)
        self.lb_I_01.setText('入力画像のディレクトリ')
        self.lb_I_01.setGeometry(50,740,700,25)
        self.lb_I_02 = QLabel(self)
        self.lb_I_02.setText('入力画像サイズ（ 縦 x 横 ）：')
        self.lb_I_02.setGeometry(50,765,500,25)



        # right_Layout
        self.lb_1 = QLabel(self)
        self.lb_1.setText('出力解像度の指定')
        self.lb_1.setGeometry(1300,100,280,30)
        self.lb_2 = QLabel(self)
        self.lb_2.setText('出力X値:')
        self.lb_2.setGeometry(1320,130,50,25)
        self.lb_3 = QLabel(self)
        self.lb_3.setText('出力Y値:')
        self.lb_3.setGeometry(1320,155,50,25)
        self.spin_box_1 = QSpinBox(self)
        self.spin_box_1.setSingleStep(1)
        self.spin_box_1.setRange(1,1920)
        self.spin_box_1.setGeometry(1375,130,100,25)
        self.spin_box_2 = QSpinBox(self)
        self.spin_box_2.setSingleStep(1)
        self.spin_box_2.setRange(1,1080)
        self.spin_box_2.setGeometry(1375,155,100,25)

        self.lb_4 = QLabel(self)
        self.lb_4.setText('ドット絵変換に関する設定')
        self.lb_4.setGeometry(1300,180,280,30)
        self.lb_4.setVisible(False)
        self.lb_5 = QLabel(self)
        self.lb_5.setText('Alpha:')
        self.lb_5.setGeometry(1320,210,50,25)
        self.lb_5.setVisible(False)
        self.lb_6 = QLabel(self)
        self.lb_6.setText('色の数:')
        self.lb_6.setGeometry(1320,235,50,25)
        self.lb_6.setVisible(False)
        self.combobox_1 = QComboBox(self)
        self.combobox_1.setGeometry(1375,210,100,25)
        self.combobox_1.setEditable(False)
        for i in range(0, 11 ,1):
            num = str(i/10)
            self.combobox_1.addItem(num)
        self.combobox_1.setVisible(False)
        self.spin_box_4 = QSpinBox(self)
        self.spin_box_4.setSingleStep(1)
        self.spin_box_4.setRange(2,256)
        self.spin_box_4.setGeometry(1375,235,100,25)
        self.spin_box_4.setVisible(False)

        self.Play_button = QPushButton('実行',self)
        self.Play_button.setGeometry(1300,600,280,30)
        self.Play_button.clicked.connect(self.Play_button_clicked)
        self.Save_button = QPushButton('保存',self)
        self.Save_button.setGeometry(1300,650,280,30)
        self.spin_box_4.setVisible(False)
        self.Save_button.clicked.connect(self.Save_button_clicked)

        self.leftLayout.addWidget(self.lb_img1)


        self.SetCombobox()
        self.create_menu()
        


    # 一番上に表示されるメニューの処理
    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("開く", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        exit_action = QAction("終了",self)
        exit_action.triggered.connect(self.exit_app)
        file_menu.addAction(exit_action)

    # ”開く“を選択されたときの処理
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Images (*.jpg *.png *.gif)")
        self.open_file_name = file_name
        self.is_open = True
        self.sb_status.showMessage(f'画像入力')
        self.lb_I_01.setText(f'入力画像のディレクトリ{file_name}')
        img_width, img_hight = IE.get_img_size(file_name)
        self.lb_I_02.setText(f'入力画像サイズ（ 縦 x 横 ）：{img_width} x {img_hight}')
        self.pre_show_image(file_name)

    # 読み込み画像の表示
    def pre_show_image(self, file_name):
        # PySideの機能で画像の読込みとリサイズ
        width, height = 1280, 720
        pm1 = QPixmap(file_name)
        pm1 = pm1.scaled( width, height, Qc.Qt.AspectRatioMode.KeepAspectRatio)

        # QLabelに「画像」をセット
        self.lb_img1.setPixmap(pm1)
        self.lb_img1.setGeometry(15,20,width,height)



    # 右のメニューの処理
    def SetCombobox(self):
        self.combobox = QComboBox(self)
        self.rightLayout.addWidget(self.combobox)
        self.combobox.setGeometry(1300,50,280,30)
        self.combobox.setEditable(False)
        # 選択内容の追加：追加順にIDが0から割り振られる
        self.combobox.addItem("選択してください")           # ID: 0
        self.combobox.addItem("ドット絵加工")               # ID: 1
        # self.combobox.addItem("モザイク処理")               # ID: 2
        # self.combobox.addItem("グレースケール処理")         # ID: 3
        # コンボボックスの選択中のIDが変更されたら呼び出す処理
        self.combobox.currentIndexChanged.connect(self.CallbackCurrentindexchangedCombobox)

    # コンボボックスの選択後の処理
    def CallbackCurrentindexchangedCombobox(self):
        select_num = self.combobox.currentIndex()       # SelectされているIDの取得
        if self.is_open == False :
            QMessageBox.information(self,"編集内容のインフォメーション","画像を選択してください\n'ファイル>開く'より選択してください")
        if select_num == 0:                             # ID=0 の時、インフォメーション表示
            QMessageBox.information(self,"編集内容選択のインフォメーション","編集内容を選択してください")
        elif select_num == 1:                           # ID=1 の時、ドット処理用のグループUI表示の関数を実行
            self.Set_dot_input()
            print(1)
        elif select_num == 2:                           # ID=2 の時、モザイク処理用のグループUI表示の関数を実行
            #----モザイク処理用グループUI表示関数----
            print(2)
            #----------
        elif select_num == 3:                           # ID=3 の時、グレースケール処理用のグループUI表示の関数を実行   
            #----グレースケール処理用グループUI表示関数----
            print(3)
            #----------

    def Set_dot_input(self):
        self.sb_status.showMessage(f'ドット絵出力モードの選択')
        self.lb_4.setVisible(True)
        self.lb_5.setVisible(True)
        self.lb_6.setVisible(True)
        self.combobox_1.setVisible(True)
        self.spin_box_4.setVisible(True)
    

    def Play_button_clicked(self):
        self.sb_status.showMessage(f'変換処理実行')
        img = cv2.imread(self.open_file_name)
        width = self.spin_box_1.value()
        height = self.spin_box_2.value()
        alpha = int(self.combobox_1.currentIndex()) / 10
        K_num = self.spin_box_4.value()
        print(f'img:{img},W x H:{width}x{height}, Alpha:{alpha}, K:{K_num}')

        self.output_img = IE.pixel_art(img,alpha,K_num)
        cv2.imshow("ouput", self.output_img)
        

    def Save_button_clicked(self):
        title = '出力画像(画像ファイル)の保存'
        default_path = os.path.expanduser('~/Picture/output.png')
        filter = "Image Files (*.png)"
        path,_ = QFileDialog.getSaveFileName(
            self,
            title,
            default_path,
            filter
        )
        print(f'path -> {path}')

        if path[10] == '':
            return
        else :
            self.save_image(path,self.output_img)
        
    def save_image(self,path,img):
        fn = path
        cv2.imwrite(fn,img)
        self.sb_status.showMessage(f'画像出力完了｜出力画像パス {fn}')



    # 終了を選択されたときの処理
    def exit_app(self):
        self.close()










def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()