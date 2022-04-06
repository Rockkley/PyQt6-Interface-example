import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,  QPushButton, QDockWidget, \
    QListWidget, QTableWidget, QTableWidgetItem, QFrame, QWidget, QPlainTextEdit, QHeaderView
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, Slot
import configparser


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Hello World")
        self.setGeometry(0, 0, 800, 800)

        # Creating all the layouts
        self.page_layout = QVBoxLayout()
        self.hor_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.table_layout = QVBoxLayout()
        self.text_layout = QVBoxLayout()

        self.editor_layout = QVBoxLayout()
        self.text_buttons_layout = QVBoxLayout()

        # Creating frames

        self.editor_frame = QFrame()
        self.editor_layout.setContentsMargins(0, 0, 0, 0)
        self.editor_frame.setLayout(self.editor_layout)

        self.table_frame = QFrame()
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_frame.setLayout(self.table_layout)

        self.background_frame = QFrame()

        # Adding layouts into layouts

        self.page_layout.addLayout(self.button_layout)
        self.page_layout.addLayout(self.hor_layout)

        # horizontal layer contains table, texts and 'x' and 'ok' buttons
        self.hor_layout.addLayout(self.table_layout)
        self.hor_layout.addLayout(self.text_layout)
        self.hor_layout.addLayout(self.editor_layout)

        # Creating Button instances
        self.style_button = Button('Hide style panel', self.style_visible).btn
        self.table_button = Button('Hide table', self.show_hide_table).btn
        self.text_panel_button = Button('Hide text panel', self.show_hide_text).btn
        self.clear_texts_button = Button('Clear text fields', self.clear_text_fields).btn
        self.add_text_field_button = Button('Add text field', self.add_editor).btn

        # Adding widgets
        self.hor_layout.addWidget(self.editor_frame)
        self.hor_layout.insertWidget(1, self.table_frame)

        self.button_layout.addWidget(self.style_button)
        self.button_layout.addWidget(self.table_button)
        self.button_layout.addWidget(self.text_panel_button)
        self.button_layout.addWidget(self.clear_texts_button)
        self.button_layout.addWidget(self.add_text_field_button)

        self.table = Table()
        self.table_layout.insertLayout(0, self.table.layout)

        self.background_frame.setLayout(self.page_layout)

        self.page_layout.addWidget(self.background_frame)
        self.setCentralWidget(self.background_frame)
        self.editor_dict = {}
        self.statusBar().setStyleSheet("border : 1px")

        # Вызовы элементов
        self.add_editor()
        self.style_panel()
        self.create_actions()
        self.create_menu_bar()

        self.style_config = configparser.ConfigParser()
        self.style_config.read(f'config/conf.ini')

        # Checking for stylesheet files in "config/"
        with open(f'config/{self.style_config["view"]["style"].lower()}.stylesheet', 'r') as i:
            self.setStyleSheet(i.read())
            a = []
            for x in range(self.style_list.count()):
                a.append(self.style_list.item(x).text())

            self.style_list.setCurrentRow(a.index(self.style_config["view"]["style"]))

    def show_hide_text(self):
        if self.editor_frame.isVisible():
            self.editor_frame.hide()
            self.text_panel_button.setText('Show text panel')
        else:
            self.editor_frame.show()
            self.text_panel_button.setText('Hide text panel')

    def clear_text_fields(self):
        for editor in self.editor_dict.values():
            editor.text.clear()

    def style_visible(self):
        if self.dock.isVisible():
            self.dock.hide()
            self.style_button.setText('Show style panel')
        else:
            self.dock.show()
            self.style_button.setText('Hide style panel')

    def create_actions(self):

        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(QApplication.instance().quit)

        self.action1 = QAction("&Action 1", self)
        self.action1.triggered.connect(self.status_action1)

        self.action2 = QAction("&Action 2", self)
        self.action2.triggered.connect(self.status_action2)

        self.action3 = QAction("&Action 3", self)
        self.action3.triggered.connect(self.status_action3)

    def status_action1(self):
        self.statusBar().showMessage('Action 1')

    def status_action2(self):
        self.statusBar().showMessage('Action 2')

    def status_action3(self):
        self.statusBar().showMessage('Action 3')

    def create_menu_bar(self):

        menu_bar = self.menuBar()

        first_menu = menu_bar.addMenu("&First menu")
        first_menu.addAction(self.exit_action)
        second_menu = menu_bar.addMenu("&Second menu")
        second_menu.addAction(self.action1)
        submenu = second_menu.addMenu('Submenu')
        submenu.addAction(self.action2)
        submenu.addAction(self.action3)

    def style_panel(self):

        self.dock = QDockWidget("Style", self)
        self.dock.setMaximumWidth(140)

        self.dock.closeEvent = self.close_style

        self.style_list = QListWidget(self)

        for x in os.listdir('config/'):
            if x.endswith(".stylesheet"):
                style_name = str(x).split('.stylesheet')[0].title()
                self.style_list.addItem(style_name)

        style_config = configparser.ConfigParser()
        style_config.read(f'config/conf.ini')

        self.style_list.currentRowChanged.connect(self.switch_style)

        self.dock.setWidget(self.style_list)

        self.dock.setGeometry(100, 0, 100, 100)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

    def close_style(self, event):
        self.style_button.setText('Show style panel')

    def switch_style(self):

        style_config = configparser.ConfigParser()
        style_config.read(f'config/conf.ini')
        current_selection = self.style_list.itemFromIndex(self.style_list.currentIndex())
        self.setStyleSheet(f'config/{current_selection.text().lower()}.stylesheet')
        with open(f'config/{current_selection.text().lower()}.stylesheet', 'r') as f:
            self.setStyleSheet(f.read())

        style_config.set('view', 'style', current_selection.text())
        with open('config/conf.ini', 'w') as configfile:
            style_config.write(configfile)

    def table_add_row(self):
        self.add_row_btn = QPushButton('Add line')
        self.add_row_btn.pressed.connect(self.add_row)

    def table_del_row(self):
        self.del_row_btn = QPushButton('Delete line')
        self.del_row_btn.pressed.connect(self.del_row)

    def show_hide_table(self):
        if self.table_frame.isVisible():
            self.table_frame.hide()
            self.table_button.setText('Show table')
        else:
            self.table_frame.show()
            self.table_button.setText('Hide table')

    def add_editor(self):
        editor = Editor()
        editor.signal.connect(self.process_editor)
        self.editor_dict.update({editor.objectName(): editor})
        self.editor_layout.addWidget(editor)
        Editor.dict_len += 1

    @Slot(list)
    def process_editor(self, signal):
        if signal[1] == "print":
            self.statusBar().showMessage(self.editor_dict[signal[0]].text.toPlainText())
        elif signal[1] == "delete":
            self.statusBar().clearMessage()
            editor = self.editor_dict.pop(signal[0])
            self.editor_layout.removeWidget(editor)
            editor.setParent(None)


