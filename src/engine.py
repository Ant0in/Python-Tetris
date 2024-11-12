

from src.game.tetramino import Tetramino
from src.game.tetris_game import TetrisGame

from src.controller import GameController

from src.common import  Action, SPAWN_BOX
from src.common import Position2D, Move, Rotation, SpecialAction

import sys


class GameEngine:


    @staticmethod
    def handle_polling(game: TetrisGame) -> Action:
        ctrl: GameController = game.getController()
        action: Action = ctrl.handleInputs()
        return action
    
    @staticmethod
    def handle_action(game: TetrisGame, action: Action) -> bool:

        # 's' est notre feedback sur l'action qu'on vient d'effectuer.

        if not action:
            s: bool = True

        elif isinstance(action, Move):
            s: bool = game.getGameBoard().tryMoveCurrent(move=action)

        elif isinstance(action, Rotation):
            s: bool = game.getGameBoard().tryRotateCurrent(rotation=action)

        elif isinstance(action, SpecialAction):
            
            match action:

                case SpecialAction.INSTANT_FALL:
                    s: bool = game.getGameBoard().tryMakeCurrentPieceInstantFall()

                case SpecialAction.USE_BAG:
                    s: bool = GameEngine.handle_bag(game=game)

                case _: raise NotImplementedError()

        return s
    
    @staticmethod
    def handle_bag(game: TetrisGame) -> bool:
        
        isBagUsable: bool = game.getBag().isUsable()
        isBagEmpty: bool = game.getBag().isEmpty()

        if not isBagUsable: return False

        if isBagEmpty:
            # On a utilisé le bag pour stocker, on va mettre la pièce courante dans le bag.
            game.getBag().setStoredPiece(p=game.getGameBoard().getCurrent())
            # On enlève cette pièce du board
            game.getGameBoard().deleteCurrent()
            # Puis on set la current à la prochaine pièce de la factory.
            GameEngine.handle_spawn(game=game, t=None)

        else:
            # On a utilisé le bag pour retrieve, on va remettre la pièce courante
            # dans la factory (en premier) puis on va mettre en current la pièce du bag
            game.getFactory().pushPiece(p=game.getGameBoard().getCurrent())
            game.getGameBoard().deleteCurrent()
            GameEngine.handle_spawn(game=game, t=game.getBag().retrievePiece())
        
        # Puis le bag devient inutilisable.
        game.getBag().setUsableFlag(False)

        return True

    @staticmethod
    def handle_falling_piece(game: TetrisGame) -> bool:
        
        # On veut appliquer la gravité quand la Game nous demande de le faire.
        if not game.shouldApplyGravity():
            return True
        
        # On tente d'appliquer la gravité.
        could_fall: bool = game.getGameBoard().tryApplyGravityOnCurrentPiece()    
        return could_fall

    @staticmethod
    def handle_placing_piece(game: TetrisGame) -> bool:
        
        # Si il n'y a pas de pièce à placer, alors on ne place pas de pièce.
        if not game.getGameBoard().getCurrent():
            return False
        
        # Si jamais on peut encore faire tomber la pièce, alors on ne la place pas.
        rowsToObstable: int = game.getGameBoard().getRowsToObstacle(piece=game.getGameBoard().getCurrent())

        if rowsToObstable > 0:
            return False
        placed_piece: bool = game.getGameBoard().tryPlaceCurrentPiece()

        # Une fois qu'on a placé une pièce, le bag redevient utilisable.
        game.getBag().setUsableFlag(True)

        return placed_piece

    @staticmethod
    def handle_spawn(game: TetrisGame, t: Tetramino | None = None) -> None:
        # Il n'y a plus de pièce active, on en fait donc spawn une nouvelle.

        if not game.getGameBoard().getCurrent():

            # Si pas de paramètre pour la pièce à spawn, par défaut dans la factory.
            if not t: t = game.getFactory().popPiece()
            game.getGameBoard().spawnPiece(t=t, tl_spawnbox=SPAWN_BOX)

    @staticmethod
    def handle_gamelogic(game: TetrisGame) -> None:
        
        # En premier lieu, on vérifie si des lignes sont complètes, pour les éliminer.
        lines_cleared: int = game.getGameBoard().clearFullLines()

        # En deuxième, nous allons gérer les détails liés au score.
        GameEngine.handle_score(game=game, lines_cleared=lines_cleared)

        # Dans un troisième temps, on gère le spawn des pièces.
        GameEngine.handle_spawn(game=game, t=None)

        # Dans un quatrième temps, on vérifie que la partie n'est pas GameOver.
        if game.getGameBoard().isGameOver(): GameEngine.handle_gameover(game=game)

    @staticmethod
    def handle_gameover(game: TetrisGame) -> None:
        # TODO : Game-Over Handling
        sys.exit(0)

    @staticmethod
    def handle_score(game: TetrisGame, lines_cleared: int) -> None:

        game.incrementLinesCleared(q=lines_cleared)
        game.getScore().updateScore(lines_cleared=lines_cleared, level=game.getLevel())
        if game.shouldLevelUp(): game.incrementLevel(q=1)

    @staticmethod
    def handling_routine(game: TetrisGame) -> None:

        # --- Action routine ---
        action: Action = GameEngine.handle_polling(game=game)
        could_move: bool = GameEngine.handle_action(game=game, action=action)

        # --- Gravity / Placing routine ---
        piece_fell: bool = GameEngine.handle_falling_piece(game=game)
        if not piece_fell: GameEngine.handle_placing_piece(game=game)

        # --- Logic routine ---
        GameEngine.handle_gamelogic(game=game)

        # Finalement, on rend de nouveau le bag disponible
        game.incrementFrame()  # Frame incr







            
            