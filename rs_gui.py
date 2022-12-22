from __init__ import *

#TODO: text -> encode values -> image (qr code/ bar code/ custom)

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(10, 50, 1980, 1080)
        self.setWindowTitle('UI')
        self.n = 0
        self.k = 0
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        imageLayout = QVBoxLayout()
        labelLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()
        msgLayout = QHBoxLayout() 

        self.fig = plt.figure(figsize=(16,5))
        self.canvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(111)

        toolbar = NavigationToolbar(self.canvas, self)

        self.fig2 = plt.figure(figsize=(16,5))
        self.canvas2 = FigureCanvas(self.fig2)
        self.ax2 = self.fig2.add_subplot(111)

        toolbar2 = NavigationToolbar(self.canvas2, self)

        # labels
        lblOriginal = QLabel("ORIGINAL")
        lblOriginal.setAlignment(Qt.AlignCenter)
        lblCorrupted = QLabel("CORRUPTED")
        lblCorrupted.setAlignment(Qt.AlignCenter)
        lblN = QLabel("N: ")
        lblK = QLabel("K: ")
        lblInput = QLabel("Input Message: ")

        imageLayout.addWidget(toolbar)
        imageLayout.addWidget(lblOriginal)
        imageLayout.addWidget(self.canvas)
        imageLayout.addWidget(toolbar2)
        imageLayout.addWidget(lblCorrupted)
        imageLayout.addWidget(self.canvas2)
        imageLayout.addStretch()

        # input fields
        self.txtInputMsg = QLineEdit()
        self.txtN = QSpinBox()
        self.txtK = QSpinBox()

        msgLayout.addWidget(lblN)
        msgLayout.addWidget(self.txtN)
        msgLayout.addWidget(lblK)
        msgLayout.addWidget(self.txtK)
        msgLayout.addWidget(lblInput)
        msgLayout.addWidget(self.txtInputMsg)

        # buttons
        self.btnGenerate = QPushButton("Generate") 
        self.btnClear = QPushButton("Clear")

        self.btnGenerate.clicked.connect(self.generate)
        self.btnClear.clicked.connect(self.clearFields)

        buttonLayout.addWidget(self.btnGenerate)
        buttonLayout.addWidget(self.btnClear)

        # adding layouts
        mainLayout.addLayout(imageLayout)
        mainLayout.addLayout(labelLayout)
        mainLayout.addLayout(msgLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
    
    def clearFields(self):
        self.txtInputMsg.clear()

        self.txtN.clear()
        self.txtK.clear()

        self.canvas.draw()
        self.ax1.cla()

        self.canvas2.draw()
        self.ax2.cla()

        self.btnGenerate.setDisabled(False)
    
    def generate(self):
        n = self.txtN.value()
        k = self.txtK.value()
        input = self.txtInputMsg.text()

        if (n <= k) or (input == ''):
            msgError = QMessageBox()
            msgError.setIcon(QMessageBox.Critical)
            msgError.setText("Error")

            msgError.setInformativeText('Text fields cannot be empty and n must be greater than k...')
            msgError.setWindowTitle("Error")
            msgError.exec_()
        else:
            self.qr = QR(n, k, input)

            mesecc = np.array(self.qr.mesecc_temp)
            mesecc = np.expand_dims(mesecc, axis=0)

            meseccCorrupt = np.array(self.qr.mesecc_temp_corrupt)
            meseccCorrupt = np.expand_dims(meseccCorrupt, axis=0)

            self.plot(mesecc, meseccCorrupt)
    
    def plot(self, dataA, dataB):
        self.im1 = self.ax1.imshow(dataA, cmap='bwr', interpolation='None')
        self.canvas.draw()

        self.im2 = self.ax2.imshow(dataB, cmap='bwr', interpolation='None')
        self.canvas2.draw()

        self.btnGenerate.setDisabled(True)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("QLabel{font-size: 20px; font-weight: bold} QPushButton{font-size: 20px}")
    win = Window()
    win.show()
    sys.exit(app.exec_())