import logging
# import requests

# from os import environ
import azure.functions as func
from FlaskApp import app
from AdminFlaskApp import app as admin_app
# from AdminFlaskApp.jobs import job_run_async_reports

logging.basicConfig(level=logging.INFO)


func_app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@func_app.route(route="{*route}")
def website_function(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)


@func_app.route(route="adm/{*route}")
def admin_function(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    def spoof_path_middleware(environ, start_response):
        environ["SCRIPT_NAME"] = "/admin"

        path = environ.get("PATH_INFO", "")

        if path.startswith("/adm"):
            environ["PATH_INFO"] = path[4:] if len(path) > 4 else "/"

        return admin_app.wsgi_app(environ, start_response)

    return func.WsgiMiddleware(spoof_path_middleware).handle(req, context)


# @func_app.function_name(name="TimerJob5Min")
# @func_app.timer_trigger(
#     schedule="0 */5 * * * *",
#     arg_name="timer5min",
#     run_on_startup=False,
#     use_monitor=True,
# )
# def timer_job_5min(timer5min: func.TimerRequest) -> None:
#     logging.info("Timer job (5 min) triggered")

#     try:
#         # job_run_async_reports()
#         logging.info("run")

#     except Exception:
#         logging.exception("Error to send request on job")

#     if timer5min.past_due:
#         logging.warning("Timer job (5 min) is past due!")


# @func_app.function_name(name="TimerJob15Min")
# @func_app.timer_trigger(
#     schedule="0 */15 * * * *",
#     arg_name="timer15min",
#     run_on_startup=False,
#     use_monitor=True,
# )
# def timer_job_15min(timer15min: func.TimerRequest) -> None:
#     logging.info("Timer job (15 min) triggered")
#     if timer15min.past_due:
#         logging.warning("Timer job (15 min) is past due!")
