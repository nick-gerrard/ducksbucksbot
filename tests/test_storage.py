import pytest

from ducksy.storage import Store


def test_roundtrip():
    s = Store("counter")
    assert s.load() == {}
    s.save({"n": 1})
    assert Store("counter").load() == {"n": 1}


@pytest.mark.parametrize("name", ["../etc", "Caps", "", "a/b"])
def test_rejects_bad_names(name):
    with pytest.raises(ValueError):
        Store(name)


def test_size_limit():
    with pytest.raises(ValueError):
        Store("big").save({"x": "y" * 300_000})
