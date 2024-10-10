async function generateKey() {
    return await window.crypto.subtle.generateKey(
        {
            name: "AES-GCM",
            length: 256,
        },
        true,
        ["encrypt", "decrypt"]
    );
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
                    const key = await generateKey();
                    const { ciphertext } = await encryptText(key, textField.value);

                    if (ciphertext) {
                        const exportedKey = await window.crypto.subtle.exportKey('raw', key);
                        localStorage.setItem('encryptionKey', JSON.stringify(Array.from(new Uint8Array(exportedKey))));
                        textField.value = toBase64(ciphertext);
                        form.submit();
                    }
                }
            }
        });
    }
});
