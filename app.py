from flask import Flask, render_template, request

app = Flask(__name__)

# Load and search for the best sequence
def find_best_sequence(target_score):
    best_seq = None
    best_score = None
    best_length = None
    max_score_seen = 0

    with open("clean_sequences.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            try:
                length = int(parts[0])
                score = int(parts[1])
                sequence = parts[2:]

                if score > max_score_seen:
                    max_score_seen = score

                if score >= target_score:
                    if best_score is None or score < best_score:
                        best_score = score
                        best_seq = sequence
                        best_length = length
            except:
                continue

    if best_seq:
        return best_score, best_length, best_seq
    else:
        return None, None, max_score_seen

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            target = int(request.form["score"].replace(",", ""))
            best_score, best_length, best_seq = find_best_sequence(target)

            if isinstance(best_seq, list):
                result = {
                    "score": best_score,
                    "length": best_length,
                    "sequence": " ".join(best_seq),
                    "input": target
                }
            else:
                result = {"error": f"No sequence found ≥ {target}. Max available: {best_seq}"}
        except ValueError:
            result = {"error": "Invalid number. Please enter a valid score."}

    return render_template("index.html", result=result)

if __name__ == "__main__":
app.run(host='0.0.0.0', port=5000)

