"""Check that all imports work as expected.

Primarily checking that:

1. No optional dependencies are required

FIXME: Replace with programmatic imports? Maybe explicit imports to check backward compatibility of public API?
    https://stackoverflow.com/questions/34855071/importing-all-functions-from-a-package-from-import

"""

from calcipy.conftest import *
from calcipy.file_helpers import *
from calcipy.log_helpers import *
from calcipy.wrappers import *

from calcipy.doit_tasks import *

from pprint import pprint
pprint(locals())
