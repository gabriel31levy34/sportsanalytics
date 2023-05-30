import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from scipy.stats import uniform
from sklearn.model_selection import train_test_split, RandomizedSearchCV as random_search
from sklearn.metrics import f1_score

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

### K-NEAREST NEIGHBORS

"""
    Finds the best k value for a given model type and returns this value
"""
def find_best_k_kneighbors(trainV_x, validate_x, trainV_y, validate_y):
    max_score = 0
    best_k = 0
    
    for k in range(1, 100):
        #neigh = KNeighborsClassifier(n_neighbors=k) - Unweighted version
        neigh = KNeighborsClassifier(n_neighbors=k, weights='distance') #INCLUDING DISTANCE WEIGHTS
        neigh.fit(trainV_x, trainV_y)

        score = neigh.score(validate_x, validate_y, sample_weight=None)
        #print("K: " + str(k) + "   Score: " + str(score))
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
    
    # Normalize validation data
    scaler = StandardScaler()
    scaler.fit(trainV_x)
    trainV_x = scaler.transform(trainV_x)
    scaler.fit(validate_x)
    validate_x = scaler.transform(validate_x)

    # Find the best k
    best_k = find_best_k_kneighbors(trainV_x, validate_x, trainV_y, validate_y) 
    
    
    #Normalize train and test data
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)
    scaler.fit(test_x)
    test_x = scaler.transform(test_x)
    
    
    #Running with optimal k from validation
    neigh = KNeighborsClassifier(n_neighbors=best_k, weights='distance') 
    neigh.fit(train_x, train_y)

    predictions = neigh.predict(test_x)
    
    # Get breakdown of predictions
    prediction_breakdown(predictions, test_y)
    
    #score = neigh.score(test_x, test_y, sample_weight=None)
    score = f1_score(test_y, predictions, average='weighted')
    print(score)
    print("F1 Score: " + str(f1_score(test_y, predictions, average='weighted')))
    print(best_k)

    return score, best_k

def decision_tree(X_train, y_train, X_test, y_test):
    
    dt_model = DecisionTreeClassifier(max_depth=10, min_samples_split=50)
    
    dt_model.fit(X_train, y_train)
    
    predictions = dt_model.predict(X_train)
    print('Training Score Accuracy {0}'.format(accuracy_score(predictions, y_train)))
    
    predictions = dt_model.predict(X_test)
    print('Test Score Accuracy {0}'.format(accuracy_score(predictions, y_test)))
    
    print(classification_report(predictions, y_test))

def SVM(x_train, y_train, x_test, y_test):
    svc = SVC(gamma = "auto")
    distributions = dict(C=uniform(loc= .5, scale = 2),
                     tol=uniform(loc=1e-5, scale=1e-3))
    print("Beginning random search")
    search = random_search(svc, distributions, random_state=0, n_iter = 100)
    params = search.fit(x_train, y_train)
    best_svm = SVC(gamma = "auto", C = params.best_params_['C'], tol = params.best_params_['tol'])
    best_svm.fit(x_train, y_train)
    predicted = best_svm.predict(x_test)
    print("Best SVM's performance on test data: ")
    print(best_svm.score(x_test,y_test))
    score = f1_score(y_test, predicted, average='weighted')
    print("F1 Score: " + str(f1_score(y_test, predicted, average='weighted')))
    
    return score, params.best_params_['C'], params.best_params_['tol']

def prediction_breakdown(predicted, y_test):
    list = ["CH", "CU","FC" , "FF", "FS","SI", "SL" ]
    #list = [0,1,2,3,4,5,6]
    
    
    dict = {}
    for item in list:
        dict[item] = 0
    
    for i in range(len(predicted)):
        if predicted[i] != y_test[i]:
            dict[y_test[i]] += 1
    
    total_missed = 0
    for key in dict:
        total_missed += dict[key]
        
    for key in dict:
        dict[key] /= total_missed
        
        
    # print(dict)
    
    # K-neighbors
    # {'CH': 0.11971830985915492, 'CU': 0.1267605633802817, 'FC': 0.28169014084507044, 'FF': 0.056338028169014086, 'FS': 0.09154929577464789, 'SI': 0.176056338028169, 'SL': 0.14788732394366197}
    
    # {0: 0.10144927536231885, 1: 0.1956521739130435, 2: 0.21739130434782608, 3: 0.06521739130434782, 4: 0.07246376811594203, 5: 0.15942028985507245, 6: 0.18840579710144928}
    
def modify_clock(data):
    for index, row in data.iterrows():
        string = row['diff_clock_label']
        
        #Parse the string
        hour = string[string.index('H') - 1]
        
        minute = string[string.index('M') - 2] + string[string.index('M') - 1]
        
        decimal = int(hour) + (int(minute)/60)
        data.at[index, 'diff_clock_label'] = decimal
        
    return data

def get_y(data, svm):
    if svm:
        le = LabelEncoder()
        le.fit(["CH", "CU","FC" , "FF", "FS","SI", "SL" ])
        y = le.transform(data["pitch_type_name"])
    else:
        y = data["pitch_type_name"]
    
    return y

        
def main():
    data = pd.read_csv("../data/full_data.csv")

    data = data[ ['spin_rate', 'active_spin', 'diff_clock_label', 'release_speed', 'pitcher_break_x', 'pitcher_break_z', 'pitch_type_name']]

    data = modify_clock(data)
    
    features = data[['spin_rate', 'active_spin', 'diff_clock_label', 'release_speed', 'pitcher_break_x', 'pitcher_break_z']]
    
    knn = True
    tree = False
    svm = False
    #format outcome
    if knn:
        classes = data["pitch_type_name"]
    else:
        classes = get_y(data, svm)
    
    # train-test split
    train_x, test_x, train_y, test_y = train_test_split(features, classes,  test_size=.2, train_size=.8, shuffle=True)
    
    #Normalize train test data
    scaler = StandardScaler()
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)
    
    #Normalize test data
    scaler.fit(test_x)
    test_x = scaler.transform(test_x)
    
    
    if knn:
        columns = ['spin_rate', 'active_spin', 'diff_clock_label', 'release_speed', 'pitcher_break_x', 'pitcher_break_z']
        kNeighbors(data, columns)
    elif tree:
        decision_tree(train_x, train_y, test_x, test_y)
    else:
        SVM(train_x, train_y, test_x, test_y)
       

if __name__=='__main__':
    main()