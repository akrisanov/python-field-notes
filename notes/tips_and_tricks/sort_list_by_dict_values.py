scores = {
    "joe": 85,
    "jane": 90,
    "alex": 80,
    "beth": 82,
}

students = ["beth", "alex", "jane", "joe"]

# Sort students by their scores, highest first
sorted(students, key=scores.get, reverse=True)
