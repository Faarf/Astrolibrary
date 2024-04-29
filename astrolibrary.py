import requests
import sys
import re
from prettytable import PrettyTable
from PIL import Image


def main():
    print()
    print("★⋆.˚⋆⭒˚｡⋆ Welcome to the Astrolibrary! ★⋆.˚⋆⭒˚｡⋆\n")
    print("In the Astrolibrary, you can search for a star to find relevant information about it.")
    print("You can compare between stars, to see how big or small etc. they are relative to eachother.")
    print("We also have our very own planetarium, where you can replace our sun from the solar system\nto a star of your choice to see the size difference, to scale!\n")

    while True:
        options = ["s", "c", "p", "x"]
        print("\nType 's' to search for a star.\nType 'c' to compare between stars.\nType 'p' to enter the planetarium.\nType 'x' to exit the library.")
        choice = input("")

        # SEARCH FOR A STAR
        if "s" in choice:
            s = ""
            while not s == "n":
                star = input("Enter a star: ").strip().lower().replace(" ", "+")
                
                info = starinfo(star)
                
                # Printing table for the star
                try:   
                    star_t = PrettyTable(["Name", "Distance (LY)", "Size (x Suns)", "Startype", "Star System", "Mass (x Suns)", "Visual Magnitude"])
                    star_t.add_row([*info])
                    print()
                    print(star_t)
                except ValueError:
                    print()
                    print(*info)
                while True:
                    s = input("\nDo you wish to try another star? (y/n) ").lower()
                    if not s == "y" and not s == "n":
                        print(f"You typed '{s}', only 'y' or 'n' is accepted.")
                    else:
                        break
                
        # COMPARE BETWEEN STARS
        if "c" in choice:
            cm = ""
            while not cm == "n":
                while True:
                    first = input("Enter the first star: ").strip().lower().replace(" ", "+")
                    star1 = starinfo(first)
                    if "Star" in star1:
                        print(*star1)
                    else:
                        break
                
                while True:
                    second = input("Enter the second star: ").strip().lower().replace(" ", "+")
                    star2 = starinfo(second)
                    if "Star" in star2:
                        print(*star2)
                    elif star1[0] == star2[0]:
                        print("You can't compare the same star.")
                    else:
                        break
                
                # Printing tables for star comparisons
                compare_t = PrettyTable(["Name", "Distance (LY)", "Size (x Suns)", "Startype", "Star System", "Mass (x Suns)", "Visual Magnitude"])
                compare_t.add_row([*star1])
                compare_t.add_row([*star2])
                compare_t.align = "c"
                print()
                print(compare_t)
            
                # Assigning relevant variables to compare between
                fstar = [*star1]
                sstar = [*star2]
                dis1, siz1, mas1 = fstar[1], fstar[2], fstar[5]
                dis2, siz2, mas2 = sstar[1], sstar[2], sstar[5]
                
                # Comparing distances and printing explanatory sentences below compare-table
                if is_bigger(dis1, dis2) == True:
                    # If a star is compared to the sun specifically (ZDE)
                    try:
                        n = dis1 / dis2
                    except ZeroDivisionError:
                        n = dis1
                    print(f"{fstar[0]} is {n:.2f} times farther away than {sstar[0]}.")
                    
                elif is_bigger(dis1, dis2) == False:
                    try:              
                        n = dis2 / dis1
                    except ZeroDivisionError:
                        n = dis2
                    print(f"{sstar[0]} is {n:.2f} times farther away than {fstar[0]}.")

                elif is_bigger(dis1, dis2) == "0":
                    print(f"{fstar[0]} and {sstar[0]} are equally far away.")

                elif is_bigger(dis1, dis2) == "x":
                    print("-Not enough information to compare distances-")
                
                # Comparing sizes
                if is_bigger(siz1, siz2) == True:
                    n1 = siz1 / siz2
                    print(f"{fstar[0]} is {n1:.2f} times bigger than {sstar[0]}.")

                elif is_bigger(siz1, siz2) == False:
                    n1 = siz2 / siz1
                    print(f"{sstar[0]} is {n1:.2f} times bigger than {fstar[0]}.")

                elif is_bigger(siz1, siz2) == "0":
                    print(f"{fstar[0]} and {sstar[0]} are equally large.")

                elif is_bigger(siz1, siz2) == "x":
                    print("-Not enough information to compare sizes-")

                # Comparing mass
                if is_bigger(mas1, mas2) == True:
                    n2 = mas1 / mas2
                    print(f"{fstar[0]} is {n2:.2f} times more massive than {sstar[0]}.")

                elif is_bigger(mas1, mas2) == False:
                    n2 = mas2 / mas1
                    print(f"{sstar[0]} is {n2:.2f} times more massive than {fstar[0]}.")

                elif is_bigger(mas1, mas2) == "0":
                    print(f"{fstar[0]} and {sstar[0]} are equally as massive.")

                elif is_bigger(mas1, mas2) == "x":
                    print("-Not enough information to compare mass-")

                while True:
                    cm = input("\nDo you wish to try another star? (y/n) ").lower()
                    if not cm == "y" and not cm == "n":
                        print(f"You typed '{cm}', only 'y' or 'n' is accepted.")
                    else:
                        break
                    
        # PLANETARIUM
        if "p" in choice:
            print("\nWelcome to the Planetarium!")
            print("⋆｡ﾟ🪐｡⋆｡ ﾟ☾ ﾟ｡⋆")
            print("In here you can get a better perspective on just how big other stars can be.")
            print("You can choose a star that should replace our own sun in the solar system and see the size difference.")

            c = ""
            while not c == "n":
                while True:
                    pstar = input("Enter a star to replace our sun: ").strip().lower().replace(" ", "+")

                    pinfo = starinfo(pstar)
                    if "Star" in pinfo:
                        print(*pinfo)
                    elif pinfo[2] == "?":
                        print(f"-Cannot find the size of {pinfo[0]}-") 
                    else:
                        break
                    
                pstar_size = pinfo[2]

                if pstar_size < 231:

                    # PLANETARIUM 1

                    star = Image.open("star.png")
                    imstar = star.copy()

                    planetarium1 = Image.open("planetarium1.png")
                    plan1 = planetarium1.copy()

                    # The diameter of Earth's orbit is approx. 299,200,000 km
                    # The size of the star's img to match the orbit is more or less 1000, 1000
                    # 1 pixel is therefore 299,200.0 km
                    plan1_pixel_size = 299200.0

                    star_size = diameter(pstar_size)
                    new_size = round(star_size, 1) / round(plan1_pixel_size, 1)
                    final_size = (round(new_size), round(new_size))

                    new_imstar = imstar.resize(final_size)
                    
                    
                    plan1.paste(new_imstar, imsize(new_size), new_imstar)
                    plan1.show()

                    print()
                    print(f"{pinfo[0].title()} has been successfully replaced!")
                    
                    while True:
                        c = input("\nDo you wish to try another star? (y/n) ").lower()
                        if not c == "y" and not c == "n":
                            print(f"You typed '{c}', only 'y' or 'n' is accepted.")
                        else:
                            break
        

                elif pstar_size >= 231 and pstar_size <= 1300:
                
                    # PLANETARIUM 2
                    
                    star = Image.open("star.png")
                    imstar = star.copy()

                    planetarium2 = Image.open("planetarium2.png")
                    plan2 = planetarium2.copy()

                    # The diameter of Jupiter's orbit is approx. 1,555,840,000 km
                    # The size of the star's img to match the orbit is more or less 925, 925
                    # 1 pixel is therefore 1,681,989.189 km
                    plan2_pixel_size = 1681989.189
                    
                    star_size = diameter(pstar_size)
                    new_size = round(star_size, 1) / round(plan2_pixel_size, 1)
                    final_size = (round(new_size), round(new_size))

                    new_imstar = imstar.resize(final_size)
                    
                    
                    plan2.paste(new_imstar, imsize(new_size), new_imstar)
                    plan2.show()
                    
                    print()
                    print(f"{pinfo[0].title()} has been successfully replaced!")

                    while True:
                        c = input("\nDo you wish to try another star? (y/n) ").lower()
                        if not c == "y" and not c == "n":
                            print(f"You typed '{c}', only 'y' or 'n' is accepted.")
                        else:
                            break
    

                elif pstar_size > 1300:
                
                    # PLANETARIUM 3
                
                    star = Image.open("star.png")
                    imstar = star.copy()

                    planetarium3 = Image.open("planetarium3.png")
                    plan3 = planetarium3.copy()

                    # The diameter of Saturn's orbit is approx. 2,869,328,000 km
                    # The size of the star's img to match the orbit is more or less 363, 363
                    # 1 pixel is therefore 7,904,484.848 km
                    plan3_pixel_size = 7904484.848
                    
                    star_size = diameter(pstar_size)
                    new_size = round(star_size, 1) / round(plan3_pixel_size, 1)
                    final_size = (round(new_size), round(new_size))

                    new_imstar = imstar.resize(final_size)
                    
                    plan3.paste(new_imstar, imsize(new_size), new_imstar)
                    plan3.show()

                    print()
                    print(f"{pinfo[0].title()} has been successfully replaced!")

                    while True:
                        c = input("\nDo you wish to try another star? (y/n) ").lower()
                        if not c == "y" and not c == "n":
                            print(f"You typed '{c}', only 'y' or 'n' is accepted.")
                        else:
                            break

        if "x" in choice:
            sys.exit("✮⋆˙ Thanks for visiting the Astrolibrary! ✮⋆˙")

        if not choice in options:
            print(f"You typed '{choice}', only 's', 'c', 'p' or 'x' is accepted.")
        
