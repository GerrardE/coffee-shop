import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
# Set up cors and allow '*' for origins
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES

# Handle GET requests for all available drinks.
@app.route('/drinks')
@cross_origin()
def get_all_drinks():
    drinks = Drink.query.all()
    try:
        drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)


# Handle GET requests for all available drinks.
@app.route('/drinks-detail')
@cross_origin()
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    try:
        drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)

# Handle endpoint to POST a new drink
@app.route('/drinks', methods=['POST'])
@cross_origin()
@requires_auth('post:drinks')
def post_drink(jwt):
    # Declare and empty data dictionary to hold all retrieved variables
    data = request.get_json()

    # set drink variable equal to corresponding model class,
    # ready for adding to the session
    recipe = data.get('recipe')
    recipe = json.dumps(recipe)

    drink = Drink(
        title=data.get('title'),
        recipe=recipe
    )

    try:
        drink.insert()
    except Exception:
        abort(400)

    drinks = Drink.query.all()
    try:
        drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)


# Handle endpoint to PATCH an existing drink
@app.route('/drinks/<int:id>', methods=['PATCH'])
@cross_origin()
@requires_auth('patch:drinks')
def patch_drink(jwt, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    # Declare and empty data dictionary to hold all retrieved variables
    data = request.get_json()

    # set drink variable equal to corresponding model class,
    # ready for adding to the session

    title = data.get('title')
    recipe = data.get('recipe')
    recipe = json.dumps(recipe)

    try:
        drink.title = title
        drink.recipe = recipe
        drink.update()
    except Exception:
        abort(422)

    drinks = Drink.query.all()
    try:
        drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)


# Handle endpoint to DELETE an existing drink
@app.route('/drinks/<int:id>', methods=['DELETE'])
@cross_origin()
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
    except Exception:
        abort(422)

    drinks = Drink.query.all()
    try:
        drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)

# Error Handling
@app.errorhandler(422)
def unprocessable_req(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable request"
    }), 422


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def failed_req(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "request failed"
    }), 400

# handle unauthorized client error
@app.errorhandler(AuthError)
def unauthorized_request(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized client error",
    }), 401


# handle unauthorized client error
@app.errorhandler(401)
def unauthorized_req(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized client error",
    }), 401


# handle forbidden errors
@app.errorhandler(403)
def forbidden_req(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden request. Please contact your administrator.",
    }), 403

# handle server errors
@app.errorhandler(500)
def server_err(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error.",
    }), 500
