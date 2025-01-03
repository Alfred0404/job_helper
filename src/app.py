from flask import Flask, render_template, request, send_file, after_this_request
from handle_cover_letter import generate_cover_letter
import os
import tempfile

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


@app.route("/save", methods=["POST"])
def save_cover_letter():
    """Save cover letter to a file and send it as a response to the user."""

    cover_letter_content = request.form["cover-letter"]
    print(cover_letter_content)

    # Utiliser un fichier temporaire pour éviter les conflits de noms de fichiers
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        filename = tmp_file.name
        try:
            tmp_file.write(cover_letter_content.encode("utf-8"))
            tmp_file.flush()  # Assurez-vous que les données sont écrites sur le disque

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(filename)
                except Exception as error:
                    app.logger.error(
                        "Error removing or closing downloaded file handle", error
                    )
                return response

            return send_file(
                filename, as_attachment=True, download_name="cover_letter.txt"
            )
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
