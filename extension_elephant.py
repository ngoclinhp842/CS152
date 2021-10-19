'''Michelle Phan
CS152B
Lab 5
Oct 6, 2021
'''

'''simulate Elephant Population Management:
calculate the population size, number of calves, juveniles, 
adult males, adults female, seniors, and culled elephants.
'''

'''How to run: 
type 'python3 elephant.py <the start number of Darted percent>
<the end number of Darted percent' in the command line.
for example: 'python3 elephant.py 0 1'
'''

import matplotlib.plot as plt
'''
how to install matplotlib:
For Mac: type 'pip3 install matplotlib'
on the terminal

/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9 -m pip install --upgrade pip
'''

# import modules
import random as rand
import sys
import stats
import numpy as np
# import elephant

#store index number of every parameter to variables
IDXCalvingInterval = 0 
IDXjuvAge = 1
IDXmaxAge = 2
IDXprobCalfSurvival = 3
IDXprobAdultSurvival = 4
TDXprobSeniorSurvival = 5
IDXCapacity = 6
IDXNumYears = 7

#store the index of individual elephant list
IDXGender = 0
IDXAge = 1
IDXMonthsPregnant = 2
IDXMonthsContraceptiveRemaining = 3

#store the index of results list
IDXPopSize = 0
IDXnumCalves = 1
IDXnumJuv = 2
IDXnumAdMale = 3
IDXnumAdFemale = 4
IDXSeniors = 5
IDXnumCulled = 6

def main(argv):
    if len(argv) < 3:
        print('''Please enter the probability of darting in the command line!''')
        return

    
    #assign the probability of darting from the command line parameter
    start_probDart = float(argv[1])
    end_probDart = float(argv[2])

    ''' assign each parameter from the table above 
    to a variable with an informative name'''
    calvingInterval = 3.1
    juvAge = 12
    maxAge = 60
    probCalfSurvival = 0.85
    probAdultSurvival = 0.996
    probSeniorSurvival = 0.20
    capacity = 8000
    numYears = 20

    #calculate step size 
    step = (end_probDart - start_probDart)
    step = step/10
    # create a list of percent with given start and end points
    percentDarted = np.arange(start_probDart, end_probDart, step)

    # make the parameter list out of the variables
    parameters = [calvingInterval, juvAge,
                    maxAge,probCalfSurvival, probAdultSurvival,
                    probSeniorSurvival,capacity,numYears]

    #store population size and percent Darted
    compareDartedPopSize = []

    for i in range(len(percentDarted)):
        percent = percentDarted[i]
        results = popSize_percentDarted(parameters,percent)
        compareDartedPopSize.append(results)

    #calculate the opimal percent darted
    opimalPercentDarted = []
    for item in compareDartedPopSize:
        percent = item[0]
        popSize = item[1]
        
        if popSize > 6500 and popSize < 8000:
            opimalPercentDarted.append(percent)

    print('Compare Darted and Population Size', compareDartedPopSize)
    print('Opimal Percent Darted', opimalPercentDarted)

    #plot the population size with the percent darted
    plt.plot(percentDarted,resultsPopSize, ls = 'r-', c = 'blue')
    plt.xlabel('Population Size')
    plt.ylabel('Percent of Darted elephants')
    plt.title('''The Population Size for Percent of Darted elephants
                    from 1 to 100 with a step of 1.''')
    plt.show()

    return

# create and return a new elephant
def newElephant( parameters, age ):
    elephant = [0,0,0,0]
        
    elephant[IDXGender] = rand.choice("fm")

    elephant[IDXAge] = age 

    # If the elephant is female and of breeding age
    if all([elephant[IDXGender] == 'f'
        , age > parameters[IDXjuvAge] 
        , age < parameters[IDXmaxAge]]):
            
        # test if the elephant is pregnant
        if rand.random() < 1.0 / parameters[IDXCalvingInterval]:
            elephant[IDXMonthsPregnant] = rand.randint(1,22)

    # return a new elephant
    return elephant

# create and initial population
def initPopulation(parameters):
    init_pop = []

    # loop for the number of elephants to create 
    for i in range(parameters[IDXCapacity]):
        # randomly choose age from range 1 to max Age
        age = rand.randint(1, parameters[IDXmaxAge])

        # append a new elephant list
        init_pop.append(newElephant(parameters, age))

    ''' return an intital population whose size equals 
    the Carrying Capacity. Each individual's age is 
    in range 1 to maximum Age'''
    return init_pop

# increase the age of each elephant by 1
def incrementAge(pop):
    new_pop = []
    for e in pop:

        # modify the second element of each elephant list. 
        e[IDXAge] += 1
        new_pop.append(e)
    
    # a new population which is 1 year older
    return new_pop

