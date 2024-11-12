


class Score:
    
    def __init__(self, score: int = 0) -> None:
        
        self._score: int = score

    def getScore(self) -> int:
        return self._score
    
    def setScore(self, s: int) -> None:
        self._score = s

    def incrementScore(self, q: int) -> None:
        self.setScore(self.getScore() + q)

    def calculateClearGain(self, lines_cleared: int, level: int) -> int:

        match lines_cleared:

            case 0: return 0
            case 1: return 40 * (lines_cleared + 1)
            case 2: return 100 * (lines_cleared + 1)
            case 3: return 300 * (lines_cleared + 1)
            case 4: return 1200 * (lines_cleared + 1)
            case _: raise NotImplementedError()

    def updateScore(self, lines_cleared: int, level: int) -> None:
        gain: int = self.calculateClearGain(lines_cleared=lines_cleared, level=level)
        self.incrementScore(q=gain)