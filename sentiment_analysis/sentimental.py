# argument parser for main
import optparse
#regex stuff for text normalization
import re
#scikit! 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
#misc
import numpy

#based on 
# https://towardsdatascience.com/sentiment-analysis-with-python-part-1-5ce197074184

parser = optparse.OptionParser()
REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")




def prep_data_from_file(fname):
    text = []
    try:
        for line in open(fname,'r'):
            REPLACE_NO_SPACE.sub("", line.lower())
            REPLACE_WITH_SPACE.sub(" ", line)
            text.append(line)
    except IOError:
        print "ERROR parsing file..."
        return []
    print "now doing regex.."
    #text = [REPLACE_NO_SPACE.sub("", line.lower()) for line in text]
    #text = [REPLACE_WITH_SPACE.sub(" ", line) for line in text]
    print "done regex.."
    
    return text

# if i could add one thing to python, it is passing arguments as references, so even immutable variables could be changed :(
def train_set(cv, X, X_test, training_data, hyperparm):
    split = [1 if i<len(training_data) / 2 else 0 for i in range(len(training_data))]
    X_train, X_val, Y_train, Y_val = train_test_split(X, split, train_size=0.75)

    max_accuracy = 0.0
    accuracy = -1.0
    if hyperparm == 0:
        for cc in numpy.arange(0.01,1.0,0.01):
            lr = LogisticRegression(C=cc)
            lr.fit(X_train, Y_train)
            accuracy = accuracy_score(Y_val, lr.predict(X_val))
            if accuracy > max_accuracy:
                hyperparm = cc
                max_accuracy = accuracy

        print ("Optimum value of C = %.2f with accuracy %s" % (hyperparm, max_accuracy))

    model = LogisticRegression(C=hyperparm)
    model.fit(X,split)

    #now on test set..
    if X_test != []:
        print ("Accuraccy on test set %s " % accuracy_score(split, model.predict(X_test)))

    return model



def main():
    
    parser.add_option('-f', '--file', action="store", dest="file", help="file name string", default='')
    parser.add_option('-d', '--dir', action="store", dest="dir", help="directory name string", default='')
    parser.add_option('-t', '--trainingset', action="store", dest="trainingset", help="training set name string", default='')
    parser.add_option('-v', '--verifyset', action="store", dest="testset", help="training set name string", default='') #look, it's 10pm. i can't think of a better keystore than -v atm..
    parser.add_option('-c', '--hyperparm', action="store",dest="c", help="c hyperparameter - 0 (default) if you want it determined", type="float", default=0)

    options, args = parser.parse_args()
    train_data = []
    test_data = []

    if options.trainingset != '':
        train_data = prep_data_from_file(options.trainingset)
        if train_data == []:
            print "ERROR Failure training.."
            exit(1)
    else:
        print "ERROR No training set specified..."
        exit(1)
    
    if options.testset != '':
        test_data = prep_data_from_file(options.testset)
        if test_data == []:
            print "ERROR Failure testing..."
            exit(1)

    cv = CountVectorizer(binary=True)
    cv.fit(train_data)
    X = cv.transform(train_data)
    X_test = []
    if test_data != []:
        X_test = cv.transform(test_data)

    trained_model = train_set(cv, X, X_test, train_data, options.c)
    
    if options.file != '':
        sampletext = prep_data_from_file(options.file)
        X_file = cv.transform(sampletext)
        print("Predicting %i positivity (0 - bad, 1 - great) of sample %s " % (trained_model.predict(X_file), options.file))
        print("Predicting probability (ie how positive) - %.5f / 10.0  " % (trained_model.predict_proba(X_file)[0][1]*10.0))







main()
