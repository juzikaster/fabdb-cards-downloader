from genericpath import isdir
import json
import requests
import os

# Output dir
output_path = "output"
# Main api
api_url = "https://api.fabdb.net/"
# Image database
image_url = "https://fabdb2.imgix.net/cards/printings/"

headers =  {
    "Content-Type": "application/json",
    "Authorization": "Bearer {api_key}".format(api_key = os.getenv("FABDB_API_KEY"))
}

def download_image(id: str):
    # Check if output folder exist. If not create it
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    filename = "{id}.png".format(id = id)    # CF for Cold Foil
    url = "{url}{name}".format(url = image_url, name = filename)
    r = requests.get(url)
    path = os.path.join(output_path, filename)
    # Write image to file
    open(path, "wb").write(r.content)

def get_next_id(page: int):
    print("Page: {page}".format(page = page))
    url = "{main}cards".format(main = api_url)
    json_r = { "page": page, "per_page": 1}
    r = requests.get(url, data=json.dumps(json_r), headers=headers)

    if page > r.json()["meta"]["last_page"]:
        return

    printings = r.json()["data"][0]["printings"]
    for image in printings:
        sku = image["sku"]["sku"]
        download_image(sku)
    get_next_id(page + 1)

if __name__ == "__main__":
    get_next_id(1)
