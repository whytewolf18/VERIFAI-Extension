const API_BASE_URL = 'http://localhost:8000';
const FB_APP_ID = process.env.FACEBOOK_APP_ID;
const FB_APP_SECRET = process.env.FACEBOOK_APP_SECRET;

const fbConfig = {
    appId: FB_APP_ID,
    appSecret: FB_APP_SECRET,
    version: 'v17.0'
};

async function fetchFromAPI(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API fetch error:', error);
        throw error;
    }
}

async function postFactCheck(text) {
    return await fetchFromAPI('/verify', 'POST', { text });
}

async function getPoliticians() {
    return await fetchFromAPI('/politicians');
}

export { postFactCheck, getPoliticians };