from app.utils.trim_words import trim_words


def test_trim_words():
    assert trim_words("one two three", 2) == "one two…"
