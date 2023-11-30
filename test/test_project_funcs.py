import unittest
from os import path, makedirs
from src.utils.common_utils import PROJECT_DIR, dict_to_csv, run_shell_command
from src.utils.repo_utils import delete_directory
from src.utils import space_utils


class MyTestCase(unittest.TestCase):
    def test_directory_deletion(self):
        if not path.exists(f"{PROJECT_DIR}/my_test_dir/"):
            makedirs(f"{PROJECT_DIR}/my_test_dir/")
        delete_directory("my_test_dir")
        self.assertEqual(False, path.exists(f"{PROJECT_DIR}/my_test_dir/"))

    def test_fetching_spaces(self):
        # Test when a spaces are fetched for a model, all the spaces have used that model.
        MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
        model_exists = True
        for space in space_utils.get_spaces_by_model(MODEL_NAME):
            if MODEL_NAME not in space.models:
                model_exists = False
                break
        self.assertEqual(True, model_exists)

    def test_dict_to_csv_writer(self):
        test_dict = {"key1": 1, "key2": 2, "key3": 3}
        DICT_CSV_PATH = f"{PROJECT_DIR}/output/test_dict.csv"
        dict_to_csv(test_dict, DICT_CSV_PATH, ["key", "value"])
        path_exists = path.exists(DICT_CSV_PATH)
        run_shell_command(f"rm -rf {DICT_CSV_PATH}")
        self.assertEqual(True, path_exists)


if __name__ == '__main__':
    unittest.main()
