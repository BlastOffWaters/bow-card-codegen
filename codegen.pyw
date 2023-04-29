from guizero import App, Text, Box, Combo, TextBox, Window, PushButton
import mysql.connector
import random
import json

# Create the basic setup
app = App(title="Code Generator")
title = Text(app, "Code Generator - Bow Card Project", 16)
spacer1 = Text(app, "", 5)
group = Box(app, layout="grid")
# Pick options to generate codes
number_to_generate_explain = Text(group, "Enter the number of codes to generate:", grid=[0,1])
number_to_generate = TextBox(group, grid=[1,1], text="1")
spacer2 = Text(group, "", 5, grid=[0,2])
type_to_generate_explain = Text(group, "Select the code type you are generating:", grid=[0,3])
type_to_generate = Combo(group, options=["Card", "Game Token"], grid=[1,3])
# Pop up the codes after being generated and submitted
def list_codes(code_list):
    # Create a basic display setup
    code_list_window = Window(app, title="Generated Codes")
    title2 = Text(code_list_window, "Generated Codes", size=14)
    codes_shown = Text(code_list_window, text=code_list, size=12)
# Add the generated code to the database
def add_code_to_db(code):
    # Print the code
    print("Code submitting to database, code is " + code)
    # Pick what type to add to the database table
    if type_to_generate.value == "Card":
        type_generating = "card"
    elif type_to_generate.value == "Game Token":
        type_generating = "game_token"
    # Load the MySQL credentials from a JSON file
    with open('mysql_credentials.json') as f:
        credentials = json.load(f)
    # Connect to the MySQL database using the retrieved credentials
    try:
        database = mysql.connector.connect(
            user=credentials['user'],
            password=credentials['password'],
            host=credentials['host'],
            database=credentials['database']
        )
        print("Connected to MySQL database")
    except mysql.connector.Error as err:
        print("Failed to connect to MySQL database: {}".format(err))
    # Add the data to the database
    mycursor = database.cursor()
    sql = "INSERT INTO general_data (code, type) VALUES (%s, %s)"
    val = (code, type_generating)
    mycursor.execute(sql, val)
    if type_generating == "card":
        sql2 = "INSERT INTO card_data (code, is_filled_out) VALUES (%s, %s)"
        val2 = (code, 0)
        mycursor.execute(sql2, val2)
    elif type_generating == "game_token":
        sql2 = "INSERT INTO game_data (code, plays) VALUES (%s, %s)"
        val2 = (code, 3)
        mycursor.execute(sql2, val2)
    database.commit()
# Generate the code and submit it to the database function
def generate_code():
    # Create an empty list of codes
    code_list = []
    # Generate the required number of codes
    for x in range(int(number_to_generate.value)):
        # Create an empty code string
        generated_code = ""
        # Generate 16 characters
        for y in range(16):
            # Pick if it should pick a number or a letter
            letter_or_number = random.randint(0, 1)
            # If it should pick a number, do so below
            if letter_or_number == 0:
                code_number = random.randint(0, 9)
                generated_code = generated_code + str(code_number)
            # If it should pick a letter, do so below
            else:
                alphabet = 'abcdefghijklmnopqrstuvwxyz'
                code_letter = random.choice(alphabet)
                generated_code = generated_code + code_letter
        # Send code to the database function
        add_code_to_db(generated_code)
        # Add the new code to the code list
        code_list.append(generated_code)
    else:
        # After all codes are submitted, send the list to the list function
        list_codes(code_list)
# Run the generate codes function
spacer3 = Text(app, "", 5)
submit_button = PushButton(app, command=generate_code, text="Generate Codes")
# Add a note so people do not interrupt the process
spacer4 = Text(app, "", 5)
note = Text(app, "Note: This may take a little, as codes must be sent to the database.")
# Make the app display
app.display()