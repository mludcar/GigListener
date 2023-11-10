import setlist_handler
import spotify_handler
import argparse
import logging

## TODO look fpr github actions

def main():
    logging.basicConfig(level=logging.INFO)
    # Command line arguments handler, 1: Group, 2: Place, 3: Year
    parser = argparse.ArgumentParser()
    parser.add_argument("band_name", type = str)
    parser.add_argument("place", type = str)
    parser.add_argument("year", type=str)
    args = parser.parse_args()
    band_name = args.band_name
    place = args.place
    year = args.year
    logging.info(f"Band: {band_name} Place: {place} Year:{year}")

    # Retrieve songlist from setlist 
    url = setlist_handler.generate_setlist_url(band_name, setlist_handler.transform_to_url(place), year)
    response = setlist_handler.get_setlist_response(url)
    setlist =setlist_handler.unwrap_response(response)
    setlist_handler.show_song_list(setlist)
    
    # Create new reproduction list
    list_name = band_name + " - " + place + " - " + year
    sp = spotify_handler.get_spotify_authentication()
    spotify_empty_list = spotify_handler.create_spotify_list(sp, list_name)

    # search songs in spotify from list created by setlist
    songs_uri = spotify_handler.search_list_spotify(sp, setlist)
    # add songs to reproduction list
    spotify_handler.add_songs_to_list(sp, songs_uri, spotify_empty_list)
    logging.info("SUCCESS!!!")

if __name__ == "__main__":
    main()
