from bottle import request, response

from deed import AuditLog, AuditMode
from deed.tracing import LOCAL_THREAD, audit_span


class AuditBuilder:

    def __init__(self, context, session):
        self.context = context
        self.session = session
        self.resource = None
        self.payload = None

    def build(self):
        log = AuditLog(**self.context)
        log.session(**self.session)
        return log


def audit(resource_type: str, action: str, audit_mode: AuditMode = None, channel: str = None,
          status_range=range(200, 300)):
    def decorator(callback):
        @audit_span
        def decorated_func(*args, **kwargs):
            LOCAL_THREAD.context.update(dict(resource_type=resource_type, action=action, audit_mode=audit_mode))
            LOCAL_THREAD.session.update(dict(where=request.remote_addr, channel=channel))
            request.audit = AuditBuilder(LOCAL_THREAD.context, LOCAL_THREAD.session)
            result = callback(*args, **kwargs)
            if response.status_code in status_range and request.audit.resource:
                payload = request.audit.payload or {}
                log = request.audit.build()
                log.audit(request.audit.resource, payload=payload)
            return result
        return decorated_func
    return decorator
