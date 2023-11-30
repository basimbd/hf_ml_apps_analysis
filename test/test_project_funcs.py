import unittest
from os import path, makedirs
from src.utils.common_utils import PROJECT_DIR
from src.utils.repo_utils import delete_directory


class MyTestCase(unittest.TestCase):
    def test_directory_deletion(self):
        if not path.exists(f"{PROJECT_DIR}/my_test_dir/"):
            makedirs(f"{PROJECT_DIR}/my_test_dir/")
        delete_directory("my_test_dir")
        self.assertEqual(False, path.exists(f"{PROJECT_DIR}/my_test_dir/"))


if __name__ == '__main__':
    unittest.main()
