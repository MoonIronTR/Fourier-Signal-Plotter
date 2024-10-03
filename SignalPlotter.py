import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QSplitter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ComponentWindow(QMainWindow):
    def __init__(self, t, y1_cos, y2_cos, y3_cos):
        super().__init__()
        self.setWindowTitle('Component Signals')
        self.setGeometry(800, 100, 1024, 768)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        
        self.plot_components(t, y1_cos, y2_cos, y3_cos)

    def plot_components(self, t, y1_cos, y2_cos, y3_cos):
        self.figure.clear()

        # Sinyal bileşenlerini çizme
        ax1 = self.figure.add_subplot(311)
        ax1.plot(t, y1_cos, label='Cosine Component 1')
        ax1.legend()
        ax1.set_title('Cosine Component 1')

        ax2 = self.figure.add_subplot(312)
        ax2.plot(t, y2_cos, label='Cosine Component 2')
        ax2.legend()
        ax2.set_title('Cosine Component 2')

        ax3 = self.figure.add_subplot(313)
        ax3.plot(t, y3_cos, label='Cosine Component 3')
        ax3.legend()
        ax3.set_title('Cosine Component 3')

        self.canvas.draw()

class SignalPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signal Plotter')
        self.setGeometry(100, 100, 1024, 768)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        
        mainLayout = QVBoxLayout(widget)
        
        # Splitter kullanarak ağırlıkları ayarlamak
        splitter = QSplitter(Qt.Vertical)
        
        # Üst panel (Form alanları)
        formWidget = QWidget()
        formLayout = QVBoxLayout(formWidget)
        
        formSubLayout = QHBoxLayout()
        
        # Sol panel (Genlik, Frekans ve Faz bilgileri)
        leftForm = QFormLayout()
        self.A1 = QLineEdit(self)
        self.f1 = QLineEdit(self)
        self.theta1 = QLineEdit(self)
        self.A2 = QLineEdit(self)
        self.f2 = QLineEdit(self)
        self.theta2 = QLineEdit(self)
        self.A3 = QLineEdit(self)
        self.f3 = QLineEdit(self)
        self.theta3 = QLineEdit(self)
        leftForm.addRow('A1:', self.A1)
        leftForm.addRow('f1:', self.f1)
        leftForm.addRow('θ1:', self.theta1)
        leftForm.addRow('A2:', self.A2)
        leftForm.addRow('f2:', self.f2)
        leftForm.addRow('θ2:', self.theta2)
        leftForm.addRow('A3:', self.A3)
        leftForm.addRow('f3:', self.f3)
        leftForm.addRow('θ3:', self.theta3)
        
        formSubLayout.addLayout(leftForm)
        
        formLayout.addLayout(formSubLayout)
        
        self.plotButton = QPushButton('Plot Signals', self)
        formLayout.addWidget(self.plotButton)
        self.plotButton.clicked.connect(self.plot_signals)
        
        splitter.addWidget(formWidget)
        
        # Alt panel (Grafik alanı)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        splitter.addWidget(self.canvas)
        
        # Splitter ağırlıklarını ayarlama
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        
        mainLayout.addWidget(splitter)
        
        self.setLayout(mainLayout)
    
    def plot_signals(self):

        # Kullanıcıdan alınan değerler
        # Tetalar otomatik olarak pi ile çarpıldı
        A1 = float(self.A1.text())
        f1 = float(self.f1.text())
        theta1 = float(self.theta1.text()) * np.pi
        A2 = float(self.A2.text())
        f2 = float(self.f2.text())
        theta2 = float(self.theta2.text()) * np.pi
        A3 = float(self.A3.text())
        f3 = float(self.f3.text())
        theta3 = float(self.theta3.text()) * np.pi
        
        # Zaman aralığı
        t = np.linspace(0, 2*np.pi, 1000)
        
        # Kosinüs sinyalleri
        y1_cos = A1 * np.cos(2 * np.pi * f1 * t + theta1)
        y2_cos = A2 * np.cos(2 * np.pi * f2 * t + theta2)
        y3_cos = A3 * np.cos(2 * np.pi * f3 * t + theta3)
        
        # Sentezlenen toplam sinyal
        y_total = y1_cos + y2_cos + y3_cos
        
        # Grafiklerin çizilmesi
        self.figure.clear()
        
        ax_total = self.figure.add_subplot(111)
        ax_total.plot(t, y_total, label='Synthesized Signal')
        ax_total.legend()
        ax_total.set_title('Synthesized Signal')
        
        self.canvas.draw()

        # İkinci pencereyi oluştur ve göster
        self.componentWindow = ComponentWindow(t, y1_cos, y2_cos, y3_cos)
        self.componentWindow.show()

