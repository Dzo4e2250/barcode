// Funkcija za prikaz sporočil uporabniku
function showMessage(message, type = 'success') {
    const messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
    messageBox.style.color = (type === 'success') ? 'green' : 'red';
}

// Funkcija za pošiljanje obrazca na strežnik
function sendData(preview = false) {
    const eanKode = document.getElementById('ean-kode').value.trim();
    const opisiArtiklov = document.getElementById('opis-artikla').value.trim();

    // Preverjanje, če so polja izpolnjena
    if (!eanKode || !opisiArtiklov) {
        showMessage("Prosimo, izpolnite obe polji: EAN kode in opise artiklov.", 'error');
        return;
    }

    const eanList = eanKode.split('\n').map(ean => ean.trim());
    for (let ean of eanList) {
        if (ean.length !== 13 || isNaN(ean)) {
            showMessage(`EAN koda ${ean} ni veljavna. Mora biti 13-mestna številka.`, 'error');
            return;
        }
    }

    const opisiList = opisiArtiklov.split('\n').map(opis => opis.trim());
    if (eanList.length !== opisiList.length) {
        showMessage("Število EAN kod se mora ujemati s številom opisov.", 'error');
        return;
    }

    // Ustvarimo podatke za pošiljanje (FormData)
    const formData = new FormData();
    formData.append('ean_codes', eanKode);
    formData.append('opisi_artiklov', opisiArtiklov);

    // Pošljemo podatke na strežnik
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        if (preview) {
            // Prikaz PDF-ja v iframe za predogled
            const iframe = document.getElementById('pdf-frame');
            iframe.src = url;
            showMessage("PDF predogled ustvarjen!", 'success');
        } else {
            // Prenos PDF datoteke
            const a = document.createElement('a');
            a.href = url;
            a.download = "ean_kode.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            showMessage("PDF uspešno ustvarjen in prenesen!", 'success');
        }
    })
    .catch(error => {
        showMessage('Napaka pri ustvarjanju PDF-ja.', 'error');
        console.error('Napaka:', error);
    });
}

// Gumb za predogled
document.getElementById('preview-btn').addEventListener('click', function () {
    sendData(true); // Pokliči funkcijo za predogled
});

// Gumb za prenos
document.getElementById('download-btn').addEventListener('click', function () {
    sendData(false); // Pokliči funkcijo za prenos
});
