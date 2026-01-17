import json
from pokemonguesser import Pokemon, PokemonGuesser

MAX_STEPS = 40
MAX_NO_PROGRESS_STEPS = 5
MAX_NUMBER_QUESTIONS = 6


def simulate_web_game(secret, all_pokemon, verbose=False):
    guesser = PokemonGuesser(all_pokemon)

    steps = 0
    no_progress_steps = 0
    last_remaining = len(guesser._remaining)
    number_questions_used = 0

    while True:
        # 🏁 Ferdig?
        if guesser.should_guess():
            break

        question = guesser.choose_best_question()

        # 💀 AI ga opp (skal egentlig aldri skje nå)
        if question is None:
            return False, "Guesser gave up (returned None)"

        qid = question._id
        rebuilt = guesser.reconstruct_question(qid)

        if rebuilt is None:
            return False, f"Failed to reconstruct question: {qid}"

        # 🧠 Hva ville brukeren svart?
        answer = rebuilt._predicate(secret)

        # 🔢 Nummer-spørsmål tracking
        is_number = qid.startswith("num:<")
        if is_number:
            number_questions_used += 1

        if number_questions_used > MAX_NUMBER_QUESTIONS:
            return (
                False,
                f"Too many number-questions ({number_questions_used})"
            )

        if verbose:
            tag = "🔢" if is_number else "❓"
            print(
                f"{tag} [{steps+1}] {rebuilt._text} -> "
                f"{'YES' if answer else 'NO'} | "
                f"remaining={len(guesser._remaining)}"
            )

        # 🔁 Bruk samme logikk som server
        guesser.apply_answer(rebuilt, answer)
        steps += 1

        current_remaining = len(guesser._remaining)

        # 🧊 Fremgangssjekk
        if current_remaining >= last_remaining:
            no_progress_steps += 1
        else:
            no_progress_steps = 0

        if no_progress_steps > MAX_NO_PROGRESS_STEPS:
            return (
                False,
                f"No progress for {no_progress_steps} steps "
                f"(remaining={current_remaining})"
            )

        last_remaining = current_remaining

        if steps > MAX_STEPS:
            return (
                False,
                f"Too many steps (> {MAX_STEPS}), "
                f"remaining={len(guesser._remaining)}"
            )

    # 🔮 Endelig gjetning
    guessed = guesser.guess()

    if guessed is None:
        return False, "Guesser returned None"

    if guessed._num != secret._num:
        return (
            False,
            f"Wrong guess: expected {secret._name}, got {guessed._name}"
        )

    return True, steps


def main():
    with open("pokemon.json") as f:
        raw = json.load(f)["pokemon"]

    all_pokemon = [Pokemon(p) for p in raw]

    total = len(all_pokemon)
    success = 0
    failures = []

    print("🧪 Running ELITE Pokémonator tests...\n")

    for secret in all_pokemon:
        ok, info = simulate_web_game(secret, all_pokemon)

        if ok:
            success += 1
        else:
            failures.append((secret._name, info))
            print(f"❌ Failed for {secret._name}: {info}")

    print("\n--- ELITE TEST RESULTS ---")
    print(f"Pokémon tested: {total}")
    print(f"Correct guesses: {success}")
    print(f"Success rate: {success / total * 100:.2f}%")

    if failures:
        print("\nFailures:")
        for name, reason in failures:
            print(f"- {name}: {reason}")
    else:
        print("\n🏆 PERFECT SCORE — YOUR AI IS LEGENDARY 🧠🔥")


if __name__ == "__main__":
    main()
