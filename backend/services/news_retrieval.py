import re
from services.google_service import search_manager  # Correct import
from typing import List, Dict

POLITICIANS = [
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
]

POLITICIAN_INFO = {
    "Bongbong Marcos": {
        "party": "Partido Federal ng Pilipinas",
        "position": "President"
    },
    "Sara Duterte": {
        "party": "Lakas-Christian Muslim Democrats",
        "position": "Vice President"
    },
    "Juan Miguel Zubiri": {
        "party": "Independent",
        "position": "Senate President"
    },
    "Martin Romualdez": {
        "party": "Lakas-Christian Muslim Democrats",
        "position": "Speaker of the House"
    },
    "Reynaldo Tamayo Jr.": {
        "party": "Partido Federal ng Pilipinas",
        "position": "Party Chairman"
    },
    "Bong Revilla": {
        "party": "Lakas-Christian Muslim Democrats",
        "position": "Party Chairman"
    },
    "Tito Sotto": {
        "party": "Nationalist People's Coalition",
        "position": "Party Chairman"
    },
    "Cynthia Villar": {
        "party": "Nacionalista Party",
        "position": "Party Chairperson"
    },
    "Ronaldo Puno": {
        "party": "National Unity Party",
        "position": "Party Chairman"
    },
    "Francis Pangilinan": {
        "party": "Liberal Party",
        "position": "Party President"
    },
    "Pantaleon Alvarez": {
        "party": "Partido para sa Demokratikong Reporma",
        "position": "Party President"
    },
    "Nancy Binay": {
        "party": "United Nationalist Alliance",
        "position": "Party Chairperson"
    },
    "Mylene Hega": {
        "party": "Akbayan Citizens' Action Party",
        "position": "Party Chairperson"
    },
    "Ernesto Ramel Jr.": {
        "party": "Aksyon Demokratiko",
        "position": "Party Chairperson"
    },
    "Rodrigo Duterte": {
        "party": "Partido Demokratiko Pilipino",
        "position": "Party Chairman"
    },
    "Greco Belgica": {
        "party": "Pederalismo ng Dugong Dakilang Samahan",
        "position": "Party President"
    },
    "Lito Monico Lorenzana": {
        "party": "Centrist Democratic Party of the Philippines",
        "position": "Party Chairman"
    },
    "Joseph Estrada": {
        "party": "Pwersa ng Masang Pilipino",
        "position": "Party President"
    },
    "Frederick Siao": {
        "party": "Asenso Iliganon Party",
        "position": "Party Leader"
    },
    "Paolo Duterte": {
        "party": "Hugpong sa Tawong Lungsod",
        "position": "Party Leader"
    },
    "Seth Frederick Jalosjos": {
        "party": "Aggrupation of Parties for Prosperity",
        "position": "Party Leader"
    },
    "Gwendolyn Garcia": {
        "party": "One Cebu",
        "position": "Party Leader"
    },
    "Tomas Osmeña": {
        "party": "Bando Osmeña - Pundok Kauswagan",
        "position": "Party Leader"
    },
    "Michael Rama": {
        "party": "Partido Barug",
        "position": "Party Leader"
    },
    "Vincent Franco Frasco": {
        "party": "Democracy of the Independent Liberal Conservative Party",
        "position": "Party Leader"
    },
    "Frenedil Castro": {
        "party": "Ugyon Kita Capiz",
        "position": "Party Leader"
    },
    "Melchor Cubillo": {
        "party": "Economic Development and Social Advancement",
        "position": "Party Leader"
    },
    "Ebrahim Abdurrahman": {
        "party": "Islamic Party of the Philippines",
        "position": "Party Leader"
    },
    "Mahid Mutilan": {
        "party": "Ompia Party",
        "position": "Party Leader"
    },
    "Fernando Toquillo": {
        "party": "Democratic Alliance of Mindanaoans for Good Government",
        "position": "Party Leader"
    },
    "Jack Duavit": {
        "party": "Nationalist People's Coalition",
        "position": "Party President"
    },
    "Luis Raymund Villafuerte": {
        "party": "National Unity Party",
        "position": "Party President"
    },
    "Isko Moreno": {
        "party": "Aksyon Demokratiko",
        "position": "Party President"
    },
    "Robin Padilla": {
        "party": "Partido Demokratiko Pilipino",
        "position": "Party President"
    },
    "Bellaflor Angara": {
        "party": "Laban ng Demokratikong Pilipino",
        "position": "Party President"
    },
    "Eduardo Bringas": {
        "party": "Pederalismo ng Dugong Dakilang Samahan",
        "position": "Party Chairman"
    },
    "Rufus Rodriguez": {
        "party": "Centrist Democratic Party of the Philippines",
        "position": "Party President"
    },
    "Jejomar Binay": {
        "party": "United Nationalist Alliance",
        "position": "Party President"
    },
    "Estelito Mendoza": {
        "party": "Sarangani Reconciliation and Reformation Organization",
        "position": "Party Leader"
    },
}
def detect_politicians(text: str) -> List[str]:
    """Detect politicians mentioned in the text"""
    mentioned_politicians = [politician for politician in POLITICIANS if politician in text]
    return mentioned_politicians

async def fetch_articles(query: str) -> Dict:
    """Fetch articles related to the query"""
    search_results = await search_manager._api_search(query, "news")
    return search_results
