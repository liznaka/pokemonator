from flask import Flask, render_template, request
import json

from pokemonguesser import PokemonGuesser

app = Flask(__name__)

# load pokemon data
with open("pokemon.json", "r") as file:
    POKEMON = json.load(file)["pokemon"]

# index page
@app.route("/", methods=["GET"])
def index():
    # show all pokemon and start-button
    return render_template("index.html", pokemon=POKEMON)

# start guessing with first question
@app.route("/start", methods=["POST"])
def start():
    guesser = PokemonGuesser(POKEMON)
    first_question = guesser.best_question()
    return render_template(
        "question.html",
        question=first_question,
        remaining=POKEMON,
        asked_questions=json.dumps(guesser.asked_questions)
    )

# handle answers and update remaining Pokémon
@app.route("/guess", methods=["POST"])
def guess():
    # fetch hidden inputs from question.html
    remaining_nums = request.form.getlist("remaining[]")
    remaining_pokemon = [p for p in POKEMON if p["num"] in remaining_nums]

    attribute = request.form["attribute"]
    value = request.form["value"]
    answer = request.form["answer"]

    # history of questions
    asked_questions_str = request.form.get("asked_questions")
    if asked_questions_str:
        asked_questions = json.loads(asked_questions_str)
    else:
        asked_questions = []
    
    # new guesser with remaining Pokémon
    guesser = PokemonGuesser(remaining_pokemon, asked_questions)
    
    # apply answer
    guesser.apply_answer(attribute, value, answer)
    
    remaining = guesser.get_remaining()

    # find matching Pokémon to asked questions
    def matching_pokemon(pokemon, asked_questions):
        for q in asked_questions:
            attr, val = q["attribute"], q["value"]
            # evolved question
            if attr == "fully_evolved":
                if pokemon[attr] != val:
                    return False
                # number question
            elif attr == "num_lt":
                if int(pokemon["num"]) >= int(val):
                    return False
            else:
                if val not in pokemon.get(attr, []):
                    return False
        return True

    
    matches = [p for p in remaining if matching_pokemon(p, asked_questions)]

    next_question = guesser.best_question()
        
    if len(matches) == 1 or next_question is None:
        # show result Pokémon
        return render_template("result.html", pokemon=matches[0] if matches else None)
    
    return render_template(
        "question.html",
        question=next_question,
        remaining=remaining,
        asked_questions=json.dumps(guesser.asked_questions)
        )

# run the app
if __name__ == "__main__":
    app.run(debug=True)
