import requests
from enum import Enum
import operator
import random
import html
from utils import json_request
from urllib.parse import urlencode
import json

"""
Example of a question:
"category":"Entertainment: Japanese Anime & Manga",
"type":"multiple",
"difficulty":"medium",
"question":"In "Toriko", which of the following foods is knowingly compatible with Toriko?",
"correct_answer":"Poison Potato",
"incorrect_answers":[
  "Mors Oil",
  "Alpacookie",
  "Parmesansho Fruit"
]
"""

class GameState(Enum):
    stop = 0
    participants = 1
    started = 2

def request_questions(num_questions, difficulty = None, category = None):
    q = {'amount':num_questions}
    if category:
        q['category'] = category
    if difficulty:
        q['difficulty'] = difficulty
    url = "https://opentdb.com/api.php?"+urlencode(q)
    data = json_request(url)
    if not data:
        return None
    if data["response_code"] == 0:
        return data["results"]

def get_categories():
    url = "https://opentdb.com/api_category.php"
    data = json_request(url)
    if not data:
        return None
    response = ""
    for category in data["trivia_categories"]:
        response += "{}: {}; ".format(category["id"], category["name"])
    return response

def get_help():
    return '!game [easy/medium/hard] [id_category] to start game.\n'\
            '"!game categories" to show possible categories. \n'\
            '"!game leaderboard" to show leaderboard. \n'\
            '"!game stop" to stop game.'

class Game:
    def __init__(self):
        self.gamestate = GameState.stop
        self.num_rounds = 3

    def start_game(self, query):
        params = query.split()

        if len(params) > 1:
            self.difficulty = params[0]
            self.category = params[1]
        elif len(params) > 0:
            if params[0] in ['easy', 'medium', 'hard']:
                self.difficulty = params[0]
                self.category = None
            else:
                self.difficulty = None
                self.category = params[0]
        else:
            self.category = None
            self.difficulty = None
        
        self.current_player = 0
        self.round = 0

    def set_participants(self, query):
        self.players = query.split()
        self.players_points = dict()
        for player in self.players:
            self.players_points[player] = 0

    def set_questions(self):
        self.questions = request_questions(len(self.players) * self.num_rounds, self.difficulty, self.category)
        if self.questions:
            return "Game started! \n"

    def ask_question(self):
        player_name = self.players[self.current_player]
        question = self.questions.pop()

        if not self.category:
            category = question["category"]
            response = "{}, This is a question about \x0303{}\x03 \n".format(player_name, category)
        else:
            response = "{}, it's your turn! \n".format(player_name)
        response += "> {} \n".format(html.unescape(question["question"]))
        answers = question["incorrect_answers"].copy()
        answers.append(question["correct_answer"])
        random.shuffle(answers)
        for i,answer in enumerate(answers):
            character = chr(ord('a')+i)
            unescaped_answer = html.unescape(answer)
            response += "\x02{}) {}\x02 \n".format(character.upper(), unescaped_answer)
            if answer == question["correct_answer"]:
                self.correct_answer = [character,unescaped_answer.lower()]
        return response

    def answer_question(self, query):
        player_name = self.players[self.current_player]
        if query.lower() in self.correct_answer:
            response = "\x0303Correct answer\x03, {}! ✓\n".format(player_name)
            self.players_points[player_name] += 1
        else:
            response = "\x0304Wrong answer\x03, {}... The correct answer was: \x02{}\x02 \n".format(player_name, self.correct_answer[1])

        return response
    
    def next_player(self):
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0
            self.round += 1
    
    def update_leaderboard(self):
        try:
            f = open("leaderboard.txt", "r")
            leaderboard = json.load(f)
            f.close()
        except FileNotFoundError:
            leaderboard = dict()
        
        for player,points in self.players_points.items():
            if player not in leaderboard:
                leaderboard[player] = 0
            leaderboard[player] += points

        with open("leaderboard.txt", "w") as f:
            f.write(json.dumps(leaderboard))

    def read_leaderboard(self):
        try:
            f = open("leaderboard.txt", "r")
            leaderboard = json.load(f)
            f.close()
        except FileNotFoundError:
            return "Leaderboard is empty"
        
        response = ""
        for player,points in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
            response += "{}: {} points \n".format(player, points)
        return response

    def finish_game(self):
        max_score = max(self.players_points.values())
        winners = [player for player,score in self.players_points.items() if score == max_score]
        winners = " and ".join(winners)
        response = "Game finished! And the winner is... {}! Congratulations! \n".format(winners)
        for player,points in sorted(self.players_points.items(), key=lambda x: x[1], reverse=True):
            response += "{}: {} points \n".format(player, points)
        return response

    def elaborate_query(self, sender, query):
        if query == "leaderboard":
            response = self.read_leaderboard()
        elif query == "categories":
            response = get_categories()
        elif query == "stop":
            self.gamestate = GameState.stop
            response = "Game stopped"
        elif self.gamestate == GameState.stop:
            self.start_game(query)
            response = "Type the space separated participants names (!game <names...>): "
            self.gamestate = GameState.participants
        elif self.gamestate == GameState.participants:
            self.set_participants(query)
            response = self.set_questions()
            if response:
                response += self.ask_question()
                self.gamestate = GameState.started
            else:
                response = "Error retrieving questions"
                self.gamestate = GameState.stop
        elif self.gamestate == GameState.started:
            if sender == self.players[self.current_player]:
                response = self.answer_question(query)
                self.next_player()
                if self.round < self.num_rounds:
                    response += self.ask_question()
                else:
                    response += self.finish_game()
                    self.update_leaderboard()
                    self.gamestate = GameState.stop
            else:
                response = "{}, it's not your turn!!".format(sender)
                
        return response