async function generateKey() {
    // Генерируем ключ только если его нет в localStorage
    const storedKey = localStorage.getItem('encryptionKey');
    if (storedKey) {
        console.log('Ключ уже существует в localStorage.');
        const rawKeyArray = JSON.parse(storedKey);
        const rawKey = new Uint8Array(rawKeyArray);
        return await window.crypto.subtle.importKey(
            'raw',
            rawKey,
            'AES-GCM',
            true,
            ['encrypt', 'decrypt']
        );
    } else {
        // Генерируем новый ключ и сохраняем его
        const key = await window.crypto.subtle.generateKey(
            {
                name: "AES-GCM",
                length: 256,
            },
            true,
            ["encrypt", "decrypt"]
        );
        const exportedKey = await window.crypto.subtle.exportKey('raw', key);
        localStorage.setItem('encryptionKey', JSON.stringify(Array.from(new Uint8Array(exportedKey))));
        console.log('Новый ключ сгенерирован и сохранен в localStorage.');
        return key;
    }
}

async function encryptText(key, text) {
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const encodedText = new TextEncoder().encode(text);

    const ciphertext = await window.crypto.subtle.encrypt(
        {
            name: "AES-GCM",
            iv: iv,
        },
        key,
        encodedText
    );

    return {
        ciphertext: new Uint8Array(ciphertext),
        iv: iv
    };
}

function toBase64(arr) {
    return btoa(String.fromCharCode(...arr));
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector('form');
    const lifetimeField = document.querySelector('select[name="lifetime_select_field"]');

    if (form && lifetimeField) {
        form.addEventListener("submit", async (event) => {
            if (lifetimeField.value === '1') {
                event.preventDefault();

                const textField = form.querySelector('textarea[name="secret_text"]');
                if (textField && textField.value) {
                    // Получаем ключ (новый или из localStorage)
                    const key = await generateKey();
                    const { ciphertext, iv } = await encryptText(key, textField.value);

                    if (ciphertext) {
                        // Сохраняем IV и зашифрованный текст в одном поле
                        textField.value = `${toBase64(iv)}:${toBase64(ciphertext)}`;
                        form.submit();
                    }
                }
            }
        });
    }
});
