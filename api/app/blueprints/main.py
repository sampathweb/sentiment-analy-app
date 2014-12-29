'''Module for Error handling and messages common to the application'''

from flask import Blueprint

main = Blueprint('main', __name__)


@main.errorhandler(413)
def error_handler_413(e):
    return 'file size too large', 413
