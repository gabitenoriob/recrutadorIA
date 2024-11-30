document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const progressBar = document.getElementById('progressBar');
    const resultBox = document.getElementById('resultBox');

    if (fileInput.files.length === 0) {
        alert('Por favor, selecione pelo menos um arquivo.');
        return;
    }

    const formData = new FormData();
    for (let file of fileInput.files) {
        formData.append('files', file);
    }

    try {
        progressBar.style.width = '0%';
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Erro no upload!');
        }

        // Atualiza o progresso para 100%
        progressBar.style.width = '100%';

        // Envia para análise de resultados
        const resultResponse = await fetch('/result', { method: 'GET' });
        const resultData = await resultResponse.json();
        
        if (resultData.message === "Resultados da análise.") {
            const resultText = resultData.results.map(result => 
                `${result.file}: ${result.evaluation}`).join('\n');
            resultBox.value = resultText;
        } else {
            resultBox.value = resultData.message;
        }
    } catch (error) {
        alert('Ocorreu um erro: ' + error.message);
    }
});
