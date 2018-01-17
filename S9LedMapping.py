import sys,time
from S9LedMapping_ui import *
from picture_qrc import  *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from serial.tools.list_ports import *
import datetime
import serial
import shutil

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        Ui_MainWindow.__init__(self)
        # logo
        self.setWindowIcon(QIcon(":picture/img/110.png"))
        # 默认时间戳
        self.time_stamp = datetime.datetime.now().strftime('%Y-%m-%d')
        # 连接到把数据库
        # function initial
        self.init_watch_table_display()
        #初始化显示大小
        self.init_default_display()
        self.update_uart_port()
        #初始化信号槽
        self.comboBox_ser.currentIndexChanged.connect(self.update_ser_name)
        self.btn_reset.clicked.connect(self.watch_view_table_clear)
        self.btn_ble.clicked.connect(self.on_click_btn_ble)
        self.btn_wifi.clicked.connect(self.on_click_btn_wifi)
        self.btn_powon.clicked.connect(self.on_click_btn_poweron)
        self.btn_kg.clicked.connect(self.on_click_btn_kg)
        self.btn_lb.clicked.connect(self.on_click_btn_lb)
        self.btn_send.clicked.connect(self.on_click_btn_send)
        self.watch_table_view.clicked.connect(self.on_click_watch_table_view)
        self.watch_table_view.pressed.connect(self.watch_table_pressed)
        self.led_rams = []
        for i in range(34):
            self.led_rams.append(0x00)
        print("led_rams: "+str(len(self.led_rams)))
        self.append_ledrams()
    def on_click_btn_send(self):
        self.send_led_rams()

    def send_led_rams(self):
        uart = serial.Serial(port=self.port_name, baudrate=115200,timeout=0.2)
        try:
            checksum = 0xC5^34
            for i in range(34):
                checksum ^= self.led_rams[i]
            send_list = [0xc5,34]+self.led_rams+[checksum]
            uart.flushOutput()
            uart.flushInput()
            uart.write(send_list)
            info =  "Send Hex: " + ' '.join('{:02x}'.format(x) for x in send_list)
            print(str(info))
            back = uart.read(4)
            if back:
                if back[0] == 0xc5:
                    self.plainTextEdit.appendPlainText("发送成功, 有回应。")
            else:
                self.plainTextEdit.appendPlainText("发送成功, 无回应。" )

            uart.close()
        except Exception as e:
            print("send Fail:", str(e))
            QMessageBox.information(self,"提示","发送失败, 请检查串口连线！")

    def update_ser_name(self):
        self.port_name = self.comboBox_ser.currentText()
        self.plainTextEdit.appendPlainText("已选择: "+str(self.port_name))
    def update_uart_port(self):
        list_port = serial.tools.list_ports.comports()
        for name in list_port:
            self.comboBox_ser.addItem(name[0])
        self.comboBox_ser.setCurrentIndex(len(list_port)-1)
        self.port_name = list_port[len(list_port)-1][0]
        print("当前串口: " +self.port_name)
    def init_default_display(self):
        # size
        self.__desktop = QApplication.desktop()
        qRect = self.__desktop.screenGeometry()  # 设备屏幕尺寸
        self.resize(qRect.width() * 50 / 100, qRect.height() * 55 / 100)
        self.move(qRect.width() / 3, qRect.height() / 30)

    def init_watch_table_display(self):

        self.watch_modle = QStandardItemModel(9, 29)
        self.watch_table_view.setModel(self.watch_modle)
        self.watch_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.watch_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


    # self.watch_modle.setItem(i, j, QStandardItem(d))
    def watch_view_table_clear(self):
        self.plainTextEdit.clear()
        self.watch_modle.clear()
        self.init_watch_table_display()
        for i in range(34):
            self.led_rams[i] = 0x00
        self.append_ledrams()

    def on_click_btn_poweron(self):
        self.toggle_btn_color(4,self.btn_powon)
    def on_click_btn_wifi(self):
        self.toggle_btn_color(3, self.btn_wifi)
    def on_click_btn_ble(self):
        self.toggle_btn_color(2, self.btn_ble)
    def on_click_btn_kg(self):
        self.toggle_btn_color(1, self.btn_kg)
    def on_click_btn_lb(self):
        self.toggle_btn_color(0, self.btn_lb)

    def toggle_btn_color(self,index,button):
       print("btn",index)
       if self.led_rams[33] & (0x01 << index):
           self.led_rams[33] = self.led_rams[33]&(0xFE << index)
           self.set_gray_text(button)
       else:
           self.led_rams[33] = self.led_rams[33] | (0x01 << index)
           self.set_red_text(button)
       self.append_ledrams()

    def set_red_text(self, comp):
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.red)
        comp.setPalette(palette)
        self.refresh_app()
        print("red")

    def set_gray_text(self, comp):
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.darkGray)
        comp.setPalette(palette)
        self.refresh_app()
        print("gray")

    def on_click_watch_table_view(self, model_index):
        pass
        # print("add:",model_index.row(),model_index.column())

    def on_click_save_watch_table_view(self):
        pass

    def watch_table_pressed(self,model_index):
        i = model_index.row(); j = model_index.column();
        print("pressed ->"+str(i)+","+str(j)+": ",end=" ")
        print(str(i),str((28-j)% 8))
        try:
           # ram0~ram28
           if i < 8:
               #
               if  self.led_rams[28 - j] & (0x01 << (7 - i)):
                   self.led_rams[28 - j] = self.led_rams[28 - j] & (0xFE << (7 - i))
                   self.setTableBackColor(i,j,False)
               else:
                   self.led_rams[28 - j] = self.led_rams[28 - j] | (0x01 << (7 - i))
                   self.setTableBackColor(i,j,True)
           # ram29~32

           else:
                if self.led_rams[29 + int((28-j)/8)]& (0x01 << (28-j)%8):
                    self.led_rams[29 + int((28 - j) / 8)] = self.led_rams[29 + int((28-j)/8)]&(0xFE << (28-j)%8)
                    self.setTableBackColor(i,j,False)
                else:
                    self.led_rams[29 + int((28 - j) / 8)] = self.led_rams[29 + int((28-j)/8)] | (0x01 << (28-j)%8)
                    self.setTableBackColor(i,j,True)

           # ram33由button按钮决定
           self.append_ledrams()

        except Exception as e:
           print("pressed: "+str(e))

    def append_ledrams(self):
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d')
        info = time_stamp+":"+' '.join('{:02x}'.format(x) for x in self.led_rams)
        print(info)
        self.plainTextEdit.appendPlainText(info)


    def setTableBackColor(self, i,j,bool):
        newItem = QStandardItem();
        if bool:
            newItem.setBackground(QColor('Red'));
        else:
            pass

        self.watch_modle.setItem(i, j, newItem)

    def pushButton_out_excle_hander(self):
        pass


    def refresh_app(self):
        qApp.processEvents()
class Custum_complains(QThread):
      # const
      def  __init__(self):
          super(Custum_complains, self).__init__()
      def run(self):
          pass
          try:
              # 串口工作主流程
              """主循环"""
              while True:
                pass
                time.sleep(0.1)
          except Exception as e:
                print(str(e))

      def mainloop_app(self):
          try:
              pass
              app = QtWidgets.QApplication(sys.argv)
              window = MyApp()
              window.show()
              pass
          except Exception as e:
              print(str(e))
          finally:
              sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        custum = Custum_complains()
        custum.start()
        custum.mainloop_app()
    except Exception as e:
        print(str(e))
    finally:
        pass




