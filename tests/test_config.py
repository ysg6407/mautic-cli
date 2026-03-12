from mautic_cli.config import ConfigManager


def test_load_returns_empty_dict_when_no_file(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    assert mgr.load() == {}


def test_save_and_load_roundtrip(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    data = {"base_url": "https://mautic.example.com", "auth_method": "basic"}
    mgr.save(data)
    assert mgr.load() == data


def test_save_creates_directory(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({"key": "value"})
    assert tmp_config_dir.exists()


def test_load_named_profile(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({"base_url": "https://a.example.com"}, profile="staging")
    result = mgr.load(profile="staging")
    assert result["base_url"] == "https://a.example.com"


def test_default_profile_is_default(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({"base_url": "https://a.example.com"})
    assert (tmp_config_dir / "config.json").exists()
