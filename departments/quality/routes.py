from flask import Blueprint, render_template
from flask_login import login_required, current_user

quality_bp = Blueprint('quality', __name__, template_folder='templates/quality')

@quality_bp.route('/dashboard')
@login_required
def dashboard():
    # Maybe check that current_user.department == 'Operations'
    if current_user.department.lower() != 'quality':
        return "Unauthorized", 403
    return render_template('dashboard.html', user=current_user)
