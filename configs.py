import os


class Settings:
    SECRETS = {
        "SSL_CERTS_CERT": os.environ.get("SSL_CERTS_CERT", None),
        "SSL_CERTS_PATH": os.environ.get("SSL_CERTS_PATH", None),
        "MLB_DATABASE_USERNAME": os.environ.get("MLB_DATABASE_USERNAME", None),
        "MLB_DATABASE_PASSWORD": os.environ.get("MLB_DATABASE_PASSWORD", None),
        "MLB_DATABASE_HOST": os.environ.get("MLB_DATABASE_HOST", None),
        "MLB_DATABASE_DB": os.environ.get("MLB_DATABASE_DB", None),
        "NCAAMB_DATABASE_USERNAME": os.environ.get("NCAAMB_DATABASE_USERNAME", None),
        "NCAAMB_DATABASE_PASSWORD": os.environ.get("NCAAMB_DATABASE_PASSWORD", None),
        "NCAAMB_DATABASE_HOST": os.environ.get("NCAAMB_DATABASE_HOST", None),
        "NCAAMB_DATABASE_DB": os.environ.get("NCAAMB_DATABASE_DB", None),
        "NFL_DATABASE_USERNAME": os.environ.get("NFL_DATABASE_USERNAME", None),
        "NFL_DATABASE_PASSWORD": os.environ.get("NFL_DATABASE_PASSWORD", None),
        "NFL_DATABASE_HOST": os.environ.get("NFL_DATABASE_HOST", None),
        "NFL_DATABASE_DB": os.environ.get("NFL_DATABASE_DB", None),
        "SPORT_DATABASE_USERNAME": os.environ.get("SPORT_DATABASE_USERNAME", None),
        "SPORT_DATABASE_PASSWORD": os.environ.get("SPORT_DATABASE_PASSWORD", None),
        "SPORT_DATABASE_HOST": os.environ.get("SPORT_DATABASE_HOST", None),
        "SPORT_DATABASE_DB": os.environ.get("SPORT_DATABASE_DB", None)
    }

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

