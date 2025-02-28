"""Test doit_tasks/test.py."""

from calcipy.doit_tasks.test import (
    task_check_types, task_coverage, task_open_test_docs, task_ptw_current, task_ptw_ff,
    task_ptw_marker, task_ptw_not_chrome, task_test, task_test_all, task_test_keyword, task_test_marker,
)


def test_task_test():
    """Test task_test."""
    result = task_test()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).endswith('" -x -l --ff --nf -vv')


def test_task_test_all():
    """Test task_test_all."""
    result = task_test_all()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).endswith('" --ff -vv')


def test_task_test_marker():
    """Test task_test_marker."""
    result = task_test_marker()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).endswith('" -x -l --ff --nf -vv -m "%(marker)s"')
    params = result['params']
    assert len(params) == 1
    assert params[0]['name'] == 'marker'
    assert params[0]['short'] == 'm'


def test_task_test_keyword():
    """Test task_test_keyword."""
    result = task_test_keyword()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).endswith('" -x -l --ff --nf -vv -k "%(keyword)s"')
    params = result['params']
    assert len(params) == 1
    assert params[0]['name'] == 'keyword'
    assert params[0]['short'] == 'k'


def test_task_coverage():
    """Test task_coverage."""
    result = task_coverage()

    actions = result['actions']
    assert len(actions) == 4
    assert '--cov-report=html' in str(actions[0])
    assert 'coverage xml' in str(actions[1])
    assert 'diff-cover' in str(actions[2])
    assert 'python -m coverage json' in str(actions[3])


def task_task_check_types():
    """Test task_check_types."""
    result = task_check_types()

    actions = result['actions']
    assert 2 <= len(actions) > 1
    assert str(actions[0]).startswitch('poetry run ')


def task_task_open_test_docs():
    """Test task_open_test_docs."""
    result = task_open_test_docs()

    actions = result['actions']
    assert 3 <= len(actions) > 2


def task_task_ptw_not_chrome():
    """Test task_ptw_not_chrome."""
    result = task_ptw_not_chrome()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).startswitch('poetry run ptw -- "')
    assert str(actions[0]).endswitch('" -m "not CHROME" -vvv')


def task_task_ptw_ff():
    """Test task_ptw_ff."""
    result = task_ptw_ff()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).startswitch('poetry run ptw -- "')
    assert str(actions[0]).endswitch('" --last-failed --new-first -m "not CHROME" -vv')


def task_task_ptw_current():
    """Test task_ptw_current."""
    result = task_ptw_current()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).startswitch('poetry run ptw -- "')
    assert str(actions[0]).endswitch('" -m "CURRENT" -vv')


def test_task_ptw_marker():
    """Test task_ptw_marker."""
    result = task_ptw_marker()

    actions = result['actions']
    assert len(actions) == 1
    assert str(actions[0]).endswith('" -vvv -m "%(marker)s"')
    params = result['params']
    assert len(params) == 1
    assert params[0]['name'] == 'marker'
    assert params[0]['short'] == 'm'
