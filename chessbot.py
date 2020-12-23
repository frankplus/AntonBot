import chess

board = chess.Board()

def show_board():
    fen = board.fen().split()[0]
    url = "http://www.fen-to-image.com/image/36/double/coords/{}".format(fen)
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