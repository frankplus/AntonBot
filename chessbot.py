import chess

def load_saved_board():
    try:
        f = open("chessboardsave.txt", "r")
        saved_chessboard = f.read()
    except FileNotFoundError:
        return None
    
    f.close()
    return saved_chessboard


saved_board = load_saved_board()
if saved_board:
    board = chess.Board(saved_board)
else:
    board = chess.Board()

def save_board(board):
    file = open('chessboardsave.txt', 'w')
    file.write(board.fen())
    file.close()


def show_board():
    global board
    fen = board.fen().split()[0]
    turn = "White" if board.turn == chess.WHITE else "Black"
    url = "{} to move https://chessboardimage.com/{}.png".format(turn, fen)
    return url

def get_help():
    return '"!chess start" to start a new game.\n'\
            '"!chess board" to show the current board. \n'\
            '"!chess takeback" to undo the last move. \n'\
            '"!chess <move>" to make a move specified in standard algebraic notation. \n'\
            '"!chess help" to show this help information'

def elaborate_query(sender, query):
    global board
    response = ""

    if query == "board":
        response = show_board()
    elif query == "start":
        board.reset()
        response = "Chess game started, GLHF! {}".format(show_board())
    elif query == "takeback":
        board.pop()
        response = show_board()
    elif query == "help":
        response = get_help()
    else:
        try:
            move = board.push_san(query)
            save_board(board)
        except:
            response = "Illegal move\n"

        if board.is_game_over():
            if board.is_checkmate():
                response += "Checkmate!\n"
            if board.is_stalemate():
                response += "Stalemate!\n"
            if board.is_insufficient_material():
                response += "Draw by insufficient material\n"

            response += "Game result: {}\n".format(board.result())
        
        response += show_board()

        

    return response