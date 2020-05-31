from os import listdir
from time import sleep
from Parsers import PbpParser, BoxScoreParser
from ParseUtils import get_player_time_up

PBP_DATA_DIR = "./dataset/96-97/pbp_pages/"
BS_DATA_DIR = "./dataset/96-97/boxscore_pages/"

season_totals = [0, 0]
def minute_string_to_sec(minute_string):
    mins, secs = minute_string.split(":")
    return int(mins)*60 + int(secs)

for pbp_file, bs_file in zip(listdir(PBP_DATA_DIR), listdir(BS_DATA_DIR)):
    print("file: ", pbp_file)
    pbp_html = None
    with open(PBP_DATA_DIR+pbp_file) as f:
        pbp_html = f.read()

    bs_html = None
    with open(BS_DATA_DIR+bs_file) as f:
        bs_html = f.read()

    at_home = True
    if pbp_file[-8:-5] != "LAL":
        at_home = False

    parser = PbpParser("K. Bryant", at_home)
    parser.feed(pbp_html)
    player_time_up = get_player_time_up(parser.score_timeline, parser.player_timeline, at_home)

    parser = BoxScoreParser("Kobe Bryant")
    parser.feed(bs_html)
    player_mp = parser.player_mp

    print(player_mp, player_time_up)
    season_totals[0] += minute_string_to_sec(player_mp)
    season_totals[1] += player_time_up

print(season_totals)








