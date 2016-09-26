import random

questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?",
}

ingredients = {
    "strong": ["glug of rum", "slug of whisky", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bacon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "spash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"],
}

def take_order():
    
    preferences = {}
    for k,v in questions.items():
        print('Order : %s' % questions.get(k))
        order = input(v + ' ')
        preferences[k] = (order == 'yes')
    print(preferences)  
    return preferences        
        
def make_drink(value):
    drinks = []
    for k,v in value.items():
        if v is True:
            drinks.append(random.choice(ingredients[k]))
    return drinks
    
def main():
    order = take_order()
    for drink in make_drink(order):
        print('I would recommend a drink with: ')
        print("    " + drink)
        
if __name__ == '__main__':
    main()
    
    
