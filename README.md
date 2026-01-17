# Pokémonator — A Heuristic Pokémon Guessing Game
A web-based guessing game inspired by the well-known Akinator. The system uses heuristic decision logic to guess a given Pokémon from Generation 1 through a series of yes/no questions.

### Disclaimer
This is a non-commercial project made for educational purposes. Pokémon and related trademarks are the property of Nintendo and The Pokémon Company

## Features
- Interactive website with Flask
- Intelligent question selection using split-quality and information gain scoring
- Binary-search-based Pokédex number questions
- Dynamic filtering of remaining Pokémon
- Links to the official Pokédex for images and external information
- 100% success rate in automated test simulations

## File structure
- main.py # Flask webserver
- pokemonguesser.py # game logic
- pokemon.json # Pokémon dataset
- templates/ # HTML files
- static/ # CSS, favicon

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

## Technologies used
- Python 3.8+
- Flask
- HTML
- CSS
- JSON dataset

## Sources and Credits:
- PokeAPI: https://pokeapi.co/
- Official Pokémon Pokédex (images and external links): https://www.pokemon.com/us/pokedex
- Pokémon JSON Dataset (modified for this project) olitreadwell (Github): https://github.com/olitreadwell/pokemon-classic-json/blob/main/pokedex.json

## Limitations
Currently only supports Generation 1 Pokémon and requires consistent and truthful user answers

## Extra
This project was developed for educational purposes and demonstrates heuristic-based decision systems, state reconstruction in stateless web applications, and full-stack development using Python and Flask.