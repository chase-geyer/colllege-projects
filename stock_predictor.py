"""
Stock market prediction using Markov chains.

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module3 as stocks
import random

### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
    #Set it up as a dictionary with a tuple keying to the dictionary of it's next number
    count = 0
    chain = {}
    keys = []
    #having the bounds to make sure I don't iterate out
    while count < len(data) - order:
        #Create a tuple of sufficient order
        key = ()
        key_count = 0
        #making sure I get every subset of keys possible
        while len(key) < order:
            #print(key)
            key = key + (data[count + key_count],)
            #print(key)
            key_count += 1
        #the next state that I need to account for in this case
        next_state = data[count + order]
        #print(key)
        if key not in keys:
            keys.append(key)
        if chain.get(key) != None:
            #print(chain[key])
            if chain[key].get(next_state) != None:
                #print(chain[key][next_state])
                chain[key][next_state] = chain[key].get(next_state) + 1
            else:
                #print(chain[key][next_state], chain[key])
                chain[key][next_state] = 1
        else:
            chain[key] = {next_state: 1} 
        count+= 1
    #print(chain)
    #print(keys)
    for key in keys:
        total = sum(chain[key].values())
        #print(key, total, chain[key], chain[key].values())
        for state in chain[key]:
            chain[key][state] = chain[key][state] / total
    #print(chain)
    return chain

#markov_chain([1,1,3,2,1,3,1, 1, 3, 1, 0], 1)
### Predict

def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    count = 0
    next_states = []
    last_clone = list(last)
    #look for where last is key, make weighted choice based on value of key in dictionary
    while count < num:
        #print(model.get(tuple(last_clone)))
        if model.get(tuple(last_clone)) == None:
            random_number = random.random()
            if random_number < 0.25:
                winner = 0
            elif  0.25 <= random_number < 0.5:
                winner = 1
            elif 0.5 <= random_number < 0.75:
                winner = 2
            else:
                winner = 3
        else:       
            choices = model[tuple(last_clone)]
            #print(choices)
            keys = []
            #creating list of keys
            for key in choices:
                keys.append(key)
            #print(keys)
            #setting probability interval to first choice (helps account for
            #default choice of key --> 1
            prob_inters = [[0, choices[keys[0]]]]
            int_indx = 1
            #creating intervals to match probability of each choice happening
            #(essentially an experimental design for randomness)
            while int_indx < len(keys):
                push_constant = prob_inters[int_indx -1][0]
                start_inter = choices[keys[int_indx-1]] + push_constant
                end_inter = choices[keys[int_indx-1]] + choices[keys[int_indx]] + push_constant
                prob_inters.append([start_inter, end_inter])
                #print(int_indx)
                int_indx += 1
                #making sure I keep track of which interval is associated to which "bin"
            interval_association = {}
            dict_count = 0
            while dict_count < len(keys):
                interval_association[tuple(prob_inters[dict_count])] = keys[dict_count]
                dict_count += 1
            random_number = random.random()
            winner = 0
            for interval in prob_inters:
                if interval[0] <= random_number < interval[1]:
                    winner = interval_association[tuple(interval)]
                    break
        last_clone.pop(0)
        last_clone.append(winner)
        next_states.append(winner)
        #print(winner, last_clone)
        #print(count)
        count +=1
    #print(next_states)
    return next_states

#predict({(0,): {1: 1}, (1,): {0: 1}}, [0], 3)
### Error

def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    count = 0
    total_squared_error = 0
    while count < len(result):
        total_squared_error += (result[count] - expected[count])**2
        count += 1
        #print(count)
    #print("resolved")
    #print(total_squared_error)
    return total_squared_error/len(result)
#print(mse([1,2,3],[2,3,4]))
### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    count = 0
    total_mse = 0
    while count < trials:
        chain = markov_chain(train, order)
        predicted = predict(chain, test, future)
        total_mse += mse(actual, predicted)
        count+=1
        if count == trials:
            break
        #print(count)
    #print("resolved")
    return total_mse/trials


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

# You might want to comment out the call to run while you are
# developing your code.  Uncomment it when you are ready to run your
# code on the provided data.

#run()
