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
    def __init__(self, initial_funds=4, target_score=200):
        """
        初始化玩家对象
        
        参数:
            initial_funds (int): 初始资金，默认为100
            target_score (int): 目标分数，默认为1000
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
    
    def play_card(self, card_index=None):
        """
        出一次牌
        
        参数:
            card_index (int, optional): 要出的牌在手中的索引，如果为None则出第一张牌
        
        返回:
            PokerCard or None: 打出的牌，如果手牌为空则返回None
        """
        if not self.hand:
            print("手牌为空，无法出牌")
            return None
        assert len(card_index) <= 5, "最多只能出牌5张"
        for index in sorted(card_index, reverse=True):
            card = self.hand.pop(index)
        
        self.play_count += 1
        print(f"打出了牌: {card}")

        return len(card_index)
    
    def discard_card(self, card_index=None):
        """
        弃一次手牌
        
        参数:
            card_index (int, optional): 要弃的牌在手中的索引，如果为None则弃第一张牌
        
        返回:
            PokerCard or None: 弃掉的牌，如果手牌为空则返回None
        """
        if not self.hand:
            print("手牌为空，无法弃牌")
            return None
        assert len(card_index) <= 5, "最多只能弃牌5张"
        for index in sorted(card_index, reverse=True):
            card = self.hand.pop(index)
        
        self.discard_count += 1
        print(f"弃掉了牌: {', '.join([str(card) for card in card_index])}")
        return len(card_index)
    
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
    def compute_score(self,hand,hand_rank:TexasPokerHandRanking,joker):
        """
        计算手牌的分数
        """
    
        hand_type=hand_rank.get_hand_type(hand)
        point,multiplier=hand_rank.get_point(hand_type)
        
        for card in hand:
            card_value=card.get_numeric_value()
            point+=card_value
            if card.has_effect():
                if card.effect.name=='MULTIPLIER_TIMES_1_5':
                    multiplier*=1.5
                elif card.effect.name=='MULTIPLIER_PLUS_4':
                    multiplier+=4
                elif card.effect.name=='POINT_PLUS_30':
                    point+=30
            point,multiplier=apply_joker(joker,card)
        point,multiplier=apply_joker_final(joker,hand)
        self.score+=point*multiplier
        return 
    
    

# 测试代码
