async function importKey(rawKey) {
    return await window.crypto.subtle.importKey(
        'raw',
        rawKey,
        'AES-GCM',
        true,
        ['encrypt', 'decrypt']
    );
}

async function decryptText(key, ciphertext, iv) {
    const decodedCiphertext = Uint8Array.from(atob(ciphertext), c => c.charCodeAt(0));
    const decodedIv = Uint8Array.from(atob(iv), c => c.charCodeAt(0));

    const decryptedData = await window.crypto.subtle.decrypt(
        {
            name: 'AES-GCM',
            iv: decodedIv,
        },
        key,
        decodedCiphertext
    );

    return new TextDecoder().decode(decryptedData);
}

document.addEventListener('DOMContentLoaded', async () => {
    const encryptedTexts = document.querySelectorAll('.encrypted-text');

    if (encryptedTexts.length > 0) {
        const storedKey = localStorage.getItem('encryptionKey');
        if (storedKey) {
            const rawKeyArray = JSON.parse(storedKey);
            const rawKey = new Uint8Array(rawKeyArray);

            try {
                const key = await importKey(rawKey);

                encryptedTexts.forEach(async (encryptedTextElem) => {
                    const encryptedData = encryptedTextElem.dataset.encryptedText;

                    if (encryptedData) {
                        const [iv, ciphertext] = encryptedData.split(':');
                        if (iv && ciphertext) {
                            try {
                                const decryptedText = await decryptText(key, ciphertext, iv);
                                encryptedTextElem.textContent = decryptedText;
                            } catch (error) {
                                console.error('Ошибка при расшифровке текста:', error);
                            }
                        }
                    }
                });
            } catch (error) {
                console.error('Ошибка при импорте ключа:', error);
            }
        }
    }
});
