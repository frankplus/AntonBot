import akinator
from enum import Enum

class GameState(Enum):
    STOP = 0,
    STARTED = 1

gamestate = GameState.STOP
aki = akinator.Akinator()

def elaborate_query(query):
    global gamestate, aki
    if query == "stop":
        gamestate = GameState.STOP
        return "Game stopped"
    elif gamestate == GameState.STOP:
        try:
            question = aki.start_game()
        except:
            return "could not start game"
        
        gamestate = GameState.STARTED
        return question
    elif gamestate == GameState.STARTED:
        question = aki.answer(query)
        if aki.progression > 80:
            gamestate = GameState.STOP
            return f"It's {aki.name} ({aki.description})! Was I correct?\n{aki.picture}\n\t"
    
        return question