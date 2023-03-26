from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timezone, timedelta
from dateutil import parser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.size = (360, 600)

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
        # Get the game time and add the game to the games_today dictionary
        game_time = str(parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone())[11:16]
        games_today[i] = [i, (game['awayTeam']['teamName'] + " vs " + game['homeTeam']['teamName']), game_time,
                          game['gameId']]

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


# Create a Kivy App
class NBA(App):
    # Build the App's UI
    def build(self):
        self.icon = "nbaicon.png"
        # Set the time to 0
        self.time = 0
        # Create a layout to hold the widgets
        self.layout = BoxLayout(orientation='vertical')

        # Create a horizontal layout for the labels
        self.label_layout = BoxLayout(orientation='horizontal')
        # Create three labels with different text
        self.label1 = Label(text=get_games("first"), font_size='16', color='#00FFCE', pos_hint={"center_x": 0.5, "center_y": 0.25})

        self.label_layout.add_widget(self.label1)

        self.label_layout_two = BoxLayout(orientation='horizontal')

        self.label3 = Label(text="Please enter the game/s I'd/s\n with a comma separator.",
                            font_size='16', color='#00FFCE', pos_hint={"center_x": 0.5, "center_y": 0.45})

        self.label_layout_two.add_widget(self.label3)


        # Add the horizontal layout to the main layout
        self.layout.add_widget(self.label_layout)
        self.layout.add_widget(self.label_layout_two)

        # Create text input widgets for the games and maximum time
        self.games_input = TextInput(text="", multiline=False, size_hint=(0.6, 0.2), padding_y=(6, 6), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.max_time_input = TextInput(text="", multiline=False, size_hint=(0.6, 0.2),  padding_y=(6, 6), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Add the text input widgets to the main layout
        self.layout.add_widget(self.games_input)
        self.layout.add_widget(self.max_time_input)

        # Hide the maximum time input field
        self.max_time_input.opacity = 0

        # Create a button to submit the form
        self.submit_button = Button(text="OK", bold=True, background_color='#00FFCE', on_release=self.first_submit
                                    , size_hint=(0.6, 0.5),
                                    pos_hint={"center_x": .5})

        self.layout.add_widget(self.submit_button)

        # Create a label to display the chosen games
        self.chosen_games_label = Label(text="chosen games:\n--------------------------\n", color='#00FFCE', font_size='16')
        self.layout.add_widget(self.chosen_games_label)

        # Return the main layout
        return self.layout

    def first_submit(self, button):
        if self.time == 0:
            # Get the chosen games from the text input widget
            self.chosen_games = self.games_input.text

            # Display the chosen games
            try:
                # Check if the input is valid
                if not self.chosen_games.replace(",", "").isdigit() and self.chosen_games.replace(",", "") > 0:
                    raise("")

                # Display only the chosen games
                self.chosen_games_label.text = "chosen games:\n--------------------------\n" + str(only_print_some(new_dict(get_games("ere"), self.chosen_games)))

            except:
                # Display an error message if the input is invalid
                self.label3.text = "Please enter the game/s I'd/s\n with a comma separator.\n  Error with input try again."

            else:
                # If the input is valid, update the labels and show the next input widget
                self.label1.text = ""
                self.label3.font_size = 16
                self.label3.pos_hint = {"center_x": 0.5, "center_y": 0.85}
                self.label3.text = "Please enter the point difference\n           (in the first area).\n\n And the time left on the clock" \
                                   "\n           (in the second area)."
                self.games_input.text = ""
                self.max_time_input.opacity = 1
                self.time += 1

        else:
            # If the submit button has already been pressed, call the second_submit() function
            self.second_submit()
            self.time += 1


    def second_submit(self):
        print(self.time) # print the current time
        try:
            if (not (self.games_input.text.isdigit()) and int(self.games_input.text > 0) or (not (self.max_time_input.text.isdigit()) and int(self.self.max_time_input.text > 0))):
                # Check if the input for point difference and time is a positive integer, and if not raise an exception
                raise("")
            self.max_score = int(self.games_input.text) # Store the max point difference as an integer
            self.max_time = int(self.max_time_input.text) # Store the max time left in the clock as an integer
        except:
            # If there is an exception, display an error message
            self.label3.font_size = 16
            self.label3.pos_hint = {"center_x": 0.5, "center_y": 0.85}
            self.label3.text = "Please enter the point difference\n           (in the first area).\n\n And the time left on the clock" \
                               "\n           (in the second area).\n\n      Error with input, go again."
        else:
            # If there is no exception, remove the input widgets and submit button
            self.layout.remove_widget(self.submit_button)
            self.layout.remove_widget(self.games_input)
            self.layout.remove_widget(self.max_time_input)
            # Call the wait_to_the_games function with the chosen games and games_today
            self.wait_to_the_games(new_dict(get_games("ere"), self.chosen_games))


    def wait_to_the_games(self, games_today):
        global is_time_right
        # Update the label with the chosen game time and points
        self.chosen_games_label.text = f"\nchosen time:{self.max_time_input.text}\nchosen points:{self.games_input.text}"

        # Store the games for the day
        self.games_today = games_today

        # Update the label to indicate that we are waiting for the games to begin
        self.label3.text = "wait for the games to began"

        # Get the current time
        this_hour = str(datetime.now())[11:16]

        # Get the first game in the list of games for today
        dict_keys = list(games_today.keys())
        v = games_today[dict_keys[0]][2]

        # Determine how many minutes until the game starts
        is_time_right = how_much_time(this_hour, games_today[dict_keys[0]][2])
        print(is_time_right)
        is_time_right = str(is_time_right).split(":")
        is_time_right = int(is_time_right[0]) * 60 + int(is_time_right[1])

        # If the game is more than 12 hours away,that mean that he already started,so wait 1 second and go to the game
        self.start_service()


    @staticmethod
    def start_service():
        from jnius import autoclass
        service = autoclass("org.test.nbaBGBeta.ServiceBack_ground")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, "")
        return service

if __name__ == "__main__":
    NBA().run()
