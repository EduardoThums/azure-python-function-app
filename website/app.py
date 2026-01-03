# function_app.py

# import azure.functions as func
from flask import Flask, Response

app = Flask(__name__)


@app.get("/return_http")
def return_http():
    return Response("<h1>Hello World™</h1>", mimetype="text/html")


# app = func.WsgiFunctionApp(
#     app=flask_app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS
# )


if __name__ == "__main__":
    app.run(debug=True)
