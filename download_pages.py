import requests
import sys
from Parsers import SeasonGamelogParser

BBREF_URL = "https://www.basketball-reference.com"

if len(sys.argv) < 2:
    print("Give gamelog page")
    exit(0)

season_gamelog_html = None
with open(sys.argv[1]) as f:
    season_gamelog_html = f.read()

parser = SeasonGamelogParser()
parser.feed(season_gamelog_html)
boxscore_urls = parser.active_game_boxscores

def download_page(dest_path, url):
    r = requests.get(BBREF_URL+url)
    with open(dest_path, "w+") as f:
        f.write(r.text)

for boxscore_url in boxscore_urls:
    page_name = boxscore_url[boxscore_url.rfind("/")+1:]

    dest_path = "dataset/96-97/boxscore_pages/" + page_name
    download_page(dest_path, boxscore_url)

    pbp_url = boxscore_url[:11] + "pbp/" + boxscore_url[11:]
    dest_path = "dataset/96-97/pbp_pages/" + page_name
    download_page(dest_path, pbp_url)




