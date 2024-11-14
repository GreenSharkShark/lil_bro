function copyLink() {
    var linkText = document.getElementById("linkContainer").innerText.trim();
    var tempInput = document.createElement("input");
    tempInput.value = linkText;
    document.body.appendChild(tempInput);

    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    // Изменение текста кнопки на "Copied"
    var copyButton = document.getElementById("copyButton");
    copyButton.innerText = "Copied";
    copyButton.disabled = true; // Опционально, чтобы предотвратить повторное нажатие
}