import pytest

from secret import rgb2hex, hex2rgb, encodeblue, encodegreen, decodeblue, decodegreen


def test_rgb2hex():
    assert rgb2hex(0, 0, 0) == "#000000"
    assert rgb2hex(255, 255, 255) == "#ffffff"
    assert rgb2hex(0, 0, 255) == "#0000ff"
    assert rgb2hex(0, 255, 0) == "#00ff00"
    assert rgb2hex(255, 0, 0) == "#ff0000"


def test_hex2rgb():
    assert hex2rgb("#000000") == (0, 0, 0)
    assert hex2rgb("#ffffff") == (255, 255, 255)
    assert hex2rgb("#0000ff") == (0, 0, 255)
    assert hex2rgb("#00ff00") == (0, 255, 0)
    assert hex2rgb("#ff0000") == (255, 0, 0)

def test_encodeblue():
    assert encodeblue("#000000", "1") == "#000001"
    assert encodeblue("#000007", "1") is None
    assert encodeblue("#000005", "1") == "#000001"
    assert encodeblue("#000001", "1") == "#000001"

def test_encodegreen():
    assert encodegreen("#000700", "1") is None
    assert encodegreen("#000500", "1") == "#000100"
    assert encodegreen("#000100", "1") == "#000100"

def test_decodeblue():
    assert decodeblue("#000000") == "0"
    assert decodeblue("#000007") is None

def test_decodegreen():
    assert decodegreen("#000100") == "1"
    assert decodegreen("#000700") is None