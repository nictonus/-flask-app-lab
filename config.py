SECRET_KEY = "secret-key-sdsfs"

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db' # погано працює в папці instance

#import os
#basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')