from flask import Flask, render_template, request
from handle_cover_letter import generate_cover_letter

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    cv_content = request.form["cv-content"]
    job_offer = request.form["job-offer"]
    print(cv_content, job_offer)
    cover_letter_content = generate_cover_letter(cv_content, job_offer)
    return render_template("index.html", cover_letter=cover_letter_content)


if __name__ == "__main__":
    app.run(debug=True)
