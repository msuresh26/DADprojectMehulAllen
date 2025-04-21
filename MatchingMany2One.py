import random
from collections import defaultdict

class Mentee:
    def __init__(self, name, preferences, interests):
        self.name = name
        self.preferences = preferences  # Top 3 mentors
        self.interests = interests
        self.mentors = []  # List of assigned mentors

class Mentor:
    def __init__(self, name, preferences, interests):
        self.name = name
        self.preferences = preferences  # Top 3 mentees
        self.interests = interests

# Jaccard-based similarity: higher overlap → lower score (score out of 4)
def similarityScore(mentee, mentor):
    set1, set2 = set(mentee.interests), set(mentor.interests)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    similarity = intersection / union if union else 0
    return 4 - similarity * 3  # normalize to 1–4 range (lower is better)

def count_blocking_pairs(mentees, mentors, matches, match_scores):
    # Build quick lookup for current matches
    mentor_to_mentee = {}
    for mentee_name, mentor_list in matches.items():
        for mentor_name in mentor_list or []:
            mentor_to_mentee[mentor_name] = mentee_name

    blocking_pairs = 0

    for mentee in mentees:
        current_mentors = matches.get(mentee.name, [])
        for mentor in mentors:
            if mentor.name in current_mentors:
                continue  # Already matched

            # Get score between this mentee and mentor
            candidate_score = match_scores.get((mentee.name, mentor.name), (float('inf'), float('inf')))
            candidate_total = sum(candidate_score)

            # Check if mentee prefers this mentor over at least one current match
            mentee_prefers = False
            for current in current_mentors:
                current_score = match_scores.get((mentee.name, current), (float('inf'), float('inf')))
                current_total = sum(current_score)
                if candidate_total < current_total:
                    mentee_prefers = True
                    break

            # Check if mentor prefers this mentee over their current match
            current_mentee_name = mentor_to_mentee.get(mentor.name)
            mentor_prefers = False
            if current_mentee_name:
                current_score = match_scores.get((current_mentee_name, mentor.name), (float('inf'), float('inf')))
                current_total = sum(current_score)
                if candidate_total < current_total:
                    mentor_prefers = True
            else:
                mentor_prefers = True  # Mentor is unassigned, so any match is preferred

            if mentee_prefers and mentor_prefers:
                print(f"Blocking pair found: {mentee.name} ↔ {mentor.name}")
                blocking_pairs += 1

    return blocking_pairs


def stable_match_with_scores(mentees, mentors):
    mentee_matches = defaultdict(list)  # List of mentors for each mentee
    mentor_matches = {}  # Tracks which mentee each mentor is matched with
    match_scores = {}
    available_mentees = mentees.copy()
    available_mentors = set(mentors)

    while available_mentees:
        mentee = available_mentees.pop(0)

        for mentor_name in mentee.preferences:
            mentor = next((m for m in mentors if m.name == mentor_name), None)
            if mentor in available_mentors and len(mentee_matches[mentee.name]) < 2:
                mentee_matches[mentee.name].append(mentor.name)
                mentor_matches[mentor.name] = mentee.name
                available_mentors.remove(mentor)

                mentee_score = mentee.preferences.index(mentor.name) + 1
                if mentee.name in mentor.preferences:
                    mentor_score = mentor.preferences.index(mentee.name) + 1
                else:
                    mentor_score = 3 + similarityScore(mentee, mentor)
                match_scores[(mentee.name, mentor.name)] = (mentee_score, mentor_score)
                break
        else:
            best_mentor = None
            best_total_score = float('inf')
            best_pair_score = ()
            for mentor in available_mentors:
                if mentor.name in mentee.preferences:
                    mentee_score = mentee.preferences.index(mentor.name) + 1
                else:
                    mentee_score = 3 + similarityScore(mentee, mentor)

                if mentee.name in mentor.preferences:
                    mentor_score = mentor.preferences.index(mentee.name) + 1
                else:
                    mentor_score = 3 + similarityScore(mentee, mentor)

                total_score = mentee_score + mentor_score

                if total_score < best_total_score and len(mentee_matches[mentee.name]) < 2:
                    best_total_score = total_score
                    best_pair_score = (mentee_score, mentor_score)
                    best_mentor = mentor

            # Now assign the best match
            if best_mentor:
                mentee_matches[mentee.name].append(best_mentor.name)
                match_scores[(mentee.name, best_mentor.name)] = best_pair_score
                available_mentors.remove(best_mentor)
            else:
                mentee_matches[mentee.name] = None

    # Assign remaining unmatched mentors to mentees with less than 2 mentors
    for mentor in available_mentors:
        best_mentee = None
        best_score = float('inf')
        best_pair_score = ()

        # Find a mentee with less than 2 mentors and the best match score
        for mentee in mentees:
            if len(mentee_matches[mentee.name]) < 2:
                mentee_score = 3+ similarityScore(mentee, mentor)
                if mentee.name in mentor.preferences:
                    mentor_score = mentor.preferences.index(mentee.name) + 1
                else:
                    mentor_score = 3 + similarityScore(mentee, mentor)
                total_score = mentor_score + mentee_score
                if total_score < best_score:
                    best_score = total_score
                    best_pair_score = (mentee_score, mentor_score)
                    best_mentee = mentee

        if best_mentee:
            mentee_matches[best_mentee.name].append(mentor.name)
            match_scores[(best_mentee.name, mentor.name)] = best_pair_score

    return mentee_matches, match_scores

