from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from shareapp.main.forms import UrlForm, FileForm


class TestUrlForm:
    def test_invalid_url(self, fake):
        form = UrlForm({"url": fake.word()})
        assert form.is_valid() is False

    def test_valid_url(self, fake):
        form = UrlForm({"url": fake.uri()})
        assert form.is_valid()


class TestFileForm:
    def test_valid_form(self, fake):
        file_name = fake.file_name()
        content = fake.binary(length=1024)
        form = FileForm(files={"file": SimpleUploadedFile(file_name, content)})
        assert form.is_valid()
