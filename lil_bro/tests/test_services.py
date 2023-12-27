from lil_bro.services import Encryptor, sha256_hash, make_link
from unittest import TestCase


class TestEncryptor(TestCase):
    def setUp(self) -> None:
        self.plain_text: str = 'test_plain_text'
        self.enc = Encryptor()

    def test_encryptor(self):
        encrypted_text = self.enc.encrypt_text(self.plain_text)
        self.assertNotEquals(self.plain_text, encrypted_text)

        decrypted_text = self.enc.decrypt_text(encrypted_text)
        self.assertEqual(self.plain_text, decrypted_text)


class TestHash(TestCase):
    def setUp(self) -> None:
        self.plain_text: str = 'plain_text'

    def test_sha256_hash(self):
        hashed_text = sha256_hash(self.plain_text)
        self.assertEqual(hashed_text, 'ae408e769d0d5e2af62058cae7e033d82628ea21ab7770ce190be7efde38b77c')


class TestLink(TestCase):
    def setUp(self) -> None:
        self.pk: str = 'ae408e769d0d5e2af62058ca'

    def test_make_link(self):
        link = make_link(self.pk)
        self.assertEqual(link, f"http://127.0.0.1:8000/secret/{self.pk}/")
