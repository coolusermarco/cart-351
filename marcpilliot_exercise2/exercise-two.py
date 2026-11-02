from flask import Flask, render_template, request
import requests

app = Flask(__name__)
NASA_SEARCH_URL = "https://images-api.nasa.gov/search"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/t1")
def t1():
    return render_template("t1.html", have_results=False)


@app.route("/getSearchCriteria")
def getSearchCriteria():
    search_criteria = request.args.get("search", "").strip()
    if not search_criteria:
        return render_template("t1.html", have_results=False)

    response = requests.get(
        NASA_SEARCH_URL,
        params={"q": search_criteria, "media_type": "image"},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    items = data["collection"]["items"]
    if not items:
        return render_template("t1.html", have_results=False)

    first_item = items[0]
    imgFromNasa = first_item["links"][0]["href"]
    description = first_item["data"][0]["description"]
    imgFromNasa = imgFromNasa.replace(" ", "%20")
    return render_template(
        "t1.html",
        have_results=True,
        description=description,
        imgPath=imgFromNasa,
        search_criteria=search_criteria,
    )


@app.route("/t2")
def t2():
    return render_template("t2.html")


@app.route("/getSearchCriteria_adv")
def getSearchCriteria_adv():
    search_criteria = request.args.get("search", "").strip()
    encodedImageLinks = []
    if search_criteria:
        response = requests.get(
            NASA_SEARCH_URL,
            params={"q": search_criteria, "media_type": "image"},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        items = data["collection"]["items"]
        for item in items:
            if item.get("links"):
                singleImage = item["links"][0]["href"]
                encodedImageLinks.append(singleImage.replace(" ", "%20"))
    return render_template("t2.html", images=encodedImageLinks, search_criteria=search_criteria)


if __name__ == "__main__":
    app.run(debug=True)
