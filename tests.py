import unittest
from datetime import datetime
from scanner import DiskUsage

FOLDER_NAME = 'test_folder'


class TestTest(unittest.TestCase):
    def test_total_files(self):
        diskusage = DiskUsage(FOLDER_NAME)
        self.assertEqual(len(diskusage.get_files_in_directory()), 9)

    def test_extension_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, extension_filter='.exe')
        self.assertEqual(len(diskusage.get_disk_usage()), 1)

    def test_creation_date_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, date_filter='16-10-2023')
        self.assertEqual(len(diskusage.get_disk_usage()), 8)

    def test_nested_level_empty_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, nested_filter='2-30')
        self.assertEqual(len(diskusage.get_disk_usage()), 0)

    def test_nested_level_full_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, nested_filter='0-1')
        self.assertEqual(len(diskusage.get_disk_usage()), 9)

    def test_size_empty_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, size_filter='0b-0b')
        self.assertEqual(len(diskusage.get_disk_usage()), 9)

    def test_size_not_empty_filter(self):
        diskusage = DiskUsage(FOLDER_NAME, size_filter='1b-10kb')
        self.assertEqual(len(diskusage.get_disk_usage()), 1)

if __name__ == "__main__":
    unittest.main()
