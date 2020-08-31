# Runner exposed to user for starting VitaBoard server

# Import backend API
from .app import app

# Run the API
def run_board():
    app.run()
