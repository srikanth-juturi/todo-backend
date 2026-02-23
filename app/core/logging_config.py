import logging

from pythonjsonlogger import jsonlogger

from app.core.request_context import get_trace_id


class TraceIdJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("trace_id", get_trace_id())


def configure_logging() -> None:
    formatter = TraceIdJsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(route)s %(method)s %(status_code)s %(latency_ms)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]
