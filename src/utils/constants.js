const API_BASE_URL = 'http://localhost:8000';
const FACEBOOK_API_URL = 'https://graph.facebook.com/v12.0';
const FACT_CHECK_ENDPOINT = '/verify';
const HEALTH_CHECK_ENDPOINT = '/health';
const POLITICIANS_ENDPOINT = '/politicians';

const SCAN_INTERVAL = 5000;
const MAX_RETRY_COUNT = 3;

export {
    API_BASE_URL,
    FACEBOOK_API_URL,
    FACT_CHECK_ENDPOINT,
    HEALTH_CHECK_ENDPOINT,
    POLITICIANS_ENDPOINT,
    SCAN_INTERVAL,
    MAX_RETRY_COUNT
};