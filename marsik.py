import os
import requests
from PIL import Image
from io import BytesIO
import argparse
from datetime import datetime, timedelta

api_key = "uUdCFCXJQQfM9N64JSCguOlltlejtKhzMkrbe0Pd"

def find_pic(earth_date, camera, key, attempts):
    link = []
    response = requests.get(f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={earth_date}&api_key={key}&camera={camera}')
    if response.status_code == 200:
        photos = response.json().get('photos', [])
        if photos:
            urls = [photo['img_src'] for photo in photos]
            for url in urls:
                print(f'here is a photo {url}')
                link.append(url)
        elif attempts > 0:
            print('No photos found for this date.')
            new_date = earth_date + timedelta(days=3) if attempts == 2 else earth_date - timedelta(days=3)
            link.extend(find_pic(new_date, camera, key, attempts - 1))
        else:
            print('gg')

    return link

def show_and_save(link):
    directory = 'photofrommars'

    if not os.path.exists(directory):
        os.makedirs(directory)

    pic = input('Save these photos? [y] or [n]: ')
    if pic == 'y':
        for i, url in enumerate(link):
            image = requests.get(url)
            if image.status_code == 200:
                img = Image.open(BytesIO(image.content))
                img.show()
                filename = os.path.join(directory, f"img_{i + 1}.jpg")
                img.save(filename)
                print('saved')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get photos from Mars')
    parser.add_argument('--earth-date', type=str, required=True, help='Earth date (YYYYMMDD)')
    parser.add_argument('--camera', type=str, required=True, help='Camera name')
    args = parser.parse_args()

    key = api_key
    camera = args.camera
    earth_date = datetime.strptime(args.earth_date, '%Y%m%d').strftime('%Y-%m-%d')
    attempts = 2

    links = find_pic(earth_date, camera, key, attempts)
    if links:
        show_and_save(links)
    else:
        print("No photos were found.")
