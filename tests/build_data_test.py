import logging
import sys
import unittest
import shutil
import os

from dodd.build_data import pipeline, copy
from kensu.utils.exceptions import NrowsConsistencyError

class TestBuildData(unittest.TestCase):
    log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

    target_directory = "tests/output"

    def setUp(self):
        env = os.environ.get("ENV", "").lower()
        if env == "staging":
            self.source_directory = "https://dodd-py-staging.s3.eu-west-3.amazonaws.com"
        elif env == "production":
            self.source_directory = "https://dodd-py-production.s3.eu-west-3.amazonaws.com"
        else:
            self.source_directory = "./data/input"

        os.mkdir(self.target_directory)        

    def tearDown(self):
        try:
            shutil.rmtree(self.target_directory)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def test_pipeline_copy_succeeds_nrows_consistency(self):
        copy(source_directory = self.source_directory, 
            target_directory = self.target_directory)

    def test_pipeline_fails_on_nrows_consistency(self):
        with self.assertRaises(NrowsConsistencyError):
            pipeline(target_directory = self.target_directory)