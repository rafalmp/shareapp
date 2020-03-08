from shareapp.main.forms import UrlForm


class TestUrlForm:
    def test_invalid_url(self, fake):
        form = UrlForm({"url": fake.word()})
        assert form.is_valid() is False

    def test_valid_url(self, fake):
        form = UrlForm({"url": fake.uri()})
        assert form.is_valid()
