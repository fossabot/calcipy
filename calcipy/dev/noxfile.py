"""nox-poetry configuration file.

[Useful snippets from docs](https://nox.thea.codes/en/stable/usage.html)

```sh
poetry run nox -l
poetry run nox --list-sessions

poetry run nox -s build_check-3.9 build_dist-3.9 check_safety-3.9
poetry run nox --session check_safety-3.9

poetry run nox --python 3.8

poetry run nox -k "not tests and not check_safety"
```

Useful nox snippets

```py
# Example conditionally skipping a session
if not session.interactive:
    session.skip('Cannot run detect-secrets audit in non-interactive shell')

# Install pinned version
session.install('detect-secrets==1.0.3')

# Example capturing STDOUT into a file (could do the same for stderr)
path_stdout = Path('.stdout.txt').resolve()
with open(path_stdout, 'w') as out:
    session.run(*shlex.split('echo Hello World!'), stdout=out)
```

"""

import re
import shlex
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse
from urllib.request import url2pathname

from loguru import logger

from ..doit_tasks.doit_globals import DG, DoitAction, DoitTask
from ..doit_tasks.test import task_coverage, task_test
from ..file_helpers import if_found_unlink

has_test_imports = False
try:
    from nox_poetry import session
    from nox_poetry.poetry import DistributionFormat
    from nox_poetry.sessions import Session
    has_test_imports = True
except ImportError:  # pragma: no cover
    pass

if has_test_imports:  # pragma: no cover  # noqa: C901
    def _run_str_cmd(session: Session, cmd_str: str) -> None:
        """Run a command string. Ensure that poetry is left-stripped.

        Args:
            session: nox_poetry Session
            cmd_str: string command to run

        """
        cmd_str = re.sub(r'^poetry run ', '', cmd_str)
        session.run(*shlex.split(cmd_str), stdout=True)

    def _run_func_cmd(action: DoitAction) -> None:
        """Run a python action.

        Args:
            action: doit python action

        Raises:
            RuntimeError: if a function action fails

        """
        # https://pydoit.org/tasks.html#python-action
        func, args, kwargs = [*list(action), {}][:3]
        result = func(args, **kwargs)
        if result not in [True, None] or not isinstance(result, (str, dict)):
            raise RuntimeError(f'Returned {result}. Failed to run task: {action}')

    def _run_doit_task(session: Session, task_fun: Callable[[], DoitTask]) -> None:
        """Run a DoitTask actions without using doit.

        Args:
            session: nox_poetry Session
            task_fun: function that returns a DoitTask

        Raises:
            NotImplementedError: if the action is of an unknown type

        """
        task = task_fun()
        for action in task['actions']:
            if isinstance(action, str):
                _run_str_cmd(session, action)
            elif getattr(action, 'action', None):
                _run_str_cmd(session, action.action)
            elif isinstance(action, (list, tuple)):
                _run_func_cmd(action)
            else:
                raise NotImplementedError(f'Unable to run {action} ({type(action)})')

    @session(python=DG.test.pythons, reuse_venv=True)
    def tests(session: Session) -> None:
        """Run doit test task for specified python versions.

        Args:
            session: nox_poetry Session

        """
        session.install('.[dev]', '.[test]')
        _run_doit_task(session, task_test)

    @session(python=[DG.test.pythons[-1]], reuse_venv=True)
    def coverage(session: Session) -> None:
        """Run doit test task for specified python versions.

        Args:
            session: nox_poetry Session

        """
        session.install('.[dev]', '.[test]')
        _run_doit_task(session, task_coverage)

    @session(python=[DG.test.pythons[-1]], reuse_venv=False)
    def build_dist(session: Session) -> None:
        """Build the project files within a controlled environment for repeatability.

        Args:
            session: nox_poetry Session

        """
        if_found_unlink(DG.meta.path_project / 'dist')
        path_wheel = session.poetry.build_package()
        logger.info(f'Created wheel: {path_wheel}')
        # Install the wheel and check that imports without any of the optional dependencies
        session.install(path_wheel)
        session.run(*shlex.split('python scripts/check_imports.py'), stdout=True)

    @session(python=[DG.test.pythons[-1]], reuse_venv=True)
    def build_check(session: Session) -> None:
        """Check that the built output meets all checks.

        Args:
            session: nox_poetry Session

        """
        # Build sdist and fix return URI, which will have file://...#egg=calcipy
        sdist_uri = session.poetry.build_package(distribution_format=DistributionFormat.SDIST)
        path_sdist = Path(url2pathname(urlparse(sdist_uri).path))
        logger.debug(f'Fixed sdist URI ({sdist_uri}): {path_sdist}')
        # Check with pyroma
        session.install('pyroma', '--upgrade')
        # PLANNED: Troubleshoot why pyroma score is so low (6/10)
        session.run('pyroma', '--file', path_sdist.as_posix(), '--min=6', stdout=True)

    @session(python=[DG.test.pythons[-1]], reuse_venv=True)
    def check_safety(session: Session) -> None:
        """Check for known vulnerabilities with safety.

        Based on: https://github.com/pyupio/safety/issues/201#issuecomment-632627366

        Args:
            session: nox_poetry Session

        Raises:
            RuntimeError: if safety exited with errors, but not caught by session

        """
        # Note: safety requires a requirements.txt file and doesn't support pyproject.toml yet
        session.poetry.export_requirements()
        # Install and run
        session.install('safety', '--upgrade')
        path_report = Path('insecure_report.json').resolve()
        logger.info(f'Creating safety report: {path_report}')
        session.run(*shlex.split(f'safety check --full-report --cache --output {path_report} --json'), stdout=True)
        if path_report.read_text().strip() != '[]':
            raise RuntimeError(f'Found safety warnings in {path_report}')
        path_report.unlink()
