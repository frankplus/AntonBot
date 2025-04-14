import chess
import chess.engine
import json
from enum import Enum
import config
import logging

try:
    chess_engine = chess.engine.SimpleEngine.popen_uci(config.CHESSENGINE_PATH)
except:
    chess_engine = None
    logging.warning("could not open chess engine")

def engine_play(board):
    global chess_engine
    try:
        result = chess_engine.play(board, chess.engine.Limit(time=0.1))
    except:
        # restart chess engine
        chess_engine.quit()
        chess_engine = chess.engine.SimpleEngine.popen_uci(config.CHESSENGINE_PATH)
        result = chess_engine.play(board, chess.engine.Limit(time=0.1))
    return result.move


def get_help():
    return '"!chess play" to play with the AI. \n'\
            '"!chess <names...>" to start a new game with the specified participants.\n'\
            '"!chess <move>" to make a move specified in standard algebraic notation. \n'\
            '"!chess board" to show the current board. \n'\
            '"!chess takeback" to undo the last move. \n'\
            '"!chess takeback <number>" to undo the last N moves. \n'\
            '"!chess load <FEN>" to load a board position. \n'\
            '"!chess stop" to stop the game.'


class GameState(Enum):
    stop = 0
    started = 1

class Game:
    def __init__(self, id=0):
        self.id = id

        json_savestate = self.load_saved_state()
        if id in json_savestate:
            gamestate = json_savestate[id]
            self.board = chess.Board(gamestate["fen"])
            self.players = gamestate["players"]
            self.gamestate = GameState(gamestate["gamestate"])
            self.against_engine = gamestate["against_engine"]
        else:
            self.board = chess.Board()
            self.gamestate = GameState.stop
            self.against_engine = False
            self.players = []

    def load_saved_state(self):
        try:
            f = open("chessboardsave.txt", "r")
            json_savestate = json.load(f)
        except FileNotFoundError:
            return dict()
        f.close()
        return json_savestate

    def save_state(self):
        gamestate = dict()
        gamestate["players"] = self.players
        gamestate["fen"] = self.board.fen()
        gamestate["gamestate"] = self.gamestate.value
        gamestate["against_engine"] = self.against_engine

        json_savestate = self.load_saved_state()
        json_savestate[self.id] = gamestate
        with open("chessboardsave.txt", "w") as f:
            f.write(json.dumps(json_savestate))

    def set_participants(self, players):
        self.players = players

    def start_game(self):
        self.board.reset()

    def get_current_player(self):
        return self.players[0] if self.board.turn == chess.WHITE else self.players[1]

    def show_board(self):

        response = ""

        if self.board.is_game_over():
            response += self.finish_game()
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            response += "{} ({}) to move".format(self.get_current_player(), turn)

        try:
            last_move = self.board.peek().uci()
            response += ", last move was {}".format(last_move)
        except:
            pass

        if self.board.is_check():
            response += " check!"

        fen = self.board.fen().split()[0]
        flip = "-flip" if self.board.turn == chess.BLACK else ""
        response += " https://chessboardimage.com/{}{}.png".format(fen, flip)
        return response

    def finish_game(self):
        response = ""
        if self.board.is_checkmate():
            response += "Checkmate!\n"
        if self.board.is_stalemate():
            response += "Stalemate!\n"
        if self.board.is_insufficient_material():
            response += "Draw by insufficient material\n"

        winner = self.players[0] if self.board.result() == "1-0" else None
        winner = self.players[1] if self.board.result() == "0-1" else None
        response += "Game result: {}\n".format(self.board.result())
        if winner: 
            response += "The winner is {}!".format(winner)
        return response

    def elaborate_query(self, sender, query):

        global chess_engine
        if not chess_engine:
            return "Could not load chess engine"

        query = query.split(" ", 1)
        command = query[0] if len(query) > 0 else ""
        params = query[1] if len(query) > 1 else None
        response = ""

        if command == "stop":
            self.gamestate = GameState.stop
            response = "Game stopped"
        elif command == "help":
            response = get_help()
        elif command == "play":
            self.set_participants(["You", "AI"])
            self.start_game()
            self.against_engine = True
            response = "Game against AI started, GLHF! {}".format(self.show_board())
            self.gamestate = GameState.started
        elif command == "load":
            try:
                self.board = chess.Board(params)
            except ValueError:
                return "Invalid FEN"
            if self.gamestate == GameState.stop or self.against_engine:
                self.set_participants(["You", "AI"] if self.board.turn == chess.WHITE else ["AI", "You"])
                self.against_engine = True
                self.gamestate = GameState.started
            response = "Loaded board position. {}".format(self.show_board())
        elif self.gamestate == GameState.stop:
            if len(query) >= 2:
                self.set_participants(query)
                self.start_game()
                self.against_engine = False
                response = "Chess game started, GLHF! {}".format(self.show_board())
                self.gamestate = GameState.started
            else:
                response = "Type the names of the two participants separated by space (!chess <names...>): "
        elif self.gamestate == GameState.started:
            if command == "board":
                response = self.show_board()
            elif command == "takeback":
                try:
                    number_takebacks = 1
                    if params:
                        number_takebacks = int(params)
                    for _ in range(number_takebacks):
                        self.board.pop()
                    response = self.show_board()
                    self.save_state()
                except:
                    response = "Could not takeback"
            elif sender == self.get_current_player() or self.against_engine:
                try:
                    move = self.board.push_san(command)
                    if self.against_engine:
                        move = engine_play(self.board)
                        if move:
                            self.board.push(move)
                    response = self.show_board()
                except ValueError:
                    response = "Illegal move\n"

                if self.board.is_game_over():
                    self.gamestate = GameState.stop

                self.save_state()
            else:
                response = "{}, it's not your turn!!".format(sender)
                
        return response

chess_instances = {}

def chess_command_handler(channel, sender, query):
    if channel not in chess_instances or chess_instances[channel].gamestate == GameState.stop:
        chess_instances[channel] = Game(channel)
    return chess_instances[channel].elaborate_query(sender, query)

def register(bot):
    bot.register_command('chess', chess_command_handler)
    bot.register_help('chess', get_help())