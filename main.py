import pyqtgraph as pg
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import (QApplication)
from PyQt5 import QtGui
import requests
import threading
from bs4 import BeautifulSoup

import pyqtgraph as pg
import requests

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)
        self.setFixedSize(1160, 666)  
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        MainWindow.setWindowTitle(self, "   TrackingСourses")
        self.show()
        
        self.BASE_CURRENCY = 'USD'
        self.DEFAULT_CURRENCY = ['RUB']

        self.AVAILABLE_BASE_CURRENCIES = [
            'USD','EUR','GBP','JPY','CHF'
            ,'CAD','AUD','RUB', 'AED', 'CZK'
            , 'CNY', 'PHP', 'SEK', 'MXN', 
            'BYN', 'PLN', 'HKD', 'NOK', 'KRW'
            , 'TRY', 'INR', 'BRL', 'ZAR'
            ]

        self.COLORS = [
            'Red', 'Blue', 'Green', 'Pink'
            , 'Brown', 'Orange', "Yellow",
            'Gray', 'Purple', 'Black', 'Lime',
            'MediumSlateBlue', 'Maroon', 'Olive',
            'Navy', 'Fuchsia', 'DarkSlateGray',
            'Aqua', 'Teal', 'Chocolate', 'Silver',
            'DeepSkyBlue', 'DarkMagenta'
            ]
        
        self.main_currency.currentIndexChanged.connect(self.CheckboxEnabled)
        self.main_currency.currentIndexChanged.connect(self.crypto_upd)
        
        self.graphWidget = pg.PlotWidget()
        
        self.widget.showGrid(y=True)
        self.widget.setBackground('white')
        self.x = 8
        self.y = [9999, -1]
        
        t = threading.Thread(target=self.plot, args=[self.x])
        t.start()

        t1 = threading.Thread(target=self.crypto, args=[self.BASE_CURRENCY])
        t1.start()
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.crypto_upd)
        self.timer.timeout.connect(self.plot_upd)
        self.timer.start()
        
        for i in self.rate_btns.buttons():
            i.stateChanged.connect(self.CheckboxWork)
            i.stateChanged.connect(self.plot_upd)

    def plot(self, x):
        X = [i for i in range(x-8, x)]
        for i in range(len(self.DEFAULT_CURRENCY)):
            Y = []
            for _ in range(x-8, x):
                temp = self.rate(self.BASE_CURRENCY, self.DEFAULT_CURRENCY[i])
                Y.append(temp)
            pen = pg.mkPen(color=self.COLORS[i], width=2) 
            if min(Y) < self.y[0]:
                self.y[0] = min(Y)
            if max(Y) < self.y[1]:
                self.y[1] = max(Y)
            self.widget.plot(X, Y, name=f"RATE{i}", pen=pen)
            self.x += 1
  
    
    def plot_upd(self):
        self.graphWidget.setXRange(self.x - 1, self.x, padding=0)
        self.graphWidget.setYRange(self.y[0], self.y[1], padding=0)
        self.widget.clear()
        self.plot(self.x)
    
    def rate(self, base, default):
        if base == default:
            return 1
        else:
            url = f"https://ru.investing.com/currencies/{base.lower()}-{default.lower()}"
            full_page = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert = float(soup.find("span", {"class": "text-2xl", "data-test": "instrument-price-last"}).text.replace(".", "").replace(",", "."))
        
            return convert
    
    def crypto(self, base):
        url = f"https://cryptocharts.ru/{base}/"
        full_page = requests.get(url)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        BTC = soup.find("span", {"id": "PRICE_BTC"}).text
        ETH = soup.find("span", {"id": "PRICE_ETH"}).text
        LTC = soup.find("span", {"id": "PRICE_LTC"}).text
        
        self.BTC.setText(BTC)
        self.ETH.setText(ETH)
        self.LTC.setText(LTC)
    
    def crypto_upd(self):
        self.crypto(self.BASE_CURRENCY)
        print([self.BTC.text(), self.ETH.text(), self.LTC.text()])

    def CheckboxEnabled(self):
        self.BASE_CURRENCY = str(self.main_currency.currentText())
        if str(self.main_currency.currentText()) == "AED":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "CZK":
            self.USD.setEnabled(False)
            self.EUR.setEnabled(False)
            self.GBP.setEnabled(False)
            self.CHF.setEnabled(False)
            self.CAD.setEnabled(False)
            self.AUD.setEnabled(False)
            self.AED.setEnabled(False)
            self.CNY.setEnabled(False)
            self.MXN.setEnabled(False)
            self.BYN.setEnabled(False)
            self.HKD.setEnabled(False)
            self.NOK.setEnabled(False)
            self.KRW.setEnabled(False)
            self.TRY.setEnabled(False)
            self.INR.setEnabled(False)
            self.BRL.setEnabled(False)
            self.ZAR.setEnabled(False)
        elif str(self.main_currency.currentText()) == "PHP":
            self.EUR.setEnabled(False)
            self.GBP.setEnabled(False)
            self.CHF.setEnabled(False)
            self.CAD.setEnabled(False)
            self.AUD.setEnabled(False)
            self.AED.setEnabled(False)
            self.BYN.setEnabled(False)
            self.PLN.setEnabled(False)
            self.BRL.setEnabled(False)
        elif str(self.main_currency.currentText()) == "SEK":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "MXN":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "BYN":
            self.GBP.setEnabled(False)
            self.JPY.setEnabled(False)
            self.CHF.setEnabled(False)
            self.CAD.setEnabled(False)
            self.AUD.setEnabled(False)
            self.AED.setEnabled(False)
            self.CZK.setEnabled(False)
            self.CNY.setEnabled(False)
            self.PHP.setEnabled(False)
            self.SEK.setEnabled(False)
            self.MXN.setEnabled(False)
            self.PLN.setEnabled(False)
            self.HKD.setEnabled(False)
            self.NOK.setEnabled(False)
            self.KRW.setEnabled(False)
            self.TRY.setEnabled(False)
            self.INR.setEnabled(False)
            self.BRL.setEnabled(False)
            self.ZAR.setEnabled(False)
        elif str(self.main_currency.currentText()) == "PLN":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "HKD":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "NOK":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "KRW":
            self.RUB.setEnabled(False)
            self.AED.setEnabled(False)
            self.CZK.setEnabled(False)
            self.PHP.setEnabled(False)
            self.SEK.setEnabled(False)
            self.MXN.setEnabled(False)
            self.BYN.setEnabled(False)
            self.PLN.setEnabled(False)
            self.NOK.setEnabled(False)
            self.TRY.setEnabled(False)
            self.BRL.setEnabled(False)
        elif str(self.main_currency.currentText()) == "TRY":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "INR":
            self.CHF.setEnabled(False)
            self.CAD.setEnabled(False)
            self.AUD.setEnabled(False)
            self.AED.setEnabled(False)
            self.BYN.setEnabled(False)
            self.PLN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "BRL":
            self.BYN.setEnabled(False)
        elif str(self.main_currency.currentText()) == "ZAR":
            self.BYN.setEnabled(False)
        else:
            self.USD.setEnabled(True)
            self.EUR.setEnabled(True)
            self.GBP.setEnabled(True)
            self.JPY.setEnabled(True)
            self.CHF.setEnabled(True)
            self.CAD.setEnabled(True)
            self.AUD.setEnabled(True)
            self.RUB.setEnabled(True)
            self.AED.setEnabled(True)
            self.CZK.setEnabled(True)
            self.CNY.setEnabled(True)
            self.PHP.setEnabled(True)
            self.SEK.setEnabled(True)
            self.MXN.setEnabled(True)
            self.BYN.setEnabled(True)
            self.PLN.setEnabled(True)
            self.HKD.setEnabled(True)
            self.NOK.setEnabled(True)
            self.KRW.setEnabled(True)
            self.TRY.setEnabled(True)
            self.INR.setEnabled(True)
            self.BRL.setEnabled(True)
            self.ZAR.setEnabled(True)

    def CheckboxWork(self):
        checkbox_btn = QApplication.instance().sender()
        
        if checkbox_btn.isChecked():
            if checkbox_btn.objectName() not in self.DEFAULT_CURRENCY:
                self.DEFAULT_CURRENCY.append(checkbox_btn.objectName())
                print(self.DEFAULT_CURRENCY)
        else:
            if checkbox_btn.objectName() in self.DEFAULT_CURRENCY:
                self.DEFAULT_CURRENCY.remove(checkbox_btn.objectName())
                print(self.DEFAULT_CURRENCY)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
