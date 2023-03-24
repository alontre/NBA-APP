from jnius import autoclass
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timedelta

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


# Define a function to return only some values of a dictionary
def only_print_some(array):
    text = ""
    # Iterate over the values in the dictionary
    for i in array.values():
        # Concatenate the second and third values of the list, separated by spaces, and a newline character
        text += str(i[1]) + "   " + str(i[2]) + "\n"
    return text

# Define a function to calculate the time difference between two input times
def how_much_time(time1, time2):
    # Parse the input times as datetime objects
    time1 = datetime.strptime(time1, "%H:%M")
    time2 = datetime.strptime(time2, "%H:%M")

    # Handle the case where time2 is on the next day
    if time2 < time1:
        time2 += timedelta(days=1)

    # Calculate the time difference and return it
    return time2 - time1

# Define a function to remove the last value from every list in a dictionary
def remove_last_value(dictionary):
    # Create a new dictionary to hold the modified values
    new_dict = {}

    # Iterate over the key-value pairs in the dictionary
    for key, value in dictionary.items():
        # Create a new list with the last value removed from the original list
        new_list = value[:-1]
        # Add the modified list to the new dictionary
        new_dict[key] = new_list

    # Return the new dictionary
    return new_dict

# Define a function to return a table of data in a dictionary
def print_table(data):
    # Remove the last value from each list in the dictionary
    data = remove_last_value(data)
    text = ""
    # Define the headers for the table
    headers = ["ID", "TEAMS", "TIME"]
    # Get the length of the longest list in the values of the dictionary
    max_len = max(data) + 1
    # Print the headers
    header_str = ' | '.join(headers)
    text += header_str + "\n"
    text += ('--' * len(header_str))
    # Print the rows of the table
    text += "\n"
    for j in range(int(list(data.keys())[0]), int(max_len)):
        row = []
        for i in range(len(headers)):
            if i < len(data[j]):
                # Right-align values for numeric columns and left-align for other columns
                if headers[i].isdigit():
                    text += (f" {data[j][i]:>{len(headers[i])}}")
                else:
                    text += (f" {data[j][i]:<{len(headers[i])}}")
            else:
                # Pad empty cells with spaces to align with headers
                text += (' ' * len(headers[i]))
        text += (' | '.join(row))
        text += "\n"
    return text


def get_games(half):
    # Initialize variables
    i = 0
    games_today = {}
    board = scoreboard.ScoreBoard()

    # Get the games for the day
    games = board.games.get_dict()
    end = len(games)

    # Loop through each game and add it to the games_today dictionary
    for game in games:
        if half == "second": # If looking for second half of a day games
            if i > int(len(games) * 0.5): # Only add games from the second half of the day
                # Get the game time and add the game to the games_today dictionary
                game_time = str(parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone())[11:16]
                games_today[i] = [i, (game['awayTeam']['teamName'] + " vs " + game['homeTeam']['teamName']), game_time,
                                  game['gameId']]
        else: # If looking for first half of a day games
            # Get the game time and add the game to the games_today dictionary
            game_time = str(parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone())[11:16]
            games_today[i] = [i, (game['awayTeam']['teamName'] + " vs " + game['homeTeam']['teamName']), game_time,
                              game['gameId']]
            if i > (len(games)) * 0.5 - 1 and half == "first": # Only add games from the first half of the day
                break # If we've added all the first half games, break out of the loop

        i += 1 # Increment the counter

    # If we're looking for first or second half games, return the games_today dictionary as a table
    if half == "first" or half == "second":
        return print_table(games_today)
    else: # Otherwise, return the games_today dictionary
        return games_today



def new_dict(my_dict, choice):
    print_table(my_dict)
    # Get a list of the keys in the dictionary
    keys = list(my_dict.keys())
    # Get a string of index positions separated by commas from the user
    indices_string = choice
    # Split the string into a list of individual index positions
    index_list = indices_string.split(",")
    # Create a new dictionary with the keys and values from the specified index positions
    new_dict = {keys[int(i)]: my_dict[keys[int(i)]] for i in index_list}
    return new_dict
