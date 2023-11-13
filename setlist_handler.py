import requests
import logging
import sys
import os

# Test purpouse only
band = 'Radiohead'
place = 'Passeio Marítimo de Algés'
year = '2016'

def main():
    url = generate_setlist_url(band, transform_to_url(place), year)
    response = get_setlist_response(url)
    setlist = unwrap_response(response)
    show_song_list(setlist)

# Generates output if you need to use a string vith commas and spaces on the url
def transform_to_url(str):
    return str.replace(',', '%2C').replace(' ', '+')

# Generate request url
def generate_setlist_url(band, place, year):
    return f"{os.environ.get['SETLIST_BASE_URL']}/search/setlists?artistName={band}&venueName={place}&year={year}"

# Realizamos la request
def get_setlist_response(url):
    logging.info("Connecting to Setlist...")
    session = requests.Session()
    session.headers.update({'x-api-key': os.environ.get['SETLIST_API_KEY'], 'Accept': 'application/json'})
    return session.get(url)

# Take the response and get your setlist
def unwrap_response(response):
    # Verifies response
    if response.status_code == 200:
        data = response.json()
        # Access to set data
        dataset = data['setlist'][0]['sets']['set']

        # Iterates dataset and append each song name
        my_setlist = []
        for data in dataset:
            for song in data['song']:
                my_setlist.append(song['name'])
        return my_setlist
    else:
        logging.error(f'Error consulting Setlist API: {response.status_code}')

# Show on terminal setlist, if there is not setlist we exit
def show_song_list(setlist):
    if not setlist:
        logging.info(f"Empty Setlist")
        sys.exit(f"EXIT!!")

    logging.info("my_setlist:")
    for song in setlist:
        logging.info(f"Track - {song}")

if __name__ == "__main__":
    main()
