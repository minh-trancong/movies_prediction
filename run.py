import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from apps.config import config_dict
from apps import create_app, db
from decimal import Decimal


# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

application = create_app(app_config)

# Register the format_currency filter
@application.template_filter('format_currency')
def format_currency(value):
    if isinstance(value, (float, Decimal)):
        formatted_value = '${:,.2f}'.format(value)
    elif isinstance(value, int):
        formatted_value = '${:,.0f}'.format(value)
    else:
        formatted_value = value
    return formatted_value


Migrate(application, db)

if not DEBUG:
    Minify(app=application, html=True, js=False, cssless=False)

if DEBUG:
    application.logger.info('DEBUG            = ' + str(DEBUG))
    application.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
    application.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    application.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT)

if __name__ == "__main__":
    application.run()
