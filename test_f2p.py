import sys
import pytest


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
def test_single_instance_lock_windows(tmp_path, monkeypatch):
    """
    This test ensures SingleInstance works on Windows.

    FAIL before fix:
        ImportError: No module named 'fcntl'

    PASS after fix:
        Uses msvcrt.locking successfully
    """

    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    from src.main import SingleInstance

    instance = SingleInstance("test-app")

    assert instance.try_lock() is True

    instance2 = SingleInstance("test-app")
    assert instance2.try_lock() is False

    instance.release()

    instance3 = SingleInstance("test-app")
    assert instance3.try_lock() is True
    instance3.release()
    