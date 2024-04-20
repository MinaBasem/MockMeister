import requests
import json
import pandas as pd
import datetime
import random
from pandas import json_normalize
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

class MainWindow(QMainWindow):
    def __init__(self):
        self.dataframe = pd.DataFrame()
        super(MainWindow, self).__init__()
        self.setWindowTitle("MockMeister v1.1")
        self.setFixedSize(800, 500)
        icon = QIcon("misc/mockmeister_simple_logo.png")
        self.setWindowIcon(icon)

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
        self.combo_box.addItems(["first_name", "last_name", "email", "phone_number", "address.city", "address.street_name", "address.street_address", "address.zip_code", "address.state", "address.country", "employment.title", "Years of experience", "Salary"])
        #combo_box.setFixedWidth(50)

        self.table = QTableWidget()
        self.table.setRowCount(15)                   # Set row count based on data
        self.table.setColumnCount(6)                 # Set column count based on data keys
        #self.table.setHorizontalHeaderLabels(list(data.keys()))     # Set column headers


        self.table.verticalHeader().setVisible(False)
        self.table.setFixedWidth(620)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)

        self.generate_button = QPushButton("Generate")
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_table)
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

        df = self.transform_data(df, needed_data)

        self.dataframe = df[needed_data]
        print(self.dataframe)
        return self.dataframe
    
    def transform_data(self, df, needed_data):
        if 'email' in needed_data:
            domain_options = ['@gmail', '@yahoo', '@hotmail']
            def replace_email(email):
                return email.replace('@email', random.choice(domain_options))
            df['email'] = df['email'].apply(replace_email)

            separator_options = ['_', '.']
            def replace_separator(email):
                return email.replace('.', random.choice(separator_options), 1)
            df['email'] = df['email'].apply(replace_separator)

            def add_random_number_to_email(email):
                add_or_not = random.choice([0, 1])
                if add_or_not == 0:
                    return email
                else:
                    random_number_str = str(random.randint(0, 9999)).zfill(4)
                    email_parts = email.split('@')
                    modified_username = email_parts[0] + "_" + random_number_str
                    return modified_username + "@" + email_parts[1]
            df['email'] = df['email'].apply(add_random_number_to_email)

        return df


    def generate_table(self):           
        try:
            new_data = self.generate_data()
            #self.save_file(new_data)

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

        except:
            message_box = QMessageBox(self)     # Shows python3 in title, fix it
            message_box.setText("Error calling API and generating table. \nPlease retry.")
            message_box.setIcon(QMessageBox.Icon.Warning)
            message_box.exec()


    def save_file(self):
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.dataframe.to_csv("data-" + formatted_datetime + ".csv", index=False)
        print("Data saved to location")

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