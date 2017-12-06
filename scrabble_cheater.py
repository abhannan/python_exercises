import scrabble
import string

list_of_words = scrabble.wordlist
scoring_parameter = scrabble.scores

user_rack = input("Please list your rack > ").lower()

rack_list = []
for letter in user_rack:
	if letter in string.ascii_lowercase:
		rack_list.append(letter)
	else:
		blank_count = user_rack.count("_")

def valid_word(word, rack):
	available_letters = rack_list[:]
	missing_counter = 0

	for letter in word:
		if letter in available_letters:		
			available_letters.remove(letter)
		else:
			missing_counter += 1
	if missing_counter <= blank_count:
		return word

def compute_score(word):
	available_letters = rack_list[:]
	score = 0
	for letter in word:
		if letter in available_letters:
			score = score + scoring_parameter[letter]
	return score

valid_words = []

for word in list_of_words:
	if valid_word(word, rack_list):
		score = compute_score(word)
		valid_words.append([score, word])

valid_words.sort()

for result in valid_words:
	score = result[0]
	word = result[1]
	print(word + ": " + str(score))
