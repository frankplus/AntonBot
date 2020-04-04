import requests
from enum import Enum
import operator
import random
import html
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
    started = 1

def request_questions(num_questions):
    url = 'https://opentdb.com/api.php?amount={}&type=multiple'.format(num_questions)
    data = requests.get(url).json()
    if data["response_code"] == 0:
        return data["results"]

class Game:
    def __init__(self):
        self.gamestate = GameState.stop
        self.num_rounds = 1

    def start_game(self, query):
        self.players = query.split()
        self.current_player = 0
        self.round = 0
        self.players_points = dict()
        for player in self.players:
            self.players_points[player] = 0
        self.questions = request_questions(len(self.players) * self.num_rounds)
        return "Game started! \n"

    def ask_question(self):
        player_name = self.players[self.current_player]
        question = self.questions.pop()
        category = question["category"]
        response = "{}, This is a question about {} \n".format(player_name, category)
        response += html.unescape(question["question"]) + '\n'
        answers = question["incorrect_answers"].copy()
        answers.append(question["correct_answer"])
        random.shuffle(answers)
        for i,answer in enumerate(answers):
            character = chr(ord('a')+i)
            unescaped_answer = html.unescape(answer)
            response += "{}) {} \n".format(character, unescaped_answer)
            if answer == question["correct_answer"]:
                self.correct_answer = [character,unescaped_answer.lower()]
                print(self.correct_answer)
        return response

    def answer_question(self, query):
        player_name = self.players[self.current_player]
        if query.lower() in self.correct_answer:
            response = "Correct answer, {}! \n".format(player_name)
            self.players_points[player_name] += 1
        else:
            response = "Wrong answer, {}... The correct answer was: {} \n".format(player_name, self.correct_answer[1])

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
        for player,points in leaderboard.items():
            response += "{}: {} points \n".format(player, points)
        return response

    def finish_game(self):
        max_score = max(self.players_points.values())
        winners = [player for player,score in self.players_points.items() if score == max_score]
        winners = " and ".join(winners)
        response = "Game finished! And the winner is... {}! Congratulations! \n".format(winners)
        for player,points in self.players_points.items():
            response += "{}: {} points \n".format(player, points)
        return response

    def elaborate_query(self, query):
        if query == "leaderboard":
            return self.read_leaderboard()
        elif self.gamestate == GameState.stop:
            response = self.start_game(query)
            response += self.ask_question()
            self.gamestate = GameState.started
        elif self.gamestate == GameState.started:
            response = self.answer_question(query)
            self.next_player()
            if self.round < self.num_rounds:
                response += self.ask_question()
            else:
                response += self.finish_game()
                self.update_leaderboard()
                self.gamestate = GameState.stop
                
        return response