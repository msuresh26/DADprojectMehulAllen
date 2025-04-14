from collections import defaultdict

def stable_match(mentees, mentors):
    # Create dictionaries to track matches and availability
    mentee_matches = {}
    mentor_matches = defaultdict(list)
    available_mentees = list(mentees.keys())

    # While there are available mentees
    while available_mentees:
        mentee = available_mentees.pop(0)
        mentee_prefs = mentees[mentee]

        # Try to match the mentee with their top preferences
        for mentor in mentee_prefs:
            if mentor not in mentor_matches or len(mentor_matches[mentor]) < len(mentees):  # Mentor can have multiple mentees
                mentee_matches[mentee] = mentor
                mentor_matches[mentor].append(mentee)
                break
            else:
                # Check if the mentor prefers this mentee over any of their current matches
                mentor_prefs = mentors[mentor]
                least_preferred_mentee = max(
                    mentor_matches[mentor],
                    key=lambda m: mentor_prefs.index(m) if m in mentor_prefs else float('inf')
                )
                mentee_rank = mentor_prefs.index(mentee) if mentee in mentor_prefs else float('inf')
                least_preferred_rank = mentor_prefs.index(least_preferred_mentee) if least_preferred_mentee in mentor_prefs else float('inf')

                if mentee_rank < least_preferred_rank:
                    # Replace the least preferred mentee with the new one
                    mentor_matches[mentor].remove(least_preferred_mentee)
                    mentor_matches[mentor].append(mentee)
                    mentee_matches[mentee] = mentor
                    available_mentees.append(least_preferred_mentee)
                    break
        else:
            # If no match is found, mentee remains unmatched
            mentee_matches[mentee] = None

    return mentee_matches

# Example input
mentees = {
    "Mentee1": ["Mentor1", "Mentor2", "Mentor3"],
    "Mentee2": ["Mentor2", "Mentor3", "Mentor1"],
    "Mentee3": ["Mentor3", "Mentor1", "Mentor2"],
    "Mentee4": ["Mentor1", "Mentor3", "Mentor2"]
}

mentors = {
    "Mentor1": ["Mentee2", "Mentee1", "Mentee3", "Mentee4"],
    "Mentor2": ["Mentee1", "Mentee3", "Mentee4", "Mentee2"],
    "Mentor3": ["Mentee3", "Mentee2", "Mentee4", "Mentee1"],
    "Mentor4": ["Mentee3", "Mentee2", "Mentee4", "Mentee1"]
}

# Run the stable matching algorithm
matches = stable_match(mentees, mentors)

# Output the matches
print("Matches:")
for mentee, mentor in matches.items():
    print(f"{mentee} -> {mentor}")