import pytest

import hwte
from hwte.file_utils import requires_package


def test_version():
    assert len(hwte.__version__.split(".")) == 3


def test_requires_package():
    requires_package("numpy")  # available
    with pytest.raises(ImportError):  # not available
        requires_package("non_existent_package")
