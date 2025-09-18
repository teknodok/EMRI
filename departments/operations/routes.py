from flask import Blueprint, render_template
from flask_login import login_required, current_user

operations_bp = Blueprint('operations', __name__, template_folder='templates/operations')

@operations_bp.route('/dashboard')
@login_required
def dashboard():
    # Maybe check that current_user.department == 'Operations'
    if current_user.department.lower() != 'operations':
        return "Unauthorized", 403
    return render_template('dashboard.html', user=current_user)
