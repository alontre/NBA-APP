import os

os.environ["KIVY_AUDIO"] = "ffpyplayer"

from nba_api.live.nba.endpoints import scoreboard
from time import sleep
from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)



def game():
    print(some)
    # Create a new scoreboard object
    board = scoreboard.ScoreBoard()

    # Get the dictionary of games from the scoreboard object
    games = board.get_dict()

    # Create an empty string to store the game information
    text = ""

    # Print the date of the scoreboard
    # Get the games to display from the games_today attribute of the object
    games_wanted = some[2]

    # Iterate through all the games in the scoreboard
    for i in range(len(games["scoreboard"]["games"])):

        # Check if the game has started
        if games["scoreboard"]["games"][i]["gameStatusText"][1:2].isnumeric() and \
                games["scoreboard"]["games"][i]["gameStatusText"][6:7].isnumeric():

            # Iterate through the games we want to display
            for ii in range(len(list(games_wanted.values()))):

                # Check if the game ID matches the ID of the game we want to display
                if games["scoreboard"]["games"][i]["gameId"] == list(games_wanted.values())[ii][3]:

                    # Calculate the game time in minutes
                    game_time = int(games["scoreboard"]["games"][i]["gameStatusText"][1:2]) * 12 - 12 + \
                                int(games["scoreboard"]["games"][i]["gameStatusText"][3:5])

                    # Get the scores of the two teams
                    score1 = int(games["scoreboard"]["games"][i]["homeTeam"]["score"])
                    score2 = int(games["scoreboard"]["games"][i]["awayTeam"]["score"])

                    # Add the game status and team names and scores to the text string
                    text += str(games["scoreboard"]["games"][i]["gameStatusText"]) + "\n"
                    text += str(str(games["scoreboard"]["games"][i]["homeTeam"]["teamName"]) + "-" + str(score1) + ":" +
                                str(score2) + "-" + str(games["scoreboard"]["games"][i]["awayTeam"]["teamName"]))

                    # Check if the score difference is within the specified range
                    is_score_good2 = score1 - score2 <= some[1] and score1 - score2 >= 0
                    is_score_good = score2 - score1 <= some[1] and score2 - score1 >= 0

                    # Check if the game time and score is within the specified range
                    if list(games_wanted.values())[ii][0] != 100 and (is_score_good or is_score_good2) and (
                            some[0] + game_time) > 48:

                        # Mark the game as displayed
                        list(games_wanted.values())[ii][0] = 100

                        # Play a sound
                        MediaPlayer = autoclass('android.media.MediaPlayer')
                        media_player = MediaPlayer()
                        media_player.setDataSource('ffd.mp3')
                        media_player.prepare()
                        media_player.start()

                        open('mypickle.pk', 'w').close()

                        # Wait until the mp3 is done playing
                        while media_player.isPlaying():
                            sleep(1)

import pickle
a = 0
while True:
    if a == 0:
        a = 1
        for i in range(some[3]):
            sleep(60)
    with open('mypickle.pk', 'rb') as fi:
        some = pickle.load(fi)
    print("service is running...")
    game()
    sleep(10)
