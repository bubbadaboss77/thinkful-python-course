class Bicycle(object):
    
    def __init__(self, model_name, weight, bike_cost):
        self.model_name = model_name
        self.weight = weight
        self.bike_cost = bike_cost
        
class Bikeshop(object):
    
    def __init__(self, name, margin, inventory):
        self.name = name
        self.margin = margin
        self.inventory = inventory
    
    def sellingprice(self,bike):
        selling_price = bike.bike_cost * self.margin
        return selling_price
    
    def profit(self,bike):
        profit = self.sellingprice(bike) - bike.bike_cost
        return profit
   
class Customer(object):
    
    def __init__(self, customername, budget):
        self.customername = customername
        self.budget = budget
    
    def potential_bikes(self, bikeshop):    
        potentialbikes = []
        for bike in bikeshop.inventory:
            if bikeshop.sellingprice(bike) <= self.budget:
                potentialbikes.append(bike)
        return potentialbikes