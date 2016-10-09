from bicycle import Bicycle, Bikeshop, Customer
import random

if __name__ == '__main__':
    
    bike_A = Bicycle("Bike A", 10, 200)
    bike_B = Bicycle("Bike B", 20, 250)
    bike_C = Bicycle("Bike C", 30, 350)
    bike_D = Bicycle("Bike D", 40, 400)
    bike_E = Bicycle("Bike E", 50, 650)
    bike_F = Bicycle("Bike F", 55, 800)
    
    
    inventory = [bike_A, bike_B, bike_C, bike_D, bike_E, bike_F]
    
    bike_shop = Bikeshop("Reed's Bikes", 1.2, inventory)
    
    
    customer1 = Customer("pat", 300)
    customer2 = Customer("owen", 450)
    customer3 = Customer("matt", 1000)
    
    customerlist = [customer1, customer2, customer3]
    
    
        
    print ("The inventory of {0} is as follows: ".format(bike_shop.name))
    for bike in inventory:
        print ("{0}, which originally cost ${1} for {2} to buy. {2} is selling it for ${3}.".format(bike.model_name, bike.bike_cost,bike_shop.name, bike_shop.sellingprice(bike)))
    print("\n")
        
    for customer in customerlist:
        print ("{0} has a budget of ${1} and can thus afford any of the following bikes: ".format(customer.customername, customer.budget))
        for bike in customer.potential_bikes(bike_shop):
             print (bike.model_name)
    profit_earned = 0
    for customer in customerlist:
        bought_bike = random.choice(customer.potential_bikes(bike_shop))
        new_budget = customer.budget - bike_shop.sellingprice(bought_bike)
        print ("{0} bought {1}, which cost ${2}. {0} now has ${3} remaining in his budget.".format(customer.customername, bought_bike.model_name,bike_shop.sellingprice(bought_bike),new_budget))
        profit_earned += bike_shop.profit(bought_bike)
        bike_shop.inventory.remove(bought_bike)
        
    print ("The remaining bikes in the {0} inventory are: ".format(bike_shop.name))
    for bike in bike_shop.inventory:
        print ("{0}, which is selling for ${1}.".format(bike.model_name, bike_shop.sellingprice(bike)))
    print ("In total, {0} made ${1} of profit.".format(bike_shop.name, profit_earned))