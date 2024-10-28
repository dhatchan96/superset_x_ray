from werkzeug.wrappers import Response

class XFrameOptionsMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # Remove any existing X-Frame-Options header
            headers = [(key, value) for key, value in headers if key.lower() != 'x-frame-options']
            # Add 'ALLOWALL' to allow iframe embedding
            headers.append(('X-Frame-Options', 'ALLOWALL'))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
