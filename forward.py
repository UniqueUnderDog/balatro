from environment import Environment
from player import Player
class GameController:
    def __init__(self):
        self.current_round = 1
        self.player = Player()
        self.environment = Environment(self.player)
    
    def start_game(self):
        self.environment.shuffle_card_pools()
        self.environment.send_poker_card(self.player.hand_limit)



    
    def process_turn(self):
        # 处理回合逻辑
        pass
if __name__ == "__main__":
    game_controller = GameController()
    game_controller.start_game()
    print(game_controller.player.get_status())
    print(game_controller.environment.get_environment_status())
    game_controller.start_game()
    print("游戏结束")