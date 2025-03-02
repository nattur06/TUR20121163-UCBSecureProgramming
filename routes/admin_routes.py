from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, Task

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    # No role-based access control (intentionally insecure)
    # Any user can access admin dashboard if they know the URL

    users = User.query.all()
    tasks = Task.query.all()

    return render_template('admin_dashboard.html', users=users, tasks=tasks)


@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # No role-based access control (intentionally insecure)
    # No CSRF protection (intentionally insecure)

    user = User.query.get_or_404(user_id)

    # Prevent deleting current user
    if user.id == session.get('user_id'):
        flash('Cannot delete yourself!')
        return redirect(url_for('admin_bp.admin_dashboard'))

    # Delete user's tasks first
    Task.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.username} deleted successfully!')
    return redirect(url_for('admin_bp.admin_dashboard'))


@admin_bp.route('/admin/assign_task', methods=['POST'])
def assign_task():
    # No role-based access control (intentionally insecure)
    # No CSRF protection (intentionally insecure)

    task_id = request.form['task_id']
    user_id = request.form['user_id']

    task = Task.query.get_or_404(task_id)
    task.user_id = user_id

    db.session.commit()

    flash('Task assigned successfully!')
    return redirect(url_for('admin_bp.admin_dashboard'))


@admin_bp.route('/admin/execute_query', methods=['POST'])
def execute_query():
    # Extremely vulnerable function that allows direct SQL execution
    # Intentionally insecure for educational purposes

    query = request.form['query']
    result = None

    try:
        # Direct execution of SQL (NEVER do this in a real application)
        result = db.engine.execute(query)
        rows = [row for row in result]
        flash('Query executed successfully!')
        return render_template('admin_dashboard.html', query_result=rows, query=query)
    except Exception as e:
        flash(f'Error executing query: {str(e)}')
        return redirect(url_for('admin_bp.admin_dashboard'))