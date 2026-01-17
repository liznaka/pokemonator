# Pokémonator — A Heuristic Pokémon Guessing Game
This project is a full-stack web application inspired by Akinator that demonstrates heuristic-based decision systems and intelligent search strategies. The system dynamically selects and scores questions based on how effectively they split the remaining Pokémon candidates, using binary search techniques for efficient narrowing of the solution space. The application reconstructs game state across stateless HTTP requests, enabling consistent gameplay without relying on server-side sessions. It integrates a structured JSON dataset and external Pokédex resources to provide a complete, interactive user experience.

### Disclaimer
This is a non-commercial project made for educational purposes. Pokémon and related trademarks are the property of Nintendo and The Pokémon Company
&nbsp;

## Features
- Interactive website with Flask
- Intelligent question selection using split-quality and information gain scoring
- Binary-search-based Pokédex number questions
- Dynamic filtering of remaining Pokémon
- Links to the official Pokédex for images and external information
- 100% success rate in automated test simulations
&nbsp;

## File structure
- main.py # Flask webserver
- pokemonguesser.py # game logic
- pokemon.json # Pokémon dataset
- templates/ # HTML files
- static/ # CSS, favicon
&nbsp;

## How to run this program
1. Requirements
    - Python 3.8 or higher
    - pip

2. Install dependencies
    - ` pip install flask`

3. Start the server
    - `python/python3 main.py`

4. Open the local Flask server URL shown in the terminal in your browser
    - (usually: http://xxx.x.x.x:xxxx)
&nbsp;

## Technologies used
- Python 3.8+
- Flask
- HTML
- CSS
- JSON dataset
&nbsp;

## Sources and Credits:
- PokeAPI: https://pokeapi.co/
- Official Pokémon Pokédex (images and external links): https://www.pokemon.com/us/pokedex
- Pokémon JSON Dataset (modified for this project) olitreadwell (Github): https://github.com/olitreadwell/pokemon-classic-json/blob/main/pokedex.json
&nbsp;

## Limitations
Currently only supports Generation 1 Pokémon and requires consistent and truthful user answers
&nbsp;

## Extra
This project was developed for educational purposes and demonstrates heuristic-based decision systems, state reconstruction in stateless web applications, and full-stack development using Python and Flask.

### AI Assistance
*This project was developed with the assistance of ChatGPT by OpenAI (GPT-5.2) as a support tool for debugging, refactoring, documentation, and exploring heuristic and architectural design choices. All final implementation and design decisions were made by the author.*