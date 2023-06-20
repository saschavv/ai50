from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

baseA = And(
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)))

baseB = And(
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)))

baseC = And(
    Implication(CKnight, Not(CKnave)),
    Implication(CKnave, Not(CKnight)))

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    baseA,
    Or(And(AKnight, sentence0),
       And(AKnave, Not(sentence0))))


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1 = And(AKnave, BKnave)
knowledge1 = And(
    baseA,
    baseB,
    Or(And(AKnight, sentence1),
       And(AKnave, Not(sentence1)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence2_1 = Or(And(AKnight,BKnight),And(AKnave,BKnave))
sentence2_2 = Or(And(AKnight,BKnave),And(AKnave,BKnight))
knowledge2 = And(
    baseA,
    baseB,
    Or(And(AKnight,sentence2_1),
       And(AKnave, Not(sentence2_1))),
    Or(And(BKnight, sentence2_2),
    And(BKnave, Not(sentence2_2)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
sentence3_1 = Or(AKnight, AKnave)
sentence3_2 = Or(Implication(AKnight, AKnave),
                 Implication(AKnave, Not(AKnave)))

knowledge3 = And(
    baseA,
    baseB,
    baseC,
    Or(And(AKnight, sentence3_1),
       And(AKnave, Not(sentence3_1))
    ),
    Or(
        And(BKnight, sentence3_2),
        And(BKnave,  Not(sentence3_2))
    ),
    Or(
        Implication(BKnight, CKnave),
        Implication(BKnave, Not(CKnave))
    ),
    Or(
        Implication(CKnight, AKnight),
        Implication(CKnave, Not(AKnight))
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
