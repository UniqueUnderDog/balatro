class PokerCard:
    # Define four suits
    SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds','Every_suits','No_suits']
    # Define 13 values
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','stone']
    
    def __init__(self, suit, value, effect=None):
        """
        Initialize a playing card
        
        Parameters:
            suit: Suit of the card, must be one of SUITS
            value: Value of the card, must be one of VALUES
            effect: Bonus effect, default is None meaning no effect
        """
        if suit not in self.SUITS:
            raise ValueError(f'Suit must be one of: {self.SUITS}')
        if value not in self.VALUES:
            raise ValueError(f'Value must be one of: {self.VALUES}')
            
        self.suit = suit
        self.value = value
        self.effect = effect  # Bonus effect, no effect by default
    
    def get_numeric_value(self):
        """Get numeric value representation of the card"""
        if self.value == 'A':
            return 11  # Can also return 11 depending on game rules
        elif self.value in ['J', 'Q', 'K']:
            return 10  # Can also return 11, 12, 13 depending on game rules
        elif self.value == 'stone':
            return 50  # Special value for stone
        else:
            try:
                return int(self.value)
            except ValueError:
                # Handle any other non-numeric values
                return 0
    
    def has_effect(self):
        """Check if the card has a bonus effect"""
        return self.effect is not None
    
    def get_suits(self):
        """Get the suit of the card"""
        if self.value== 'stone':
            return 'NO_suits'
        return self.suit
    def get_info(self):
        """Get the information of the card"""
        return {
            'suit':self.suit,
            'value':self.value,
            'effect':self.effect
        }
# Test code for PokerCard class and related components
if __name__ == "__main__":
    print("===== Testing Poker Card System =====\n")
    
    # ------------------------------
    # Test 1: Basic Card Creation
    # ------------------------------
    print("[Test 1] Basic Card Creation:")
    try:
        # Create normal cards
        card1 = PokerCard('Spades', 'A')
        card2 = PokerCard('Hearts', '10')
        card3 = PokerCard('Clubs', 'K')
        
        # Test custom suits and values added by user
        special_card1 = PokerCard('Every_suits', 'Q')
        special_card2 = PokerCard('Diamonds', 'stone')
        print(card1.get_numeric_value())
        print(card2.get_suits())
        print(card3.has_effect())
        print(special_card1)
        print(special_card2)
        print("  ✓ All basic cards created successfully")
    except Exception as e:
        print(f"  ✗ Error creating basic cards: {e}")
    
    # ------------------------------
    # Test 2: Card Effect Creation
    # ------------------------------
    