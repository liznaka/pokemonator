import random

class PokemonGuesser:
    def __init__(self, pokemon_list, asked_questions=None):
        self.remaining = pokemon_list.copy()
        self.asked_questions = asked_questions or []
        # lowest num 0001
        self.min_num = min(int(p["num"]) for p in self.remaining)
        # highest num 0151
        self.max_num = max(int(p["num"]) for p in self.remaining)


        # mark fully evolved as "yes"/"no"
        for p in self.remaining:
            p["fully_evolved"] = "yes" if not p.get("next_evolution") else "no"

     
    def apply_answer(self, attribute, value, answer):
        self.asked_questions.append({
            "attribute": attribute,
            "value": value
        })

        if attribute == "num_lt":
            cutoff = int(value)
            if answer == "yes":
                self.remaining = [p for p in self.remaining if int(p["num"]) < cutoff]
                self.max_num = cutoff - 1
            else:
                self.remaining = [p for p in self.remaining if int(p["num"]) >= cutoff]
                self.min_num = cutoff
            return
        elif attribute == "fully_evolved":
            self.remaining = [p for p in self.remaining if p[attribute] == answer]
        else:
            if answer == "yes":
                self.remaining = [p for p in self.remaining if value in p.get(attribute, [])]
            else:
                self.remaining = [p for p in self.remaining if value not in p.get(attribute, [])]

    def get_remaining(self):
        return self.remaining

    # extract values for given from remaining Pokémon
    def extract_unique_values(self, key):
        values = set()
        for poke in self.remaining:
            for v in poke.get(key, []):
                values.add(v)
        return sorted(values)

    def best_question(self):
        # return next question, or None
        types = self.extract_unique_values("type")
        weaknesses = self.extract_unique_values("weaknesses")
        questions = [
            {"attribute": "type", "values": types},
            {"attribute": "weaknesses", "values": weaknesses},
            {"attribute": "fully_evolved", "values": ["yes", "no"]}
        ]

        asked_keys = {(q["attribute"], q["value"]) for q in self.asked_questions}
        candidates = []

        for q in questions:
            for value in q["values"]:
                if (q["attribute"], value) in asked_keys:
                    continue

                yes = [
                    p for p in self.remaining
                    if (p[q["attribute"]] == value if q["attribute"] == "fully_evolved" else value in p.get(q["attribute"], []))
                ]
                no = [
                    p for p in self.remaining
                    if p not in yes
                ]

                # ignore questions that don't split Pokémon
                if len(yes) == 0 or len(no) == 0:
                    continue

                score = abs(len(yes) - len(no))  # smaller = more balanced
                candidates.append((score, {"attribute": q["attribute"], "value": value}))

         # only ask number question once
        if not any(q["attribute"] == "num_lt" for q in self.asked_questions):
            nums = sorted(int(p["num"]) for p in self.remaining)
            mid = nums[len(nums) // 2]
            yes = [p for p in self.remaining if int(p["num"]) < mid]
            no = [p for p in self.remaining if int(p["num"]) >= mid]
            if yes and no:  # only valid if it splits remaining
                score = abs(len(yes) - len(no))
                candidates.append((score, {"attribute": "num_lt", "value": mid}))

        if not candidates:
            return None

        # pick the most balanced candidate
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]
    
        