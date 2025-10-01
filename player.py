from card.Tarot import apply_tarot
from card.joker.joker import joker
from card.Tarot.tarot_card import TarotCard
from card.poker.poker_card import PokerCard
from card.Tarot.apply_tarot import apply_tarrot
from utils.texas_poker_hand_ranking import TexasPokerHandRanking
import math


         

class Player:
    """
    玩家类，包含游戏中玩家的所有属性和操作方法
    """
    def __init__(self, initial_funds=4, target_score=200, hand_limit=8, plays_per_round=4, discards_per_round=3):
        """
        初始化玩家对象
        
        参数:
            initial_funds (int): 初始资金，默认为4
            target_score (int): 目标分数，默认为200
            hand_limit (int): 手牌上限，默认为8
            plays_per_round (int): 每回合出牌次数，默认为4
            discards_per_round (int): 每回合弃牌次数，默认为3
        """
        self.hand = []  # 手牌
        self.poker_hand_rank = TexasPokerHandRanking()
        self.deck = []  # 牌组中的牌
        self.play_count = 0  # 出牌次数
        self.discard_count = 0  # 弃牌次数
        self.jokers = []  # 当前拥有的小丑牌
        self.tarot_cards = []  # 当前拥有的塔罗牌
        self.funds = initial_funds  # 当前的资金
        self.score = 0  # 当前的分数
        self.target_score = target_score  # 目标分数
        
        # 回合制相关属性
        self.hand_limit = hand_limit  # 手牌上限
        self.plays_per_round = plays_per_round  # 每回合出牌次数
        self.discards_per_round = discards_per_round  # 每回合弃牌次数
        self.current_plays = 0  # 当前回合已出牌次数
        self.current_discards = 0  # 当前回合已弃牌次数
    
    def play_card(self, card_index=None):
        """
        出一次牌
        
        参数:
            card_index (list): 要出的牌在手中的索引列表
        
        返回:
            bool: 是否成功出牌
        """
        if not self.hand:
            print("手牌为空，无法出牌")
            return False
            
        if self.current_plays >= self.plays_per_round:
            print(f"本回合出牌次数已用完 ({self.current_plays}/{self.plays_per_round})")
            return False
            
        if card_index is None or len(card_index) == 0:
            print("请选择要出的牌")
            return False
            
        if len(card_index) > 5:
            print("最多只能出牌5张")
            return False
        
        # 验证索引有效性
        for index in card_index:
            if index < 0 or index >= len(self.hand):
                print(f"无效的牌索引: {index}")
                return False
        
        # 出牌
        played_cards = []
        for index in sorted(card_index, reverse=True):
            card = self.hand.pop(index)
            played_cards.append(card)
        
        print(f"打出了牌: {', '.join([str(card) for card in played_cards])}")
        
        # 计算分数
        score = self.compute_score(played_cards, TexasPokerHandRanking(), self.jokers)
        self.score += score
        print(f"本次出牌得分: {score}, 总分: {self.score}/{self.target_score}")
        
        # 更新当前回合出牌次数
        self.current_plays += 1
        
        return True
    
    def discard_card(self, card_index=None):
        """
        弃一次手牌
        
        参数:
            card_index (list): 要弃的牌在手中的索引列表
        
        返回:
            int: 弃掉的牌数量，如果无法弃牌则返回0
        """
        if not self.hand:
            print("手牌为空，无法弃牌")
            return 0
            
        if self.current_discards >= self.discards_per_round:
            print(f"本回合弃牌次数已用完 ({self.current_discards}/{self.discards_per_round})")
            return 0
            
        if card_index is None or len(card_index) == 0:
            print("请选择要弃的牌")
            return 0
            
        if len(card_index) > 5:
            print("最多只能弃牌5张")
            return 0
        
        # 验证索引有效性
        for index in card_index:
            if index < 0 or index >= len(self.hand):
                print(f"无效的牌索引: {index}")
                return 0
        
        # 弃牌
        discarded_cards = []
        for index in sorted(card_index, reverse=True):
            card = self.hand.pop(index)
            discarded_cards.append(card)
        
        self.current_discards += 1
        self.discard_count += 1
        print(f"弃掉了牌: {', '.join([str(card) for card in discarded_cards])}")
        return len(discarded_cards)
    
    def use_tarot_card(self, tarot_index=None,card_index=None):
        """
        使用tarot牌
        
        参数:
            tarot_index (int, optional): 要使用的塔罗牌索引，如果为None则使用第一张
        
        返回:
            bool: 是否成功使用塔罗牌
        """
        if not self.tarot_cards:
            print("没有塔罗牌可以使用")
            return False
        
        if tarot_index is None or tarot_index < 0 or tarot_index >= len(self.tarot_cards):
            return False # 默认使用第一张塔罗牌
        else:
            tarot_card = self.tarot_cards.pop(tarot_index)
        
        apply_tarot(tarot_card, self.hand[card_index])
        # 根据塔罗牌类型执行相应效果
        print(f"使用了塔罗牌: {tarot_card.tarot_type} - {tarot_card.description}")
        
        # 根据塔罗牌类型执行不同效果
        
            
        return True
    
    def new_round(self):
        """
        开始新回合，重置回合相关计数器
        """
        self.current_plays = 0
        self.current_discards = 0
        print(f"新回合开始！出牌次数: {self.plays_per_round}, 弃牌次数: {self.discards_per_round}")
    
    def can_play(self):
        """
        检查是否还能出牌
        
        返回:
            bool: 是否还能出牌
        """
        return self.current_plays < self.plays_per_round and len(self.hand) > 0
    
    def can_discard(self):
        """
        检查是否还能弃牌
        
        返回:
            bool: 是否还能弃牌
        """
        return self.current_discards < self.discards_per_round and len(self.hand) > 0
    
    def has_won(self):
        """
        检查是否达到胜利条件
        
        返回:
            bool: 是否获胜
        """
        return self.score >= self.target_score
    
    def add_card_to_hand(self, card):
        """
        向手牌添加一张牌
        
        参数:
            card (PokerCard): 要添加的扑克牌
        """
        
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)
        print(f"获得了新牌: {card}")
        
    
    def buy_joker(self, joker_card):
        """
        购买一张小丑牌
        
        参数:
            joker_card (joker): 要购买的小丑牌
        """
        if isinstance(joker_card, joker):
            if self.funds >= joker_card.get_price():
                self.jokers.append(joker_card)
                self.funds -= joker_card.get_price()
                print(f"获得了新小丑牌: {joker_card.name}")
            else:
                print("资金不足，无法购买小丑牌")
                return False
        else:
            print("只能添加joker类型的牌")
            return False
        return True
    def sell_joker(self, joker_card):
        """
        出售一张小丑牌
        
        参数:
            joker_card (joker): 要出售的小丑牌
        """
        if isinstance(joker_card, joker):
            if joker_card in self.jokers:
                self.jokers.remove(joker_card)
                self.funds += math.floor(joker_card.get_price() * 0.7)
                print(f"出售了小丑牌: {joker_card.name}")
            else:
                print("你没有这张小丑牌")
        else:
            print("只能出售joker类型的牌")
    
    def buy_tarot_card(self, tarot_card):
        """
        购买一张塔罗牌
        
        参数:
            tarot_card (TarotCard): 要添加的塔罗牌
        """
        if isinstance(tarot_card, TarotCard):
            if self.funds >= tarot_card.get_price():
                self.tarot_cards.append(tarot_card)
                self.funds -= tarot_card.get_price()
                print(f"获得了新塔罗牌: {tarot_card.tarot_type}-{tarot_card.description}")

            else:
                print("资金不足，无法购买塔罗牌")
                return False
        else:
            print("只能添加TarotCard类型的牌")
            return False
        return True
    def sell_tarot(self, tarot_card):
        """
        出售一张塔罗牌
        
        参数:
            tarot_card (TarotCard): 要出售的塔罗牌
        """
        if isinstance(tarot_card, TarotCard):
            if tarot_card in self.tarot_cards:
                self.tarot_cards.remove(tarot_card)
                
                self.funds += math.floor(tarot_card.get_price() * 0.7)
                print(f"出售了塔罗牌: {tarot_card.tarot_type}-{tarot_card.description}")
            else:
                print("你没有这张小塔罗牌")
        else:
            print("只能出售TarotCard类型的牌")
    
    def get_status(self):
        """
        获取玩家当前状态
        
        返回:
            dict: 包含玩家所有状态信息的字典
        """
        status = {
            "手牌数量": len(self.hand),
            "牌组数量": len(self.deck),
            "剩余出牌次数": self.play_count,
            "剩余弃牌次数": self.discard_count,
            "拥有小丑牌数量": len(self.jokers),
            "拥有塔罗牌数量": len(self.tarot_cards),
            "当前资金": self.funds,
            "当前分数": self.score,
            "目标分数": self.target_score,
            "手牌详情": [str(card.get_info()) for card in self.hand],
            "小丑牌详情": [str(jk) for jk in self.jokers],
            "塔罗牌详情": [str(card.get_info()) for card in self.tarot_cards],
            "当前计分倍率": self.poker_hand_rank.hand_rank
        }
        
        return status
    
    def apply_tarot_card(self,tarot_card,hand):
        """
        应用塔罗牌的效果
        
        参数:
            tarot_card (TarotCard): 要应用的塔罗牌
            hand (list[PokerCard]): 玩家的手牌
        """
        apply_tarrot(tarot_card,hand)
    def compute_score(self, hand, hand_rank: TexasPokerHandRanking, jokers):
        """
        计算手牌的分数
        
        参数:
            hand: 手牌列表
            hand_rank: 牌型判断器
            jokers: 小丑牌列表
        
        返回:
            int: 计算得到的分数
        """
        if not hand:
            return 0
        
        # 获取牌型基础分数和倍率
        hand_type = hand_rank.get_hand_type(hand)
        base_point, base_multiplier = hand_rank.get_point(hand_type)
        
        total_point = base_point
        total_multiplier = base_multiplier
        
        # 计算每张牌的点数和效果
        for card in hand:
            card_value = card.get_numeric_value()
            total_point += card_value
            
            # 处理牌的特殊效果
            if card.has_effect():
                if hasattr(card.effect, 'name'):
                    if card.effect.name == 'MULTIPLIER_TIMES_1_5':
                        total_multiplier *= 1.5
                    elif card.effect.name == 'MULTIPLIER_PLUS_4':
                        total_multiplier += 4
                    elif card.effect.name == 'POINT_PLUS_30':
                        total_point += 30
        
        # TODO: 应用小丑牌效果（需要实现apply_joker函数）
        # for joker_card in jokers:
        #     total_point, total_multiplier = apply_joker(joker_card, total_point, total_multiplier)
        
        final_score = int(total_point * total_multiplier)
        return final_score 
    
    

    def __str__(self):
        """返回玩家状态的字符串表示"""
        return f"玩家状态 - 资金: {self.funds}, 分数: {self.score}/{self.target_score}, 手牌: {len(self.hand)}张, 小丑牌: {len(self.jokers)}张, 塔罗牌: {len(self.tarot_cards)}张"
    
    def __repr__(self):
        """返回玩家的详细表示"""
        return f"Player(funds={self.funds}, score={self.score}, target_score={self.target_score})"

# 测试代码
