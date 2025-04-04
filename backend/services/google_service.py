from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.config import GOOGLE_API_KEYS, GOOGLE_SEARCH_CX, get_source_patterns
from utils.gpt_utils import generate_sources_gpt  # Import the GPT utility

# Google Search API configuration
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

class SearchManager:
    def __init__(self):
        self.current_key_index = 0
        self.use_gpt_fallback = False

    async def _api_search(self, query: str, search_type: str) -> Optional[Dict]:
        if self.use_gpt_fallback:
            return await generate_sources_gpt(query)
        
        try:
            service = build("customsearch", "v1", developerKey=GOOGLE_API_KEYS[self.current_key_index])
            res = service.cse().list(q=query, cx=GOOGLE_SEARCH_CX, num=10).execute()
            filtered_items = self._filter_results(res.get('items', []))
            return {"items": filtered_items}
        except HttpError as e:
            print(f"Google API error: {str(e)}")
            return None

    def _filter_results(self, items: List[Dict]) -> List[Dict]:
        allowed_patterns = get_source_patterns("news") + get_source_patterns("government")
        filtered_items = [item for item in items if any(pattern in item['link'] for pattern in allowed_patterns)]
        return filtered_items

search_manager = SearchManager()