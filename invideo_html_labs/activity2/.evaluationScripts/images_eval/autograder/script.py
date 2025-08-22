import json

from bs4 import BeautifulSoup

# Define the grading structure
marks = {
    "Images": {
        "Starry Night Image": 0,
        "Mona Lisa Image": 0,
        "Blue Marble Image": 0,
        "Mona Lisa Figcaption": 0,
    }
}

feedback = {
    "Images": {
        "Starry Night Image": "",
        "Mona Lisa Image": "",
        "Blue Marble Image": "",
        "Mona Lisa Figcaption": "",
    }
}

# Load and parse the student's HTML file
with open("/home/labDirectory/images_activity/index.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Check for Starry Night image
starry_night = soup.find("img", {"src": "starry-night.jpg"})
if (
    starry_night
    and starry_night.get("alt") == "Starry Night"
    and starry_night.get("align") == "right"
):
    marks["Images"]["Starry Night Image"] = 1
    feedback["Images"]["Starry Night Image"] = (
        "Correct Starry Night image with alignment."
    )
else:
    feedback["Images"]["Starry Night Image"] = (
        "Starry Night image is incorrect or missing alignment."
    )

# Check for Mona Lisa image inside figure with figcaption
mona_lisa_figure = soup.find("figure")
mona_lisa_img = (
    mona_lisa_figure.find("img", {"src": "mona-lisa.jpg"}) if mona_lisa_figure else None
)
mona_lisa_caption = mona_lisa_figure.find("figcaption") if mona_lisa_figure else None

if mona_lisa_img and mona_lisa_img.get("alt") == "Mona Lisa":
    marks["Images"]["Mona Lisa Image"] = 1
    feedback["Images"]["Mona Lisa Image"] = "Correct Mona Lisa image."
else:
    feedback["Images"]["Mona Lisa Image"] = "Mona Lisa image is incorrect or missing."

if mona_lisa_caption and mona_lisa_caption.text == "Mona Lisa":
    marks["Images"]["Mona Lisa Figcaption"] = 1
    feedback["Images"]["Mona Lisa Figcaption"] = "Correct figcaption for Mona Lisa."
else:
    feedback["Images"]["Mona Lisa Figcaption"] = (
        "Mona Lisa figcaption is incorrect or missing."
    )

# Check for Blue Marble image
blue_marble = soup.find("img", {"src": "the-blue-marble.jpg"})
if blue_marble and blue_marble.get("alt") == "The Blue Marble":
    marks["Images"]["Blue Marble Image"] = 1
    feedback["Images"]["Blue Marble Image"] = "Correct Blue Marble image."
else:
    feedback["Images"]["Blue Marble Image"] = (
        "Blue Marble image is incorrect or missing."
    )

# Compile the results
overall = {"data": []}
for category, val in marks["Images"].items():
    status = "success" if val == 1 else "fail"
    overall["data"].append(
        {
            "testid": "Images/" + category,
            "status": status,
            "score": val,
            "maximum marks": 1,
            "message": feedback["Images"][category],
        }
    )

# Save results to JSON file
with open("/home/.evaluationScripts/evaluate.json", "w") as f:
    json.dump(overall, f, indent=4)
