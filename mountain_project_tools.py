import json
import os
import requests


def mountain_project_api(latitude, longitude, distance, min_difficulty, max_difficulty, results, api_key):
    '''pull data from the mountain project api'''
    url = f"https://www.mountainproject.com/data/get-routes-for-lat-lon?lat={latitude}"\
          f"&lon={longitude}&maxDistance={distance}&minDiff={min_difficulty}"\
          f"&maxDiff={max_difficulty}&maxResults={results}&key={api_key}"

    # write file, creating directory if not present
    os.makedirs(os.path.dirname('data/'), exist_ok=True)
    f = open('data/route_info.json', 'wb')
    f.write(requests.get(url).content)
    f.close()


def route_info_by_id(route_id):
    '''try to open route data, if present return route description'''
    f = open('data/route_info.json', 'r')
    data = json.load(f)
    for route in data["routes"]:
        if route["id"] == route_id:
            if route["pitches"] == 1:
                return f'{route["name"]} - {route["rating"]}\r\n{route["type"]} - ' \
                       f'Single Pitch\r\n\r\n{route["location"][1]}, {route["location"][0]}'
            else:
                return f'{route["name"]} - {route["rating"]}\r\n{route["type"]} - ' \
                       f'{route["pitches"]} Pitches\r\n\r\n{route["location"][1]}, {route["location"][0]}'
    f.close()


def pull_image(image_name, image_url, file_extension):
    '''pull an image from url, define name and file extenstion - abc, .jpg'''
    os.makedirs(os.path.dirname('images/'), exist_ok=True)
    f = open(f'images/{image_name}{file_extension}', 'wb')
    f.write(requests.get(image_url).content)
    f.close()


def pull_all_images():
    '''pulls all images from json'''
    # open file
    if not os.path.isfile("data/route_info.json"):
        print("[ERROR] Mountain project data not found.  Try running mountain_project_api() first.")
    else:
        f = open('data/route_info.json', 'r')
        data = json.load(f)

        # download each file
        duplicate_image = 0
        print('Download initiated.')
        for route in data["routes"]:
            route_id = route["id"]
            # search for file exists
            # add try except
            if os.path.isfile(f"images/{route_id}.jpg"):
                duplicate_image += 1
            else:
                try:
                    pull_image(image_name=route_id,
                            image_url=route["imgMedium"], file_extension=".jpg")
                except Exception:
                    print(f'Failed to download image. Route ID: {route_id}')
        if duplicate_image is not 0:
            if duplicate_image is 1:
                print(
                    f'Download complete. {duplicate_image} image already present.')
            else:
                print(
                    f'Download complete. {duplicate_image} images already present.')
        else:
            print('Download complete.')
