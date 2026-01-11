import json
from pokemonguesser import PokemonGuesser

# ---- LOAD DATA ----
with open("pokemon.json", "r") as f:
    POKEMON = json.load(f)["pokemon"]

MAX_QUESTIONS = 30

# ---- HELPER: korrekt svar ----
def correct_answer(pokemon, attribute, value):
    if attribute == "fully_evolved":
        return "yes" if not pokemon.get("next_evolution") else "no"
    elif attribute == "num_lt":
        return "yes" if int(pokemon["num"]) < int(value) else "no"
    else:
        return "yes" if value in pokemon.get(attribute, []) else "no"

# ---- SIMULER EN HEL SPILLRUNDE ----
def simulate_game(target):
    guesser = PokemonGuesser(POKEMON)
    questions = 0

    while questions < MAX_QUESTIONS:
        question = guesser.best_question()

        # Ingen spørsmål → appen ville gjettet nå
        if question is None:
            break

        attribute = question["attribute"]
        value = question["value"]

        answer = correct_answer(target, attribute, value)
        guesser.apply_answer(attribute, value, answer)

        remaining = guesser.get_remaining()

        if target not in remaining:
            return False, questions + 1

        questions += 1

    return target in guesser.get_remaining(), questions

# ---- RUN TESTS ----
success = 0
failures = []
suspicious_loops = []

for pokemon in POKEMON:
    ok, steps = simulate_game(pokemon)
    if ok:
        success += 1
    else:
        failures.append((pokemon["name"], steps))

    if steps > 20:
        suspicious_loops.append((pokemon["name"], steps))

# ---- PRINT RESULTS ----
print("====== TEST RESULT ======")
print(f"Total Pokémon: {len(POKEMON)}")
print(f"Successful guesses: {success}")
print(f"Failed guesses: {len(failures)}")

if suspicious_loops:
    print("\n⚠️ Suspicious loops (games taking >20 questions):")
    for name, steps in suspicious_loops:
        print(f"- {name} ({steps} questions)")

if failures:
    print("\n❌ Failed Pokémon:")
    for name, steps in failures:
        print(f"- {name} (eliminated after {steps} questions)")
