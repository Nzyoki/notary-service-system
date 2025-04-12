from app import create_app, db
from app.models import User, Document

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Allows for database interactions in Flask shell"""
    return {'db': db, 'User': User, 'Document': Document}

if __name__ == '__main__':
    app.run(debug=True)