from . import bp
from flask import render_template
from flask_babel import _

@bp.app_errorhandler(404)
def error_404(error):
    return render_template('error_404.html', title=_('Page not found'), error=error), 404

@bp.app_errorhandler(500)
def error_500(error):
    return render_template('error_500.html', title=_('Application error'), error=error), 500