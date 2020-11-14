from flask import Flask, render_template, request, json

app = Flask(__name__)

street = {}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == "POST":
        street_name = request.form["element_1"]
        named_after = request.form["element_3"]
        description = request.form["element_2"]
        category = request.form["element_4"]

        for i in ["street_name", "named_after", "description", "category"]:
            street[i] = eval(i)
        print(street)
        with open('mydata.json', 'w') as f:
            json.dump(street, f)
        return render_template("ulica.html", ulica=street)
    else:
        return render_template("form.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)