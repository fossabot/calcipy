"""doit Helpers.

Register all defaults doit tasks in a dodo.py file with the below snippet:

`from calcipy.doit_tasks import *  # noqa: F401,F403,H303 (Run 'doit list' to see tasks). skipcq: PYL-W0614`

"""

__all__ = [  # noqa: F405
    'DOIT_CONFIG_RECOMMENDED',
    'TASKS_CI',
    'TASKS_LOCAL',
    # from .code_tag_collector
    'task_collect_code_tags',
    # from .doc
    'task_cl_bump_pre',
    'task_cl_bump',
    'task_cl_write',
    'task_deploy',
    'task_document',
    'task_open_docs',
    'task_serve_docs',
    # from .lint
    'task_auto_format',
    'task_lint_critical_only',
    'task_lint_project',
    'task_lint_python',
    'task_pre_commit_hooks',
    'task_radon_lint',
    'task_security_checks',
    # from .packaging
    'task_check_for_stale_packages',
    'task_lock',
    'task_publish',
    # from .test
    'task_check_types',
    'task_coverage',
    'task_nox_test',
    'task_nox_coverage',
    'task_nox',
    'task_open_test_docs',
    'task_ptw_current',
    'task_ptw_ff',
    'task_ptw_marker',
    'task_ptw_not_chrome',
    'task_test_all',
    'task_test_keyword',
    'task_test_marker',
    'task_test',
]

from getpass import getuser

from .code_tag_collector import task_collect_code_tags
from .doc import *  # noqa: F401,F403,H303. lgtm [py/polluting-import]
from .lint import *  # noqa: F401,F403,H303. lgtm [py/polluting-import]
from .packaging import *  # noqa: F401,F403,H303. lgtm [py/polluting-import]
from .test import *  # noqa: F401,F403,H303. lgtm [py/polluting-import]

TASKS_CI = [
    'nox_test',
    'nox_coverage',
    'pre_commit_hooks',
    'security_checks',
]
"""More forgiving tasks to be run in CI."""

TASKS_LOCAL = [
    'collect_code_tags',
    'cl_write',
    'lock',
    'nox_coverage',
    'auto_format',
    'document',
    'check_for_stale_packages',
    'pre_commit_hooks',
    'lint_project',
    'security_checks',
    'check_types',
]
"""Full suite of tasks for local development."""

DOIT_CONFIG_RECOMMENDED = {
    'action_string_formatting': 'old',  # Required for keyword-based tasks
    'default_tasks': TASKS_CI if getuser().lower() == 'appveyor' else TASKS_LOCAL,
}
"""doit Configuration Settings. Run with `poetry run doit`."""
