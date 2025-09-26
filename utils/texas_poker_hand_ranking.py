import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card.poker.poker_card import PokerCard

class TexasPokerHandRanking:
    """
    德扑牌型等级类，定义了德扑中所有可能的牌型及其对应的点数和倍数
    """
    def __init__(self):
        """
        初始化德扑牌型
        """
        self.hand_rank ={
            'ROYAL_FLUSH': {'points': 140, 'multiplier': 8.0},
            'STRAIGHT_FLUSH': { 'points': 100, 'multiplier': 8.0},
            'FOUR_OF_A_KIND': { 'points': 60, 'multiplier': 7.0},
            'FULL_HOUSE': { 'points': 40, 'multiplier': 4.0},
            'FLUSH': {'points': 35, 'multiplier': 4.0},
            'STRAIGHT': {'points': 30, 'multiplier': 4.0},
            'THREE_OF_A_KIND': {'points': 30, 'multiplier': 3.0},
            'TWO_PAIR': {'points': 20, 'multiplier': 2.0},
            'ONE_PAIR': {'points': 10, 'multiplier': 2.0},
            'HIGH_CARD': {'points': 5, 'multiplier': 1.0}
        }
    
    def get_points(self, hand_type):
        """
        获取牌型对应的点数
        
        返回:
            牌型点数和倍数的元组
        """
        if hand_type in self.hand_rank:
            return self.hand_rank[hand_type]['points'], self.hand_rank[hand_type]['multiplier']
        return 0, 1.0
    
    def get_hand_type(self, cards):
        """
        输入是1-5张牌，判断属于德扑的哪种牌型，按照德扑牌型由高到低的顺序牌型
        
        参数:
            cards: 包含1-5张PokerCard对象的列表
        
        返回:
            牌型类型字符串
        """
        # 检查输入有效性
        if not isinstance(cards, list) or len(cards) < 1 or len(cards) > 5:
            raise ValueError("输入必须是包含1-5张牌的列表")
        
        for card in cards:
            if not isinstance(card, PokerCard):
                raise ValueError("列表中的元素必须是PokerCard对象")
        
        # 如果只有1张牌，直接返回高牌
        if len(cards) == 1:
            return 'HIGH_CARD'
        
        # 预处理牌的数值和花色
        values = []
        suits = []
        for card in cards:
            # 处理'A'可以作为1或14的情况
            if card.value == 'A':
                values.append(1)
                values.append(14)
            else:
                try:
                    num_value = int(card.value) if card.value not in ['J', 'Q', 'K'] else {'J': 11, 'Q': 12, 'K': 13}[card.value]
                    values.append(num_value)
                except:
                    # 处理特殊情况如stone
                    values.append(0)
            
            suits.append(card.suit)
        
        # 按照牌型从高到低检查
        if self._is_royal_flush(cards, values, suits):
            return 'ROYAL_FLUSH'
        elif self._is_straight_flush(cards, values, suits):
            return 'STRAIGHT_FLUSH'
        elif self._is_four_of_a_kind(cards, values):
            return 'FOUR_OF_A_KIND'
        elif self._is_full_house(cards, values):
            return 'FULL_HOUSE'
        elif self._is_flush(cards, suits):
            return 'FLUSH'
        elif self._is_straight(cards, values):
            return 'STRAIGHT'
        elif self._is_three_of_a_kind(cards, values):
            return 'THREE_OF_A_KIND'
        elif self._is_two_pair(cards, values):
            return 'TWO_PAIR'
        elif self._is_one_pair(cards, values):
            return 'ONE_PAIR'
        else:
            return 'HIGH_CARD'
    
    def _is_royal_flush(self, cards, values, suits):
        """判断是否为皇家同花顺：同一花色的10, J, Q, K, A"""
        # 需要至少5张牌
        if len(cards) != 5:
            return False
        
        # 检查是否是同花顺
        if not self._is_straight_flush(cards, values, suits):
            return False
        
        # 检查是否包含10, J, Q, K, A
        card_values = [card.value for card in cards]
        return '10' in card_values and 'J' in card_values and 'Q' in card_values and 'K' in card_values and 'A' in card_values
    
    def _is_straight_flush(self, cards, values, suits):
        """判断是否为同花顺：同一花色的连续数字"""
        # 需要至少5张牌
        if len(cards) != 5:
            return False
        
        # 检查是否是同花
        if not self._is_flush(cards, suits):
            return False
        
        # 检查是否是顺子
        return self._is_straight(cards, values)
    
    def _is_four_of_a_kind(self, cards, values):
        """判断是否为四条：四张相同点数的牌"""
        # 需要至少4张牌
        if len(cards) < 4:
            return False
        
        # 统计每种数值出现的次数
        value_count = {}
        for card in cards:
            if card.value == 'A':
                val = 'A'
            else:
                val = card.value
            value_count[val] = value_count.get(val, 0) + 1
        
        # 检查是否有数值出现了4次
        return 4 in value_count.values()
    
    def _is_full_house(self, cards, values):
        """判断是否为葫芦：三张相同点数的牌加一对"""
        # 需要至少5张牌
        if len(cards) != 5:
            return False
        
        # 统计每种数值出现的次数
        value_count = {}
        for card in cards:
            if card.value == 'A':
                val = 'A'
            else:
                val = card.value
            value_count[val] = value_count.get(val, 0) + 1
        
        # 检查是否有数值出现了3次，且有数值出现了2次
        counts = list(value_count.values())
        return 3 in counts and 2 in counts
    
    def _is_flush(self, cards, suits):
        """判断是否为同花：五张同一花色的牌"""
        # 需要至少5张牌
        if len(cards) != 5:
            return False
        
        # 检查所有牌是否为同一花色
        first_suit = suits[0]
        return all(suit == first_suit for suit in suits)
    
    def _is_straight(self, cards, values):
        """判断是否为顺子：五张连续数字的牌"""
        # 需要至少5张牌
        if len(cards) != 5:
            return False
        
        # 获取唯一数值（去除重复的A值）
        unique_values = []
        for card in cards:
            if card.value == 'A':
                unique_values.append(1)
                unique_values.append(14)
            else:
                try:
                    num_value = int(card.value) if card.value not in ['J', 'Q', 'K'] else {'J': 11, 'Q': 12, 'K': 13}[card.value]
                    unique_values.append(num_value)
                except:
                    unique_values.append(0)
        
        # 排序并去重
        unique_values = sorted(list(set(unique_values)))
        
        # 检查是否存在连续的5个数字
        for i in range(len(unique_values) - 4):
            if unique_values[i+4] - unique_values[i] == 4:
                return True
        
        return False
    
    def _is_three_of_a_kind(self, cards, values):
        """判断是否为三条：三张相同点数的牌"""
        # 需要至少3张牌
        if len(cards) < 3:
            return False
        
        # 统计每种数值出现的次数
        value_count = {}
        for card in cards:
            if card.value == 'A':
                val = 'A'
            else:
                val = card.value
            value_count[val] = value_count.get(val, 0) + 1
        
        # 检查是否有数值出现了3次
        return 3 in value_count.values()
    
    def _is_two_pair(self, cards, values):
        """判断是否为两对：两副对子"""
        # 需要至少4张牌
        if len(cards) < 4:
            return False
        
        # 统计每种数值出现的次数
        value_count = {}
        for card in cards:
            if card.value == 'A':
                val = 'A'
            else:
                val = card.value
            value_count[val] = value_count.get(val, 0) + 1
        
        # 检查是否有两个不同的数值各出现了2次
        pair_count = 0
        for count in value_count.values():
            if count >= 2:
                pair_count += 1
        
        return pair_count >= 2
    
    def _is_one_pair(self, cards, values):
        """判断是否为一对：两张相同点数的牌"""
        # 需要至少2张牌
        if len(cards) < 2:
            return False
        
        # 统计每种数值出现的次数
        value_count = {}
        for card in cards:
            if card.value == 'A':
                val = 'A'
            else:
                val = card.value
            value_count[val] = value_count.get(val, 0) + 1
        
        # 检查是否有数值出现了2次或更多
        return any(count >= 2 for count in value_count.values())
    


