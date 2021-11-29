from PyQt5.QtWidgets import QAction
from kink import inject, di

from back_end.native_file_handling.file_functions import load, create, save
from front_end.load_screen.models import MainWindow, ChapterWindow
from shared.dataclasses import Chapter, Project


@inject
def create_new_chapter(title: str, window: ChapterWindow, scenes: list, project: Project):
    chapter = Chapter(title=title, scenes=scenes, window=window)
    project.chapters.append(chapter)


@inject
class StartFunctions:
    def __init__(self):
        self.main_window = MainWindow()

        menu_bar = self.main_window.menuBar()

        file_menu = self.main_window.menuBar().addMenu("&File")

        save_action = QAction("&save", self.main_window)

        file_menu.addAction(save_action)

        save_action.triggered.connect(save)


    def open_existing(self):
        project, chapter_data = load(directory="test", title="test")
        for chapter in chapter_data:
            title = chapter.title
            new_chapter_editor = ChapterWindow(title=title, scenes=chapter.scenes)
            new_chapter = Chapter(title=title, window=new_chapter_editor)
            project.chapters.append()
            self.main_window.mdi_layout.addSubWindow(new_chapter_editor)
            new_chapter.scenes = new_chapter_editor.scene_list
            # TODO add chapter to navigation
        self.main_window.show()

    def start_new(self, title: str, directory: str, chapter_title: str):
        project: Project = create(directory=directory, title=title)
        di[Project] = project
        print(di[Project])
        new_chapter_editor = ChapterWindow(title=chapter_title, scenes=[])
        create_new_chapter(title=chapter_title, window=new_chapter_editor, scenes=new_chapter_editor.scene_list)
        print(di[Project])
        self.main_window.mdi_layout.addSubWindow(new_chapter_editor)
        self.main_window.show()


class ThemeChoices:
    def select(self):
        ...

    def list(self):
        ...