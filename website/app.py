# function_app.py

# import azure.functions as func
from flask import Flask, Response, current_app
from website.secrets_plugin import init_secret_manager

app = Flask(__name__)

app.config["SECRET_NAME"] = "testeeduardo"
app.config["SECRET_PROVIDER"] = "azure"

init_secret_manager(app)


@app.get("/return_http")
def return_http():
    return Response(
        f"<h1>Hello World™: {current_app.config['teste']}</h1>", mimetype="text/html"
    )


# app = func.WsgiFunctionApp(
#     app=flask_app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS
# )


if __name__ == "__main__":
    app.run(debug=True)