class Editor(QWidget):
    signal = Signal(list)
    dict_len = 1

    def __init__(self):
        super(Editor, self).__init__()
        self.setObjectName(f"{id(self)}")
        self.layout = QHBoxLayout(self)
        self.text = QPlainTextEdit()

        self.text.setPlainText('Text_'+str(self.dict_len))
        self.text.setStyleSheet('background-color: white')
        self.layout.addWidget(self.text)
        self.btn_layout = QVBoxLayout()
        self.btn1 = QPushButton("X")
        self.btn1.setFixedWidth(35)
        self.btn2 = QPushButton("OK")
        self.btn2.setFixedWidth(35)
        self.btn_layout.addWidget(self.btn1)
        self.btn_layout.addWidget(self.btn2)
        self.layout.addLayout(self.btn_layout)
        self.btn1.clicked.connect(self.delete_editor)
        self.btn2.clicked.connect(self.print_text)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def delete_editor(self):
        self.signal.emit([self.objectName(), "delete"])

    def print_text(self):
        self.signal.emit([self.objectName(), "print"])


class Button(QWidget):
    def __init__(self, name, action):
        super(Button, self).__init__()
        self.btn = QPushButton(text=name)
        self.btn.clicked.connect(action)


class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.layout = QVBoxLayout()
        self.button_table_layout = QHBoxLayout()
        self.button_table_layout.addWidget(Button('Add line', self.add_row).btn)
        self.button_table_layout.addWidget(Button('Delete line', self.del_row).btn)
        self.layout.addLayout(self.button_table_layout)
        self.table = QTableWidget()  # Создаём таблицу
        self.table.setColumnCount(3)  # Устанавливаем три колонки
        self.table.setStyleSheet('background-color: white')
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Id", "Parameter", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.layout.insertWidget(0, self.table)

    def add_row(self):

        self.table.insertRow(self.table.rowCount())
        self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem('Id_' + str(self.table.rowCount())))
        self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem('Parameter_' + str(self.table.rowCount())))
        self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(str(self.table.rowCount()) * 3))

    def del_row(self):
        if self.table.rowCount() > 0:
            self.table.removeRow(self.table.rowCount() - 1)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    app.exec()


if __name__ == '__main__':
    main()
