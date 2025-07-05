from authlib.integrations.flask_client import OAuth

from api.config import Config

oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': (
            'openid email profile '
        )
    }
)
