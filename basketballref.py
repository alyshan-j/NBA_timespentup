from Parsers import PbpParser, BoxScoreParser
from ParseUtils import get_player_time_up

"""
with open("pbp19961120.txt") as f:
    text = f.read()

parser = PbpParser("K. Bryant", True)
parser.feed(text)

ttu = get_team_time_up_windows(parser.score_timeline, True)
pto = get_player_time_on_windows(parser.player_timeline)
print(ttu)
print(pto)
ans = get_player_time_up(ttu, pto)
print(ans)
"""

pbp_html = None
with open("dataset/96-97/pbp_pages/199611200LAL.html") as f:
    pbp_html = f.read()

bs_html = None
with open("dataset/96-97/boxscore_pages/199611200LAL.html") as f:
    bs_html = f.read()

parser = PbpParser("K. Bryant", True)
parser.feed(pbp_html)
player_time_up = get_player_time_up(parser.score_timeline, parser.player_timeline, True)

parser = BoxScoreParser("Kobe Bryant")
parser.feed(bs_html)
player_mp = parser.player_mp

print(player_mp, player_time_up)