# Sample mentees and mentors
mentees = [
    Mentee("Mentee1", preferences=["Mentor1", "Mentor2", "Mentor3"], interests=["AI", "Data Science", "Python", "Startups"]),
    Mentee("Mentee2", preferences=["Mentor2", "Mentor3", "Mentor1"], interests=["Design", "AI", "Leadership", "Startups"]),
    Mentee("Mentee3", preferences=["Mentor3", "Mentor1", "Mentor2"], interests=["AI", "Python", "Robotics", "Gaming"]),
    Mentee("Mentee4", preferences=["Mentor1", "Mentor3", "Mentor2"], interests=["AI", "Blockchain", "Startups", "VR"]),
    Mentee("Mentee5", preferences=["Mentor2", "Mentor1", "Mentor4"], interests=["Leadership", "Data Science", "Design", "VR"]),
    Mentee("Mentee6", preferences=["Mentor4", "Mentor1", "Mentor3"], interests=["Gaming", "Startups", "AI", "Blockchain"]),
    Mentee("Mentee7", preferences=["Mentor1", "Mentor3", "Mentor2"], interests=["Robotics", "Gaming", "Design", "Startups"]),
    Mentee("Mentee8", preferences=["Mentor3", "Mentor2", "Mentor4"], interests=["AI", "Robotics", "Data Science", "Leadership"])
]

mentors = [
    Mentor("Mentor1", preferences=["Mentee2", "Mentee1", "Mentee3"], interests=["Python", "Data Science", "AI", "ML"]),
    Mentor("Mentor2", preferences=["Mentee1", "Mentee3", "Mentee4"], interests=["Design", "Product", "Leadership", "AI"]),
    Mentor("Mentor3", preferences=["Mentee3", "Mentee2", "Mentee4"], interests=["AI", "Startups", "Gaming", "VR"]),
    Mentor("Mentor4", preferences=["Mentee3", "Mentee2", "Mentee4"], interests=["Data Science", "Leadership", "Blockchain", "Startups"]),
    Mentor("Mentor5", preferences=["Mentee1", "Mentee5", "Mentee6"], interests=["AI", "Robotics", "Startups", "Gaming"]),
    Mentor("Mentor6", preferences=["Mentee7", "Mentee8", "Mentee5"], interests=["Design", "Leadership", "Blockchain", "AI"]),
    Mentor("Mentor7", preferences=["Mentee6", "Mentee8", "Mentee7"], interests=["Startups", "Gaming", "Blockchain", "Leadership"]),
    Mentor("Mentor8", preferences=["Mentee8", "Mentee7", "Mentee5"], interests=["AI", "VR", "Robotics", "Data Science"])
]


# Run the stable matching algorithm with scores
matches, match_scores = stable_match_with_scores(mentees, mentors)

# Output the matches and scores
# print("Matches and Scores:")
# total_score = 0
# for mentee_name, mentor_names in matches.items():
#     for mentor_name in mentor_names:
#         score = match_scores.get((mentee_name, mentor_name), "N/A")
#         total_score += score
#         print(f"{mentee_name} -> {mentor_name} (Score: {score:.2f})")
# print(f"Total score: {total_score:.2f}\n*lower score is better")

print("Matches and Scores:")
total_score = 0
for mentee_name, mentor_names in matches.items():
    for mentor_name in mentor_names:
        score_pair = match_scores.get((mentee_name, mentor_name), (0, 0))
        mentee_score, mentor_score = score_pair
        combined_score = mentee_score + mentor_score
        total_score += combined_score
        print(f"{mentee_name} -> {mentor_name} (Mentee Score: {mentee_score:.2f}, Mentor Score: {mentor_score:.2f}, Total: {combined_score:.2f})")
print(f"Total score: {total_score:.2f}\n*lower score is better")

blocking_pairs = count_blocking_pairs(mentees, mentors, matches, match_scores)
print(f"Number of blocking pairs: {blocking_pairs}")