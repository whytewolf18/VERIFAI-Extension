# Fact Check Extension

## Overview
The Fact Check Extension is a browser extension designed to provide real-time fact-checking for content on Facebook. It leverages the VERIFAI API to analyze claims made in posts and comments, helping users identify misinformation.

## Project Structure
```
fact-check-extension
├── src
│   ├── background
│   │   └── background.js
│   ├── content
│   │   ├── content.js
│   │   └── factChecker.js
│   ├── popup
│   │   ├── popup.html
│   │   ├── popup.js
│   │   └── popup.css
│   └── utils
│       ├── api.js
│       └── constants.js
├── assets
│   └── icons
├── manifest.json
└── README.md
```

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd fact-check-extension
   ```

2. **Load the Extension in Your Browser**
   - Open your browser and navigate to the extensions page (e.g., `chrome://extensions` for Chrome).
   - Enable "Developer mode".
   - Click on "Load unpacked" and select the `fact-check-extension` directory.

3. **Permissions**
   - The extension requires permissions to access Facebook and make API calls. Ensure that the necessary permissions are granted in the `manifest.json`.

## Usage
- Once the extension is loaded, navigate to Facebook.
- The extension will automatically scan posts and comments for claims.
- Click on the extension icon to open the popup and view the fact-checking results.

## Development
- **Background Script**: Located in `src/background/background.js`, this script manages the extension's lifecycle and handles messages from content scripts.
- **Content Script**: The main logic for scraping Facebook content is in `src/content/content.js`, while the fact-checking logic is in `src/content/factChecker.js`.
- **Popup UI**: The user interface for displaying results is defined in `src/popup/popup.html` and styled in `src/popup/popup.css`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.