if __name__ == "__main__":
    # 创建TexasPokerHandRanking实例
    hand_ranking = TexasPokerHandRanking()
    
    # 创建测试用例
    test_cases = [
        # 皇家同花顺 (Royal Flush)
        [
            PokerCard('Spades', '10'),
            PokerCard('Spades', 'J'),
            PokerCard('Spades', 'Q'),
            PokerCard('Spades', 'K'),
            PokerCard('Spades', 'A')
        ],
        # 同花顺 (Straight Flush)
        [
            PokerCard('Hearts', '5'),
            PokerCard('Hearts', '6'),
            PokerCard('Hearts', '7'),
            PokerCard('Hearts', '8'),
            PokerCard('Hearts', '9')
        ],
        # 四条 (Four of a Kind)
        [
            PokerCard('Spades', 'Q'),
            PokerCard('Hearts', 'Q'),
            PokerCard('Diamonds', 'Q'),
            PokerCard('Clubs', 'Q'),
            PokerCard('Spades', 'K')
        ],
        # 葫芦 (Full House)
        [
            PokerCard('Spades', '8'),
            PokerCard('Hearts', '8'),
            PokerCard('Diamonds', '8'),
            PokerCard('Clubs', '3'),
            PokerCard('Spades', '3')
        ],
        # 同花 (Flush)
        [
            PokerCard('Diamonds', '2'),
            PokerCard('Diamonds', '5'),
            PokerCard('Diamonds', '9'),
            PokerCard('Diamonds', 'J'),
            PokerCard('Diamonds', 'A')
        ],
        # 顺子 (Straight)
        [
            PokerCard('Spades', '3'),
            PokerCard('Hearts', '4'),
            PokerCard('Clubs', '5'),
            PokerCard('Diamonds', '6'),
            PokerCard('Spades', '7')
        ],
        # 三条 (Three of a Kind)
        [
            PokerCard('Spades', 'K'),
            PokerCard('Hearts', 'K'),
            PokerCard('Diamonds', 'K'),
            PokerCard('Clubs', '2'),
            PokerCard('Spades', '5')
        ],
        # 两对 (Two Pair)
        [
            PokerCard('Spades', '10'),
            PokerCard('Hearts', '10'),
            PokerCard('Clubs', '7'),
            PokerCard('Diamonds', '7'),
            PokerCard('Spades', 'A')
        ],
        # 一对 (One Pair)
        [
            PokerCard('Spades', 'Q'),
            PokerCard('Hearts', 'Q'),
            PokerCard('Clubs', '2'),
            PokerCard('Diamonds', '5'),
            PokerCard('Spades', '8')
        ],
        # 高牌 (High Card)
        [
            PokerCard('Spades', '2'),
            PokerCard('Hearts', '5'),
            PokerCard('Clubs', '7'),
            PokerCard('Diamonds', 'J'),
            PokerCard('Spades', 'A')
        ],
        # 单张牌 (High Card)
        [
            PokerCard('Spades', 'A')
        ],
        # 两张牌 - 一对
        [
            PokerCard('Spades', 'K'),
            PokerCard('Hearts', 'K')
        ],
        # 三张牌 - 三条
        [
            PokerCard('Spades', '8'),
            PokerCard('Hearts', '8'),
            PokerCard('Diamonds', '8')
        ]
    ]
    
    # 预期结果
    expected_results = [
        'ROYAL_FLUSH', 'STRAIGHT_FLUSH', 'FOUR_OF_A_KIND', 'FULL_HOUSE', 'FLUSH',
        'STRAIGHT', 'THREE_OF_A_KIND', 'TWO_PAIR', 'ONE_PAIR', 'HIGH_CARD',
        'HIGH_CARD', 'ONE_PAIR', 'THREE_OF_A_KIND'
    ]
    
    # 运行测试并显示结果
    print("===== 德扑牌型判断测试 =====")
    for i, (cards, expected) in enumerate(zip(test_cases, expected_results)):
        try:
            result = hand_ranking.get_hand_type(cards)
            points, multiplier = hand_ranking.get_points(result)
            
            # 格式化显示牌
            cards_str = ", ".join([f"{card.value} of {card.suit}" for card in cards])
            
            # 显示测试结果
            print(f"\n测试 {i+1}:")
            print(f"牌组: {cards_str}")
            print(f"预期牌型: {expected}")
            print(f"实际牌型: {result}")
            print(f"点数: {points}, 倍数: {multiplier}")
            print(f"测试结果: {'✓ 通过' if result == expected else '✗ 失败'}")
        except Exception as e:
            print(f"\n测试 {i+1}: 错误 - {str(e)}")
    
    print("\n===== 测试完成 =====")
    
    
    
    