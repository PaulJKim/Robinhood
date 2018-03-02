from flask import Flask, render_template, request, redirect, Response
import json
from Robinhood import Robinhood

app = Flask(__name__)
rh_client = Robinhood()
logged_in = False

@app.route("/login", methods=['POST'])
def login():
    content = request.get_json(force=True)
    logged_in = rh_client.login(username="user", password="pass")
    print rh_client.get_fundamentals("MSFT")
    print logged_in
    return "Hello World"


if __name__ == "__main__":
    app.run()
