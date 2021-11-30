import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from kink import di

from shared.dataclasses import Project


@dataclass
class ChapterData:
    title: str
    scenes: List[str]


def load(directory: str):
    print(directory)
    with open(directory, 'r') as f:
        chapter_list_raw = f.read()
    chapter_split_list = chapter_list_raw.split("OSMOSISCHAPTERSTART")
    title = re.search(r"TITLE(.*?)START", chapter_split_list[0]).group(1)
    del chapter_split_list[0]
    chapter_data = []
    for chapter_path in chapter_split_list:
        print(chapter_path)
        chapter_title = re.search(r"chapters/(.*?).osmc", chapter_split_list[0]).group(1)
        with open(chapter_path, 'r') as f:
            print("reading")
            all_scenes = f.read()
        scene_list = all_scenes.split("OSMOSISSCENEBREAK")
        scene_list.remove("")
        chapter_data.append(ChapterData(title=chapter_title, scenes=scene_list))

    parent_directory = directory.split(f"{title}.osm")[0]
    return Project(title=title, folder_location=parent_directory, chapters=[]), chapter_data


def create(directory: str, title: str):
    full_directory = directory + "/" + title
    return Project(title=title, folder_location=full_directory, chapters=[])


def save():
    project = di[Project]
    print(type(project))
    if not Path.is_dir(Path(project.folder_location)):
        Path.mkdir(Path(project.folder_location))
        Path.mkdir(Path(f"{project.folder_location}/chapters/"))
    osm_file_contents = f"TITLE{project.title}START"
    for chapter in project.chapters:
        chapter_path = f"{project.folder_location}/chapters/{chapter.title}.osmc"
        new_chapter_identifier = f"OSMOSISCHAPTERSTART{chapter_path}"
        osm_file_contents = osm_file_contents + new_chapter_identifier
        with open(chapter_path, 'w+') as f:
            for scene in chapter.scenes:
                f.write("OSMOSISSCENEBREAK")
                f.write(scene.toHtml())
    osm_file_location = f"{project.folder_location}/{project.title}.osm"
    with open(osm_file_location, 'w+') as f:
        f.write(osm_file_contents)
