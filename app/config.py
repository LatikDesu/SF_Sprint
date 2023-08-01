import os

from dotenv import load_dotenv

load_dotenv(".env")

HOST_DB = os.environ.get("FSTR_DB_HOST")
PORT_DB = os.environ.get("FSTR_DB_PORT")
NAME_DB = os.environ.get("FSTR_DB_NAME")
USER_DB = os.environ.get("FSTR_DB_LOGIN")
PASSWORD_DB = os.environ.get("FSTR_DB_PASS")
