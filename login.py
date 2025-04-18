from PyQt6.QtWidgets import *
import pymysql
from data.database import Database
from ui.login_ui import *
from data.config import *
from mainw import MainW
import sys

class AuthorizationWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.enter)


    def enter(self):
        login = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text()
        if login and password:
            try:
                role_id = self.db.checkUser(login, password)
                if role_id:
                    if role_id == 2:

                        # main_win = MainApp(self.db, self.link, self)
                        # main_win.show()
                        # self.setVisible(False)
                        QMessageBox.information(self, 'Внимание', 'Успешный вход администратора')
                    else:
                        QMessageBox.information(self, 'Внимание', f'Добро пожаловать!')
                        main_user_win = MainW(self.db)
                        main_user_win.show()

                else:
                    QMessageBox.warning(self, 'Внимание', 'Проверьте введенные данные')
            except:
                print("Er")
        else:
            QMessageBox.warning(self, 'Внимание', 'Введите логин и пароль')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthorizationWindow(Database(host, user, password, database))
    window.show()
    sys.exit(app.exec())