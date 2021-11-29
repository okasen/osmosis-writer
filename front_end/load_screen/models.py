
from typing import List

from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtWidgets import QTextEdit, QMdiSubWindow, QWidget, QGridLayout, QMdiArea, QLabel, QVBoxLayout, QMainWindow


class SceneEditor(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(QTextEdit, self).__init__(*args, **kwargs)
        self.setFontPointSize(14)
        self.setPlaceholderText("Blank pages are intimidating, so we put these words here.")
        self.setAutoFormatting(QTextEdit.AutoAll)


class ChapterWindow(QMdiSubWindow):
    def __init__(self, title: str, scenes: List[str], *args, **kwargs):
        super(QMdiSubWindow, self).__init__(*args, **kwargs)

        self.oldPos = self.pos()
        self.pressed = False
        containing_widget = QWidget()
        containing_layout = QVBoxLayout()
        title_label = QLabel()
        title_label.setText(title)
        self.scene_list = []
        if not scenes:
            editor = SceneEditor()
            editor.setPlaceholderText("Blank pages are intimidating, so we put some words here")
            containing_layout.addWidget(editor)
            self.scene_list.append(editor)
        for scene in scenes:
            editor = SceneEditor()
            editor.setHtml(scene)
            containing_layout.addWidget(editor)
            self.scene_list.append(editor)

        containing_layout.addWidget(title_label)
        containing_widget.setLayout(containing_layout)
        self.setWidget(containing_widget)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed = True

    def mouseMoveEvent(self, event):
        if self.pressed:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressed = False


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.main_screen = QWidget()
        self.main_layout = QGridLayout()
        self.setGeometry(QRect(50, 50, 1600, 800))
        self.work_tab_pane = QWidget()
        self.work_tab_layout = QGridLayout()
        self.mdi_layout = QMdiArea()
        self.main_screen.setLayout(self.main_layout)

        self.work_tab_layout.setGeometry(QRect(0,0,400,800))

        self.main_layout.addWidget(self.mdi_layout, 1,1,Qt.AlignRight)
        self.main_layout.addWidget(self.work_tab_pane, 1,1,Qt.AlignLeft)
        self.setCentralWidget(self.main_screen)

        self.main_screen.show()
        self.mdi_layout.show()