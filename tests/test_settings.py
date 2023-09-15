import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSettingsStandard(unittest.TestCase):
    def setUp(self):
        import os

        os.environ["TG_TOKEN"] = "token"
        os.environ["TG_PREFIX"] = "/prefix/"
        os.environ["TG_WEBHOOK_CUSTOM_URL"] = ""
        os.environ["HOST"] = "100.0.0.1/"
        os.environ["PORT"] = "7999"

    def test_settings_standard(self):
        from utils.settings import Settings

        settings = Settings()
        self.assertEqual(settings.host, "100.0.0.1")
        self.assertEqual(
            settings.get_tg_webhook_url(), "https://100.0.0.1:7999/prefix/token"
        )


class TestSettingsCustom(unittest.TestCase):
    def setUp(self):
        import os

        os.environ["TG_TOKEN"] = "token"
        os.environ["TG_PREFIX"] = "prefix"
        os.environ["TG_WEBHOOK_CUSTOM_URL"] = "some.com/foo"
        os.environ["HOST"] = "100.0.0.1/"
        os.environ["PORT"] = "7999"

    def test_settings_custom(self):
        from utils.settings import Settings

        settings = Settings()
        self.assertEqual(settings.host, "100.0.0.1")
        self.assertEqual(
            settings.get_tg_webhook_url(), "https://some.com/foo/prefix/token"
        )


class TestSettingsNgrok(unittest.TestCase):
    def setUp(self):
        import os

        os.environ["TG_TOKEN"] = "token"
        os.environ["TG_PREFIX"] = "prefix"
        os.environ["TG_WEBHOOK_CUSTOM_URL"] = "ngrok.io"
        os.environ["HOST"] = "100.0.0.1/"
        os.environ["PORT"] = "7999"

    def test_settings_ngrok(self):
        from utils.settings import Settings

        settings = Settings()
        self.assertEqual(settings.host, "100.0.0.1")
        self.assertEqual(settings.is_ngrok_enabled(), True)
