import random
current_hand = []

def drawnextcard():
	global current_hand
	current_hand.append(random.randrange(1,10))

def gethandvalue():
	return sum(current_hand)

def play():
	global current_hand
	if gethandvalue() <= 21:
		drawnextcard()
	if gethandvalue() > 21:
		print("Busted.")
	if gethandvalue() == 21:
		print("You win!")

