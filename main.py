import speech_recognition as sr
import json
import re

# Initialize recognizer
recognizer = sr.Recognizer()

# Predefined menu and questions
menu_options = {
    "header": ["Truck Serial Number", "Truck Model","Inspection ID","Inspector Name","Inspection Employee ID"],
    "tyres": ["Tire Pressure for Left Front", "Tire Pressure for Right Front","Tire Condition for Left Front – (Good, Ok, Needs Replacement)",
              "Tire Condition for Right Front – (Good, Ok, Needs Replacement)",
              "Tire Pressure for Left Rear","Tire Pressure for Right Rear",
              "Tire Condition for Left Rear – (Good, Ok, Needs Replacement)",
              "Tire Condition for Right Rear – (Good, Ok, Needs Replacement)",
              "Overall Tire Summary: (<1000 characters)","Attached images of each tire in the same order."],
    "option 3": ["Question 3.1", "Question 3.2"],
    "option 4": ["Question 4.1", "Question 4.2"],
    "option 5": ["Question 5.1", "Question 5.2"]
}

# Function to recognize speech
def recognize_speech(recognizer, source):
    try:
        recognizer.adjust_for_ambient_noise(source,0.2)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        speech = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {speech}")
        return speech
    except sr.UnknownValueError:
        print("Sorry, I did not understand that. Could you please repeat?")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

# Function to guide through the menu
def navigate_menu(recognizer):
    selected_option = None
    print("Please choose a menu option by saying one of the following: ", ", ".join(menu_options.keys()))

    with sr.Microphone() as source:
        while not selected_option:
            input("Press Enter when you are ready to speak.")
            speech = recognize_speech(recognizer, source)
            if speech in menu_options:
                selected_option = speech
                print(f"You selected {selected_option}")
            else:
                print("Option not recognized, please try again.")

    return selected_option

# Function to ask questions and record answers
def ask_questions(selected_option, recognizer):
    answers = {}
    questions = menu_options[selected_option]

    for question in questions:
        print(question)
        answers[question] = []

        with sr.Microphone() as source:
            while True:
                input("Press Enter when you are ready to speak.")
                print("Listening for your answer. Say 'over' when done.")
                speech = recognize_speech(recognizer, source)
                if "over" in speech:
                    speech = str(speech)
                    s = re.findall('over.*$', speech)
                    if s != []:
                        speech = speech.replace(s[0], '')
                    answers[question].append(speech)
                    break

    return answers

# Function to ask if the user wants to continue
def ask_continue(recognizer):
    print("Do you want to continue to the next menu? Please say 'yes' or 'no'.")

    with sr.Microphone() as source:
        while True:
            input("Press Enter when you are ready to speak.")
            speech = recognize_speech(recognizer, source)
            if "yes" in speech:
                return True
            elif "no" in speech:
                return False
            else:
                print("Response not recognized, please say 'yes' or 'no'.")

# Main function
def main():
    all_answers = {}
    completed_options = set()

    while len(completed_options) < len(menu_options):
        selected_option = navigate_menu(recognizer)
        if selected_option in completed_options:
            print("You have already completed this option. Please choose another.")
            continue

        answers = ask_questions(selected_option, recognizer)
        all_answers[selected_option] = answers
        completed_options.add(selected_option)

        if len(completed_options) < len(menu_options):
            if not ask_continue(recognizer):
                break
        else:
            print("You have completed all menu options.")
            break

    # Save answers to a JSON file
    with open("answers.json", "w") as f:
        json.dump(all_answers, f, indent=4)
    print("Your answers have been saved.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()
