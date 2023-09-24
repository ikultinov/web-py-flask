from flask import Flask, jsonify, request
from models import Session, Advertisement
from flask.views import MethodView
from schema import CreateAdvertisement, PatchAdvertisement, VALIDATION_CLASS
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def get_advertisement(session: Session, adv_id: int):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, message="advertisement doesn't exist")

    return adv


class AdvertisementView(MethodView):

    def get(self, adv_id: int):
        with Session() as session:
            adv = get_advertisement(session, adv_id)
            return jsonify(
                {
                    "id": adv.id,
                    "article": adv.article,
                    "description": adv.description,
                    "owner": adv.owner,
                    "create_date": adv.create_date.isoformat()
                }
            )

    def post(self):
        json_data = validate_json(request.json, CreateAdvertisement)
        with Session() as session:
            adv = Advertisement(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["advertisement"]} is busy')
            return jsonify({"id": adv.id})

    def patch(self, adv_id: int):
        json_data = validate_json(request.json, PatchAdvertisement)
        with Session() as session:
            adv = get_advertisement(session, adv_id)
            for field, value in json_data.items():
                setattr(adv, field, value)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["advertisement"]} is busy')
            return jsonify(
                {
                    "id": adv.id,
                    "article": adv.article,
                    "description": adv.description,
                    "owner": adv.owner,
                    "create_date": adv.create_date.isoformat()
                }
            )

    def delete(self, adv_id: int):
        with Session() as session:
            adv = get_advertisement(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({"status": "success"})


app.add_url_rule("/advertisement/<int:adv_id>",
                 view_func=AdvertisementView.as_view("with_advertisement_id"),
                 methods=["GET", "PATCH", "DELETE"]
                 )

app.add_url_rule('/advertisement/',
                 view_func=AdvertisementView.as_view("create_advertisement"),
                 methods=['POST']
                 )

if __name__ == "__main__":
    app.run()
