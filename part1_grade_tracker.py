# ============================================================
# Task 1 - Data Parsing & Profile Cleaning
# Student Grade Tracker
# ============================================================

raw_students = [
    {"name": "  ayesha SHARMA  ", "roll": "101", "marks_str": "88, 72, 95, 60, 78"},
    {"name": "ROHIT verma",       "roll": "102", "marks_str": "55, 68, 49, 72, 61"},
    {"name": "  Priya Nair  ",    "roll": "103", "marks_str": "91, 85, 88, 94, 79"},
    {"name": "karan MEHTA",       "roll": "104", "marks_str": "40, 55, 38, 62, 50"},
    {"name": " Sneha pillai ",    "roll": "105", "marks_str": "75, 80, 70, 68, 85"},
]

# We'll store all cleaned students here so we can use them later
cleaned_students = []

# -- Step 1: Loop through raw data and clean each student ---------------------
for student in raw_students:

    # Clean the name: strip whitespace from both ends, then apply Title Case
    clean_name = student["name"].strip().title()

    # Convert roll number from string to integer
    clean_roll = int(student["roll"])

    # Split the marks string on ", " and convert each piece to an integer
    clean_marks = [int(m) for m in student["marks_str"].split(", ")]

    # Build a clean student dictionary
    cleaned = {
        "name":  clean_name,
        "roll":  clean_roll,
        "marks": clean_marks,
    }
    cleaned_students.append(cleaned)

    # -- Step 2: Validate the name --------------------------------------------
    # Split name into individual words and check every word is alphabetic only
    # .isalpha() returns True only if all characters are letters (no digits/symbols)
    words = clean_name.split()
    is_valid = all(word.isalpha() for word in words)

    if is_valid:
        print(f"[VALID]   Valid name   - {clean_name}")
    else:
        print(f"[INVALID] Invalid name - {clean_name}")

    # -- Step 3: Print formatted profile card ---------------------------------
    print("================================")
    print(f"Student : {clean_name}")
    print(f"Roll No : {clean_roll}")
    print(f"Marks   : {clean_marks}")
    print("================================")
    print()  # blank line between cards for readability

# -- Step 4: Find roll 103 and print name in ALL CAPS and lowercase -----------
for student in cleaned_students:
    if student["roll"] == 103:
        print(f"Roll 103 - ALL CAPS  : {student['name'].upper()}")
        print(f"Roll 103 - lowercase : {student['name'].lower()}")
        break  # found what we need, no point continuing the loop


# ============================================================
# Task 2 - Marks Analysis Using Loops & Conditionals
# ============================================================

print()
print("============================================================")
print("Task 2 - Marks Analysis")
print("============================================================")

student_name = "Ayesha Sharma"
subjects     = ["Math", "Physics", "CS", "English", "Chemistry"]
marks        = [88, 72, 95, 60, 78]


# -- Helper function: assign a grade based on marks --------------------------
# Putting this in a function avoids repeating the if/elif block every time
def get_grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"


# -- Part 1: Print each subject with marks and grade label -------------------
print(f"\nStudent: {student_name}")
print("-" * 40)
print(f"{'Subject':<12} {'Marks':>6} {'Grade':>6}")
print("-" * 40)

for i in range(len(subjects)):
    subject = subjects[i]
    score   = marks[i]
    grade   = get_grade(score)
    print(f"{subject:<12} {score:>6} {grade:>6}")

print("-" * 40)


# -- Part 2: Calculate total, average, highest and lowest --------------------

total   = sum(marks)
average = round(total / len(marks), 2)

# Find highest: loop through and track which index has the biggest mark
highest_index = 0
for i in range(1, len(marks)):
    if marks[i] > marks[highest_index]:
        highest_index = i

# Find lowest: same idea but looking for the smallest mark
lowest_index = 0
for i in range(1, len(marks)):
    if marks[i] < marks[lowest_index]:
        lowest_index = i

print(f"\nTotal marks   : {total}")
print(f"Average marks : {average}")
print(f"Highest       : {subjects[highest_index]} ({marks[highest_index]})")
print(f"Lowest        : {subjects[lowest_index]} ({marks[lowest_index]})")


# -- Part 3: While loop - simulated marks-entry system -----------------------
print()
print("--------------------------------------------")
print("Marks Entry System - type 'done' to stop")
print("--------------------------------------------")

new_subjects_added = 0  # counter for how many valid subjects were added

while True:

    # Ask for subject name first
    subject_input = input("Enter subject name (or 'done' to stop): ").strip()

    # Stop condition: user typed 'done'
    if subject_input.lower() == "done":
        break

    # Ask for marks for that subject
    marks_input = input(f"Enter marks for {subject_input} (0-100): ").strip()

    # Validate: check the input is actually a number
    # .isdigit() only works for integers, so we use a try/except to catch decimals too
    try:
        new_mark = float(marks_input)

        # Validate: check the number is within the allowed range
        if 0 <= new_mark <= 100:
            # Valid entry - add to both lists and count it
            subjects.append(subject_input)
            marks.append(int(new_mark))  # store as int to match existing marks
            new_subjects_added += 1
            print(f"  Added: {subject_input} - {int(new_mark)}")
        else:
            # Number is outside 0-100 range
            print(f"  WARNING: Marks must be between 0 and 100. '{marks_input}' was not added.")

    except ValueError:
        # Input could not be converted to a number at all
        print(f"  WARNING: '{marks_input}' is not a valid number. Entry was not added.")

