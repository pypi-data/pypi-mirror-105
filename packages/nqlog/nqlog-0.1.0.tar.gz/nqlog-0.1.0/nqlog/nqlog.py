import datetime
import logging as python_logging
import os
import uuid
import threading
import traceback

from google.cloud import logging as gcp_logging

SEVERITY = {
    "NOTSET": python_logging.NOTSET,
    "DEBUG": python_logging.DEBUG,
    "INFO": python_logging.INFO,
    "WARN": python_logging.WARN, # Do not swap this line with the next as google does not like WARN.
    "WARNING": python_logging.WARNING,
    "ERROR": python_logging.ERROR,
    "CRITICAL": python_logging.CRITICAL
}

LEVELS = {n: s for s, n in SEVERITY.items()}

class Entry():
    """A log entry, associated with an individual request."""

    def __init__(self, gcp_logger, max_duration=None, level=python_logging.INFO,
                 log_name='request_log', resource=None):
        """
        Creates a log entry.
        :param gcp_logger: Logger to be used for output.  If None, we just print.
        :param max_duration: Maximum duration, in seconds, after which the entry is
            flushed and a new entry is created.
        :param level: Minimum logging level.
        :param log_name: log to use for logging.
        :param resource: resource to use for logging.
        """
        self.gcp_logger = gcp_logger
        self.max_level = None
        self.id = uuid.uuid1() # In case we flush it.
        self.messages = []
        self.max_duration = max_duration
        self.level = LEVELS.get(level, python_logging.INFO) if isinstance(level, str) else level
        self.logname = "projects/{project_id}/logs/{logname}".format(
            project_id=os.getenv('GOOGLE_CLOUD_PROJECT', default="default"),
            logname=log_name)
        self.resource = resource
        self.stage = "Initial" # or Partial or Final.
        self.write("{kind} log for {id}".format(kind="Initial", id=self.id), level=level)

    def write(self, text, level="INFO"):
        """Writes an individual log line to our aggregated log."""
        this_level = SEVERITY[level]
        now = datetime.datetime.utcnow()
        if (self.max_duration is not None and self.start_time is not None and
                now - self.start_time >= datetime.timedelta(seconds=self.max_duration)):
            # If this is over max duration, spits out the log.
            self.flush()
        if this_level >= self.level:
            self.max_level = this_level if self.max_level is None else max(self.max_level, this_level)
            self.messages.append(dict(level=level, text=text, timestamp=now))
        # If we are local, no point in waiting to print.
        if self.gcp_logger is None:
            self.flush()

    def flush(self, final=False):
        """Flushes existing entries."""
        if final:
            self.stage = "Final"
        self.output()
        self.stage = "Partial"
        self.messages = []
        self.max_level = None

    @property
    def start_time(self):
        return None if len(self.messages) == 0 else self.messages[0]['timestamp']

    def output(self):
        """Writes itself to the log."""
        # Adjusts the max level; default is INFO.
        if self.max_level is None:
            self.max_level = SEVERITY["INFO"]
        # Adds a message about this being a partial or final output.
        now = datetime.datetime.utcnow()
        text = "{kind} log for {id}".format(kind=self.stage, id=self.id)
        self.messages.append(dict(level=LEVELS[self.level], text=text, timestamp=now))
        # Sends the block of lines to the Google logger.
        all_text = "\n" + "\n".join("{date} - {level}: {msg}".format(
            date = m['timestamp'].isoformat(),
            level=m['level'],
            msg=m['text']) for m in self.messages)
        kwargs = {} if self.resource is None else {"resource": self.resource}
        if self.gcp_logger is not None:
            self.gcp_logger.log_text(all_text, severity=LEVELS[self.max_level],
                                     **kwargs)
        else:
            print("---", LEVELS[self.max_level], "---", all_text)

class LogContext(threading.local):

    def __init__(self, level="DEBUG"):
        self.entry = None
        self.client = None
        self.min_level = SEVERITY[level]

    def write(self, *text, level="INFO"):
        # If we don't have an entry, we cannot log.
        if self.entry is None:
            return
        if SEVERITY[level] >= self.min_level:
            # Produces a single string. We do this only if above level as it can
            # be expensive.
            s = text[0] if len(text) == 0 else text[0] % tuple(text[1:])
            self.entry.write(s, level=level)

    def flush(self, final=False):
        self.entry.flush(final=final)

    def reinit(self, local=False, log_name="request_log", **kwargs):
        """
        (Re)initializes the logger.
        :param local: If true, we are just printing locally.
        :param log_name: Name of the log to use.
        :param kwargs: Arguments to be passed to entry creation.
        :return: Nothing.
        """
        gcp_logger = None
        if not local:
            if self.client is None:
                self.client = gcp_logging.Client()
            gcp_logger = self.client.logger(log_name)
        if self.entry is not None and len(self.entry.messages) > 0:
            self.entry.flush(final=True)
        self.entry = Entry(gcp_logger, **kwargs)


log_context = LogContext()


def logthis(local=False, log_name="request_log", resource=None,
            max_duration=None, level="DEBUG"):
    """
    Decorator to cause a function to be logged.
    :param local: if True, the logging is just local.  In that case,
        you do not need to specify a resource, nor a log_name.
        This is used for local testing of the code.
    :param log_name: Name of the log to be used for logging.
    :param resource: resource to be used for logging.  You can create a
        resource e.g. via:
        from google.cloud.logging.resource import Resource
        resource = Resource( type='gae_app',
                    labels={
                        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT")
                        "module_id": os.getenv("GAE_MODULE")
                        "service_id": os.getenv("GAE_SERVICE")
                        "version_id": os.getenv("GAE_VERSION")
                       })
    :param max_duration: Max duration of a log entry in seconds.
        If the request takes longer than this, the log entry is broken into
        multiple log entries, each of at most max_duration length.
    :param level: Minimum level at which logging occurs.
    """
    def wrap(f):
        def wrapped(*args, **kwargs):
            log_context.reinit(local=local, log_name=log_name, resource=resource,
                               max_duration=max_duration, level=level)
            try:
                r = f(*args, **kwargs)
                log_context.flush(final=True)
                return r
            except:
                log_context.write(traceback.format_exc(), level="ERROR")
                log_context.flush(final=True)
                traceback.print_exc() # For normal log
                raise
        return wrapped
    return wrap


class Logging:

    def __init__(self):
        pass

    def log(self, *text, severity="INFO"):
        log_context.write(*text, level=severity)

    def debug(self, *text):
        self.log(*text, severity="DEBUG")

    def info(self, *text):
        self.log(*text, severity="INFO")

    def warning(self, *text):
        self.log(*text, severity="WARNING")

    def warn(self, *text):
        self.log(*text, severity="WARN")

    def error(self, *text):
        self.log(*text, severity="ERROR")

    def critical(self, *text):
        self.log(*text, severity="CRITICAL")

logging = Logging()
logger = logging