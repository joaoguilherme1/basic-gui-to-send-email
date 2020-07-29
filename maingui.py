import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import credential as cr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(object):

    def __init__(self):
        super().__init__()
        self.list_of_files= []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(611, 380)
        MainWindow.setStyleSheet("background-color: rgb(2, 179, 255);\n"
"background-color: rgb(0, 144, 188);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.botaoenviar1 = QtWidgets.QPushButton(self.centralwidget)
        self.botaoenviar1.setGeometry(QtCore.QRect(510, 250, 81, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.botaoenviar1.setFont(font)
        self.botaoenviar1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 11pt \"Arial\";")
        self.botaoenviar1.setObjectName("botaoenviar1")
        self.Contador = QtWidgets.QLCDNumber(self.centralwidget)
        self.Contador.setGeometry(QtCore.QRect(280, 210, 64, 23))
        self.Contador.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.Contador.setObjectName("Contador")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 240, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 280, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 320, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.remetente = QtWidgets.QLineEdit(self.centralwidget)
        self.remetente.setGeometry(QtCore.QRect(180, 240, 311, 31))
        self.remetente.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.remetente.setObjectName("remetente")

        self.titulo = QtWidgets.QLineEdit(self.centralwidget)
        self.titulo.setGeometry(QtCore.QRect(180, 280, 311, 31))
        self.titulo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.titulo.setObjectName("titulo")

        self.corpotexto = QtWidgets.QLineEdit(self.centralwidget)
        self.corpotexto.setGeometry(QtCore.QRect(180, 320, 311, 31))
        self.corpotexto.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.corpotexto.setObjectName("corpotexto")

        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(20, 10, 581, 192))
        self.treeView.setObjectName("treeView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.populate()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.treeView.customContextMenuRequested.connect(self.counter)
        self.botaoenviar1.clicked.connect(self.send_email)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.botaoenviar1.setText(_translate("MainWindow", "Enviar"))
        self.label.setText(_translate("MainWindow", "Remetente:"))
        self.label_2.setText(_translate("MainWindow", "Titulo do Email:"))
        self.label_3.setText(_translate("MainWindow", "Texto do Email:"))
        self.remetente.setPlaceholderText(_translate("MainWindow", "Para quem deseja mandar este email ?"))
        self.titulo.setPlaceholderText(_translate("MainWindow", "Qual é o título do email ?"))
        self.corpotexto.setPlaceholderText(_translate("MainWindow", "Escreva algo para enviar junto do email:"))

    def counter(self):
        self.Contador.display(len(self.list_of_files))

    def populate(self):
        #PUT YOUR PATH INSIDE THE MARKERS
        path = "SELECT YOUR PATH"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath("SELECT YOUR PATH")
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        add_to_list = menu.addAction("Mover para Lista")
        add_to_list.triggered.connect(self.list_of_files)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def list(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        self.list_of_files.append(file_path)

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = cr.email
        msg['To'] = self.remetente.text()
        msg['Subject'] = self.titulo.text()

        arroz = QMessageBox()
        arroz.setWindowTitle("Atualização")

        msg.attach(MIMEText(self.corpotexto.text()))

        if self.list_of_files == []:
            arroz.setText("Add something fisrt")

        else:
            for f in self.list_of_files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)


            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(cr.email, cr.password)
                    smtp.send_message(msg)
                    arroz.setText("O Email foi enviado com sucesso!")
                    arroz.exec_()
            except:
                arroz.setText("O email não foi enviado. Verifique se existe algum erro de digitação")
                arroz.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())