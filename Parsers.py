from html.parser import HTMLParser

"""
Parse player game log pages:
https://www.basketball-reference.com/players/b/bryanko01/gamelog/1997
Goal:
Get links to boxscores for games when player played (active_game_boxscores)

Note:
The page has two tables - one for regular season, one for playoffs.
The playoff table is commented out in the HTML, so the parser doesn't get to it.
Should parse this page for playoff games:
https://www.basketball-reference.com/players/b/bryanko01/gamelog-playoffs/
"""
class SeasonGamelogParser(HTMLParser):
    in_gamelink_cell = False
    box_score_link = None
    did_not_play = False
    active_game_boxscores = []

    def handle_starttag(self, tag, attrs):
        if tag == "td" and len(attrs) > 1 and attrs[1][1] == "date_game":
            self.in_gamelink_cell = True

        if self.in_gamelink_cell and tag == "a":
            self.box_score_link = attrs[0][1]

        if tag == "td" and len(attrs) > 1 and attrs[1][1] == "reason":
            self.did_not_play = True

    def handle_endtag(self, tag):
        if tag == "td" and self.in_gamelink_cell:
            self.in_gamelink_cell = False

        if tag == "tr":
            if self.did_not_play == False and self.box_score_link is not None:
                self.active_game_boxscores.append(self.box_score_link)
            self.did_not_play = False
            self.box_score_link = None

    def handle_data(self, data):
        pass


"""
Parse Play-By-Play pages
https://www.basketball-reference.com/boxscores/pbp/199611200LAL.html
Goal:
Get a score timeline - list of tuples with (time, score)
Get a player timeline - list of tuples with (time, INFO)
    INFO - either SUB-IN, SUB-OUT or PRESENT
Timelines are partioned by quarters/periods
"""
class PbpParser(HTMLParser):
    def __init__(self, PLAYER_NAME=None, AT_HOME=None):
        super().__init__()

        self.td_count = 0
        self.score_timeline = []
        self.player_timeline = []
        self.row_data = []
        self.cell_data = []
        self.current_score = "0-0"
        self.q_index = -1

        self.PLAYER_NAME = PLAYER_NAME #K.Bryant
        #If player is playing at home, their action data will be in cell #5, otherwise it will be cell #1 (0-indexed)
        self.PLAYER_ACTION_CELL = 5 if AT_HOME else 1


    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.td_count += 1

    """
    Note: Function updates q_index
    """
    def parse_score_timeline(self):
        if len(self.row_data) == 2:
            if self.row_data[1][1] == "Start of 1st quarter":
                #weird, but start of 1st quarter row has ['12:00.0'] instead of ['\n', '12:00.0' 
                self.row_data[0].append(self.row_data[0][0])

            if self.row_data[1][1].startswith("Start of"):
                self.score_timeline.append([])
                self.player_timeline.append([])
                self.q_index += 1
        if len(self.row_data) >= 3:
            self.current_score = self.row_data[3][0]
        self.score_timeline[self.q_index].append((self.row_data[0][1], self.current_score))

    """
    The "grammar" for this timeline is:
    (PRESENT) (SUB-OUT) (SUB-IN)
    SUB-OUT can only follow PRESENT or SUB-IN
    SUB-IN can not immediately follow PRESENT
    PRESENT can only appear once, and must be the first record in a period's timeline
    """
    def parse_player_timeline(self):
        SUBST_LINE = " enters the game for "
        cell_data = self.row_data[self.PLAYER_ACTION_CELL]
        time = self.row_data[0][1]
        if self.PLAYER_NAME in cell_data:
            #substitution
            if SUBST_LINE in cell_data:
                if cell_data[0] == self.PLAYER_NAME:
                    self.player_timeline[self.q_index].append((time, "SUB-IN"))
                else:
                    self.player_timeline[self.q_index].append((time,"SUB-OUT"))
            #player action without sub-in or sub-out (player started the quarter)
            elif len(self.player_timeline[self.q_index]) == 0:
                self.player_timeline[self.q_index].append((time, "PRESENT"))

    def handle_endtag(self, tag):
        if tag == "td":
            self.row_data.append([x for x in self.cell_data])
            self.cell_data = []
        if tag == "tr":
            self.td_count = 0
            if len(self.row_data) >= 2:
                self.parse_score_timeline()
            if self.PLAYER_NAME is not None and len(self.row_data) >= 3:
                self.parse_player_timeline()
            self.row_data = []

    def handle_data(self, data):
        if self.td_count > 0:
            self.cell_data.append(data)

"""
Parse box score pages
https://www.basketball-reference.com/boxscores/199611030LAL.html

Goal:
Get minutes played for PLAYER_NAME
"""
class BoxScoreParser(HTMLParser):
    def __init__(self, PLAYER_NAME=None):
        super().__init__()
        self.PLAYER_NAME = PLAYER_NAME
        self.player_mp = None
        self.in_player_row = False
        self.in_mp_cell = False
        self.found = False

    def handle_starttag(self, tag, attrs):
        if self.found:
            return
        if tag == "td" and len(attrs) > 1 and attrs[1][1] == "mp" and self.in_player_row:
            self.in_mp_cell = True

    def handle_endtag(self, tag):
        if self.found:
            return
        if tag == "td":
            self.in_mp_cell = False

    def handle_data(self, data):
        if self.found:
            return
        if data == self.PLAYER_NAME:
            self.in_player_row = True
        if self.in_mp_cell:
            self.player_mp = data
            self.found = True




