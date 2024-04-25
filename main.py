import pandas as pd
import datetime
import random
import os
from PyQt5.QtCore import (Qt, QSize, QUrl)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QToolBar,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QListWidget,
    QSpinBox,
    QAbstractItemView,
    QFileDialog,
    QMessageBox
)

from misc.messages import help_text # type: ignore
from data import DataGeneration, DataTransformation # type: ignore

class MainWindow(QMainWindow):
    def __init__(self):

        self.data_generation, self.data_transformation = DataGeneration(), DataTransformation()

        self.dataframe = pd.DataFrame()
        super(MainWindow, self).__init__()
        self.setWindowTitle("MockMeister v1.2")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "misc", "mockmeister_simple_logo.png")))

        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        toolbar.setMovable(False)

        self.save_button = QAction("Save", self)
        self.save_button.triggered.connect(self.save_file)

        self.open_button = QAction("Open", self)
        self.open_button.triggered.connect(self.open_file)

        self.help_button = QAction("Help", self)
        self.help_button.triggered.connect(self.show_help)

        #self.about_button = QAction("About", self)
        #self.about_button.triggered.connect(self.show_about)

        toolbar.addAction(self.save_button)
        toolbar.addAction(self.open_button)
        toolbar.addAction(self.help_button)
        #toolbar.addAction(self.about_button)

        V_layout = QVBoxLayout()
        H_layout = QHBoxLayout()
        Left_Column_layout = QVBoxLayout()
        Top_Left_Column_layout = QHBoxLayout()
        self.Bottom_Left_Column_layout = QHBoxLayout()

        count_label = QLabel("Row count: ")
        self.counter_widget = QSpinBox()
        self.counter_widget.setMinimum(1)
        self.counter_widget.setMaximum(100)
        self.counter_widget.valueChanged.connect(self.get_spinbox_value)

        self.Bottom_Left_Column_layout.addWidget(count_label)
        self.Bottom_Left_Column_layout.addWidget(self.counter_widget)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)

        self.combo_box = QComboBox()
        self.fields = {      # key is API name, value is display name
            "first_name": "First Name", 
            "last_name": "Last Name", 
            "email": "Email", 
            "address.city": "City", 
            "address.street_name": "Street Name", 
            "address.street_address": "Street Address",
            "address.zip_code": "Zip Code", 
            "address.state": "State", 
            "address.country": "Country", 
            "employment.title": "Title", 
            "years_of_experience": "Years of experience"}
        self.combo_box.addItems(self.fields.values())


        self.table = QTableWidget()
        self.table.setRowCount(15)                   # Set row count based on data
        self.table.setColumnCount(6)                 # Set column count based on data keys

        self.table.verticalHeader().setVisible(False)
        self.table.setFixedWidth(620)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)

        self.generate_button = QPushButton("Generate")
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_table_in_UI)
        add_button = QPushButton("+")
        add_button.setFixedWidth(20)
        add_button.clicked.connect(self.add_button_func)
        remove_button = QPushButton("-")
        remove_button.setFixedWidth(20)
        remove_button.clicked.connect(self.remove_button_func)

        Top_Left_Column_layout.addWidget(self.combo_box)
        Top_Left_Column_layout.addWidget(add_button)
        Top_Left_Column_layout.addWidget(remove_button)

        Left_Column_layout.addLayout(Top_Left_Column_layout)
        Left_Column_layout.addWidget(self.list_widget)
        Left_Column_layout.addLayout(self.Bottom_Left_Column_layout)
        Left_Column_layout.addWidget(self.generate_button)
        H_layout.addLayout(Left_Column_layout)
        H_layout.addWidget(self.table)
        V_layout.addLayout(H_layout, stretch=8)

        self.save_as_csv_button = QPushButton("Export as CSV")
        self.save_as_csv_button.clicked.connect(self.save_file)
        V_layout.addWidget(self.save_as_csv_button)

        widget = QWidget()
        widget.setLayout(V_layout)
        self.setCentralWidget(widget)

    
    def display_message_box(self, title, message):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        #message_box.setIcon(QMessageBox.Icon.icon)
        message_box.exec()


    def add_button_func(self):
        self.generate_button.setEnabled(True)
        combo_box_selected_text = self.combo_box.currentText()
        self.list_widget.addItem(combo_box_selected_text)

        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        unique_items = set(items)   # Convert the list to a set to remove duplicates
        self.list_widget.clear()    # Clear the list widget

        for item in unique_items:   # Add the unique items back to the list widget
            self.list_widget.addItem(item)

    def remove_button_func(self):
        
        selected_item = self.list_widget.currentItem()
        if selected_item:
            row = self.list_widget.currentRow()
            self.list_widget.takeItem(row)

    def get_spinbox_value(self):
        value = self.counter_widget.value()
        return value
    
    def get_requested_fields(self):        # Returns data selected in the list box
        items = []
        for row in range(self.list_widget.count()):
            display_name = self.list_widget.item(row).text()
            # Lookup the key based on the display name
            key = next(key for key, value in self.fields.items() if value == display_name)
            items.append(key)
        return items


    def generate_table_in_UI(self):
        
        try:
            row_count = self.get_spinbox_value()
            requested_fields = self.get_requested_fields()
            new_data = self.data_generation.generate_data(row_count, requested_fields)

            self.table.clearContents()          # Clear the existing table
            self.table.setRowCount(0)
            self.table.setColumnCount(0)

            # Set the table rows and columns count depending on dataframe
            self.table.setRowCount(len(new_data))
            self.table.setColumnCount(len(new_data.columns))

            # Set the horizontal header labels from the DataFrame column names
            self.table.setHorizontalHeaderLabels(list(new_data.columns))

            # Populate the table cells with data from the DataFrame
            for row, row_data in new_data.iterrows():
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))  # Convert value to string for display
                    self.table.setItem(row, col, item)

            self.dataframe = new_data
            return new_data

        except:
            self.display_message_box("Error", "Error calling API and generating table. \nPlease retry.")


    def save_file(self):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%d-%m-%Y-%H-%M-%S")
        file_path = os.path.join(os.path.dirname(__file__), "saves", "data-" + formatted_datetime + ".csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.dataframe.to_csv(file_path, index=False)
        print("Data saved to:", file_path)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.ShowDirsOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv)", options=options)

        if filename:
            try:
                new_data = pd.read_csv(filename)
                self.table.clearContents()
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.table.setRowCount(len(new_data))
                self.table.setColumnCount(len(new_data.columns))
                self.table.setHorizontalHeaderLabels(list(new_data.columns))

                for row, row_data in new_data.iterrows():
                    for col, value in enumerate(row_data):
                        item = QTableWidgetItem(str(value)) 
                        self.table.setItem(row, col, item)

            except pd.errors.ParserError:
                print("Error parsing CSV file.")

    def show_help(self):
        help_box = QMessageBox(self)     # Shows python3 in title, fix it
        help_box.setWindowTitle("Help")
        help_box.setText(help_text)
        help_box.setIcon(QMessageBox.Icon.Information)
        help_box.exec()

    """def show_about(self):
        help_box = QMessageBox(self)
        about_text = "MockMeister v1.1 \nhttps://github.com/MinaBasem/MockMeister"
        help_box.setText(about_text)
        help_box.setIcon(QMessageBox.Icon.Warning)
        help_box.exec()"""

    """def open_url(self, url):
        try:
            from PyQt5.QtCore import QUrl, QDesktopServices
            QDesktopServices.openUrl(QUrl(url))
        except:
            QMessageBox.critical(self, "Error", "Failed to open link.")"""

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()