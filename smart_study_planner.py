# Smart Study Planner
# A console-based Python program for recording study sessions

import json


# List used to store all study sessions
sessions = []

# File used to save the study sessions
FILE_NAME = "study_log.txt"


def classify_session(duration):
    """
    Classifies a study session according to its duration.
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def load_sessions():
    """
    Loads previously saved study sessions from the text file.
    """
    global sessions

    try:
        with open(FILE_NAME, "r") as file:
            sessions = json.load(file)

        print(f"{len(sessions)} saved session(s) loaded successfully.")

    except FileNotFoundError:
        sessions = []
        print("No previous study records found.")

    except json.JSONDecodeError:
        sessions = []
        print("The study log is empty or damaged. Starting with no sessions.")


def save_sessions():
    """
    Saves all study sessions to the text file.
    """
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(sessions, file, indent=4)

        print("Study sessions saved successfully.")

    except OSError:
        print("The study sessions could not be saved.")


def get_valid_duration():
    """
    Requests a positive duration from the user.
    It continues asking until the user enters a valid number.
    """
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))

            if duration > 0:
                return duration
            else:
                print("Duration must be greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a valid positive number.")


def add_session():
    """
    Allows the user to enter and store a new study session.
    """
    print("\n--- Add a Study Session ---")

    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date or day: ").strip()
    duration = get_valid_duration()

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)

    classification = classify_session(duration)

    print("\nStudy session added successfully.")
    print(f"Session classification: {classification}")


def view_sessions():
    """
    Displays all recorded study sessions in a formatted table.
    """
    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded.")
        return

    print("-" * 88)
    print(
        f"{'No.':<5}"
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date/Day':<15}"
        f"{'Minutes':<12}"
        f"{'Class':<10}"
    )
    print("-" * 88)

    for number, session in enumerate(sessions, start=1):
        classification = classify_session(session["duration"])

        print(
            f"{number:<5}"
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12g}"
            f"{classification:<10}"
        )

    print("-" * 88)


def search_sessions():
    """
    Searches for study sessions using a subject name.
    """
    print("\n--- Search Sessions by Subject ---")

    if not sessions:
        print("No study sessions have been recorded.")
        return

    search_subject = input("Enter the subject to search for: ").strip().lower()

    matching_sessions = []

    for session in sessions:
        if search_subject in session["subject"].lower():
            matching_sessions.append(session)

    if not matching_sessions:
        print(f"No sessions were found for '{search_subject}'.")
        return

    print(f"\nSessions found for '{search_subject}':")
    print("-" * 83)
    print(
        f"{'No.':<5}"
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date/Day':<15}"
        f"{'Minutes':<10}"
        f"{'Class':<8}"
    )
    print("-" * 83)

    total_minutes = 0

    for number, session in enumerate(matching_sessions, start=1):
        duration = session["duration"]
        classification = classify_session(duration)
        total_minutes += duration

        print(
            f"{number:<5}"
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{duration:<10g}"
            f"{classification:<8}"
        )

    print("-" * 83)
    print(f"Number of matching sessions: {len(matching_sessions)}")
    print(f"Total study time: {total_minutes:g} minutes")


def view_statistics():
    """
    Calculates and displays useful study statistics.
    """
    print("\n--- Study Statistics ---")

    if not sessions:
        print("No study sessions are available for analysis.")
        return

    total_sessions = len(sessions)
    total_minutes = sum(session["duration"] for session in sessions)
    average_duration = total_minutes / total_sessions

    short_sessions = 0
    medium_sessions = 0
    long_sessions = 0

    subject_totals = {}

    for session in sessions:
        duration = session["duration"]
        classification = classify_session(duration)

        if classification == "Short":
            short_sessions += 1
        elif classification == "Medium":
            medium_sessions += 1
        else:
            long_sessions += 1

        subject = session["subject"]

        if subject in subject_totals:
            subject_totals[subject] += duration
        else:
            subject_totals[subject] = duration

    longest_session = max(sessions, key=lambda session: session["duration"])
    weakest_subject = min(subject_totals, key=subject_totals.get)
    strongest_subject = max(subject_totals, key=subject_totals.get)

    print(f"Total number of sessions: {total_sessions}")
    print(f"Total study time: {total_minutes:g} minutes")
    print(f"Average session duration: {average_duration:.2f} minutes")

    print("\nSession classifications:")
    print(f"Short sessions: {short_sessions}")
    print(f"Medium sessions: {medium_sessions}")
    print(f"Long sessions: {long_sessions}")

    print("\nStudy time by subject:")

    for subject, minutes in subject_totals.items():
        print(f"{subject}: {minutes:g} minutes")

    print(
        f"\nLongest session: {longest_session['subject']} - "
        f"{longest_session['topic']} "
        f"({longest_session['duration']:g} minutes)"
    )

    print(
        f"Subject with the most study time: "
        f"{strongest_subject} ({subject_totals[strongest_subject]:g} minutes)"
    )

    print(
        f"Subject needing more attention: "
        f"{weakest_subject} ({subject_totals[weakest_subject]:g} minutes)"
    )


def display_menu():
    """
    Displays the main menu.
    """
    print("\n================================")
    print("       SMART STUDY PLANNER")
    print("================================")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("================================")


def main():
    """
    Controls the main operation of the program.
    """
    load_sessions()

    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()

        elif choice == "2":
            view_sessions()

        elif choice == "3":
            search_sessions()

        elif choice == "4":
            view_statistics()

        elif choice == "5":
            save_sessions()
            print("Thank you for using the Smart Study Planner.")
            break

        else:
            print("Invalid menu choice. Please select a number from 1 to 5.")


# Starts the program
if __name__ == "__main__":
    main()