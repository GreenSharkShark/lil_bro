import base64
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
from botocore.session import Session
from config.settings import key_arn
import hashlib


class Encryptor:
    """
    Encrypts and decrypts data using AWS KMS
    """

    def __init__(self):
        """
        str key: Amazon Resource Name (ARN) of the &KMS; key
        botocore_session: existing botocore session instance
        type botocore_session: botocore.session.Session
        """
        self.key = key_arn
        self.botocore_session = Session()

    def __setup(self):
        """
            Set up an encryption client with an explicit commitment policy. If you do not explicitly choose a
            commitment policy, REQUIRE_ENCRYPT_REQUIRE_DECRYPT is used by default.
        """

        client = aws_encryption_sdk.EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)

        # Create an AWS KMS master key provider
        kms_kwargs = dict(key_ids=[self.key])
        if self.botocore_session is not None:
            kms_kwargs["botocore_session"] = self.botocore_session
        master_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(**kms_kwargs)

        return master_key_provider, client

    def encrypt_text(self, source_plaintext: str) -> str:

        master_key_provider, client = self.__setup()

        # Encrypt the plaintext source data
        ciphertext, encryptor_header = client.encrypt(source=source_plaintext, key_provider=master_key_provider)

        #  Converting bytes to a string for saving in the database
        ciphertext_str = base64.b64encode(ciphertext).decode('utf-8')

        return ciphertext_str

    def decrypt_text(self, ciphertext: str) -> str:

        master_key_provider, client = self.__setup()

        # Converting string to bytes for decryption
        ciphertext_bytes = base64.b64decode(ciphertext)

        # Decrypt the ciphertext
        cycled_plaintext, decrypted_header = client.decrypt(source=ciphertext_bytes, key_provider=master_key_provider)

        #  Converting bytes to a string
        plaintext = cycled_plaintext.decode('utf-8')

        return plaintext


def sha256_hash(text):
    # Преобразовываем текст в байтовую строку (так как hashlib работает с байтами)
    text_bytes = text.encode('utf-8')

    # Создаем объект хеша SHA-256
    sha256 = hashlib.sha256()

    # Обновляем хеш с байтами текста
    sha256.update(text_bytes)

    # Получаем хэшированное значение в виде шестнадцатеричной строки
    hashed_text = sha256.hexdigest()

    return hashed_text


def make_link(hash: str) -> str:
    return f"http://127.0.0.1:8000/secret/{hash}/"
