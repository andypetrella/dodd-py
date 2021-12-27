import os
import utilities

# Sample of a working test
def test_uuid():
    uuid = utilities.create_uuid()
    assert len(uuid) == 32
    assert uuid.find('-') == -1

    if os.environ["ENV"] in ["Development", "Production"]:
        assert os.environ["KENSU_TOKEN"] is None
    else:
        assert os.environ["KENSU_TOKEN"] == ''