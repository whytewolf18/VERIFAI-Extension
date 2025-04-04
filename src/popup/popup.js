document.addEventListener('DOMContentLoaded', async () => {
    const resultContainer = document.getElementById('resultContainer');
    const checkButton = document.getElementById('checkButton');
    const claimInput = document.getElementById('claimInput');

    checkButton.addEventListener('click', async () => {
        const claim = claimInput.value;
        if (!claim) {
            resultContainer.innerText = 'Please enter a claim to check.';
            return;
        }

        chrome.runtime.sendMessage({ action: 'checkClaim', claim }, (response) => {
            if (response.error) {
                resultContainer.innerText = `Error: ${response.error}`;
            } else {
                resultContainer.innerHTML = `
                    <h3>Fact-Check Result</h3>
                    <p><strong>Claim:</strong> ${claim}</p>
                    <p><strong>Classification:</strong> ${response.result.classification}</p>
                    <p><strong>Explanation:</strong> ${response.result.explanation}</p>
                `;
            }
        });
    });
});