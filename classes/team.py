class Team:
    def __init__(self, players, fitness):
        self.players = players
        self.fitness = fitness

    def tradePlayer(self, player1, player2, player2Team):
        if player1 not in self.players:
            print("Player is not in the team.")
            return None
        self.players.append(player2)
        player2Team.removePlayer(player2)
        player1.removePlayer(player1)
        return self.players
    
    def removePlayer(self, player, playerTeam):
        playerTeam.remove(player)
        return None
    
    