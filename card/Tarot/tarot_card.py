class TarotCard:
    """
    塔罗牌类，具有改变扑克卡牌属性、资金加倍、转变花色、生成石头牌、摧毁手牌和增加手牌点数等功能
    """
    
    # 定义塔罗牌类型
    TAROT_TYPES = {
        'POINT_BOOST': '增加一张手牌30点数',
        'MULTIPLIER_ADD': '增加一张手牌4倍率',
        'MULTIPLIER_BOOST': '使一张手牌在计算时倍率乘1.5',
        'FUND_DOUBLE': '当前拥有的资金加倍（最多20）',
        'SUIT_TRANSFORM': '转变最多三种花色为',
        'STONE_GENERATOR': '生成一张石头牌',
        'CARD_DESTROY': '摧毁最多两张手牌',
        'SELECTIVE_BOOST': '选定最多两张手牌加1点数'
    }
    
    def __init__(self,  tarot_type,price, value=None,**kwargs):
        """
        初始化塔罗牌
        
        参数:
            name: 塔罗牌名称
            tarot_type: 塔罗牌类型，必须是TAROT_TYPES中的一种
            value: 数值参数，根据卡牌类型有不同含义
        """
        
        if tarot_type not in self.TAROT_TYPES:
            raise ValueError(f'塔罗牌类型必须是以下之一: {list(self.TAROT_TYPES.keys())}')
        self.tarot_type = tarot_type
        self.price=price
        # 根据塔罗牌类型设置默认值
        self.suits=kwargs.get('suits',None)
        self.description = self.TAROT_TYPES[tarot_type]
        
    def get_price(self):
        return self.price
    
    def __str__(self):
        """返回塔罗牌的字符串表示"""
        if self.suits:
            return f"{self.tarot_type} - {self.description}{self.suits} (价格: {self.price})"
        return f"{self.tarot_type} - {self.description} (价格: {self.price})"
    
    def __repr__(self):
        """返回塔罗牌的详细表示"""
        return f"TarotCard(tarot_type='{self.tarot_type}', price={self.price})"
    
    def get_info(self):
        if self.suits:
            return {
                'tarot_type':self.tarot_type,
                'price':self.price,
                'description':self.description+self.suits,
            }
        return {
            'tarot_type':self.tarot_type,
            'price':self.price,
            'description':self.description,
            
        }
