from django.core.files.uploadedfile import SimpleUploadedFile

from shareapp.main.forms import UrlForm, FileForm
from shareapp.main.models import SharedItem


class TestUrlForm:
    def test_invalid_url(self, fake):
        form = UrlForm({"url": fake.word()})
        assert form.is_valid() is False

    def test_valid_url(self, fake):
        form = UrlForm({"url": fake.uri()})
        assert form.is_valid()

    def test_save(self, fake, create_user):
        url = fake.uri()
        user = create_user()
        form = UrlForm({"url": url})
        form.is_valid()
        item = form.save(user)

        assert isinstance(item, SharedItem)
        assert SharedItem.objects.filter(url=url).exists()


class TestFileForm:
    def test_valid_form(self, fake):
        file_name = fake.file_name()
        content = fake.binary(length=1024)
        form = FileForm(files={"file": SimpleUploadedFile(file_name, content)})
        assert form.is_valid()

    def test_save(self, fake, create_user):
        file_name = fake.file_name()
        content = fake.binary(length=1024)
        user = create_user()
        form = FileForm(files={"file": SimpleUploadedFile(file_name, content)})
        form.is_valid()
        item = form.save(user)

        assert isinstance(item, SharedItem)
        assert SharedItem.objects.filter(file__endswith=file_name).exists()
