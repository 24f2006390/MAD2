import os

from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "instance", "app.db")

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

