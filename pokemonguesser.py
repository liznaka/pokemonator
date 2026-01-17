## imports ##
import random

## object class for Pokémon ##
class Pokemon:
    def __init__(self, data: dict):
        self._num = int(data["num"])
        self._name = data["name"]
        self._img = data.get("img")

        self._types = set(data.get("type", []))
        self._weaknesses = set(data.get("weaknesses", []))

        self._evolves_from = "prev_evolution" in data
        self._evolves_into = "next_evolution" in data

    ## properties for safe frontend fetching ##
    @property
    def name(self):
        return self._name

    @property
    def num(self):
        return self._num

    @property
    def img(self):
        return self._img

    @property
    def types(self):
        return list(self._types)

    @property
    def weaknesses(self):
        return list(self._weaknesses)

    ## methods for checking traits ##
    def has_type(self, t: str) -> bool:
        return t in self._types

    def is_dual_type(self) -> bool:
        return len(self._types) > 1

    def has_weakness(self, w: str) -> bool:
        return w in self._weaknesses
    
    def weakness_count(self) -> int:
        return len(self._weaknesses)

    def evolves_from(self) -> bool:
        return self._evolves_from

    def evolves_into(self) -> bool:
        return self._evolves_into

## object class for Question ##
class Question:
    def __init__(self, qid: str, text: str, predicate):
        self._id = qid
        self._text = text
        self._predicate = predicate

    # method to split and remove none matching Pokémon
    def split(self, pokemons):
        yes, no = [], []
        for p in pokemons:
            (yes if self._predicate(p) else no).append(p)
        return yes, no

## actual game logic, "AI"-system ##
class PokemonGuesser:
    TOP_K = 3 # random between top 3 questions
    MIN_SPLIT_QUALITY = 0.2

    # avoid constant number questions
    MAX_NUMBER_QUESTIONS = 6
    MIN_STEPS_BETWEEN_NUMBER = 2
    
    # limit for no progress where number question is allowed
    NO_PROGRESS_TRIGGER = 2

    def __init__(self, pokemon_list):
        self._all_pokemon = pokemon_list
        self._remaining = pokemon_list[:]
        self._asked_questions = []

        # for tracking
        self._since_number_question = 999
        self._no_progress_steps = 0
        self._last_remaining = len(self._remaining)
        self._number_questions_used = 0  # 🔥 test expects this

        self._all_questions = self.generate_questions()
        self._question_map = {q._id: q for q in self._all_questions}

    # method for specifically Pokémon-number question
    def number_question(self, qid=None):
        if qid is None:
            # find "middle" num value Pokémon and split accordingly
            sorted_pokemon = sorted(self._remaining, key=lambda p: p._num)
            mid = len(sorted_pokemon) // 2
            threshold = sorted_pokemon[mid]._num
            qid = f"num:<{threshold}"
        else:
            threshold = int(qid.split("<")[1])

        return Question(
            qid,
            f"Is your Pokémon's number less than {threshold}?",
            lambda p, t=threshold: p._num < t
        )

    # reconstruct number-question with right limit
    def reconstruct_question(self, qid):
        if qid.startswith("num:<"):
            return self.number_question(qid)
        return self._question_map.get(qid)

    # method to generate all other questions
    def generate_questions(self):
        questions = []
        all_types = set()
        all_weaknesses = set()
        all_weakness_counts = set()

        # register all possible types, weaknsesses and amounts
        for p in self._all_pokemon:
            all_types.update(p._types)
            all_weaknesses.update(p._weaknesses)
            all_weakness_counts.add(len(p._weaknesses))

        # question for one or dual type Pokémon
        questions.append(Question(
            "dual_type",
            "Does your Pokémon have more than one type?",
            lambda p: p.is_dual_type()
        ))

        # ask for previous evolution
        questions.append(Question(
            "evolves_from",
            "Does your Pokémon evolve from another Pokémon?",
            lambda p: p.evolves_from()
        ))

        # ask for next evolution
        questions.append(Question(
            "evolves_into",
            "Does your Pokémon evolve into another Pokémon?",
            lambda p: p.evolves_into()
        ))

        # ask for number of weaknesses
        for n in sorted(all_weakness_counts):
            questions.append(Question(
                f"weakness_gt:{n}",
                f"Does your Pokémon have more than {n} weaknesses?",
                lambda p, n=n: p.weakness_count() > n
            ))

        # ask for specific type
        for t in all_types:
            questions.append(Question(
                f"type:{t}",
                f"Is your Pokémon a {t} type?",
                lambda p, t=t: p.has_type(t)
            ))

        # ask for specific weakness
        for w in all_weaknesses:
            questions.append(Question(
                f"weakness:{w}",
                f"Is your Pokémon weak to {w}?",
                lambda p, w=w: p.has_weakness(w)
            ))

        return questions

    # returns quality of split, closer to 50/50 is ideal
    def split_quality(self, question):
        yes, no = question.split(self._remaining)
        total = len(self._remaining)

        if not yes or not no:
            return 0.0

        return min(len(yes), len(no)) / total

    # AI-brain behind questioning
    def choose_best_question(self):
        # Pokémon is known (1 left)
        if len(self._remaining) <= 1:
            return None

        # do not repeat questions
        candidates = [
            q for q in self._all_questions
            if q not in self._asked_questions
        ]

        # evaluete questions, strong = better, weak = worse
        strong = []
        weak = []

        # use split_quality() to determine strong/weak
        for q in candidates:
            quality = self.split_quality(q)

            if quality >= self.MIN_SPLIT_QUALITY:
                strong.append((quality, q))
            elif quality > 0:
                weak.append((quality, q))

        # sort list of strong questions and return random
        if strong:
            strong.sort(key=lambda x: x[0], reverse=True)
            return random.choice([q for _, q in strong[:self.TOP_K]])

        # only use number-question if progress is slow and other rules allow it
        if (
            self._number_questions_used < self.MAX_NUMBER_QUESTIONS
            and (
                self._since_number_question >= self.MIN_STEPS_BETWEEN_NUMBER
                or self._no_progress_steps >= self.NO_PROGRESS_TRIGGER
            )
        ):
            self._number_questions_used += 1
            return self.number_question()

        # sort list of weak questions and return one
        if weak:
            weak.sort(key=lambda x: x[0], reverse=True)
            return weak[0][1]

        # last resort use of number questions
        self._number_questions_used += 1
        return self.number_question()

    # game logic, splitting logic
    def apply_answer(self, question, answer: bool):
        before = len(self._remaining)

        yes, no = question.split(self._remaining)
        self._remaining = yes if answer else no
        self._asked_questions.append(question)

        after = len(self._remaining)

        # track progress
        if after >= before:
            self._no_progress_steps += 1
        else:
            self._no_progress_steps = 0

        # track use of number question
        if question._id.startswith("num:<"):
            self._since_number_question = 0
        else:
            self._since_number_question += 1

    # one Pokémon left, guess
    def should_guess(self):
        return len(self._remaining) <= 1

    # guess Pokémon (should be correct or None)
    def guess(self):
        return self._remaining[0] if self._remaining else None