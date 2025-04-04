
const API_BASE_URL = 'http://localhost:8000';

async function factCheck(text) {
    try {
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error during fact-checking:', error);
        throw new Error('Fact-checking failed');
    }
}

export { factCheck };