import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    Integers = ['Administrative', 'Informational', 'ProductRelated', 'OperatingSystems', 'Browser', 'Region', 'TrafficType']
    Floats = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay']
    evidence = []
    labels = []
    
    with open('filename', mode='r') as file:
        shoppingcsv = csv.reader(file)
        #skipping the first row

        header = next(shoppingcsv)
        
        #creating a dictionary of the column names and their indexes
        #this will be used to correct the data types later
        header_dict = {header.index(item): item  for item in header}
        
        Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        
        for line in shoppingcsv:
            rows = []
            #iterating over the line to define the data types
            for element in line:
                #getting element index to identify column
                element_index = line.index(element)

                # Month, an index from 0 (January) to 11 (December)
                if header_dict[element_index] = 'Month':
                    #getting month index by the index of the month name in Months list
                    month_index = Months.index(element)
                    rows.append(int(month_index))

                # VisitorType, an integer 0 (not returning) or 1 (returning)
                if header_dict[element_index] = 'VisitorType':
                    if element = 'New_Visitor':
                        rows.append(0)
                    else:
                        rows.append(1)

                # Weekend, an integer 0 (if false) or 1 (if true)
                if header_dict[element_index] = 'Weekend':
                    if element = 'FALSE':
                        rows.append(0)
                    else:
                        rows.append(1)
                # 1 if Revenue is true, and 0 otherwise.
                if header_dict[element_index] = 'Revenue'
                    if element = 'FALSE':
                            labels.append(0)
                        else:
                            labels.append(1)

                if header_dict[element_index] in Integers:
                    rows.append(int(element))

                if header_dict[element_index] in Floats:
                    rows.append(float(element))

            evidence.append(row)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
