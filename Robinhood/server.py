from flask import Flask, url_for
app = Flask(__name__)

if __name__ == "__main__":
	app.run()

@app.route("/output")
def output():
	return "Hello World!"