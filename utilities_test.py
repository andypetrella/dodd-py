import os
import utilities

# Sample of a working test
def test_uuid():
    uuid = utilities.create_uuid()
    print(os.environ["KENSU_TOKEN"])
    assert len(uuid) == 32
    assert uuid.find('-') == -1
 
# Sample of a failing test
def test_failing():
    print(os.environ["KENSU_TOKEN"])
    uuid = utilities.create_uuid()
    assert uuid is None