from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
import gettext
from typing import Callable, MutableMapping, Any, Awaitable

from starlette.types import ASGIApp


class I18nMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_locale = 'en') -> None:
        super().__init__(app)
        self.default_locale = default_locale

    async def dispatch(self, request: Request, call_next):
        lang = request.query_params.get('lang') or request.headers.get('Accept-Language', 'en')[:2]
        if lang not in ['en','de']:
            lang = self.default_locale
        request.state.locale = lang
        request.state.gettext = gettext.translation(
            'messages', localedir='translations', languages=[lang], fallback=True
        ).gettext
        return await call_next(request)