import scrabble

list_of_words = scrabble.wordlist
scoring_parameter = scrabble.scores

user_rack = input("Please list your rack > ").lower()
rack_list = []
for letter in user_rack:
	rack_list.append(letter)

def valid_word(word, rack):
	available_letters = rack[:]

	for letter in word:
		if letter not in available_letters:
			return False
		available_letters.remove(letter)
	return True

def compute_score(word):
	score = 0
	for letter in word:
		score = score + scoring_parameter[letter]
	return score

valid_words = []

# Calling the functions
for word in list_of_words:
	if valid_word(word, rack_list):
		score = compute_score(word)
		valid_words.append([score, word])
print(valid_words)

valid_words.sort()

for i in valid_words:
	score = i[0]
	word = i[1]
	print(word + ": " + str(score))
