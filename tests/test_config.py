from src import config


def test_config_defaults():
    assert config.DATA_FOLDER == "data/"
    assert config.KAGGLE_FOLDER.endswith("kaggle/train/")
    assert config.GCP_FOLDER.endswith("gcp/")
    assert config.CSV_FILENAME == "all_data.csv"
    assert config.LABELS == ["cat", "dog"]
    assert config.DEFAULT_TEST_IMAGE.endswith("test/1.jpg")