# calculate elephants survival
def calcSurvival(parameters, pop):
    new_population = []

    for e in pop:
        #check if the elephant is more than 60 years old
        if e[IDXAge] > 60:
            # check if the elephant survice
            if rand.random() < parameters[TDXprobSeniorSurvival]:
                new_population.append(e)

        #check if the elephant's age is in rang [2, 60]
        if e[IDXAge] >= 2 and e[IDXAge] <= 60:
            # check if the elephant survice
            if rand.random() < parameters[IDXprobAdultSurvival]:
                new_population.append(e)

        # check if the elephant is 1 years old
        if e[IDXAge] == 1:
            # check if the elephant survice
            if rand.random() < parameters[IDXprobCalfSurvival]:
                new_population.append(e)

    # return the population including only survial members
    return new_population

# randomly decide which elephant is darted
def dartElephants(parameters, pop, percentDarted):
    juvAge = parameters[IDXjuvAge]
    maxAge = parameters[IDXmaxAge]

    for e in pop:
        # check if the elephant is female and in breeding age
        if e[IDXGender] == 'f' and e[IDXAge] > juvAge and e[IDXAge] < maxAge:
            # randomly decide whether the elephant is darted
            if rand.random() < percentDarted:
                # if the elephant is darted, the pregnant month is 0 
                e[IDXMonthsPregnant] = 0

                # the contraceptive month remained is 22 
                e[IDXMonthsContraceptiveRemaining] = 22

    # return the population after being darted
    return pop

# check if the population size exceeds the carryingCapacity
# if yes, randomly reduce the population size
def cullElephants(parameters , pop):
    carryingCapacity = parameters[IDXCapacity]

    # calculate the number of elephant culled
    numCulled = len(pop) - carryingCapacity

    # if numbers of culled elephant is larger than 0
    if numCulled > 0:
        # randomly shuffle the population
        rand.shuffle(pop)
    else: 
        # else, set the number of elephant culled to 0
        numCulled = 0

    # Only include number of elephant within the Capacity
    newPopulation = pop[:carryingCapacity]

    # return the new population and number of culled elephants
    return (newPopulation, numCulled)

'''determine whether the population should be darted or culled 
and call the appropriate function.'''
def controlPopulation( parameters, population, percentDarted ):
    #store percent darted 

    # if the parameter value for "percent darted" is zero:
    if percentDarted == 0:
        # call cullElephants, storing the return values in a two variables 
        (newpop, numCulled) = cullElephants( parameters, population)
    else:
        # call dartElephants and store the result in a variable named newpop
        newpop = dartElephants(parameters, population, percentDarted)

        # set a variable named numCulled to zero
        numCulled = 0

    # return the new population and number of culled elephants
    return (newpop, numCulled)

# moves the simulation forward by one month.
def simulateMonth(parameters, population):
    calvingInterval = parameters[IDXCalvingInterval]
    juvAge = parameters[IDXjuvAge]
    maxAge = parameters[IDXmaxAge]

    # calculate the pregnant probability
    pregChance = 1.0 / (calvingInterval * 12 - 22)

    for e in population:
        # assign to gender the IDXGender item in e
        gender = e[IDXGender]

        # assign to age the IDXAge item in e
        age = e[IDXAge]

        # assign to monthsPregnant the IDXMonthsPregnant item in e
        monthsPregnant = e[IDXMonthsPregnant]

        ''' assign to monthsContraceptive 
        the IDXMonthsContraceptiveRemaining item in e '''
        monthsContraceptive = e[IDXMonthsContraceptiveRemaining]


        #if gender is female and the elephant is an adult
        if gender == 'f' and age > juvAge and age < maxAge:
            # if monthsContraceptive is greater than zero
            if monthsContraceptive > 0:
                '''decrement the months of contraceptive left 
                (IDXMonthsContraceptiveRemaining element of e) by one'''
                e[IDXMonthsContraceptiveRemaining] -= 1
            # else if monthsPregnant is greater than zero
            elif monthsPregnant > 0:
                # if monthsPregnant is greater than or equal to 22
                if monthsPregnant >= 22:
                    '''create a new elephant of age 1 
                    and append it to the population list'''
                    population.append(newElephant(parameters, 1))

                    '''reset the months pregnant 
                    (the IDXMonthsPregnant element of e) to zero'''
                    e[IDXMonthsPregnant] = 0

                else:
                    '''increment the months pregnant 
                    (IDXMonthsPregnant element of e) by 1'''
                    e[IDXMonthsPregnant] += 1
            else:
                # if the elephant becomes pregnant
                if rand.random() < pregChance:
                    # set months pregnant (IDXMonthsPregnant element of e) to 1
                    e[IDXMonthsPregnant] = 1
    
    # return the population after a month
    return population

