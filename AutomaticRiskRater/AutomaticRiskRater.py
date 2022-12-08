#for output
import matplotlib.pyplot as plt
# pytorch mlp for regression
from numpy import vstack
from numpy import sqrt
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torch import Tensor
from torch.nn import Linear
from torch.nn import Sigmoid
from torch.nn import Module
from torch.optim import SGD
from torch.nn import MSELoss
from torch.nn.init import xavier_uniform_

# Notes on allZonesErcot.csv
# 0 - zone east
# 1 - zone west
# 2 - zone coast
 
# dataset definition
class CSVDataset(Dataset):
    # load the dataset
    def __init__(self, path):
        # load the csv file as a dataframe
        df = read_csv(path, header=None)
        df = df.iloc[1: , :]  # skip 1st row
        # store the inputs and outputs
        self.X = df.values[:, :-1].astype('float32')
        self.y = df.values[:, -1].astype('float32')
        # ensure target has the right shape
        self.y = self.y.reshape((len(self.y), 1))
 
    # number of rows in the dataset
    def __len__(self):
        return len(self.X)
 
    # get a row at an index
    def __getitem__(self, idx):
        return [self.X[idx], self.y[idx]]
 
    # get indexes for train and test rows
    def get_splits(self, n_test=0.33):
        # determine sizes
        test_size = round(n_test * len(self.X))
        train_size = len(self.X) - test_size
        # calculate the split
        return random_split(self, [train_size, test_size])
 
# model definition
class MLP(Module):
    # define model elements
    def __init__(self, n_inputs):
        super(MLP, self).__init__()
        # input to first hidden layer
        self.hidden1 = Linear(n_inputs, 10)
        xavier_uniform_(self.hidden1.weight)
        self.act1 = Sigmoid()
        # second hidden layer
        self.hidden2 = Linear(10, 8)
        xavier_uniform_(self.hidden2.weight)
        self.act2 = Sigmoid()
        # third hidden layer and output
        self.hidden3 = Linear(8, 1)
        xavier_uniform_(self.hidden3.weight)
 
    # forward propagate input
    def forward(self, X):
        # input to first hidden layer
        X = self.hidden1(X)
        X = self.act1(X)
         # second hidden layer
        X = self.hidden2(X)
        X = self.act2(X)
        # third hidden layer and output
        X = self.hidden3(X)
        return X
 
# prepare the dataset
def prepare_data(path):
    # load the dataset
    dataset = CSVDataset(path)
    # calculate split
    train, test = dataset.get_splits()
    # prepare data loaders
    train_dl = DataLoader(train, batch_size=32, shuffle=True)
    test_dl = DataLoader(test, batch_size=1024, shuffle=False)
    return train_dl, test_dl
 
# train the model
def train_model(train_dl, model):
    # define the optimization
    criterion = MSELoss()
    optimizer = SGD(model.parameters(), lr=0.01, momentum=0.9)
    # enumerate epochs
    for epoch in range(100):
        # enumerate mini batches
        for i, (inputs, targets) in enumerate(train_dl):
            # clear the gradients
            optimizer.zero_grad()
            # compute the model output
            yhat = model(inputs)
            # calculate loss
            loss = criterion(yhat, targets)
            # credit assignment
            loss.backward()
            # update model weights
            optimizer.step()
 
# evaluate the model
def evaluate_model(test_dl, model):
    predictions, actuals = list(), list()
    for i, (inputs, targets) in enumerate(test_dl):
        # evaluate the model on the test set
        yhat = model(inputs)
        # retrieve numpy array
        yhat = yhat.detach().numpy()
        actual = targets.numpy()
        actual = actual.reshape((len(actual), 1))
        # store
        predictions.append(yhat)
        actuals.append(actual)
    predictions, actuals = vstack(predictions), vstack(actuals)
    # calculate mse
    mse = mean_squared_error(actuals, predictions)
    return mse
 
# make a class prediction for one row of data
def predict(row, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat

def grade(yhat):
    aScore = 0.063
    res = ''
    if yhat < aScore:
        res = "A"
    elif yhat < 2 * aScore:
        res = "B"
    elif yhat < 3 * aScore:
        res = "C"
    else:
        res = "D"
    print("Demand risk: ", res)
        
 
# prepare the data
#path = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/housing.csv'
print('Machine learning model learning. This may take up to 90 seconds.')
path = "allZonesErcot.csv"
train_dl, test_dl = prepare_data(path)
#print(len(train_dl.dataset), len(test_dl.dataset))
# define the network
model = MLP(3)
# train the model
train_model(train_dl, model)
# evaluate the model
mse = evaluate_model(test_dl, model)
print('MSE: %.3f, RMSE: %.3f' % (mse, sqrt(mse)))
# make a prediction (expect class=1)


#get date:
userInput = input("Input date (month, day): ")
month,day = userInput.split(',')
monthDays = (int(month) - 1)*30 
days = int(day) + monthDays
rows = [[],[],[] ]
for h in range(3):  #zone code
    for i in range(24):     # hour
        rows[h].append([h, days, i ] ) 
#output
res = [0,0,0]
variations = [[],[],[]]
for h in range(3):  #zone code
    for i in range(24):
        yhat = predict(rows[h][i], model)
        res[h] += yhat
        variations[h].append(yhat[0])


#plot
x_axis = [i for i in range(24)]
y_axis_west = variations[0]
y_axis_east = variations[1]
y_axis_coast = variations[2]

plt.plot(x_axis, y_axis_west, label = 'Zone West', color = 'red')
plt.plot(x_axis, y_axis_east, label = 'Zone East', color = 'green')
plt.plot(x_axis, y_axis_coast, label = 'Zone Coast', color = 'blue')

plt.title('Day-Ahead-Market: Load variance on '+ str(month) + "/" + str(day) + "/2022")
plt.xlabel('Hour')
plt.ylabel('Variation')
res[0] = res[0]/24
res[1] = res[1]/24
res[2] = res[2]/24

print('\nZone-West (red)')
print('Predicted Demand Variation: %.5f' % res[0])
grade(res[0])
print('\nZone-East (green)')
print('Predicted Demand Variation: %.5f' % res[1])
grade(res[1])
print('\nZone-Coast (blue)')
print('Predicted Demand Variation: %.5f' % res[2])
grade(res[2])

ymin = min( min(variations[0]), min(variations[1]), min(variations[2]) )
ymax = max( max(variations[0]) , max(variations[1]), max(variations[2]) )
plt.xlim([0, 24])
plt.ylim([ymin - 0.001, ymax + 0.001])
plt.show()
