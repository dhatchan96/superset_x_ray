import logging
import os
from typing import Optional  # <-- Add this line

from flask import Flask
from superset.initialization import SupersetAppInitializer
from superset.middleware import XFrameOptionsMiddleware  # Import the custom middleware

logger = logging.getLogger(__name__)

def create_app(superset_config_module: Optional[str] = None) -> Flask:
    app = SupersetApp(__name__)

    try:
        # Allow user to override our config completely
        config_module = superset_config_module or os.environ.get(
            "SUPERSET_CONFIG", "superset.config"
        )
        app.config.from_object(config_module)

        app_initializer = app.config.get("APP_INITIALIZER", SupersetAppInitializer)(app)
        app_initializer.init_app()

        # Apply the custom X-Frame-Options middleware
        app.wsgi_app = XFrameOptionsMiddleware(app.wsgi_app)

        return app

    except Exception:
        logger.exception("Failed to create app")
        raise


class SupersetApp(Flask):
    pass
