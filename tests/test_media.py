"""Tests for ducksy.media."""

import discord
import pytest

from ducksy.media import media_dir, random_image


def test_empty_dir_returns_none():
    d = media_dir("call")
    assert d.is_dir()
    assert random_image("call") is None


def test_ignores_non_images_and_dotfiles():
    d = media_dir("call")
    (d / "notes.txt").write_text("not an image")
    (d / "data.json").write_text("{}")
    (d / ".DS_Store").write_bytes(b"")
    (d / ".hidden.png").write_bytes(b"\x89PNG")
    (d / "subdir.png").mkdir()

    assert random_image("call") is None


@pytest.mark.parametrize("filename", ["a.png", "B.JPG", "c.jpeg", "d.GiF", "e.webp"])
def test_picks_an_image(filename):
    d = media_dir("call")
    (d / "ignore.txt").write_text("nope")
    (d / ".secret.jpg").write_bytes(b"nope")
    (d / filename).write_bytes(b"fake-image-bytes")

    picked = random_image("call")
    assert isinstance(picked, discord.File)
    try:
        assert picked.filename == filename
    finally:
        picked.close()


@pytest.mark.parametrize("name", ["../etc", "Caps", "", "a/b"])
def test_rejects_bad_names(name):
    with pytest.raises(ValueError):
        media_dir(name)
