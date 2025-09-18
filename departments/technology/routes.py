from flask import Blueprint, render_template
from flask_login import login_required, current_user

technology_bp = Blueprint('technology', __name__, template_folder='templates/technology')

@technology_bp.route('/dashboard')
@login_required
def dashboard():
    # Maybe check that current_user.department == 'Operations'
    if current_user.department.lower() != 'technology':
        return "Unauthorized", 403
    return render_template('dashboard.html', user=current_user)
