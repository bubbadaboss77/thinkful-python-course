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

def take_order(value):
    value[0] = value
    preferences = {}
    for k,v in questions.items():
        print('Order : %s' % questions.get(k))
        
        

if __name__ == '__main__':
    take_order()
    value = input(questions.keys())
    
'''    
def side_effect_test(value):
    # Do something to modify the value
    value[1] = "orange"
    print("Inside the function, the value becomes {}".format(value))

if __name__ == "__main__":
    # Create the value
    value = ["red", "green", "blue"]

    print("Outside the function, the value starts as {}".format(value))

    side_effect_test(value)

    print("Outside the function, the value is now {}".format(value))    
'''    