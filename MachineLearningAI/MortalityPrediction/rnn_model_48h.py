import os
import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch.optim as optim
import matplotlib.pyplot as plt
from utils import *
from sklearn.metrics import roc_curve, auc, accuracy_score


torch.manual_seed(0)
if torch.cuda.is_available():
	torch.cuda.manual_seed(0)

# Set a correct path to the preprocessed data files 
PATH_TRAIN_SEQS = "../data/48hr_mortality/processed/mortality.seqs.train"
PATH_TRAIN_LABELS = "../data/48hr_mortality/processed/mortality.labels.train"
PATH_VALID_SEQS = "../data/48hr_mortality/processed/mortality.seqs.validation"
PATH_VALID_LABELS = "../data/48hr_mortality/processed/mortality.labels.validation"
PATH_TEST_SEQS = "../data/48hr_mortality/processed/mortality.seqs.test"
PATH_TEST_LABELS = "../data/48hr_mortality/processed/mortality.labels.test"
PATH_TEST_IDS = "../data/48hr_mortality/processed/mortality.ids.test"
PATH_OUTPUT = "../output48hr/mortality/"

if not os.path.exists('../output48hr/mortality'):
    os.mkdir('../output48hr')
    os.mkdir('../output48hr/mortality')    
else:    
    pass



n_epoch = 10
n_batch = 1
USE_CUDA = False  # Set 'True' if GPU is used
n_worker = 0
class_names = ['Alive', 'Dead']

# Data loading
print('===> Loading entire datasets')
train_seqs = pickle.load(open(PATH_TRAIN_SEQS, 'rb'))
train_labels = pickle.load(open(PATH_TRAIN_LABELS, 'rb'))
valid_seqs = pickle.load(open(PATH_VALID_SEQS, 'rb'))
valid_labels = pickle.load(open(PATH_VALID_LABELS, 'rb'))
test_seqs = pickle.load(open(PATH_TEST_SEQS, 'rb'))
test_labels = pickle.load(open(PATH_TEST_LABELS, 'rb'))

num_features = calculate_num_features(train_seqs)
train_dataset = VisitSequenceWithLabelDataset(train_seqs, train_labels, num_features)
valid_dataset = VisitSequenceWithLabelDataset(valid_seqs, valid_labels, num_features)
test_dataset = VisitSequenceWithLabelDataset(test_seqs, test_labels, num_features)
train_loader = DataLoader(dataset=train_dataset, batch_size=n_batch, shuffle=True, collate_fn=visit_collate_fn, num_workers=n_worker)
valid_loader = DataLoader(dataset=valid_dataset, batch_size=n_batch, shuffle=False, collate_fn=visit_collate_fn, num_workers=n_worker)
test_loader = DataLoader(dataset=test_dataset, batch_size=1, shuffle=False, collate_fn=visit_collate_fn, num_workers=n_worker)

# construct RNN model class
class VariableRNN(nn.Module):
    def __init__(self, dim_input):
        super(VariableRNN, self).__init__()
        self.fc1 = nn.Linear(in_features=dim_input, out_features=32)
        self.rnn = nn.GRU(input_size=32, hidden_size=16, num_layers=1, batch_first=True, dropout=0.5)
        self.fc2 = nn.Linear(in_features=16, out_features=2)

    def forward(self, input_tuple):

        seqs, lengths = input_tuple
        LEN =max(lengths)     
        seqs=seqs.view(-1,LEN,num_features)
        seqs = torch.relu(self.fc1(seqs))        
        seqs, h = self.rnn(seqs)
        seqs = self.fc2(seqs[:,-1,:])
        return seqs



model = VariableRNN(num_features)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

device = torch.device("cuda" if torch.cuda.is_available() and USE_CUDA else "cpu")
model.to(device)
criterion.to(device)

best_val_acc = 0.0
train_losses, train_accuracies = [], []
valid_losses, valid_accuracies = [], []

#fit the model
for epoch in range(n_epoch):
	train_loss, train_accuracy = train(model, device, train_loader, criterion, optimizer, epoch)
	valid_loss, valid_accuracy, valid_results = evaluate(model, device, valid_loader, criterion)

	train_losses.append(train_loss)
	valid_losses.append(valid_loss)

	train_accuracies.append(train_accuracy)
	valid_accuracies.append(valid_accuracy)

	is_best = valid_accuracy > best_val_acc  
	if is_best:
		best_val_acc = valid_accuracy
		torch.save(model, os.path.join(PATH_OUTPUT, "VariableRNN.pth"))

best_model = torch.load(os.path.join(PATH_OUTPUT, "VariableRNN.pth"))

train_loss, train_accuracy, train_results = evaluate(best_model, device, train_loader, criterion)

valid_loss, valid_accuracy, valid_results = evaluate(best_model, device, valid_loader, criterion)



# make prediction for testing data
def predict_mortality(model, device, data_loader):
    model.eval()
    probas=[]
    with torch.no_grad():
        for i, (input, target) in enumerate(data_loader):
            if isinstance(input, tuple):
                input = tuple([e.to(device) if type(e) == torch.Tensor else e for e in input])
            else:
                input = input.to(device)
            target = target.to(device)

            output = model(input)
            
            y_pred = output.detach().to('cpu')
            proba = F.softmax(y_pred).numpy().tolist()  
            proba=[a[1] for a in proba]
            probas.append(proba)
        
        probas=[a[0] for a in probas]
    
    return probas


test_prob = predict_mortality(best_model, device, test_loader)
test_label_pred =[round(i) for i in test_prob]

# Calculate accuracy for testing data prediction
test_accuracy =accuracy_score(test_labels, test_label_pred)
print ('Accuracy of testing dataset: ', round(test_accuracy,2))

# Calculate ROC score the testing data
fpr, tpr, _ = roc_curve(test_labels, test_prob)
roc_auc = auc(fpr, tpr)

print ('ROC_AUC score: ', round(roc_auc,2))

def ROC_PLOT(fpr,tpr):

    plt.figure()
    fig=plt.gcf()
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % auc(fpr,tpr))
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    pass

# plot learning curve (loos curver and accuracy curve)
plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies)    
#  plot confusion matrix for  the training data
plot_confusion_matrix(train_results, class_names)
#  plot confusion matrix for  the validation data
plot_confusion_matrix(valid_results, class_names)
# plot ROC curve
ROC_PLOT(fpr,tpr)



