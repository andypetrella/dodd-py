import os
import utilities

# Sample of a working test
def test_uuid():
    uuid = utilities.create_uuid()
    assert len(uuid) == 32
    assert uuid.find('-') == -1
 
# Sample of a failing test
def test_failing():
    uuid = utilities.create_uuid()
    assert os.environ["KENSU_TOKEN"] is None
    assert uuid is None