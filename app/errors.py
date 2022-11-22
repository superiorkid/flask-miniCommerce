from werkzeug.exceptions import InternalServerError, NotFound
from flask import render_template


def error_handlers(app, db):

    @app.errorhandler(InternalServerError)
    def internal_server_error(*args, **kwargs):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(NotFound)
    def not_found(*args, **kwargs):
        return render_template('errors/404.html'), 404
