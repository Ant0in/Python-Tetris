

from src.common import Move, Rotation, SpecialAction

import keyboard




class GameController:
    
    # priority order
    DEFAULT: dict = {
        'space': SpecialAction.INSTANT_FALL,
        'b': SpecialAction.USE_BAG,
        'left': Move.LEFT,
        'right': Move.RIGHT,
        'down': Move.DOWN,
        'c': Rotation.LEFT,
        'v': Rotation.RIGHT,
    }

    COOLDOWN_TIME: int = 5

    def __init__(self, config: dict | None = None) -> None:
        
        self._config: dict = config if config else GameController.DEFAULT
        self._cooldowned_keys: dict = dict()

    def getConfig(self) -> dict:
        return self._config
    
    def getCooldownedKeys(self) -> dict:
        return self._cooldowned_keys

    def putKeyInCooldown(self, key: str) -> None:
        self.getCooldownedKeys()[key] = GameController.COOLDOWN_TIME

    def handleCooldown(self) -> None:

        cooldown: dict = self.getCooldownedKeys()
        done: list[str] = list()

        for k in cooldown:
            if cooldown[k] != 0: cooldown[k] -= 1
            else: done.append(k)

        for k in done: cooldown.pop(k)
            
    def getUserActions(self) -> Move | Rotation | SpecialAction | None:

        for k, a in self.getConfig().items():

            if keyboard.is_pressed(k):

                if k not in self.getCooldownedKeys():
                    self.putKeyInCooldown(key=k)
                    return a
        
        return None
    
    def handleInputs(self) -> Move | Rotation | SpecialAction | None:
        action: Move | Rotation | SpecialAction | None = self.getUserActions()
        self.handleCooldown()
        return action
    
