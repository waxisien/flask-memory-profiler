import os

import psutil
from flask import current_app, _app_ctx_stack


class MemoryProfiler(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def _get_used_memory(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss

    def _format_value(self, value):
        return round(value/(1024**2), 2)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['flask-memory-profiler'] = self
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown)

    def before_request(self):
        ctx = _app_ctx_stack.top
        ctx.flask_memory_profiler_initial = self._get_used_memory()

    def after_request(self, response):
        ctx = _app_ctx_stack.top
        initial = ctx.flask_memory_profiler_initial
        current = self._get_used_memory()
        variance = round((current-initial)/initial*100, 2)
        variance_sign = '+' if variance >= 0 else ''

        current_app.logger.debug(
            f'Memory Usage: {self._format_value(initial)} MB -> {self._format_value(current)} MB '
            f'({variance_sign}{variance}%)'
        )

        return response
    
    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'flask_memory_profiler_initial'):
            ctx.flask_memory_profiler_initial = None
