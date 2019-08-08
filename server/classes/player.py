class Player:
    score, civet, grelottine, launched = 0, 0, 0, 0
    name = ""

    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def add_score(self, score, by):
        self.score += score
        print(f"{self.name} vient d'obtenir {score} grace a {by}, son score est desormais de {self.score}")

    def remove_score(self, score):
        self.score -= score

        if self.score < 0:
            self.score = 0
        print(f"{self.name} vient de perdre {score} son score est desormais de {self.score}")

    def add_civet(self):
        self.civet += 1

    def add_grelottine(self):
        if self.grelottine > 0:
            print(f"{self.name} possède déjà une Grelottine")
            return
        print(f"{self.name} vient de gagner une Grelottine")
        self.grelottine = 1

    def available_civet(self):
        return self.civet
