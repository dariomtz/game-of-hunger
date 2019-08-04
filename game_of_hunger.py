import pyrebase
import os
import atexit
import time
import game_calculations

def return_to_neutral():
	game().child(player_name).update({'ready': False})
	game().child(enemy_name).update({'ready': False})

	game().child(player_name).update({'eating': True})
	game().child(player_name).update({'attacking': True})
	game().child(player_name).update({'defending': True})

	game().child(enemy_name).update({'eating': True})
	game().child(enemy_name).update({'attacking': True})
	game().child(enemy_name).update({'defending': True})

def final_function():
	if game().child('server_name').get().val() == player_name:
		game().update({'server': False})
		
	players_online = game().child('players_online').get().val()
	game().update({'players_online': (players_online - 1)})

	game().child(player_name).update({'ready': True})

	if game().child('players_online').get().val() == 0:
		game().remove()

def game():
	g = db.child("game_rooms").child('-' + room_code)
	return g

config = {
  "apiKey": "AIzaSyDT-WgTSmyeVxv8uHaSYJqVMQq-Pnf0an0",
  "authDomain": "hunger-games-c7ab1.firebaseapp.com",
  "databaseURL": "https://hunger-games-c7ab1.firebaseio.com",
  "storageBucket": "hunger-games-c7ab1.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

atexit.register(final_function)

os.system('clear')

room_code = ''

print('\nTHE GAME OF HUNGER\n')

print('This is a stategy game about SURVIVING')
print('You are trapped in an island with another person and your resources are limited.\n')

print('Help is on its way and will arrive in six days,')
print('but there\'s not enough food for the two of you.')
print('So, you and the other person devided the food you had in two equal parts parts:')
print(' * 12 chicken nuggets')
print('Therefore you have 6.\n')
print('From now on your priority is to SURVIVE\n')
print('Every breakfast, lunch and dinner you will have to choose between:')
print('-->Eating from your nuggets')
print('-->Stealing nuggets from the other.')
print('-->Protect your nuggets\n')

print('¡Psst!Hey!\n')
print('I want to remind you that the other person won\'t be nice in order to SURVIVE.\n')


while True:
	print('1 = Create a new game')
	print('2 = Join a game-room')
	type_of_game = input('>>')

	os.system('clear')

	if type_of_game == '1':

		days = 6

		new_player = {
			'health':120,
			'food': game_calculations.calculate_food(days),
			'turns_no_eaten': 0,
			'eating': False,
			'defending': False,
			'attacking': False,
			'alive': True,
			'ready': False,
			'last_turn': ''
		}

		new_game = {
			'server': False,
			'players_online': 0,
			'server_checked': False,
			'server_name': '',
			'days': days,
			'turns': game_calculations.calculate_turns(days),
			'game_over': False,
			'player_1': new_player,
			'player_2': new_player
		}

		room = db.child("game_rooms").push(new_game)
		room_code = room['name'][1:]
		print('\nYou are now in a new game-room!\n')
		break

	elif type_of_game == '2':

		while True:

			print('Write the code of the game-room:')
			r_c = input('>>')
			ref_ = db.child("game_rooms").child('-' + r_c).get()
			players = db.child("game_rooms").child('-' + r_c).child('players_online').get()
			os.system('clear')

			if str(ref_.val()) == 'None':
				print('Invalid code.')

			elif players.val() == 2:
				print('The game-room is already full.')

			else:
				room_code = r_c
				break

		break

	else:
		print('Invalid option')

player_name = ''
game_is_over = False
days = [6,5,4,3,2,1]
food_hours = ['Dinner', 'Lunch', 'Breakfast']
decision = ''
turn_ = 18

players_online = game().child('players_online').get().val()

if players_online == 0:
	player_name = 'player_1'
	enemy_name = 'player_2'

	game().update({'server': True})
	game().update({'server_name': player_name})
	game().update({'players_online': (players_online + 1)})
	
elif players_online == 1:

	server_name = game().child('server_name').get()
	if server_name.val() == 'player_1':
		player_name = 'player_2'
		enemy_name = 'player_1'

	else:
		player_name = 'player_1'
		enemy_name = 'player_2'

	game().update({'players_online': (players_online + 1)})

while not game().child('game_over').get().val():
	if game().child('server_name').get().val() == player_name:
		game().update({'server_checked': False})


	if game().child('players_online').get().val() == 1:
		print('\nYour game-room code is: ' + str(room_code) + '\n')
		print('Waiting for the other player to join...')

		animation = "|/-\\"
		idx = 0

		while game().child('players_online').get().val() == 1:
			print('	',animation[idx % len(animation)], end="\r")
			idx += 1
			time.sleep(0.1)

	os.system('clear')

	if game().child('turns').get().val() != turn_:

		animation = "|/-\\"
		idx = 0

		while game().child('turns').get().val() != turn_:
			print('	',animation[idx % len(animation)], end="\r")
			idx += 1
			time.sleep(0.1)

	os.system('clear')

	print('\n' ,player_name, '\n' )
	#print('Turno: ', game().child('turns').get().val())
	print(food_hours[(game().child('turns').get().val()-1)%3], 'of day', days[int((game().child('turns').get().val()+2)/3)-1]) 
	print('Your hitpoints:', game().child(player_name).child('health').get().val(), '/ 120')
	print('Your nuggets:', game().child(player_name).child('food').get().val())

	if not game().child('turns').get().val() == 18:
		print('\n',game().child(player_name).child('last_turn').get().val())
		game().child(player_name).update({'last_turn': ''})

	while True:
		print('\nYou must choose:')
		print('	1 = Eat')
		print('	2 = Steal nuggets')
		print('	3 = Protect your own nuggets')
		decision = input('>>')

		if decision == '1':
			game().child(player_name).update({'eating': True})
			break

		elif decision == '2':
			game().child(player_name).update({'attacking': True})
			break

		elif decision == '3':
			game().child(player_name).update({'defending': True})
			break

		else:
			print('Invalid option')

	print('You are ready!')
	game().child(player_name).update({'ready': True})

	if not game().child(enemy_name).child('ready').get().val():
		print('Waiting for the other player to choose...')
		animation = "|/-\\"
		idx = 0

		while not game().child(enemy_name).child('ready').get().val():
			print('	',animation[idx % len(animation)], end="\r")
			idx += 1
			time.sleep(0.1)

	if game().child('players_online').get().val() == 1:
		print('The other player is offline :(')
		print('You will have to choose again this meal.')

		if not game().child('server').get().val():
			#make me server
			game().update({'server': True})
			game().update({'server_name': player_name})

		#return to neutral
		return_to_neutral()

		continue

	if game().child('server_name').get().val() == player_name and game().child('players_online').get().val() == 2:
		
		game_dict = game().get().val()

		game().set(game_calculations.game_calculations(game_dict))
		
	turn_ -= 1

	if not game().child('server_checked').get().val():

		animation = "|/-\\"
		idx = 0

		while not game().child('server_checked').get().val():
			print('	',animation[idx % len(animation)], end="\r")
			idx += 1
			time.sleep(0.1)

if game().child(player_name).child('alive').get().val() and not game().child(enemy_name).child('alive').get().val():
	print('\nYou won! :)\n')

elif not game().child(player_name).child('alive').get().val() and game().child(enemy_name).child('alive').get().val(): 
	print('\nYou lost! :(\n')

elif game().child(player_name).child('alive').get().val() == game().child(enemy_name).child('alive').get().val():
	print('\nYou tied! :/\n')





