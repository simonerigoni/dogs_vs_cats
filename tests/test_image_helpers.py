import base64

import dash_app
from src import predict


def test_parse_input_arguments_default(monkeypatch):
    monkeypatch.setattr("sys.argv", ["predict.py"])
    assert predict.parse_input_arguments() == predict.DEFAULT_TEST_IMAGE


def test_parse_input_arguments_custom_path(monkeypatch):
    monkeypatch.setattr("sys.argv", ["predict.py", "--image_path", "data/test/2.jpg"])
    assert predict.parse_input_arguments() == "data/test/2.jpg"


def test_check_extension_match_signature_accepts_png_header():
    content = base64.b64encode(bytes.fromhex("89504e470d0a1a0a0000")).decode()
    assert dash_app.check_extension_match_signature(content, "png") is True


def test_check_extension_match_signature_rejects_mismatched_header():
    content = base64.b64encode(bytes.fromhex("ffd8ff0000000000")).decode()
    assert dash_app.check_extension_match_signature(content, "png") is False


def test_is_file_ok_accepts_valid_png():
    raw = bytes.fromhex("89504e470d0a1a0a0000")
    content = "data:image/png;base64," + base64.b64encode(raw).decode()
    assert dash_app.is_file_ok("cat.png", content) is True


def test_is_file_ok_rejects_bad_extension_and_payload():
    assert dash_app.is_file_ok("cat.txt", "data:image/png;base64,aaaa") is False
    raw = bytes.fromhex("89504e470d0a1a0a0000")
    content = "data:image/png;base64," + base64.b64encode(raw).decode()
    assert dash_app.is_file_ok("cat.gif", content) is False


def test_remove_all_file_from_folder(tmp_path):
    nested = tmp_path / "sub"
    nested.mkdir()
    (tmp_path / "a.txt").write_text("a")
    (nested / "b.txt").write_text("b")
    dash_app.remove_all_file_from_folder(str(tmp_path))
    assert list(tmp_path.iterdir()) == []


def test_save_image_and_get_encoded_image(tmp_path, monkeypatch):
    monkeypatch.setattr(dash_app, "DEFAULT_MEDIA_DIRECTORY", str(tmp_path))
    raw = bytes.fromhex("89504e470d0a1a0a0000")
    content = "data:image/png;base64," + base64.b64encode(raw).decode()
    dash_app.save_image("cat.png", content)
    saved = tmp_path / "cat.png"
    assert saved.read_bytes() == raw
    encoded = dash_app.get_encoded_image(str(saved))
    assert encoded.startswith("data:image/png;base64,")
    payload = encoded.split(",", 1)[1]
    assert base64.b64decode(payload) == raw
