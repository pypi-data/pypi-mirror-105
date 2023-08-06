import os
from typing import Set
from .platform import Platform
from ..settings import Settings


class MacOS(Platform):

    def extract(self):
        import tarfile
        tar = tarfile.open(Settings.download_path, "r:gz")
        tar.extractall()
        tar.close()
