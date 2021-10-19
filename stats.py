'''Michelle Phan
Sep 22, 2021
CS152B
Project 3
Fall 2020'''

'''A function library: sum(), mean(), min()
max(), variance()'''

'''how to run:
type 'python3 stats.py' on the terminal'''

def sum(data):
    '''caculate the sum of a list
    parameter: a data list
    return the sum of the list'''

    sum = 0.0
    for i in range(len(data)):
        sum += data[i]
    return sum

def test():
    '''test the function sum ( )'''
    numbers = []
    sum_numbers = sum(numbers)
    # print(sum_numbers)

def mean(data):
    '''calculate the average of 
    a list'''
    sum_data = sum(data)
    mean = sum_data / len(data)
    return mean

def min(data):
    '''find the min of a list'''
    min = data[0]
    for i in range(len(data)):
        if min > data[i]:
            min = data[i]
    return min

def max(data):
    '''find the max of a list'''
    max = data[0]
    for i in range(len(data)):
        if max < data[i]:
            max = data[i]
    return max

def variance(data):
    '''calculate the variance of a list'''
    '''formula of variance: 
    https://www.investopedia.com/terms/v/variance.asp'''

    my_mean = mean(data)
    var_list = []

    '''calculate the sum of the difference 
    between each item and the mean'''
    for i in range(len(data)):
        var_list.append(pow(data[i] - my_mean, 2))
    total = sum(var_list)
    
    var = total / (len(data) - 1)

    return var

if __name__ == "__main__":
    test()
    mean()
    sum()
    variance()
    min()
    max()

