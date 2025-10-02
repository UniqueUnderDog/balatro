import random
from card.poker.poker_card import PokerCard
from card.joker.joker import joker
from card.Tarot.tarot_card import TarotCard

class Environment:
    def __init__(self, player):
        """
        初始化游戏环境
        
        参数:
            player: 玩家对象
        """
        self.player = player
        self.poker_card_pool = []  # 扑克牌池
        self.tarot_card_pool = []  # 塔罗牌池
        self.joker_card_pool = []  # 小丑牌池
        self.score = 0  # 当前的分数
        self.round=0 #当前轮次
        self.target_score = 300  # 目标分数
        self.shop = {"jokers": [], "tarots": []}  # 商店
        
        # 初始化所有卡牌池
        self._init_poker_card_pool()
        self._init_tarot_card_pool()
        self._init_joker_card_pool()
        
        # 初始化商店
        self.init_shop()
    def get_poker_card_pool(self):
        """
        获取扑克牌池
        
        返回:
            list: 包含所有扑克牌的列表
        """
        return self.poker_card_pool
    
    def get_tarot_card_pool(self):
        """
        获取塔罗牌池
        
        返回:
            list: 包含所有塔罗牌的列表
        """
        return self.tarot_card_pool
    
    def get_joker_card_pool(self):
        """
        获取小丑牌池
        
        返回:
            list: 包含所有小丑牌的列表
        """
        return self.joker_card_pool
    
    def get_environment_status(self):
        """
        获取游戏环境的状态
        
        返回:
            dict: 包含环境状态的字典
        """
        return {
            "poker_card_pool": self.poker_card_pool,
            "tarot_card_pool": self.tarot_card_pool,
            "joker_card_pool": self.joker_card_pool,
            "shop": self.shop
        }
    def _init_poker_card_pool(self):
        """
        初始化扑克牌池
        """
        # 定义扑克牌的花色和点数
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        # 创建标准52张牌的扑克牌池
        for suit in suits:
            for value in values:
                self.poker_card_pool.append(PokerCard(suit, value))
        
        # 打乱牌池顺序
        random.shuffle(self.poker_card_pool)
    
    def _init_tarot_card_pool(self):
        """
        初始化塔罗牌池
        """
        # 定义塔罗牌类型和价格
        tarot_types = [
            ('POINT_BOOST', 3),
            ('MULTIPLIER_ADD', 4),
            ('MULTIPLIER_BOOST', 6),
            ('FUND_DOUBLE', 3),
            ('SUIT_TRANSFORM', 4),
            ('STONE_GENERATOR', 4),
            ('CARD_DESTROY', 5),
            ('SELECTIVE_BOOST', 4)
        ]
        
        # 创建塔罗牌池
        for tarot_type, price in tarot_types:
            self.tarot_card_pool.append(TarotCard(tarot_type, price))
        
        # 打乱牌池顺序
        random.shuffle(self.tarot_card_pool)
    
    def _init_joker_card_pool(self):
        """
        初始化小丑牌池
        """
        # 定义一些小丑牌
        joker_cards = [
            joker("幸运星",price=1,effect="增加所有牌的点数"),
            joker("魔术师", price=1,effect="改变一张牌的花色"),
            joker("小丑王", price=1,effect="提升所有小丑牌的效果"),
            
        ]
        
        # 添加到小丑牌池
        self.joker_card_pool.extend(joker_cards)
        
        # 打乱牌池顺序
        random.shuffle(self.joker_card_pool)
    
    def send_poker_card(self, num=7):
        """
        从poker池中无放回地发指定数量的牌给玩家
        
        参数:
            num: 发牌数量，默认为1
        
        返回:
            list: 发给玩家的牌列表
        """
        sent_cards = []
        
        # 检查牌池是否有足够的牌
        if len(self.poker_card_pool) < num:
            print(f"牌池中的牌不足，只能发{len(self.poker_card_pool)}张牌")
            num = len(self.poker_card_pool)
        
        # 无放回地发牌
        for _ in range(num):
            card = self.poker_card_pool.pop()
            self.player.add_card_to_hand(card)
            sent_cards.append(card)
        
        return sent_cards
    
    def refill_hand(self):
        """补牌到手牌上限"""
        cards_needed = self.player.hand_limit - len(self.player.hand)
        if cards_needed > 0:
            sent_cards = self.send_poker_card(cards_needed)
            print(f"补牌 {len(sent_cards)} 张")
    
    def init_shop(self):
        """
        初始化商店，从牌池中随机选择卡牌放入商店
        """
        # 从小丑牌池中随机选择2张放入商店
        if len(self.joker_card_pool) >= 2:
            self.shop["jokers"] = random.sample(self.joker_card_pool, 2)
        elif len(self.joker_card_pool) > 0:
            self.shop["jokers"] = self.joker_card_pool.copy()
        
        # 从塔罗牌池中随机选择2张放入商店
        if len(self.tarot_card_pool) >= 2:
            self.shop["tarots"] = random.sample(self.tarot_card_pool, 2)
        elif len(self.tarot_card_pool) > 0:
            self.shop["tarots"] = self.tarot_card_pool.copy()
        
        print("商店已初始化完成")
    
    def get_shop_items(self):
        """
        获取商店中的所有物品
        
        返回:
            dict: 包含商店中所有物品的字典
        """
        return self.shop
    
    def refresh_shop(self):
        """
        刷新商店，重新从牌池中随机选择卡牌
        """
        # 清空当前商店
        self.shop = {"jokers": [], "tarots": []}
        
        # 重新初始化商店
        self.init_shop()
        
        print("商店已刷新")
    
    def buy_joker_from_shop(self, index):
        """
        从商店购买小丑牌（购买后从全局牌池移除）
        
        参数:
            index: 要购买的小丑牌在商店中的索引
        
        返回:
            bool: 是否购买成功
        """
        # 检查索引是否有效
        if 0 <= index < len(self.shop["jokers"]):
            joker_card = self.shop["jokers"][index]
            # 检查玩家是否有足够的资金
            if self.player.buy_joker(joker_card):
                # 从商店中移除该小丑牌
                self.shop["jokers"].pop(index)
                
                # 从全局小丑牌池中移除该卡牌（实现卖了就没了的功能）
                if joker_card in self.joker_card_pool:
                    self.joker_card_pool.remove(joker_card)
                
                print(f"成功购买了小丑牌: {joker_card.name}")
                return True
        
        print("购买失败")
        return False
    
    def buy_tarot_from_shop(self, index):
        """
        从商店购买塔罗牌（购买后不从全局牌池移除，可再次出现）
        
        参数:
            index: 要购买的塔罗牌在商店中的索引
        
        返回:
            bool: 是否购买成功
        """
        # 检查索引是否有效
        if 0 <= index < len(self.shop["tarots"]):
            tarot_card = self.shop["tarots"][index]
            
            # 检查玩家是否有足够的资金
            if self.player.buy_tarot_card(tarot_card):
                # 从商店中移除该塔罗牌（但不从全局牌池移除，所以可以再次出现）
                self.shop["tarots"].pop(index)
                
                # 将塔罗牌添加给玩家
                
                print(f"成功购买了塔罗牌: {tarot_card.tarot_type}")
                return True
        
        print("购买失败")
        return False
    
    def sell_joker_to_shop(self, index):
        """
        从商店售卖小丑牌（将小丑牌放回全局牌池）
        
        参数:
            index: 要售卖的小丑牌在玩家手中的索引
        
        返回:
            bool: 是否售卖成功
        """
        # 检查索引是否有效
        if 0 <= index < len(self.player.jokers):
            joker_card = self.player.jokers[index]
        else:
            print("索引无效，无法售卖小丑牌")
            return False
        
        # 添加到全局小丑牌池（实现放回功能）
        if joker_card not in self.joker_card_pool:
            self.joker_card_pool.append(joker_card)
            
            # 返还一部分购买价格（例如原价的70%）
            self.player.sell_joker(joker_card)
            print(f"成功卖出了小丑牌: {joker_card.name}")
            return True
        
        print("售卖失败")
        return False
    def sell_tarot_to_shop(self, index):
        """
        从商店售卖塔罗牌（将塔罗牌放回全局牌池）
        
        参数:
            index: 要售卖的塔罗牌在玩家手中的索引
        
        返回:
            bool: 是否售卖成功
        """
        # 检查索引是否有效
        if 0 <= index < len(self.player.tarots):
            tarot_card = self.player.tarots[index]
        else:
            print("索引无效，无法售卖塔罗牌")
            return False
        
        # 添加到全局塔罗牌池（实现放回功能）
        if tarot_card not in self.tarot_card_pool:
            self.tarot_card_pool.append(tarot_card)
            
            # 返还一部分购买价格（例如原价的70%）
            self.player.sell_tarot(tarot_card)
            
                
            print(f"成功卖出了塔罗牌: {tarot_card.tarot_type}，获得了{sell_price}金币")
            return True
        
        print("售卖失败")
        return False
    def get_shop_status(self):
        """
        获取商店的状态
        
        返回:
            dict: 包含商店状态的字典
        """
        return {
            "jokers": self.shop["jokers"],
            "tarots": self.shop["tarots"]
        }
    
    def get_environment_status(self):
        """
        获取游戏环境的状态
        
        返回:
            dict: 包含环境状态的字典
        """
        return {
            "poker_card_pool": self.poker_card_pool,
            "tarot_card_pool": self.tarot_card_pool,
            "joker_card_pool": self.joker_card_pool,
            "shop": self.get_shop_status()
        }
    def shuffle_card_pools(self):
        """
        洗牌所有牌池
        """
        random.shuffle(self.poker_card_pool)
        random.shuffle(self.tarot_card_pool)
        random.shuffle(self.joker_card_pool)
    
    def check_game_end(self):
        """
        检查游戏是否结束
        
        返回:
            bool: 如果游戏结束则返回True，否则返回False
        """
        # 检查玩家是否还有足够的资金
        if self.player.play_count == 0 and self.score<self.target:
            print("游戏结束，玩家未达到目标分数")
            return True
        elif self.score>=self.target:
            print("游戏结束，玩家达到目标分数")
            return True
        
        return False
    
    def update_score(self):
        """
        更新当前轮次的分数
        
        参数:
            score (int): 要更新的分数
        """
        self.score =self.player.score
    
        

