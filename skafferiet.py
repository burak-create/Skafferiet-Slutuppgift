import sys
import skafferi_db as sk
import recept_db as re

#Creating class, getter and setter functions for supplies
class Supply:

    def __init__ (self, name, amount, unit):
        self.__name = name
        self.__amount = amount
        self.__unit = unit

    def set_supplyName(self, name):
        self.__name = name
    def set_amount(self, amount):
        self.__amount = amount
    def set_unit(self, unit):
        self.__unit = unit

    def get_supplyName(self):
        return self.__name
    def get_amount(self):
        return self.__amount
    def get_unit(self):
        return self.__unit


#Creating clas, getter and setter functions for recipes
class Recipe:
    def __init__(self, title, portions, supply, amount, unit, instructions):
        self.__title = title
        self.__portions = portions
        self.__supply = supply
        self.__amount = amount
        self.__unit = unit
        self.__instructions = instructions

    def set_title(self, title):
        self.__title = title
    def set_portions(self, portions):
        self.__portions = portions
    def set_supply(self, supply):
        self.__supply = supply
    def set_amount(self, amount):
        self.__amount = amount
    def set_unit(self, unit):
        self.__unit = unit
    def set_instructions(self, instructions):
        self.__instructions = instructions

    def get_title(self):
        return self.__title
    def get_portions(self):
        return self.__portions
    def get_supply(self):
        return self.__supply
    def get_amount(self):
        return self.__amount
    def get_unit(self):
        return self.__unit
    def get_instructions(self):
        return self.__instructions


#Create a dictionary for a mesaurement converting
def convert(val, unit_in):
    conv = {'mg':0.000001, 'cg':0.00001, 'dg': 0.0001, 'g':0.001, 'dag': 0.01,
            'hg':0.1,'kg':1, 'ml':0.001, 'cl':0.01, 'dl':0.1, 'l':1, 'hekto':0.1,
            'dal':10, 'hl':100, 'kl':1000, 'msk':0.015, 'mks':0.005}
    return val*conv[unit_in]


#A parse function which handle user input
#Checking for every item e.g supply name, amount and unit
def parse(item):
    item = item.replace(" ", "")
    ing_name = ""
    unit ="" 
    num = ""
    count = 0
    for i in range(len(item)): 
        if(item[i] >= 'a' and item[i] <= 'z') or (item[i] in nonEng): 
            ing_name += item[i]
            count +=1
        else:
            break
    start = count
    for i in range(start,len(item)): 
        if(item[i].isdigit()) or item[i] == ".":  
            num += item[i]
            count += 1
        else:
            break
    start = count
    for i in range(start,len(item)):
        if(item[i] >= 'a' and item[i] <= 'z'): 
            unit += item[i]
        else:
            break
    if unit != 'styck' and unit != 'st':
        num = str(convert(float(num), unit))
        unit = "kg"
    else:
        unit = "styck"
    return (ing_name,num,unit)


#A print function for recipes
def printRecipe(item):
    print ("Recept id:", item[0])
    print ("Recept titel:", item[1])
    itemNames = item[2].split()
    itemamounts = item[3].split()
    itemsunit = item[4].split()
    printstring = "Receptingredienser:"
    for i in range(len(itemNames)):
        printstring += " " + itemNames[i] + " " + itemamounts[i] + " " + itemsunit[i]
        if i != len(itemNames)-1:
            printstring += ","
    print(printstring)
    print ("Portion:", item[5])
    print("Instruktioner:", item[6])


#A supply adding function. It checks if item exist already or not
#If its exist adding increments them on the db file otherwise adds to the database
def add_supply(supllies):
    supplist = []
    for item in supllies:
        if not item:
            break
        ing_name,num,unit = parse(item)
        supplist.append(Supply(ing_name,num,unit))
    for i in range(len(supplist)):
        supp = sk.return_supplies()
        flag = True
        for item in supp:
            if supplist[i].get_supplyName() in item and supplist[i].get_unit() in item:
                sk.increment_supply(str(item[0]),item[1],str(float(item[2])+float(supplist[i].get_amount())),item[3])
                flag = False
        if flag: 
            sk.add_supply(supplist[i].get_supplyName(),supplist[i].get_amount(),supplist[i].get_unit())


#This function helps to insert parsed user input to database
def add_rec(rcp,all_supllies):
    for item in all_supllies:
        if not item:
            break
        ing_name,num,unit = parse(item)
        rcp.set_supply(rcp.get_supply()+ " " +  ing_name)
        rcp.set_amount(rcp.get_amount() + " " + num)
        rcp.set_unit(rcp.get_unit() + " " + unit)
    re.add_recipe(rcp.get_title(), rcp.get_supply(), rcp.get_amount(), rcp.get_unit() , rcp.get_portions(), rcp.get_instructions())


