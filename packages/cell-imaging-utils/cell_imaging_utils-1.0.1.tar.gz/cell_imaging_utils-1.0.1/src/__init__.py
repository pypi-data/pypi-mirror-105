from src.datasets_metadata.datasetes__metadata_scv import DatasetMetadataSCV
from src.datasets_metadata.datasetes__metadata_pickle import DatasetMetadataPickle

__author__ = "Lion Ben Nedava"
__email__ = "lionben89@gmail.com"
__version__ = "1.0.0"


def get_module_version():
    return __version__


__all__ = ["DatasetMetadataSCV", "DatasetMetadataPickle"]
