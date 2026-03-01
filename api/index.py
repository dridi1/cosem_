from api import create_app
from api.extensions import bcrypt, db
from api.models import ContactMessage, Polygon, User


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8009)
