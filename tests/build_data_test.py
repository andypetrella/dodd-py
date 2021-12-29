import logging
import sys
import unittest
import shutil

from src.build_data import pipeline, copy
from kensu.utils.exceptions import NrowsConsistencyError

class MyTest(unittest.TestCase):
    log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

    target_directory = "tests/output"

    def setUp(self):
        import os
        os.mkdir(self.target_directory)

    def tearDown(self):
        import shutil
        try:
            shutil.rmtree(self.target_directory)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def test_pipeline_copy_succeeds_nrows_consistency(self):
        copy(target_directory = self.target_directory)

    def test_pipeline_fails_on_nrows_consistency(self):
        with self.assertRaises(NrowsConsistencyError):
            pipeline(target_directory = self.target_directory)