class HarmoniksWindow(QMainWindow):
    def __init__(self, y1, y2, y3, y_total, t):
        super().__init__()
        self.setWindowTitle('1st ,2nd ,3rd Harmonics Signals')
        self.setGeometry(800, 100, 1024, 768)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        
        self.plot_harmonics(y1, y2, y3, y_total, t)

    def plot_harmonics(self, y1, y2, y3, y_total, t):
        self.figure.clear()
        
        ax1 = self.figure.add_subplot(311)
        ax1.plot(t, y1, label='1. Harmonic')
        ax1.legend()
        ax1.set_title('1. Harmonic')
        
        ax2 = self.figure.add_subplot(312)
        ax2.plot(t, y2, label='2. Harmonic')
        ax2.legend()
        ax2.set_title('2. Harmonic')
        
        ax3 = self.figure.add_subplot(313)
        ax3.plot(t, y3, label='3. Harmonic')
        ax3.legend()
        ax3.set_title('3. Harmonic')
        
        self.canvas.draw()

class FourierSeriesAnalysis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Fourier Series Analysis')
        self.setGeometry(100, 100, 1024, 768)
        
        widget = QWidget()
        self.setCentralWidget(widget)
        
        mainLayout = QVBoxLayout(widget)
        
        # Splitter kullanarak ağırlıkları ayarlamak
        splitter = QSplitter(Qt.Vertical)
        
        # Üst panel (Form alanları)
        formWidget = QWidget()
        formLayout = QVBoxLayout(formWidget)
        
        formSubLayout = QHBoxLayout()
        
        # Sol panel (a katsayıları)
        leftForm = QFormLayout()
        self.a0 = QLineEdit(self)
        self.ak1 = QLineEdit(self)
        self.ak2 = QLineEdit(self)
        self.ak3 = QLineEdit(self)
        leftForm.addRow('a0:', self.a0)
        leftForm.addRow('a1:', self.ak1)
        leftForm.addRow('a2:', self.ak2)
        leftForm.addRow('a3:', self.ak3)
        
        # Sağ panel (b katsayıları ve diğer parametreler)
        rightForm = QFormLayout()
        self.bk1 = QLineEdit(self)
        self.bk2 = QLineEdit(self)
        self.bk3 = QLineEdit(self)
        self.w0 = QLineEdit(self)
        rightForm.addRow('b1:', self.bk1)
        rightForm.addRow('b2:', self.bk2)
        rightForm.addRow('b3:', self.bk3)
        rightForm.addRow('w0:', self.w0)
        
        formSubLayout.addLayout(leftForm)
        formSubLayout.addLayout(rightForm)
        
        formLayout.addLayout(formSubLayout)
        
        self.plotButton = QPushButton('Plot Signals', self)
        formLayout.addWidget(self.plotButton)
        self.plotButton.clicked.connect(self.plot_signals)
        
        splitter.addWidget(formWidget)
        
        # Alt panel (Grafik alanı)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        splitter.addWidget(self.canvas)
        
        # Splitter ağırlıklarını ayarlama
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        
        mainLayout.addWidget(splitter)
        
        self.setLayout(mainLayout)
    
    def plot_signals(self):
        """
        # Kullanıcıdan alınan değerler
        # w0 otomatik olarak pi ile çarpıldı
        a0 = float(self.a0.text())
        ak1 = float(self.ak1.text())
        bk1 = float(self.bk1.text())
        ak2 = float(self.ak2.text())
        bk2 = float(self.bk2.text())
        ak3 = float(self.ak3.text())
        bk3 = float(self.bk3.text())
        w0 = float(self.w0.text()) * np.pi
        

        """

        # 3.soru için
        try:
            a0 = eval(self.a0.text().replace('^', '**').replace('pi', 'np.pi'))
            ak1 = eval(self.ak1.text().replace('^', '**').replace('pi', 'np.pi'))
            bk1 = eval(self.bk1.text().replace('^', '**').replace('pi', 'np.pi'))
            ak2 = eval(self.ak2.text().replace('^', '**').replace('pi', 'np.pi'))
            bk2 = eval(self.bk2.text().replace('^', '**').replace('pi', 'np.pi'))
            ak3 = eval(self.ak3.text().replace('^', '**').replace('pi', 'np.pi'))
            bk3 = eval(self.bk3.text().replace('^', '**').replace('pi', 'np.pi'))
            w0 = eval(self.w0.text().replace('^', '**').replace('pi', 'np.pi')) * np.pi
        except:
            print("Invalid input")
            return

        # Zaman aralığı
        T = 2 * np.pi / w0  # w0 = 2 * pi / T, so T = 2 * pi / w0
        t = np.linspace(-1.5 * T, 1.5 * T, 2000)
        
        # Fourier Serileri ile hesaplanan sinyaller
        y1 = ak1 * np.cos(w0 * t) + bk1 * np.sin(w0 * t)
        y2 = ak2 * np.cos(2 * w0 * t) + bk2 * np.sin(2 * w0 * t)
        y3 = ak3 * np.cos(3 * w0 * t) + bk3 * np.sin(3 * w0 * t)
        
        # Sentezlenen toplam sinyal
        y_total = a0 + y1 + y2 + y3
        
        # Alt paneldeki birleşik grafiği çizme
        self.figure.clear()
        
        ax_combined = self.figure.add_subplot(111)
        ax_combined.plot(t, y_total, label='Synthesized Signal')
        ax_combined.legend()
        ax_combined.set_title('Synthesized Signal')
        
        self.canvas.draw()

        # İkinci pencereyi oluştur ve göster
        self.harmonicsWindow = HarmoniksWindow(y1, y2, y3, y_total, t)
        self.harmonicsWindow.show()

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Signals and Systems Project')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.label = QLabel("Choose the operation you want to perform:", self)
        self.label.setFont(QFont('Arial', 24))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(50, 150, 700, 50)  # QLabel'in boyutunu manuel olarak ayarladık
        self.label.setParent(centralWidget)

        self.plotButton = QPushButton("Cosine Signals Plotting", self)
        self.plotButton.setGeometry(250, 250, 300, 50)
        self.plotButton.clicked.connect(self.startPlotting)
        self.plotButton.setParent(centralWidget)

        self.analysisButton = QPushButton("Fourier Series Analysis in Sine-Cosine Form", self)
        self.analysisButton.setGeometry(250, 320, 300, 50)
        self.analysisButton.clicked.connect(self.startAnalysis)
        self.analysisButton.setParent(centralWidget)

    def startPlotting(self):
        print("Starting Cosine Signals Plotting")
        self.signalPlotter = SignalPlotter()
        self.signalPlotter.show()

    def startAnalysis(self):
        print("Starting Fourier Series Analysis in Sine-Cosine Form ")
        self.fourierAnalysis = FourierSeriesAnalysis()
        self.fourierAnalysis.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.show()
    sys.exit(app.exec_())
