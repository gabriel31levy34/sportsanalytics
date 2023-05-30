import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier


### K-NEAREST NEIGHBORS

"""
    Finds the best k value for a given model type and returns this value
"""
def find_best_k_kneighbors(trainV_x, validate_x, trainV_y, validate_y):
    max_score = 0
    best_k = 0
    
    for k in range(1, 50):
        #neigh = KNeighborsClassifier(n_neighbors=k) - Unweighted version
        neigh = KNeighborsClassifier(n_neighbors=k, weights='distance') #INCLUDING DISTANCE WEIGHTS
        neigh.fit(trainV_x, trainV_y)

        score = neigh.score(validate_x, validate_y, sample_weight=None)
        print("K: " + str(k) + "   Score: " + str(score))
        if score > max_score:
            max_score = score
            best_k = k
                
    return best_k



"""
    Using the sklearn library and specifically KNeighborsClassifier to predict
"""
def kNeighbors(data, features):
    
    # Split data into x and y and then do train, validate, test split
    x = data[features]
    y = data.loc[:, "pitch_type_name"].values
    
    # train-test split
    train_x, test_x, train_y, test_y = train_test_split(x, y,  test_size=.2, train_size=.8, shuffle=True) 
    
    # validate split
    trainV_x, validate_x, trainV_y, validate_y = train_test_split(train_x, train_y,  test_size=.2, train_size=.8, shuffle=True)
    
    # Normalize 
    scaler = StandardScaler()
    scaler.fit(trainV_x)
    trainV_x = scaler.transform(trainV_x)

    scaler.fit(validate_x)
    validate_x = scaler.transform(validate_x)
    
    
    # Find the best k
    best_k = find_best_k_kneighbors(trainV_x, validate_x, trainV_y, validate_y) 
    print(best_k)
    
    #Normalize train test data
    scaler = StandardScaler()
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)

    scaler.fit(test_x)
    test_x = scaler.transform(test_x)
    
    
    #Running with optimal k from validation
    neigh = KNeighborsClassifier(n_neighbors=best_k, weights='distance') 
    #neigh = KNeighborsClassifier(n_neighbors=best_k)
    neigh.fit(train_x, train_y)

    predictions = neigh.predict(test_x)
    
    score = neigh.score(test_x, test_y, sample_weight=None)
    
    print(score)  # 0.87241 with k=6 and weighted K-neighbors  ## 0.9379310344827586 with k=6 and reduced features
    print(best_k)

    return score



def modify_clock(data):
    for index, row in data.iterrows():
        #print(row)
        string = row['diff_clock_label']
        
        #Parse the string
        hour = string[string.index('H') - 1]
        
        minute = string[string.index('M') - 2] + string[string.index('M') - 1]
        
        decimal = int(hour) + (int(minute)/60)
        #print(hour)
        #print(minute)
       
        
        
        #row[1]['diff_clock_label'] = 1
        data.at[index, 'diff_clock_label'] = decimal
        
    return data
        
def main():
    data = pd.read_csv("full_data.csv")


    print(data) # [6943 rows x 30 columns]

    # , 'release_speed', 'movement_inches'
    data = data[ ['spin_rate', 'active_spin', 'diff_clock_label', 'pitch_type_name']] # add spin direction

    print(data)
    
    data = modify_clock(data)
    
    
    features = data.loc[:, ['spin_rate', 'active_spin', 'diff_clock_label']]

    classes = data.loc[:, "pitch_type_name"]
    
    
    features = ['spin_rate', 'active_spin', 'diff_clock_label']
    print(kNeighbors(data, features))

    
if __name__ == "__main__":
    main()


