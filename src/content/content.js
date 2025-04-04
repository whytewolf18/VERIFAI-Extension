const API_BASE_URL = 'http://localhost:8000';
const SCAN_INTERVAL = 5000;
let isProcessing = false;

// API endpoints
const ENDPOINTS = {
    VERIFY: `${API_BASE_URL}/verify`,
    POLITICIANS: `${API_BASE_URL}/politicians`
};

const FACEBOOK_SELECTORS = {
    postContent: '[data-ad-comet-preview="message"]',
    article: '[role="article"]'
};

const CLASSIFICATIONS = {
    'TRUE': 'verifai-true',
    'FALSE': 'verifai-false',
    'MISLEADING': 'verifai-misleading',
    'UNVERIFIED': 'verifai-unverified'
};

const POLITICIANS_KEYWORDS = [
    "Bongbong Marcos",
    "Joseph Estrada",
    "Lito Lapid",
    "Sara Duterte",
    "Juan Miguel Zubiri",
    "Martin Romualdez",
    "Reynaldo Tamayo Jr.",
    "Bong Revilla",
    "Tito Sotto",
    "Cynthia Villar",
    "Ronaldo Puno",
    "Francis Pangilinan",
    "Pantaleon Alvarez",
    "Nancy Binay",
    "Mylene Hega",
    "Ernesto Ramel Jr.",
    "Rodrigo Duterte",
    "Greco Belgica",
    "Lito Monico Lorenzana",
    "Joseph Estrada",
    "Frederick Siao",
    "Paolo Duterte",
    "Seth Frederick Jalosjos",
    "Gwendolyn Garcia",
    "Tomas Osmeña",
    "Michael Rama",
    "Vincent Franco Frasco",
    "Frenedil Castro",
    "Melchor Cubillo",
    "Ebrahim Abdurrahman",
    "Mahid Mutilan",
    "Fernando Toquillo",
    "Jack Duavit",
    "Luis Raymund Villafuerte",
    "Isko Moreno",
    "Robin Padilla",
    "Bellaflor Angara",
    "Eduardo Bringas",
    "Rufus Rodriguez",
    "Jejomar Binay",
    "Estelito Mendoza",
    "Tiburcio Pasquil",
    "Senate of The Philippines",
    "House of Representatives",
    "Senate",
    "House",
    "Philippine President",
    "Duterte",
    "BBM"
];

async function detectPoliticians(text) {
    try {
        const response = await fetch(ENDPOINTS.POLITICIANS);
        const data = await response.json();
        const politicians = data.politicians;
        
        const verifyResponse = await fetch(ENDPOINTS.VERIFY, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                type: 'politician_mention',
                source: 'facebook',
                politicians: []
            })
        });
        const verifyData = await verifyResponse.json();
        
        return Object.keys(politicians).filter(politician => 
            text.includes(politician) && verifyData.verified
        );
    } catch (error) {
        console.error('Failed to detect politicians:', error);
        return [];
    }
}

async function analyzeClaim(text) {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({ 
            action: 'classify', 
            text 
        }, async (response) => {
            if (chrome.runtime.lastError) {
                console.error('Message error:', chrome.runtime.lastError);
                reject(chrome.runtime.lastError);
            } else if (response.error) {
                reject(response.error);
            } else {
                resolve(response.result);
            }
        });
    });
}

async function verifyContent(text) {
    try {
        const response = await fetch(ENDPOINTS.VERIFY, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                type: 'facebook_post',
                source: 'facebook',
                politicians: []
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Verification failed:', errorData);
            return null;
        }

        const result = await response.json();
        console.log('Verification result:', result);
        return result;
    } catch (error) {
        console.error('Verification failed:', error);
        return null;
    }
}

function highlightPoliticians(element, politicians) {
    politicians.forEach(politician => {
        const regex = new RegExp(`\\b${politician}\\b`, 'gi');
        element.innerHTML = element.innerHTML.replace(regex, `<span class="highlight">${politician}</span>`);
    });
}

function createTooltipContent(result) {
    const tooltip = document.createElement('div');
    tooltip.className = 'verifai-tooltip';
    
    // Create tooltip header
    const header = document.createElement('div');
    header.className = 'verifai-tooltip-header';
    header.textContent = `This claim is ${result.classification}!`;
    
    // Create tooltip body
    const body = document.createElement('div');
    body.className = 'verifai-tooltip-body';
    body.textContent = result.explanation;
    
    // Add unverified reason if applicable
    if (result.classification === 'UNVERIFIED' && result.unverified_reason) {
        const reasonDiv = document.createElement('div');
        reasonDiv.className = 'verifai-tooltip-reason';
        reasonDiv.innerHTML = `<strong>Why Unverified:</strong><br/>${result.unverified_reason}`;
        body.appendChild(reasonDiv);
    }
    
    // Add sources if available
    if (result.sources && result.sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'verifai-tooltip-sources';
        sourcesDiv.innerHTML = '<strong>Sources:</strong><br/>' + 
            result.sources.join('<br/>');
        body.appendChild(sourcesDiv);
    }
    
    tooltip.appendChild(header);
    tooltip.appendChild(body);
    
    return tooltip;
}

function underlineText(element, result) {
    console.log('Applying classification:', result.classification);
    
    // Create a wrapper
    const wrapper = document.createElement('div');
    wrapper.className = `verifai-${result.classification.toLowerCase()}`;
    wrapper.innerHTML = element.innerHTML;
    
    // Add tooltip
    const tooltip = createTooltipContent(result);
    wrapper.appendChild(tooltip);
    
    // Replace original content
    element.innerHTML = '';
    element.appendChild(wrapper);
    
    console.log('Applied styles to element:', element.outerHTML);
}

async function scanFacebookContent() {
    if (isProcessing) return;
    isProcessing = true;

    try {
        const posts = document.querySelectorAll(FACEBOOK_SELECTORS.postContent);
        console.log(`Found ${posts.length} posts`);

        for (const post of posts) {
            if (!post.hasAttribute('data-verifai-checked')) {
                const content = post.innerText;
                console.log(`Analyzing post content: ${content}`);
                
                const mentionedPoliticians = await detectPoliticians(content);
                if (mentionedPoliticians.length > 0) {
                    const verificationResult = await verifyContent(content);
                    if (verificationResult?.classification) {
                        highlightPoliticians(post, mentionedPoliticians);
                        underlineText(post, verificationResult);
                        post.setAttribute('data-fact-check', verificationResult.analysis);
                    }
                }
                post.setAttribute('data-verifai-checked', 'true');
            }
        }
    } catch (error) {
        console.error('Scan error:', error);
    } finally {
        isProcessing = false;
    }
}

function observeFacebookPosts() {
    const observer = new MutationObserver(async (mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    // Look for Facebook posts content
                    const postContent = node.querySelector('[data-ad-comet-preview="message"]');
                    if (postContent && !postContent.hasAttribute('data-verifai-checked')) {
                        const text = postContent.textContent;
                        const result = await verifyContent(text);
                        if (result && result.classification) {
                            underlineText(postContent, result);
                        }
                        postContent.setAttribute('data-verifai-checked', 'true');
                    }
                }
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

console.log("Initializing VERIFAI extension...");
observeFacebookPosts();
setInterval(scanFacebookContent, SCAN_INTERVAL);