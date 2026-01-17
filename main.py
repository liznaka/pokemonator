## imports ##
from flask import Flask, render_template, request, redirect
import json

from pokemonguesser import Pokemon, PokemonGuesser

main = Flask(__name__)

## load Pokémon objects from pokemon.json ##
with open("pokemon.json", "r") as file:
    raw = json.load(file)["pokemon"]
    ALL_POKEMON = [Pokemon(p) for p in raw]

# faster look up
POKEMON_BY_NUM = {p._num: p for p in ALL_POKEMON}

## index route (start page) ##
@main.route("/", methods=["GET"])
def index():
    return render_template("index.html", pokemon=raw)

## start game route ##
@main.route("/start", methods=["POST"])
def start():
    # new AI-like guesser
    guesser = PokemonGuesser(ALL_POKEMON)

    question = guesser.choose_best_question()

    # one Pokémon left or no good questions left
    if question is None or guesser.should_guess():
        # send to result page with remaining Pokémon
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    # send first question with remaining Pokémon and list of asked questions
    return render_template(
        "question.html",
        question={
            "id": question._id,
            "text": question._text
        },
        remaining=[p._num for p in guesser._remaining],
        asked_questions=[]
    )

## guess route to register answers ##
@main.route("/guess", methods=["POST"])
def guess():
    # read answer
    answer = request.form.get("answer")

    # debugging
    if answer not in ("yes", "no"):
        return redirect("/")

    # translate to bool
    answer = (answer == "yes")

    ## actual "smart-thinking" logic ##
    # fetch remaining Pokémon
    remaining_nums = set(map(int, request.form.getlist("remaining[]")))
    remaining = [POKEMON_BY_NUM[n] for n in remaining_nums]

    # fetch asked questions
    asked_ids = request.form.getlist("asked[]")

    # new AI-like guesser for remaining
    guesser = PokemonGuesser(remaining)

    # rebuild asked questions
    for qid in asked_ids:
        q = guesser.reconstruct_question(qid)
        if q:
            guesser._asked_questions.append(q)

    # find answered question
    qid = request.form.get("question_id")
    current_question = guesser.reconstruct_question(qid)

    # debugging
    if not current_question:
        return redirect("/")

    # remove non-match Pokémon
    guesser.apply_answer(current_question, answer)

    # one Pokémon left -> guess
    if guesser.should_guess():
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    # generate next "best" question
    next_question = guesser.choose_best_question()

    # system unable to find next question, show result
    if next_question is None:
        return render_template(
            "result.html",
            pokemon=guesser.guess(),
            final=True
        )

    # send new question
    return render_template(
        "question.html",
        question={
            "id": next_question._id,
            "text": next_question._text
        },
        remaining=[p._num for p in guesser._remaining],
        asked_questions=asked_ids + [qid]
    )

## run server ##
if __name__ == "__main__":
    main.run(debug=True)