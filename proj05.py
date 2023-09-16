###########################################################################################################################################
##
## Source Code
##
## Programming Project #5  
##
## read extrasolar planetary data from a file 
##   
## apply some fourmlas 
##
## detect if the planet has a possibility of life-supporting 
##
###########################################################################################################################################


import math

#Constants
PI = math.pi   
EARTH_MASS =  5.972E+24    # kg
EARTH_RADIUS = 6.371E+6    # meters
SOLAR_RADIUS = 6.975E+8    # radius of star in meters
AU = 1.496E+11             # distance earth to sun in meters
PARSEC_LY = 3.262
# first function is used to open a file and it repeatedly promot a file until the file opened
def open_file():
    loop="True"
    #the function will open the file but the function will print an erorr message if the file couldn't be opened and will promot for a name of the file again
    while loop!= "False":
        try:
            if loop == "True":
                promot= input("Input data to open: ")
                the_file= promot + ".csv"
                the_file= open(the_file,"r")
                
                
            elif loop == "Eror":
                promot= input("Enter a file name: ")
                the_file= promot + ".csv"
                the_file= open(the_file,"r")
            loop= "False"
            return the_file
        except FileNotFoundError:
            print("\nError: file not found.  Please try again.")
            loop ="Eror"
        
        


# a function that used to make try to make the value float but if it couldn't it would return a value of -1
def make_float(s):
    try:
        s= float(s)
        return s

    except ValueError:
        return -1
# a function that take a mass and radius of a spherical object in terms of earth and preform calulations on it to calculate and return the density 
def get_density(mass, radius):
    if mass <0 or radius <0 or radius == 0:
        return -1
    else:
        mass_interms_earth= float(mass) * EARTH_MASS
        radius__interms_earth= float(radius) * EARTH_RADIUS
        volume = ((4/3) * math.pi * (radius__interms_earth)**3)
        density= mass_interms_earth/volume
        return density
        

    
# a function that takes multiple parameters and preform calculations on it to detect if it is in the range of life support which will return True in this case and it would return False if the it is not in the range of life support
def temp_in_range(axis, star_temp, star_radius, albedo, low_bound, upp_bound):
    if axis <0 or star_temp <0 or star_radius <0 or albedo <0 or low_bound <0 or upp_bound <0 :
        return -1

    new_axis= float(axis) *AU
    new_star_radius= float(star_radius) *SOLAR_RADIUS
    planet_temp = star_temp * (new_star_radius/(2*new_axis))**(0.5)  * (1-albedo)**(0.25)
    if low_bound <= planet_temp <= upp_bound :
        return True
    else:
        return False
#a function that is used to filter the data and return the promted distance as float if it is valid 
def get_dist_range():

    loop="True"
    while loop!= "False":
        try:
            
            promot= float(input("\nEnter maximum distance from Earth (light years): "))
                
            if promot >0:
                loop = "False"
                return promot
            else:
                print("\nError: Distance needs to be greater than 0.")

        except ValueError:
            print("\nError: Distance needs to be a float." )
        
    
        

def main():


    
    filee = open_file()
    
    maximum_distance= get_dist_range() / PARSEC_LY
    low_bound= 200
    upp_bound=350
    albedo= 0.5
    max_num_of_plantes=-1
    max_num_of_stars=-1
    min_plantes= 1000
    min_stars= 1000
    density=0
    mass_total=0
    status_planet=0
    habit_planet=0
    num_planet=0
    rocky_num=0
    geaseous_num = 0
    rocky_name= ""
    gaseous_name = ""
    rocky_min =101
    geaseous_min = 101

    
    
    filee.readline()
    for line in filee:

        distance= make_float(line[114:]) 

        if distance >= maximum_distance or distance <0:
            continue
        planet_name = line[:25].strip()
        number_of_stars_in_a_system= make_float(line[50:57])
        number_of_planets = make_float(line[58:65])
        axis= make_float(line[66:77])
        planet_radius= make_float(line[78:85])
        mass_planet= make_float(line[86:96])
        star_temp= make_float(line[97:105])
        star_radius= make_float(line[106:113])

        
        if mass_planet > 0 and distance <= maximum_distance and distance >0:
            num_planet= num_planet+1
            mass_total= mass_total + mass_planet
            
            avemass= mass_total/num_planet
            
            

        if max_num_of_plantes <number_of_planets:
            max_num_of_plantes = number_of_planets

        if min_plantes > number_of_planets:
            min_plantes= number_of_planets

        if max_num_of_stars < number_of_stars_in_a_system:
            max_num_of_stars= number_of_stars_in_a_system

        if min_stars >number_of_stars_in_a_system:
            min_stars= number_of_stars_in_a_system
        density= get_density(mass_planet,planet_radius )
        if temp_in_range(axis, star_temp,star_radius,albedo,low_bound,upp_bound) == True:
            habit_planet +=1
            if (0 < planet_radius and planet_radius <1.5) or (0 < mass_planet and mass_planet <10) or (density > 2000):
                rocky_num +=1
                if rocky_min >= distance:
                    rocky_min = distance
                    rocky_name = planet_name
            else:
                geaseous_num+=1
                if geaseous_min >= distance:
                    geaseous_min = distance
                    gaseous_name = planet_name


    print("\nNumber of stars in systems with the most stars: {:d}.".format(int(max_num_of_stars)))
    print("Number of planets in systems with the most planets: {:d}.".format(int(max_num_of_plantes)))
    
    print("Average mass of the planets: {:.2f} Earth masses.".format(avemass))
    print("Number of planets in circumstellar habitable zone: {:d}.".format(habit_planet))
    if rocky_num ==0 :
        print("No rocky planet in circumstellar habitable zone.")
    else:
        print("Closest rocky planet in the circumstellar habitable zone {} is {:.2f} light years away.".format(rocky_name,rocky_min *PARSEC_LY))
    if geaseous_num == 0:
        print("No gaseous planet in circumstellar habitable zone.")
    else:
        print("Closest gaseous planet in the circumstellar habitable zone {} is {:.2f} light years away.".format(gaseous_name,geaseous_min *PARSEC_LY))
   
    
print('''Welcome to program that finds nearby exoplanets '''\
          '''in circumstellar habitable zone.''')

        
        

if __name__ == "__main__":
    main()


