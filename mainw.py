from PyQt6.QtWidgets import *
import pymysql
from data.database import Database
from ui.main_ui import *
from data.config import *
import sys

class MainW(QWidget):
    def __init__(self, db, parrent=None):
        super().__init__()
        self.db = db
        self.parrent = parrent
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.populate_comboBox()
        self.ui.comboBox.currentTextChanged.connect(self.print_table)
        self.ui.tableWidget.cellChanged.connect(self.updateData)

    def populate_comboBox(self):
        tables = self.db.getTables()
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(tables)

    def print_table(self, tb_name):
        self.ui.tableWidget.blockSignals(True)
        self.ui.tableWidget.clear()
        labels, data = self.db.getDataFromTable(tb_name)
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(data[0]))
        self.ui.tableWidget.setHorizontalHeaderLabels(labels)
        for row_in, ss in enumerate(data):
            for col_in, item in enumerate(ss):
                self.ui.tableWidget.setItem(row_in, col_in, QTableWidgetItem(item))

        self.ui.tableWidget.setColumnHidden(0, True)
        self.ui.tableWidget.blockSignals(False)

    def updateData(self, row, column):
        new_data = self.ui.tableWidget.item(row, column).text()
        data_column = self.ui.tableWidget.takeHorizontalHeaderItem(column).text()
        id_data = self.ui.tableWidget.item(row, 0).text()
        id_column = self.ui.tableWidget.takeHorizontalHeaderItem(0).text()
        table = self.ui.comboBox.currentText()
        error = self.db.updateDB(table, new_data, data_column, id_data, id_column)
        self.print_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainW(Database(host, user, password, database))
    window.show()
    sys.exit(app.exec())