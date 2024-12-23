import os

from dotenv import load_dotenv
from mistralai import Mistral

from utils import *

load_dotenv()


def get_cover_letter(offer="", resume=""):
    """
    Uses the Ollama API to generate a cover letter in English from a job offer, a cover letter template, and personal information.

    Args:
        offer (str): The job offer from which the cover letter should be generated.
        cover_letter_template (str): The template that should be followed to generate the cover letter.
        resume (str): The resume information that should be included in the cover letter.

    Returns:
        str: The generated cover letter.

    Raises:
        Exception: If there was an error calling the Ollama API.
    """
    try:

        prompt = f"""
        Tu es un expert en rédaction de lettre de motivation.
        Je te fournis un offre d'emploi et des informations personnelles.
        Tu dois utiliser ces informations pour composer une lettre de motivation en francais.
        Dans un premier temps, présente mon profil, en disant que je veux me spécialiser dans l'intelligence artificielle.
        Ensuite, aborde mon parcours académique et mes experiences professionnelles.
        Parle ensuite de mes projets personnels et professionnels, qui m'ont permis de mieux comprendre le domaine de l'intelligence artificielle et de monter en competences.
        certaines experiences ont un tag "!Important", n'hésite pas a mettre l'accent dessus.
        - Offre d'emploi:\n{offer}
        - Informations personnelles:\n{resume}

        En t'aidant de ces informations, compose une lettre de motivation en francais, ave des paragraphes distincts et clairs.
        Inclus les liens vers mon proifl github (Alfred0404), linkedin (alfred-de-vulpian) et mon portfolio (alfreddevulpian.vercel.app) a la fin de la lettre de motivation.

        N'indique pas mon numero de telephone, seulement mon mail (alfred.devulpian@edu.ece.fr).
        N'indique pas mon nom, adresse, code postal ou ville et ne met pas de date.
        ne met pas de nom de l'entreprise, adresse de l'entreprise, code postal ou ville de l'entreprise et ne met pas de date.
        cette lettre est sous la forme d'un document pdf, pas une lettre physique.
        ne mets pas d'objet non plus.

        """

        print("[get_cover_letter]\tGenerating cover letter...")
        api_key = os.environ["MISTRAL_API_KEY"]
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)

        chat_response = (
            client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            .choices[0]
            .message.content
        )

        print("[get_cover_letter]\tresponse:\n", chat_response)

        return chat_response

    except Exception as e:
        print(f"[get_cover_letter]\tError: {e}")
        raise


def main():
    offer = read_file(filename="./offers/offer.txt")
    personal_infos = read_file(filename="./inputs/resume.txt")

    save_file(
        filename="./cover_letters/saved_cover_letter.txt",
        content=get_cover_letter(offer, personal_infos),
    )


if __name__ == "__main__":
    main()
