# -*- coding: utf-8 -*-

class joker:
    """
    Joker类，代表扑克牌中的小丑牌，拥有名称、效果和额外效果三个字段
    """
    def __init__(self, name, price,effect, extra_effect=None):
        """
        初始化joker对象
        
        参数:
            name (str): Joker的名称
            effect (str): Joker的主要效果描述
            extra_effect (str, optional): Joker的额外效果描述，默认为None
        """
        self.name = name
        self.price = price
        self.effect = effect
        self.extra_effect = extra_effect
    
    def get_info(self):
        """
        获取joker对象的信息
        
        返回:
            dict: 包含joker的名称、效果和额外效果的字典
        """
        return {
            'name':self.name,
            'price':self.price,
            'effect':self.effect,
            'extra_effect':self.extra_effect
        }
    def get_price(self):
        """
        获取joker对象的价格
        
        返回:
            int: joker的价格
        """
        return self.price
