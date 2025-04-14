from collections import defaultdict

def stable_match(mentees, mentors):
    # Create dictionaries to track matches and availability
    mentee_matches = {}
    mentor_matches = defaultdict(list)
    available_mentees = list(mentees.keys())

    # # While there are available mentees
    # while available_mentees:
    #     mentee = available_mentees.pop(0)
    #     mentee_prefs = mentees[mentee]

    #     # Try to match the mentee with their top preferences
    #     for mentor in mentee_prefs:
    #         if len(mentor_matches[mentor]) < 1:  # Each mentor can have one mentee
    #             mentee_matches[mentee] = mentor
    #             mentor_matches[mentor].append(mentee)
    #             break
    #         else:
    #             # Check if the mentor prefers this mentee over their current match
    #             current_mentee = mentor_matches[mentor][0]
    #             mentor_prefs = mentors[mentor]
    #             if mentor_prefs.index(mentee) < mentor_prefs.index(current_mentee):
    #                 # Replace the current mentee with the new one
    #                 mentor_matches[mentor][0] = mentee
    #                 mentee_matches[mentee] = mentor
    #                 available_mentees.append(current_mentee)
    #                 break
    #     else:
    #         # If no match is found, mentee remains unmatched
    #         mentee_matches[mentee] = None

    # While there are available mentees
    while available_mentees:
        mentee = available_mentees.pop(0)
        mentee_prefs = mentees[mentee]

        # Try to match the mentee with their top preferences
        for mentor in mentee_prefs:
            if len(mentor_matches[mentor]) < 1:  # Each mentor can have one mentee
                mentee_matches[mentee] = mentor
                mentor_matches[mentor].append(mentee)
                break
            else:
                # Check if the mentor prefers this mentee over their current match
                current_mentee = mentor_matches[mentor][0]
                mentor_prefs = mentors[mentor]
                # Use a high index if the mentee is not in the mentor's preference list
                mentee_rank = mentor_prefs.index(mentee) if mentee in mentor_prefs else float('inf')
                current_mentee_rank = mentor_prefs.index(current_mentee) if current_mentee in mentor_prefs else float('inf')
                if mentee_rank < current_mentee_rank:
                    # Replace the current mentee with the new one
                    mentor_matches[mentor][0] = mentee
                    mentee_matches[mentee] = mentor
                    available_mentees.append(current_mentee)
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
    "Mentor1": ["Mentee2", "Mentee1", "Mentee3"],
    "Mentor2": ["Mentee1", "Mentee3", "Mentee4"],
    "Mentor3": ["Mentee3", "Mentee2", "Mentee4"],
    "Mentor4": ["Mentee3", "Mentee2", "Mentee4"]
}

# Run the stable matching algorithm
matches = stable_match(mentees, mentors)

# Output the matches
print("Matches:")
for mentee, mentor in matches.items():
    print(f"{mentee} -> {mentor}")