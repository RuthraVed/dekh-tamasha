from src import app_config

app = app_config.app
app.testing = True
connex_app = app_config.connex_app
connex_app.add_api('swagger.yaml', strict_validation=True)
