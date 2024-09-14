# 2022-2024 Marc Schubert <schubert.mc.ai@gmail.com>

from anki import hooks
from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
import os
import json
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QTextEdit,
                             QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QInputDialog, QColorDialog, QDialog, QLabel, QLineEdit, 
                             QMessageBox, QComboBox, QAbstractItemView)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, pyqtSignal

addon_folder = os.path.dirname(__file__)

def read_json():
    filepath = os.path.join(addon_folder,"user_files","config.json")
    file = open(filepath)
    data = json.load(file)
    return data

def write_json(dump):
    filepath = os.path.join(addon_folder , "user_files" , "config.json")
    file = open(filepath, "w")
    file.write(json.dumps(dump))
    return 0


def write_settings(settings):
    filepath = os.path.join(addon_folder,"user_files", "settings.json")
    with open(filepath, "w") as file:
        json.dump(settings, file)

def read_settings():
    filepath = os.path.join(addon_folder,"user_files", "settings.json")
    if os.path.exists(filepath):
        with open(filepath) as file:
            return json.load(file)
    return {"fontWeight": "normal"}  

class ManualEditing(QMainWindow):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manual Editing of Data")
        self.layout = QVBoxLayout()
        self.text =QTextEdit()
        self.text.setText(json.dumps(read_json()))

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save_btn_clicked)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel_btn_clicked)

        self.btns = QWidget()
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.cancelButton)
        self.btn_layout.addWidget(self.saveButton)
        self.btns.setLayout(self.btn_layout)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.btns)
        self.mayor_widget = QWidget()
        self.mayor_widget.setLayout(self.layout)

        self.setCentralWidget(self.mayor_widget)

    def save_btn_clicked(self):
        plain_text = self.text.toPlainText()
        try:
            write_json(json.loads(plain_text))
            self.data_saved.emit()
            self.close()
        except Exception as e:
            error_json = '[{"word": "Ramucirumab", "group": "VEGF-Inhibitor", "color": "MediumTurquoise"}, {"word": "Certolizumab", "group": "TNF-Inhibitor", "color": "DarkTurquoise"}, {"word": "CiclosporinA", "group": "Calcineurin-Inhibitor", "color": "Teal"}]'
            QMessageBox.critical(self, "JSON Format Error", "Invalid JSON format. Please ensure the data is correctly formatted as a JSON object. Example format:\n" + error_json + "\nError details: " + str(e))
        

    def cancel_btn_clicked(self):
        self.close()


class EntryDialog(QDialog):
    def __init__(self, word='', group='', color=QColor('white'), parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Entry')

        # Setup layout
        layout = QVBoxLayout()

        # Word field
        self.word_edit = QLineEdit(word)
        layout.addWidget(QLabel('Word:'))
        layout.addWidget(self.word_edit)

        # Group field
        self.group_edit = QLineEdit(group)
        layout.addWidget(QLabel('Group:'))
        layout.addWidget(self.group_edit)


        # Color field
        self.color_edit = QPushButton('Choose Color')
        self.color_edit.clicked.connect(self.choose_color)
        self.color = color
        self.color_edit.setStyleSheet(f'background-color: {self.color.name()}')
        layout.addWidget(QLabel('Color:'))
        layout.addWidget(self.color_edit)

        # Buttons for save or cancel
        buttons_layout = QHBoxLayout()
        self.btn_save = QPushButton('Save')
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel = QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_cancel)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor(self.color)
        if color.isValid():
            self.color = color
            self.color_edit.setStyleSheet(f'background-color: {color.name()}')

    def get_data(self):
        return self.word_edit.text(), self.group_edit.text(), self.color.name()


class ShareDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Share Your Dataset with the Community")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Message Label
        message_label = QLabel("""
        <p><strong>Have you created a 🎨 ColorCoding 🌈 dataset that has been particularly helpful in your studies?</strong><br> Do you think it might benefit others as well?<br><br>
        We encourage you to share your dataset with the community!</p>
        <p><strong>How to Share Your Datasets:</strong><br>
        1. Save your dataset using the button below to a location on your computer.<br>
        2. Send the file to <a href="mailto:schubert.mc.ai@gmail.com">schubertmc</a>. We will then upload it to the ‘Datasets’ section <a href=https://ankiweb.net/shared/info/2113325087>here</a>.</p>
        <p>Please let us know if you want to be credited for your dataset or prefer to remain anonymous.</p>
        <p><strong>🎨 Thank you! 🌈</strong><br><br>
        Please choose a location to save your dataset file below:</p>
        """)
        message_label.setOpenExternalLinks(True)
        message_label.setTextFormat(Qt.TextFormat.RichText)  


        layout.addWidget(message_label)

        # Save Button
        save_button = QPushButton("Save Dataset As...")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_file(self):
        options = QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, 
                                                "Save File", 
                                                "", 
                                                "JSON Files (*.json)", 
                                                options=options)
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(self.data, f, indent=4)
            self.accept()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setFixedSize(300, 100)

        layout = QVBoxLayout()

        self.boldCheckBox = QCheckBox("Apply bold formatting to colored words")
        cur_setting = self.read_current_setting()
        font_bool = 1 if cur_setting == "bold" else 0
        self.boldCheckBox.setChecked(font_bool)
        layout.addWidget(self.boldCheckBox)

        self.btnSave = QPushButton("Save")
        self.btnSave.clicked.connect(self.save_settings)
        self.btnCancel = QPushButton("Cancel")
        self.btnCancel.clicked.connect(self.cancel_settings)
        layout.addWidget(self.btnSave)

        self.setLayout(layout)

    def cancel_settings(self):
        print("Changes canceled!")
        self.close()

    def save_settings(self):
        bold_setting = self.boldCheckBox.isChecked()
        print(bold_setting)
        bold_string = "bold" if bold_setting else "normal"

        self.write_settings({'fontWeight': bold_string})
        self.accept() 

    def read_current_setting(self):
        settings = self.read_settings()
        return settings.get('fontWeight', False)

    @staticmethod
    def write_settings(settings):
        filepath = os.path.join(addon_folder,"user_files" ,"settings.json")  
        with open(filepath, "w") as file:
            json.dump(settings, file)

    @staticmethod
    def read_settings():
        filepath = os.path.join(addon_folder,"user_files" , "settings.json")
        if os.path.exists(filepath):
            with open(filepath) as file:
                return json.load(file)
        return {}



