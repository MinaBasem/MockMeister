import requests
import json
import pandas as pd
from pandas import json_normalize
from PyQt5.QtCore import (Qt, QSize)
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
    QAbstractItemView
)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MockMeister v1.0")
        self.setFixedSize(800, 500)

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
        self.combo_box.addItems(["first_name", "last_name", "email", "phone_number", "address.city", "address.street_name", "address.street_address", "address.zip_code", "address.state", "address.country", "employment.title", "Years of experience", "Salary"])
        #combo_box.setFixedWidth(50)

        self.table = QTableWidget()
        self.table.setRowCount(15)                   # Set row count based on data
        self.table.setColumnCount(6)                        # Set column count based on data keys
        #self.table.setHorizontalHeaderLabels(list(data.keys()))     # Set column headers


        self.table.verticalHeader().setVisible(False)
        self.table.setFixedWidth(620)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)

        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_table)
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
        Left_Column_layout.addWidget(generate_button)
        H_layout.addLayout(Left_Column_layout)
        H_layout.addWidget(self.table)
        V_layout.addLayout(H_layout, stretch=8)

        V_layout.addWidget(QLabel("@MinaBasem"))

        widget = QWidget()
        widget.setLayout(V_layout)
        self.setCentralWidget(widget)

    def add_button_func(self):
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
    
    def get_all_items(self):
        items = []
        for row in range(self.list_widget.count()):
            item = self.list_widget.item(row)
            items.append(item.text())  # Append the text of each item to the list
        return items

    def generate_data(self):
        count = self.get_spinbox_value()
        random_data_generator_url = "https://random-data-api.com/api/v2/users?size=" + str(count) + "&is_xml=true"
        response = requests.get(random_data_generator_url)
        data = json.loads(response.text)
        df = json_normalize(data)
        needed_data = self.get_all_items()
        print(df[needed_data])
        return df[needed_data]


    def generate_table(self):
        new_data = self.generate_data()

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

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()