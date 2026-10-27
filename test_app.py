import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from groq import APIConnectionError
from streamlit.testing.v1 import AppTest
import httpx


class TicketAppTests(unittest.TestCase):
    def analyze(self, content=None, error=None):
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}), patch("groq.Groq") as groq:
            create = groq.return_value.chat.completions.create
            create.side_effect = error
            create.return_value = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
            )
            app = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
            app.text_area[0].input("My package never arrived.")
            app.button[0].click().run()
            self.assertFalse(app.exception)
            self.assertEqual(create.call_args.kwargs["max_tokens"], 1000)
            self.assertNotIn("response_format", create.call_args.kwargs)
            return app

    def test_text_analysis(self):
        text = "Category: Delivery\n\nSummary: The package never arrived."
        app = self.analyze(text)
        self.assertEqual(app.markdown[-1].value, text)
        self.assertFalse(app.json)
        self.assertFalse(app.error)

    def test_api_failure(self):
        error = APIConnectionError(request=httpx.Request("POST", "https://example.com"))
        app = self.analyze(error=error)
        self.assertIn("Could not analyze", app.error[0].value)

if __name__ == "__main__":
    unittest.main()
