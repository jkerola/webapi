class Config():
    '''Object that holds configuration values for the main app.'''
    # This secret key is available here for demonstration purposes
    # Another key will be used for production
    SECRET_KEY = 'ce1f924e02c9459b3fdce86e59afe2a6fea89e690752889f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coffee.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