def food_advice(supplies,recipes):
    min_missing = float('inf')
    name_macth = []
    final_missing_list = []
    existing_items = []
    item_amount = []
    item_unit = []
    #Creates a array for existing items
    for item in supplies:
        existing_items.append(item[1])
        item_amount.append(item[2])
        item_unit.append(item[3])
    #Checking items in recipes
    for item in recipes:
        temp_missing = 0
        missing_list = []
        all_ing = item[2].split()
        all_ing_amount = item[3].split()
        all_ing_unit = item[4].split()
        for j in range(len(all_ing)):
            if all_ing[j] in alwaysInStock: #Checking stok for always exist items
                continue
            #Checking supplies in pantry, amount and unit of supplies.
            elif all_ing[j] in existing_items and all_ing_amount[j] < item_amount[existing_items.index(all_ing[j])] and all_ing_unit[j] == item_unit[existing_items.index(all_ing[j])]:
                continue
            else:
                temp_missing += 1
                missing_list.append([all_ing[j],all_ing_amount[j],all_ing_unit[j]]) #Creates an array for non exist items
        if min_missing > temp_missing:
            min_missing = temp_missing
            name_macth = []
            name_macth.append(item)
            final_missing_list = []
            final_missing_list.append(missing_list)
        elif min_missing == temp_missing:
            name_macth.append(item)
            final_missing_list.append(missing_list)
    for i in range(len(name_macth)):
        printRecipe(name_macth[i])
        printMissingItems = "Antal saknade föremål är " + str(min_missing) + " (saknas: "
        for item in final_missing_list[i]:
            if item[0] in existing_items and item[2] == item_unit[existing_items.index(item[0])]:
                printMissingItems += " " + item[0] + " " + str(float(item[1])-float(item_amount[existing_items.index(item[0])])) + " " + item[2]
            else:
                printMissingItems += " " + item[0] + " " + item[1] + " " + item[2]
        printMissingItems += ")"
        print (printMissingItems)
        if i!= len(name_macth)-1:
            print ("\nEtt annat förslag med samma saknade antal artiklar")


def menu(pantryMenu):
    menuChoices()
    choice = 0

    while choice !=8:

        choice = int(input("Vad vill du göra?\n: "))

        if choice == 1:
            sk.list_supply()
      
        elif choice == 2:
            print("Var vänlig skriv matvaran, mängd och enhet(kg/styc): ")
            supllies = input("Matvaran, mängden och enheten: ").lower().split(",")
            add_supply(supllies)

        elif choice == 3:
            print("Dina matvaror ligger nedan. Vänligen välj varan som du vill ta bort: ")
            sk.list_supply()
            name = input("Namnet av matvaran: ").lower()
            sk.delete_supply(name)

        elif choice == 4:
            print("Var vänlig skriv skriv recep titeln, mängden, portionen, matvaran samt instruktionen: ")
            title = input("Titeln: ").lower()
            supply = input("Matvaror (t.ex: <matvaran> <mängd> <enhet>, ...): ").lower()
            portions = input("Portionen: ").lower()
            instructions = input("Instruktionen: ").capitalize()
            all_supllies = supply.split(",")
            rcp = Recipe(title, portions, "", "", "", instructions)
            add_rec(rcp,all_supllies)
            
        elif choice == 5:
            recipes = re.return_recipe()
            for i in range(len(recipes)):
                printRecipe(recipes[i])
                if i != len(recipes)-1:
                    print("")
            print("Dina recepter ligger ovan. Vänligen skriv recepten id som du vill ta bort: ")
            name = input("Recepten som ska ta borts: ").lower()
            re.delete_recipe(name)
        
        elif choice == 6:
            print("Mat förslag; ")
            supplies = sk.return_supplies()
            recipes = re.return_recipe()
            food_advice(supplies,recipes)
            
        elif choice == 7:
            recipes = re.return_recipe()
            for i in range(len(recipes)):
                printRecipe(recipes[i])
                if i != len(recipes)-1:
                    print("")

        elif choice == 8:
            sk.exit()
            re.exit()
            sys.exit()

        else:
            print("Ogiltigt val. Vänligen försök igen!")
        
        menuChoices()

def menuChoices():
        print("""
1. Se skafferiet
2. Lägga matvaror till skafferiet
3. Ta bort matvaror
4. Lägga in recept
5. Ta bort recept
6. Få matförslag enligt minsta matvaror som saknas
7. Visa recept list
8. Avbryt
""")


if __name__ == "__main__":
    alwaysInStock = ["vatten","peppar","matolja","salt"]
    nonEng = ["ä", "å", "ö"] #Creating a list for non english characters
    menu(alwaysInStock)