class ComplexWindow4(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("🎨 Color Coding 🌈 - Settings")
        self.setGeometry(100, 100, 600, 700) 

        # Main layout
        main_layout = QVBoxLayout()

        # Button to add entries
        self.btnAdd = QPushButton("Add Entry")
        self.btnAdd.clicked.connect(self.add_entry)
        main_layout.addWidget(self.btnAdd)


        # Table setup
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnCount(5)  
        self.table.setHorizontalHeaderLabels(["Word", "Group", "Color", "Edit", "Delete"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Disable editing cells directly
        self.load_data()
        main_layout.addWidget(self.table)


        # Buttons at the bottom
        button_layout = QHBoxLayout()
        self.btnSave = QPushButton("Save")
        self.btnCancel = QPushButton("Cancel")
        self.btnSettings = QPushButton("Font Settings")
        self.btnModifyManually = QPushButton("Modify Manually")
        self.btnShare = QPushButton("Share your Dataset")
        
        # Connect buttons to their functionalities
        self.btnSave.clicked.connect(self.save_data)
        self.btnCancel.clicked.connect(self.cancel_changes)
        self.btnModifyManually.clicked.connect(self.modify_manually)
        self.btnShare.clicked.connect(self.share_functionality)
        self.btnSettings.clicked.connect(self.open_settings_dialog)

        # Adding buttons to the horizontal layout
        button_layout.addWidget(self.btnSave)
        button_layout.addWidget(self.btnCancel)
        button_layout.addWidget(self.btnSettings)
        button_layout.addWidget(self.btnModifyManually)
        button_layout.addWidget(self.btnShare)

        main_layout.addLayout(button_layout)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


    def save_data(self):
        data_to_save = []
        for row in range(self.table.rowCount()):
        # Extract the data from each column in the row
            #print(row)
            word = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            group = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            color = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            data_to_save.append({
                "word": word,
                "group": group,
                "color": color
            })
        try:
            write_json(list(reversed(data_to_save)))
            print("Data saved!")
            self.close()
        except Exception as e:
            error_json = '[{"word": "Ramucirumab", "group": "VEGF-Inhibitor", "color": "MediumTurquoise"}, {"word": "Certolizumab", "group": "TNF-Inhibitor", "color": "DarkTurquoise"}, {"word": "CiclosporinA", "group": "Calcineurin-Inhibitor", "color": "Teal"}]'
            QMessageBox.critical(self, "JSON Format Error", "Invalid JSON format. Please ensure the data is correctly formatted as a JSON object. Example format:\n" + error_json + "\nError details: " + str(e))   

    def cancel_changes(self):
        print("Changes canceled!")
        self.close()

    def modify_manually(self):
        self.manual_editing = ManualEditing()
        self.manual_editing.data_saved.connect(self.refresh_table)
        self.manual_editing.show()
        print("Modify manually activated!")

    def refresh_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)
        self.load_data()


    def load_data(self):
        data_dict = read_json()
        for entry in data_dict:
            self.add_table_entry(entry['word'], entry['group'], entry['color'])

    def add_table_entry(self, word, group, color):
        row_position = 0  # Always insert at the top
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(word))
        self.table.setItem(row_position, 1, QTableWidgetItem(group))
        self.table.setItem(row_position, 2, QTableWidgetItem(color))
        self.table.item(row_position, 2).setBackground(QColor(color))

        # Edit button
        btnEdit = QPushButton('Edit')
        btnEdit.clicked.connect(self.edit_entry)
        self.table.setCellWidget(row_position, 3, btnEdit)

        # Delete button
        btnDelete = QPushButton('Delete')
        btnDelete.clicked.connect(self.delete_entry)
        self.table.setCellWidget(row_position, 4, btnDelete)

    def add_entry(self):
        dialog = EntryDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            word, group, color = dialog.get_data()
            self.add_table_entry(word, group, color)

    def edit_entry(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            current_word = self.table.item(row, 0).text()
            current_group = self.table.item(row, 1).text()
            current_color = self.table.item(row, 2).text()
            dialog = EntryDialog(current_word, current_group, QColor(current_color))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                word, group, color = dialog.get_data()
                self.table.item(row, 0).setText(word)
                self.table.item(row, 1).setText(group)
                self.table.item(row, 2).setText(color)
                self.table.item(row, 2).setBackground(QColor(color))

    def delete_entry(self, row):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            self.table.removeRow(row)
    
    def share_functionality(self):
        data_to_share = read_json()
        share_dialog = ShareDialog(data_to_share)
        share_dialog.exec()


    def open_settings_dialog(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()
    

    
def complex_settings_gui():
    mw.myWidget = widget = ComplexWindow4()
    widget.show()


# Setup buttons
def setupButtons(buttons, editor):
    icon_path = os.path.join(addon_folder,"icon3232.png")
    btn = editor.addButton(icon_path,
                           "foo",
                           performConversion,
                           tip= "Color Words",
                           label = "C",
                           rightside=True, 
                           )
    buttons.append(btn)


# Launch engine 
def performConversion(editor):
    webview = editor.web
    js_path = os.path.join(addon_folder,"changer_static.js")
    with open(js_path, "r", encoding="utf-8") as js_file:
        js = js_file.read()
        webview.eval(js)
        data = read_json()
        font_settings = read_settings()
        fontWeight = font_settings.get("fontWeight")
        webview.eval(f"initializeWithData({json.dumps(data)}, '{fontWeight}')")



# Setup actions
action_settings = QAction("🎨 Color Coding 🌈 ", mw)
qconnect(action_settings.triggered, complex_settings_gui)
mw.form.menuTools.addAction(action_settings)


editors = []
def add_to_editors(editor)->None:
    editor = editor.web
    editors.append(editor)

gui_hooks.editor_did_init_buttons.append(setupButtons)
#gui_hooks.editor_did_init.append(setupLiveChanger)
gui_hooks.editor_did_init.append(add_to_editors)

