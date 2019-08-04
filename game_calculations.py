
def calculate_turns(days):
    turns = 3*int(days)
    return turns

def calculate_food(days):
    food = (3*int(days))-12
    return food

def calculate_hungry(player_selected, game_stats):

    if not game_stats[player_selected]["eating"]:
        game_stats[player_selected]["health"] -= 10
        game_stats[player_selected]["last_turn"] += "You didn't eat: -10 hitpoints because of hunger.\n"

        if game_stats[player_selected]["turns_no_eaten"] == 3:
            game_stats[player_selected]["health"] -= 10
            game_stats[player_selected]["turns_no_eaten"] = 0
            game_stats[player_selected]["last_turn"] += "You haven't eaten during 3 meals: -10 more hitpoints because of hunger.\n"

        else:
            game_stats[player_selected]["turns_no_eaten"] += 1

    else:

        if game_stats[player_selected]['food'] >= 1:
            game_stats[player_selected]['food'] -= 1
            game_stats[player_selected]["turns_no_eaten"] = 0
            game_stats[player_selected]["last_turn"] += "You ate: -1 nugget.\n"

        else:
            game_stats[player_selected]["last_turn"] += "You don't have any food.\n"
            game_stats[player_selected]["health"] -= 10
            game_stats[player_selected]["last_turn"] += "You didn't eat: -10 hitpoints because of hunger.\n"

            if game_stats[player_selected]["turns_no_eaten"] == 3:
                game_stats[player_selected]["health"] -= 10
                game_stats[player_selected]["turns_no_eaten"] = 0
                game_stats[player_selected]["last_turn"] +=  "You haven't eaten during 3 meals: -10 more hitpoints because of hunger.\n"

            else:
                game_stats[player_selected]["turns_no_eaten"] += 1

    return game_stats

def calculate_attack(player_selected, enemy, game_stats):

    if game_stats[player_selected]["attacking"]:

        if not game_stats[enemy]["defending"]:

            if game_stats[enemy]['food'] >= 2:

                game_stats[enemy]['food'] -= 2
                game_stats[player_selected]['food'] += 2
                game_stats[player_selected]["last_turn"] += "You managed to steal successfully: +2 nuggets.\n"
                game_stats[enemy]["last_turn"] += "You have been stolen successfully: -2 nuggets.\n"

            elif (game_stats[enemy]['food'] < 2) and (game_stats[enemy]['food'] > 0):

                game_stats[player_selected]["food"] += game_stats[enemy]['food']
                game_stats[enemy]['food'] = 0
                game_stats[player_selected]["last_turn"] += "You managed to steal successfully: +1 nuggets.\n"
                game_stats[enemy]["last_turn"] += "You have been stolen successfully: -1 nuggets.\n"

            else:

                game_stats[player_selected]["last_turn"] += "You almost managed to steal, but the other person doesn't have any food.\n"
                game_stats[enemy]["last_turn"] += "The other person almost managed to steal to you, but you don't have any food.\n"

        elif game_stats[enemy]["defending"]:

            if game_stats[player_selected]['food'] >= 1:

                game_stats[enemy]['food'] += 1
                game_stats[player_selected]['food'] -= 1
                game_stats[player_selected]["last_turn"] += "You failed to steal: -1 nugget.\n"
                game_stats[enemy]["last_turn"] += "The other person failed to steal: +1 nugget.\n"

            else:
                game_stats[player_selected]["last_turn"] += "You failed to steal and you don't have any food to lose.\n"
                game_stats[enemy]["last_turn"] += "The other person failed to steal to you and he doesn't have any food to lose.\n"

    return game_stats

def return_to_neutral(player_selected, game_stats):

    game_stats[player_selected]["eating"] = False
    game_stats[player_selected]["defending"] = False
    game_stats[player_selected]["attacking"] = False
    game_stats[player_selected]["ready"] = False

    return game_stats

def see_if_alive(player_selected, game_stats):

    if game_stats[player_selected]["health"] <= 0:
        game_stats[player_selected]["alive"] = False
        game_stats[player_selected]["last_turn"] += "You have starved to death.\n"

    if not game_stats[player_selected]["alive"]:
        game_stats["game_over"] = True

    return game_stats

def game_calculations(game_dictionary):

    for index in range(1, 3):
        player = "player_"+str(index)
        game_dictionary = calculate_hungry(player, game_dictionary)

    for index in range(1, 3):
        player = "player_"+str(index)

        if player == "player_1":
            enemy = "player_2"

        else:
            enemy = "player_1"

        game_dictionary = calculate_attack(player, enemy, game_dictionary)

    for index in range(1, 3):

        player = "player_"+str(index)
        game_dictionary = return_to_neutral(player, game_dictionary)
        game_dictionary = see_if_alive(player, game_dictionary)

    game_dictionary["turns"] -= 1

    if game_dictionary['turns'] == 0:
        game_dictionary['game_over'] = True

    game_dictionary['server_checked'] = True

    return game_dictionary