def starinfo(s):

    names = distance = size = startype = starsystem = mass = apparent = "?"

    response = requests.get(f"http://www.stellar-database.com/Scripts/search_star.exe?Name={s}")

    web = response.text

    if "No star name matching" in web or "found with a name matching" in web:
        return ["Star", "not", "found", "in", "the", "database."]
    
    if name := re.search(r"Proper names:</B> ([1-9a-zA-Z ]+)", web):
        names = name.group(1)

    if disfromsol := re.search(r"Distance from Sol:</B> (\d+(?:.\d+)?)", web):
        _ = disfromsol.group(1)
        distance = round(float(_), 1)

    if diameter := re.search(r"Diameter:</B> (\d+(?:.\d+)?) x Sol", web):
        _ = diameter.group(1)
        size = round(float(_), 1)

    if sclass := re.search(r"Spectral class:</B> (\w\d)", web):
        startype = sclass.group(1)
    

    if arity := re.search(r"Arity:</B> ([1-9a-zA-Z, ]*)", web):
        starsystem = arity.group(1)
        if "singular" in starsystem:
            starsystem = "Singular"
        if "binary" in starsystem:
            starsystem = "Binary"
        if "trinary" in starsystem:
            starsystem = "Triple"
        if "quarternary" in starsystem:
            starsystem = "Quadruple"
        if "quinary" in starsystem:
            starsystem = "Quintuple"
        if "hexary" in starsystem:
            starsystem = "Sextuple"

    if solmass := re.search(r"Mass:</B> (\d+(?:.\d+)?) x Sol", web):
        _ = solmass.group(1)
        mass = round(float(_), 1)

    if vismag := re.search(r"Apparent visual magnitude:</B> ((?:\+|-)\d+(?:.\d+)?)", web):
        apparent = vismag.group(1)
        
    return [names, distance, size, startype, starsystem, mass, apparent]


def is_bigger(x, y):
    # Checking if the value is known or not
    if x == "?" or y == "?":
        return "x" 
    # If the first value is higher than the second
    elif float(x) > float(y):
        return True
    # If the second value is higher than the first
    elif float(y) > float(x):
        return False
    # If its the same
    elif float(x) == float(y):
        return "0"

def diameter(n):
    return round(n * 1391400, 3)



def imsize(n):
    # Because all the solar system images are 1080x1080, the center is 540x540
    size = 540 - (n / 2)
    size1 = round(int(size))
    return (size1, size1)



if __name__ in "__main__":
    main()