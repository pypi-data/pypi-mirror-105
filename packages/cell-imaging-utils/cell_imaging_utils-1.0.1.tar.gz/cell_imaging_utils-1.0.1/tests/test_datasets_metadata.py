import os
import logging

from BGU_cell_imaging_utils.src.datasets_metadata.datasetes__metadata_scv import DatasetMetadataSCV

log = logging.getLogger(__name__)
svcs_save_dir = "{}\\svcs".format(os.getcwd())
results_save_dir = "{}\\results".format(os.getcwd())


organelle_name = "Nuclear_envelop"
train_file_name = "image_list_train.csv"
test_file_name = "image_list_test.csv"

if not os.path.exists(results_save_dir):
    os.makedirs(results_save_dir)

def test_datasets_metadata() -> None:
    seg_image_list_train = DatasetMetadataSCV("{}\\{}\\{}".format(svcs_save_dir,organelle_name,train_file_name),"{}\\{}\\{}".format(results_save_dir,organelle_name,train_file_name))
    print(seg_image_list_train.get_table())
    
    return None


test_datasets_metadata()