from flask import Blueprint
from flask import jsonify, request, abort
from flask import current_app

portal_mockup = Blueprint('portal_mockup', __name__)

faq_data = [
    {"question": "QUESTION1", "answer": "ANSWER"},
    {"question": "QUESTION2 dasf asd fasd f asdf ads fas df asd fsad f asd fasd f asd f asd fasd f asdf",
        "answer": "ANSWER2 sdaf asd f asdf asd f dsaf sad f asd  ads fasd f sad f asd fsda f sad f asd fsa df asd f asd fa sdf asd fas df asd fas df as df asd fa sdf asd f asd fas df asd f sd fa sd fas df asd f asd fas fa d"},
    {"question": "QUESTION3", "answer": "ANSWER3"},
    {"question": "QUESTION4 dasf asd fasd f asdf ads fas df asd fsad f asd fasd f asd f asd fasd f asdf",
        "answer": "ANSWER4 sdaf asd f asdf asd f dsaf sad f asd  ads fasd f sad f asd fsda f sad f asd fsa df asd f asd fa sdf asd fas df asd fas df as df asd fa sdf asd f asd fas df asd f sd fa sd fas df asd f asd fas fa d"},
]


@portal_mockup.route('/dapmApi/portal', methods=['POST'])
def get():
    try:
        logger = current_app.logger
        data = request.json
        logger.info(f"Received Body={data}")

        response = {
            "status": "Success", "detail": "", "data": faq_data
        }

        logger.info(f"Response={response}")
        return jsonify(response)

    except Exception:
        abort(500)
