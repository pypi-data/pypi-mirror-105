import unittest
import folders
import os

class TestFolders(unittest.TestCase):

    def test_get_file_name(self):
        result = folders.get_file_name("Base\Slides\pass.svs")
        #Test folders
        self.assertEquals(result, "pass")
        #Test no folders
        self.assertEquals(folders.get_file_name("no_parent_folder.jpg"), "no_parent_folder")

    

    def test_is_folder(self):
        directory_path = "test_dir"
        folders.is_folder(directory_path)
        self.assertTrue(os.path.exists("./"+directory_path))
        os.rmdir(directory_path)


    

if __name__ == '__main__':
    unittest.main()