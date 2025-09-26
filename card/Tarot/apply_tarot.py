from .tarot_card import TarotCard
from ..poker.poker_card import PokerCard

def apply_tarrot(tarot_card:TarotCard,poker_card:PokerCard=None,**kwargs):
        """
        应用塔罗牌效果到手牌
        """
        tarot_type=tarot_card.tarot_type
        
        if tarot_type == 'POINT_BOOST':
            # 给一张poker手牌增加点数30
            assert isinstance(poker_card, list[PokerCard]), "必须是PokerCard对象"
                # 选择第一张手牌来应用效果
            assert len(poker_card) == 1, "POINT_BOOST效果只能应用于一张牌"
            # 选择第一张手牌来应用效果
            poker_card.effect = 'POINT_PLUS_30'
            return poker_card
            
                
        elif tarot_type == 'MULTIPLIER_ADD':
            assert isinstance(poker_card, list[PokerCard]), "必须是PokerCard对象"
            assert len(poker_card) == 1, "MULTIPLIER_ADD效果只能应用于一张牌"
            poker_card.effect='MULTIPLIER_PLUS_4'
            return poker_card
            
                
        elif tarot_type == 'MULTIPLIER_BOOST':
            assert isinstance(poker_card, list[PokerCard]), "必须是PokerCard对象"
            assert len(poker_card) == 1, "MULTIPLIER_BOOST效果只能应用于一张牌"
            poker_card.effect='MULTIPLIER_TIMES_1_5'
            return poker_card
            
            
        elif tarot_type == 'SUIT_TRANSFORM':
            # 最多转变三张手牌为一种花色
            assert isinstance(poker_card, list[PokerCard])
            assert len(poker_card) <= 3, "SUIT_TRANSFORM效果最多只能应用于三张牌"
            target_suit = tarot_card.suit
            transformed_cards = []
            # 创建新的手牌列表，保留牌的值但改变花色
            new_hand = []
            for i, card in enumerate(poker_card):
                # 转变花色
                new_card = PokerCard(target_suit, card.value, card.effect)
                transformed_cards.append((card, new_card))
                new_hand.append(new_card)
            return 
            
        elif tarot_type == 'STONE_GENERATOR':
            # 生成一张石头牌加入手牌
            stone_card = PokerCard('No_suits', 'stone')  # 使用方块作为石头牌的默认花色
            return stone_card
            
        elif tarot_type == 'CARD_DESTROY':
            # 摧毁两张手牌
            assert isinstance(poker_card, list[PokerCard])
            assert len(poker_card) <= 2, "CARD_DESTROY效果最多只能应用于两张牌"
            return None
            
        elif tarot_type == 'SELECTIVE_BOOST':
            assert isinstance(poker_card, list[PokerCard])
            assert len(poker_card) <= 3, "SELECTIVE_BOOST效果最多只能应用于两张牌"
            # 将两张选定手牌点数加一
            for i in range(len(poker_card)):
                card=poker_card[i]
                if card.value in ['2','3','4','5','6','7','8','9',]:
                    card.value=str(int(card.value)+1)
                    poker_card[i]=card
                else:
                    if card.value=='J':
                        card.value='Q'
                    elif card.value=='Q':
                        card.value='K'
                    elif card.value=='K':
                        card.value='A'
                    elif card.value=='A':
                        card.value='2'
                    elif card.value=='10':
                        card.value='J'
                    poker_card[i]=card
            
        return poker_card