# create the population after a year
def simulateYear(parameters, population):

    # simulate the survival population
    pop = calcSurvival( parameters, population )

    # increase the age of the population by 1
    pop = incrementAge (pop)

    # simulate the population over 12 months
    for num in range(12):
        pop = simulateMonth(parameters, pop)

    # return the population after a year
    return pop

'''calculates how many calves, juveniles, 
adult males, adult females, and seniors are in the population. '''
def calcResults(parameters, population, numCulled):
    '''Initialize variables to hold the number of calves, juveniles, 
    adult males, adult females, and seniors.'''
    numCalves = 0
    numJuv = 0
    numAdMale = 0
    numAdFemale = 0
    numSeniors = 0

    juvAge = parameters[IDXjuvAge]
    maxAge = parameters[IDXmaxAge]

    for e in population:
        # check if e is a calf
        if e[IDXAge] == 1:
            # increase the number of calves by 1
            numCalves += 1
        
        # check if e is a juvenile
        if e[IDXAge] > 1 and e[IDXAge] <= juvAge:
            #increase the number of juveniles by 1
            numJuv += 1

        #check if e is a senior:
        if e[IDXAge] > 60:
            # increase the number of seniors by 1
            numSeniors += 1

        #check if e is an adult male:
        if e[IDXGender] == 'm' and e[IDXAge] > juvAge and e[IDXAge] <= maxAge:
            # increase the number of adult male by 1
            numAdMale += 1

        #check if e is an adult female:
        if e[IDXGender] == 'f' and e[IDXAge] > juvAge and e[IDXAge] <= maxAge:
            # increase the number of adult female by 1
            numAdFemale += 1

    populationSize = len(population)
        
    # return num_pop list include results values
    num_pop = [populationSize, numCalves, numJuv, numAdMale, 
    numAdFemale, numSeniors, numCulled]

    return num_pop

def runSimulation(parameters, percentDarted):
    '''run simulation for N years.
    Check if the population is out of control, 
    if not, return the results'''
    popsize = parameters[IDXCapacity]

    # init the population
    population = initPopulation( parameters )
    [population,numCulled] = controlPopulation( parameters, 
    population, percentDarted)

    # run the simulation for N years, storing the results
    results = []
    for i in range(parameters[IDXNumYears]):
        population = simulateYear( parameters, population )
        
        [population,numCulled] = controlPopulation( parameters, 
                                    population, percentDarted )
        
        results.append(calcResults( parameters, population,numCulled))
    
    return results

def test():
    # assign each parameter from the table above to a variable with an informative name
    calvingInterval = 3.1
    percentDarted = 0.0
    juvAge = 12
    maxAge = 60
    probCalfSurvival = 0.85
    probAdultSurvival = 0.996
    probSeniorSurvival = 0.20
    capacity = 7000
    numYears = 200

    # make the parameter list out of the variables
    parameters = [calvingInterval, percentDarted,juvAge,
                    maxAge,probCalfSurvival, probAdultSurvival,
                    probSeniorSurvival,capacity,numYears]
    
    # print the parameter list
    # print(parameters)

    # test_initPopulation(parameters) with  capacty 20
    def test_initPopulation(parameters):
        parameters[IDXCapacity] = 20

        init_pop = initPopulation(parameters)

        print(init_pop)
        return 

    #test incrementAge()
    def test_incrementAge(parameters):
        parameters[IDXCapacity] = 20
        pop = initPopulation(parameters)

        print('Initial Population:',pop)
        new_pop = incrementAge(pop)
        print('New Population:',new_pop)

        return 

        
    test_incrementAge(parameters)

# if __name__ == "__main__":
#     test()

def rearrangeData(results, # input list to rearrange
                    index): # number of row or index to create column
    '''Rearrange data from the results into into 
    a list which stores the columns value.'''

    #create lists to store each value 
    results_column = []

    #append value to each list 
    for i in range(len(results)):
        results_column.append(results[i][index])
    
    return results_column

'''calculate the population size with 
a specific percent Darted'''
'''return a list of results, in which
each item is a list of [percent Darted, the average pop size]'''
def popSize_percentDarted(parameters, percentDarted):

    #calculate the results 
    results = runSimulation(parameters, percentDarted)
        
    #create lists to store each value 
    total_pop = rearrangeData(results, IDXPopSize)
    
    #calculate average values of each factors 
    avg_pop = stats.mean(total_pop) 

    return [percentDarted,avg_pop]

if __name__ == "__main__":
    main(sys.argv)
