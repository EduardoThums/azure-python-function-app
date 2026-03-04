import logging


__current_app = None


def init(app):
    global __current_app
    __current_app = app


def job_run_async_reports():
    with __current_app.app_context():
        logging.info("run job_run_async_reports")
