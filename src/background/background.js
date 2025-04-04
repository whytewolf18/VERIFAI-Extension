const API_BASE_URL = 'http://localhost:8000';
let backendStatus = false;

async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        backendStatus = response.ok;
        console.log('Backend status:', backendStatus ? 'Connected' : 'Disconnected');
    } catch (error) {
        console.error('Health check failed:', error);
        backendStatus = false;
    }
}

function initializeBackend() {
    checkBackendStatus();
    chrome.alarms.create('healthCheck', { periodInMinutes: 1 });
}

const messageHandlers = {
    getBackendStatus: (request, sender, sendResponse) => {
        sendResponse({ status: backendStatus });
        return true;
    },
    classify: async (request, sender, sendResponse) => {
        if (!backendStatus) {
            sendResponse({ error: 'Backend is not available' });
            return true;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/verify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: request.text,
                    // Add any additional required fields
                    type: 'facebook_post',
                    source: 'facebook',
                    politicians: request.politicians || []
                })
            });
            
            if (response.status === 422) {
                const error = await response.json();
                console.error('Validation error:', error);
                sendResponse({ error: 'Invalid request format' });
                return true;
            }
            
            const result = await response.json();
            sendResponse({ result });
        } catch (error) {
            console.error('Classification failed:', error);
            sendResponse({ error: error.message });
        }
        return true;
    }
};

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Received message:', request);
    const handler = messageHandlers[request.action];
    if (handler) {
        return handler(request, sender, sendResponse);
    }
    return false;
});

chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === 'healthCheck') {
        checkBackendStatus();
    }
});

chrome.runtime.onInstalled.addListener(() => {
    console.log('VERIFAI Extension installed');
    initializeBackend();
});