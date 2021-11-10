from flask import Flask, render_template, request

# Flask constructor
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/data', methods=["GET", "POST"])
def data():
    form_data = request.form
    return render_template("data.html", form_data=form_data)


if __name__ == '__main__':
    app.run()