# After the loop: print summary
print()
print("--------------------------------------------")
print(f"New subjects added : {new_subjects_added}")

# Recalculate average across all subjects (original + new)
updated_total   = sum(marks)
updated_average = round(updated_total / len(marks), 2)
print(f"Updated average    : {updated_average} (across {len(marks)} subjects)")
print("--------------------------------------------")


# ============================================================
# Task 3 - Class Performance Summary
# ============================================================

print()
print("============================================================")
print("Task 3 - Class Performance Summary")
print("============================================================")

class_data = [
    ("Ayesha Sharma",  [88, 72, 95, 60, 78]),
    ("Rohit Verma",    [55, 68, 49, 72, 61]),
    ("Priya Nair",     [91, 85, 88, 94, 79]),
    ("Karan Mehta",    [40, 55, 38, 62, 50]),
    ("Sneha Pillai",   [75, 80, 70, 68, 85]),
]

# -- Step 1: Compute average and result status for each student ---------------
# We build a processed list so we can loop through it multiple times below
# Each entry stores: (name, average, status)
processed = []

for name, marks_list in class_data:

    # Round average to 2 decimal places
    avg = round(sum(marks_list) / len(marks_list), 2)

    # Pass if average is 60 or above, otherwise Fail
    status = "Pass" if avg >= 60 else "Fail"

    processed.append((name, avg, status))


# -- Step 2: Print formatted class report table ------------------------------
print()
print(f"{'Name':<18}| {'Average':^7} | Status")
print("-" * 40)

for name, avg, status in processed:
    # :>6.2f means: right-align, width 6, exactly 2 decimal places
    print(f"{name:<18}| {avg:>6.2f}  | {status}")

print()


# -- Step 3: Summary statistics ----------------------------------------------

# Count passes and fails by looping and checking the status field
pass_count = 0
fail_count = 0

for name, avg, status in processed:
    if status == "Pass":
        pass_count += 1
    else:
        fail_count += 1

# Find the class topper: student with the highest average
# Start by assuming the first student is the topper, then check the rest
topper_name = processed[0][0]
topper_avg  = processed[0][1]

for name, avg, status in processed[1:]:  # start from index 1, already checked 0
    if avg > topper_avg:
        topper_name = name
        topper_avg  = avg

# Class average: average of all individual averages
all_averages  = [avg for name, avg, status in processed]
class_average = round(sum(all_averages) / len(all_averages), 2)

# Print the summary
print(f"Students passed  : {pass_count}")
print(f"Students failed  : {fail_count}")
print(f"Class topper     : {topper_name} ({topper_avg})")
print(f"Class average    : {class_average}")


# ============================================================
# Task 4 - String Manipulation Utility
# ============================================================

print()
print("============================================================")
print("Task 4 - String Manipulation Utility")
print("============================================================")

essay = "  python is a versatile language. it supports object oriented, functional, and procedural programming. python is widely used in data science and machine learning.  "

# -- Step 1: Strip whitespace from both ends ----------------------------------
# All steps below use clean_essay so we work on the same base string
clean_essay = essay.strip()
print(f"\nStep 1 - Stripped essay:\n{clean_essay}")

# -- Step 2: Title Case -------------------------------------------------------
# .title() capitalises the first letter of every word
title_essay = clean_essay.title()
print(f"\nStep 2 - Title Case:\n{title_essay}")

# -- Step 3: Count occurrences of "python" ------------------------------------
# clean_essay is already all-lowercase after strip(), so .count("python")
# will catch every occurrence without needing .lower() again
python_count = clean_essay.count("python")
print(f"\nStep 3 - Count of 'python': {python_count}")

# -- Step 4: Replace "python" with "Python 🐍" --------------------------------
# Since clean_essay is lowercase, replacing "python" catches all occurrences
replaced_essay = clean_essay.replace("python", "Python 🐍")
print(f"\nStep 4 - After replace:\n{replaced_essay}")

# -- Step 5: Split into sentences on ". " (period + space) -------------------
# This splits at sentence boundaries; the last sentence won't have ". " after it
sentences = clean_essay.split(". ")
print(f"\nStep 5 - Sentences list:\n{sentences}")

# -- Step 6: Print each sentence numbered, ensuring it ends with "." ----------
print("\nStep 6 - Numbered sentences:")
for i, sentence in enumerate(sentences, start=1):
    # .endswith(".") checks if the sentence already has a full stop
    # If not, we add one — this handles the last sentence which loses its "."
    # when we split on ". "
    if not sentence.endswith("."):
        sentence = sentence + "."
    print(f"{i}. {sentence}")
