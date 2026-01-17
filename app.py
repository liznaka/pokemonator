from flask import Flask, render_template, request, redirect
import json

from pokemonguesser import Pokemon, PokemonGuesser

app = Flask(__name__)

# ----------------------
# Load Pokémon data
# ----------------------
with open("pokemon.json", "r") as file:
    raw = json.load(file)["pokemon"]
    ALL_POKEMON = [Pokemon(p) for p in raw]

POKEMON_BY_NUM = {p._num: p for p in ALL_POKEMON}

# ----------------------
# Index
# ----------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", pokemon=raw)

# ----------------------
# Start game
# ----------------------
@app.route("/start", methods=["POST"])
def start():
    guesser = PokemonGuesser(ALL_POKEMON)

    question = guesser.choose_best_question()

    # 🏆 Hvis det bare er én igjen (edge case)
    if question is None or guesser.should_guess():
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    return render_template(
        "question.html",
        question={
            "id": question._id,
            "text": question._text
        },
        remaining=[p._num for p in guesser._remaining],
        asked_questions=[]
    )

# ----------------------
# Answer question
# ----------------------
@app.route("/guess", methods=["POST"])
def guess():
    answer = request.form.get("answer")

    if answer not in ("yes", "no"):
        return redirect("/")

    answer = (answer == "yes")

    # -------------------
    # Rebuild game state
    # -------------------
    remaining_nums = set(map(int, request.form.getlist("remaining[]")))
    remaining = [POKEMON_BY_NUM[n] for n in remaining_nums]

    asked_ids = request.form.getlist("asked[]")

    guesser = PokemonGuesser(remaining)

    # Rebuild asked questions
    for qid in asked_ids:
        q = guesser.reconstruct_question(qid)
        if q:
            guesser._asked_questions.append(q)

    # -------------------
    # Apply current answer
    # -------------------
    qid = request.form.get("question_id")
    current_question = guesser.reconstruct_question(qid)

    if not current_question:
        return redirect("/")

    guesser.apply_answer(current_question, answer)

    # -------------------
    # Check win condition
    # -------------------
    if guesser.should_guess():
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    # -------------------
    # Next question
    # -------------------
    next_question = guesser.choose_best_question()

    # 🧠 Hvis systemet ikke finner flere spørsmål
    if next_question is None:
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    return render_template(
        "question.html",
        question={
            "id": next_question._id,
            "text": next_question._text
        },
        remaining=[p._num for p in guesser._remaining],
        asked_questions=asked_ids + [qid]
    )

# ----------------------
# Run
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
