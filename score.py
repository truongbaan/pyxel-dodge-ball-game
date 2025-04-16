#function to get and write the score for saving
def save_score(score_list, filename="scores.txt"):
    #Saves a list of tuples to a text file.
    with open(filename, "w") as file:
        for score_tuple in score_list:
            file.write(str(score_tuple) + "\n")

def load_scores(filename = "scores.txt"):
    scores = []
    try:
        with open(filename, "r") as file:
            for line in file:
                map_number, score, cleared = line.strip()[1 : -1].split(",") # 1 and -1 is to ignore the '[' and the ']'
                scores.append([int(map_number), int(score), int(cleared)])
    except FileNotFoundError:
        print(f"File not found: {filename}. Initializing default scores.")
        scores = [[i, 0, 0] for i in range(24)]
        save_score(scores, filename)  # Create the file with default values
    return scores

if __name__ == "__main__":
    #to reset if needed
    reset = []
    for i in range(24):
        reset.append([i, 0, 0])
    save_score(reset)