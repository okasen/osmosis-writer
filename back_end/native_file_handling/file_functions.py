
from dataclasses import dataclass
from pathlib import Path
from typing import List

from kink import inject, di

from shared.dataclasses import Project


@dataclass
class ChapterData:
    title: str
    scenes: List[str]


def load(directory: str, title: str):
    test_chapter_data = ChapterData(title="chapter one", scenes=["text"])
    return Project(title="test", folder_location="C:/Users/Jenni/test_project/", chapters=None), [test_chapter_data]


def create(directory: str, title: str):
    full_directory = directory + "/" + title
    return Project(title=title, folder_location=full_directory, chapters=[])


def save():
    project = di[Project]
    print("saving")
    print(type(project))
    if not Path.is_dir(Path(project.folder_location)):
        print("making new folder")
        Path.mkdir(Path(project.folder_location))
        Path.mkdir(Path(f"{project.folder_location}/chapters/"))
        print("made")
    osm_file_contents = f"***TITLE***={project.title}***START***="
    for chapter in project.chapters:
        chapter_path = f"{project.folder_location}/chapters/{chapter.title}.osmc"
        new_chapter_identifier = f"***CHAPTERSTART***{chapter_path}***CHAPTEREND***"
        osm_file_contents = osm_file_contents + new_chapter_identifier
        with open(chapter_path, 'w+') as f:
            for scene in chapter.scenes:
                f.write("***SCENEBREAK***")
                f.write(scene.toHtml())
    osm_file_location = f"{project.folder_location}/{project.title}.osm"
    with open(osm_file_location, 'w+') as f:
        f.write(osm_file_contents)
