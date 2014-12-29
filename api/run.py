'''Creates the application using config settings.'''

from app import create_app

application = create_app('app.settings.Config')
