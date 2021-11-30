import sys
from os.path import expanduser

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QFileDialog, QDialog, QLabel, QApplication, QLineEdit
from kink import inject

from front_end.load_screen.views import StartFunctions


class PathNotSetException(Exception):
    pass


@inject
class StartWindow(QWidget):
    def __init__(self, start_functions: StartFunctions):
        super().__init__()
        self.start_functions = start_functions

        self.setWindowTitle("Select your settings")

        layout = QVBoxLayout()

        open_button = QPushButton("Open Existing Osmosis Project")
        new_button = QPushButton("Start New Osmosis Project")
        cancel_button = QPushButton("Close Osmosis Writer")

        open_button.clicked.connect(self.open_existing_project)
        new_button.clicked.connect(self.open_new_project)
        cancel_button.clicked.connect(self.close_start)

        layout.addWidget(open_button)
        layout.addWidget(new_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def open_existing_project(self):
        try:
            project_path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "OSM documents (*.osm)")
            if not project_path:
                raise PathNotSetException("Please select an existing OSM project or start a new one.")
            self.start_functions.open_existing(project_path)
        except PathNotSetException as e:
            error_dialog = QDialog()
            error_layout = QVBoxLayout()

            error_text_label = QLabel(str(e))
            error_layout.addWidget(error_text_label)

            restart_button = QPushButton("Ok")

            restart_button.clicked.connect(error_dialog.accept)
            cancel_button = QPushButton("Quit OsmosisWriter")
            cancel_button.clicked.connect(error_dialog.close)
            cancel_button.clicked.connect(self.close_start)

            error_layout.addWidget(restart_button)
            error_layout.addWidget(cancel_button)

            error_dialog.setLayout(error_layout)
            error_dialog.exec()

    @staticmethod
    def text_input_factory(label: str, placeholder: str):
        dialog = QDialog()
        layout = QVBoxLayout()

        naming_info_label = QLabel(label)
        namer = QLineEdit()
        namer.setPlaceholderText(placeholder)

        layout.addWidget(naming_info_label)
        layout.addWidget(namer)

        confirm_button = QPushButton("confirm")
        confirm_button.setEnabled(False)
        confirm_button.clicked.connect(dialog.accept)

        cancel_button = QPushButton("cancel")
        cancel_button.clicked.connect(dialog.reject)

        layout.addWidget(confirm_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)
        dialog.isModal()

        namer.textChanged.connect(lambda x: confirm_button.setEnabled(True))

        dialog.exec()

        while True:
            if dialog.Accepted:
                return namer.text()
            elif dialog.Rejected:
                return ""

    def build_new_project(self, title: str):
        project_title = title
        directory_dialog = QFileDialog()
        directory_dialog.setFileMode(QFileDialog.Directory)
        home_dir = expanduser("~")
        directory_dialog.setDirectory(str(home_dir))
        project_parent_directory = directory_dialog.getExistingDirectory()

        label = "Enter your chapter title:"
        placeholder = "Type your chapter title here"
        chapter_title = self.text_input_factory(label=label, placeholder=placeholder)

        self.start_functions.start_new(
            title=project_title,
            directory=project_parent_directory,
            chapter_title=chapter_title
        )

    def open_new_project(self):
        label = "Enter your project name below:"
        placeholder = "Type your project name here"
        project_title = self.text_input_factory(label=label, placeholder=placeholder)
        if project_title == "":
            raise Exception

        self.build_new_project(title=project_title)

    def close_start(self):
        self.close()


app = QApplication(sys.argv)

window = StartWindow()

window.show()

app.exec()
