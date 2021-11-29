from dataclasses import dataclass
from typing import List, Optional

from front_end.load_screen.models import ChapterWindow, SceneEditor


@dataclass
class Chapter:
    title: str
    window: ChapterWindow
    scenes: Optional[List[SceneEditor]]


@dataclass
class Project:
    title: str
    folder_location: str
    chapters: Optional[List[Chapter]]