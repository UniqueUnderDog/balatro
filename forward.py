from environment import Environment
from player import Player

class GameController:
    def __init__(self):
        self.current_round = 1
        self.player = Player()
        self.environment = Environment(self.player)
        self.game_over = False
    
    def start_game(self):
        """开始游戏"""
        print("=== Balatro 游戏开始 ===")
        print(f"目标分数: {self.player.target_score}")
        print(f"初始资金: {self.player.funds}")
        
        # 发初始手牌
        self.environment.send_poker_card(self.player.hand_limit)
        print(f"发牌完成，当前手牌数: {len(self.player.hand)}")
        
        # 开始游戏循环
        while not self.game_over:
            self.process_round()
            
        self.end_game()
    
    def process_round(self):
        """处理一个回合"""
        print(f"\n=== 第 {self.current_round} 回合 ===")
        self.player.new_round()
        
        # 显示当前状态
        
        
        # 回合循环：玩家可以使用塔罗牌、出牌，直到出牌次数用完
        while self.player.can_play() and not self.player.has_won():
            self.show_game_status()
            action = self.get_player_action()
            
            if action == "play":
                self.handle_play_cards()
            elif action == "discard":
                self.handle_discard_cards()
            elif action == "tarot":
                self.handle_use_tarot()
            else:
                print("无效的选择，请重新输入")
                continue
            
            # 检查胜利条件
            if self.player.has_won():
                self.game_over = True
                return
        
        # 回合结束，补牌到手牌上限
        self.refill_hand()
        self.current_round += 1
        
        # 检查是否需要结束游戏（可以添加其他结束条件）
        if self.current_round > 10:  # 示例：10回合后结束
            self.game_over = True
    
    def show_game_status(self):
        """显示游戏状态"""
        print(f"\n当前状态:")
        print(f"分数: {self.player.score}/{self.player.target_score}")
        print(f"资金: {self.player.funds}")
        print(f"剩余出牌次数: {self.player.plays_per_round - self.player.current_plays}")
        print(f"剩余弃牌次数: {self.player.discards_per_round - self.player.current_discards}")
        print(f"手牌 ({len(self.player.hand)}张):")
        for i, card in enumerate(self.player.hand):
            print(f"  {i}: {card}")
        
        if self.player.tarot_cards:
            print(f"塔罗牌 ({len(self.player.tarot_cards)}张):")
            for i, tarot in enumerate(self.player.tarot_cards):
                print(f"  {i}: {tarot}")
    
    def get_player_action(self):
        """获取玩家行动选择"""
        print("\n请选择行动:")
        actions = []
        
        if self.player.can_play():
            actions.append("play - 出牌")
        if self.player.can_discard():
            actions.append("discard - 弃牌")
        if self.player.tarot_cards:
            actions.append("tarot - 使用塔罗牌")
        
        for action in actions:
            print(f"  {action}")
        
        choice = input("请输入选择: ").strip().lower()
        return choice
    
    def handle_play_cards(self):
        """处理出牌"""
        if not self.player.can_play():
            print("无法出牌")
            return
        
        print("请选择要出的牌（输入索引，用空格分隔，最多5张）:")
        try:
            indices_input = input("牌索引: ").strip()
            if not indices_input:
                print("未选择任何牌")
                return
            
            indices = [int(x) for x in indices_input.split()]
            success = self.player.play_card(indices)
            
            if success:
                print(f"成功出牌")
                self.refill_hand()
        except ValueError:
            print("输入格式错误，请输入数字")
        except Exception as e:
            print(f"出牌失败: {e}")
    
    def handle_discard_cards(self):
        """处理弃牌"""
        if not self.player.can_discard():
            print("无法弃牌")
            return
        
        print("请选择要弃的牌（输入索引，用空格分隔，最多5张）:")
        try:
            indices_input = input("牌索引: ").strip()
            if not indices_input:
                print("未选择任何牌")
                return
            
            indices = [int(x) for x in indices_input.split()]
            discarded_count = self.player.discard_card(indices)
            
            if discarded_count > 0:
                print(f"成功弃掉 {discarded_count} 张牌")
        except ValueError:
            print("输入格式错误，请输入数字")
        except Exception as e:
            print(f"弃牌失败: {e}")
    
    def handle_use_tarot(self):
        """处理使用塔罗牌"""
        if not self.player.tarot_cards:
            print("没有塔罗牌可以使用")
            return
        
        print("请选择要使用的塔罗牌索引:")
        try:
            tarot_index = int(input("塔罗牌索引: ").strip())
            
            # 根据塔罗牌类型，可能需要选择目标牌
            print("请选择目标牌索引（如果不需要可直接回车）:")
            card_input = input("目标牌索引: ").strip()
            card_index = int(card_input) if card_input else None
            
            success = self.player.use_tarot_card(tarot_index, card_index)
            if success:
                print("塔罗牌使用成功")
        except ValueError:
            print("输入格式错误，请输入数字")
        except Exception as e:
            print(f"使用塔罗牌失败: {e}")
    
    def end_game(self):
        """结束游戏"""
        print("\n=== 游戏结束 ===")
        if self.player.has_won():
            print("🎉 恭喜！你达到了目标分数！")
        else:
            print("游戏结束")
        
        print(f"最终分数: {self.player.score}/{self.player.target_score}")
        print(f"游戏回合数: {self.current_round - 1}")
        print(f"剩余资金: {self.player.funds}")

if __name__ == "__main__":
    game_controller = GameController()
    game_controller.start_game()