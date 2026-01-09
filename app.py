from flask import Flask, render_template, request
import json

app = Flask(__name__)

# load pokemon data
with open("pokemon.json", "r") as file:
    POKEMON = json.load(file)["pokemon"]

# index page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", pokemon=POKEMON)

@app.route("/guess", methods=["POST"])
def guess():
    answers = request.form.to_dict()
    
    remaining_pokemon = POKEMON.copy()
    for poke in POKEMON:
        score = 0

        # type (Grass, Poison)
        if "type" in answers and answers["type"]:
        # remove pokemon without right attribute
            remaining_pokemon = [p for p in remaining_pokemon if answers["type"] in p["type"]]

        # weakness
        if "weakness" in answers and answers["weakness"]:
        # remove pokemon without right attribute
            remaining_pokemon = [p for p in remaining_pokemon if answers["weakness"] in p.get("weaknesses", [])]

# run the app
if __name__ == "__main__":
    app.run(debug=True)
