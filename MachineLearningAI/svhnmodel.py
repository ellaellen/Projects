# -*- coding: utf-8 -*-
"""mymodel.ipynb
"""

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.optim import lr_scheduler
from torchvision import models,transforms,datasets

torch.manual_seed(0)
if torch.cuda.is_available():
        torch.cuda.manual_seed(0)
NUM_EPOCHS = 50
USE_CUDA = True 
# Path for saving model
PATH_OUTPUT = "../output"
os.makedirs(PATH_OUTPUT, exist_ok=True)
save_file = 'mymodel.pth'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
'''
train_data = loadmat('train_32x32.mat')
test_data = loadmat('test_32x32.mat')
X_train = train_data['X']
y_train = train_data['y']
X_test = test_data['X']
y_test = test_data['y']
print(X_train.shape, y_train.shape)

# transpose the train and test data
X_train = X_train.transpose((3,0,1,2))
y_train = y_train[:,0]
X_test = X_test.transpose((3,0,1,2))
y_test = y_test[:,0]
print(X_train.shape, y_train.shape)
print(np.unique(y_train))
print(np.unique(y_test))

# convert label 10 to 0
y_train[y_train == 10] = 0
y_test[y_test == 10] = 0
print(np.unique(y_train))

# split training to training + validation
X_train, X_validation, y_train, y_validation = train_test_split(X_train,y_train,test_size=0.13,random_state = 7)

# convert color images to grayscale
train_gray = np.expand_dims(np.dot(X_train,[0.2990,0.5870,0.1140]),axis=3).astype(np.float32)
validation_gray = np.expand_dims(np.dot(X_validation,[0.2990,0.5870,0.1140]),axis=3).astype(np.float32)
test_gray = np.expand_dims(np.dot(X_test,[0.2990,0.5870,0.1140]),axis=3).astype(np.float32)

print(train_gray.shape, test_gray.shape)
print(y_train.shape, y_test.shape)
'''

transform = transforms.Compose([
                                #transforms.Resize(64),
                                #transforms.CenterCrop(224),
                                #transforms.RandomCrop(32, padding=4),
                                #transforms.RandomRotation(degrees=15),
                                #transforms.ColorJitter(),
                                #transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1),
                                #transforms.RandomHorizontalFlip(),
                                #transforms.Grayscale(num_output_channels=3),
                                #transforms.RandomVerticalFlip(),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])
svhn = datasets.SVHN('svhn',download=True,transform = transform, split='train')
svhn_test = datasets.SVHN('svhn_test',download=True,transform = transform, split='test')
#svhn_extra = datasets.SVHN('extra', download=True, transform=transform, split='extra')
#data = np.concatenate([svhn.data, svhn_extra.data], axis = 0)
#labels = np.concatenate([svhn.labels, svhn_extra.labels], axis=0)
#svhn.data = data
#svhn.labels = labels


svhn_train,svhn_validation = train_test_split(svhn, test_size=0.3,random_state = 7)
#svhn_train,svhn_validation = train_test_split(svhn, test_size=0.8,random_state = 7)
#leave,svhn_validation = train_test_split(svhn_validation, test_size=0.5,random_state = 7)

train_loader = torch.utils.data.DataLoader(svhn_train, batch_size=64,shuffle=True,num_workers=4)
valid_loader = torch.utils.data.DataLoader(svhn_validation, batch_size=32,num_workers=4)
test_loader = torch.utils.data.DataLoader(svhn_test, batch_size=32,num_workers=4, shuffle=False)


                
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(num_features=32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(num_features=64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.drop_out = nn.Dropout(p=0.4)
        self.fc1 = nn.Linear(4096, 1000)
        self.fc2 = nn.Linear(1000, 10)
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.drop_out(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out
#model = MyCNN()
model = ConvNet()


model.to(device)
print(model)
#criterion = nn.NLLLoss()
criterion = nn.CrossEntropyLoss()
criterion.to(device)
#optimizer = optim.Adam(model.classifier.parameters(), lr=0.001, weight_decay=0.001)
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.001)
#optimizer = optim.SGD(model.classifier.parameters(), lr=0.001,momentum=0.9,weight_decay=0.0005)
#optimizer = optim.SGD(model.parameters(), lr=0.001,momentum=0.9,weight_decay=0.0005)
print(optimizer)

class AverageMeter(object):
        """Computes and stores the average and current value"""

        def __init__(self):
                self.reset()

        def reset(self):
                self.val = 0
                self.avg = 0
                self.sum = 0
                self.count = 0

        def update(self, val, n=1):
                self.val = val
                self.sum += val * n
                self.count += n
                self.avg = self.sum / self.count


def compute_batch_accuracy(output, target):
        """Computes the accuracy for a batch"""
        with torch.no_grad():

                batch_size = target.size(0)
                _, pred = output.max(1)
                correct = pred.eq(target).sum()

                return correct * 100.0 / batch_size


def train(model, device, data_loader, criterion, optimizer, epoch, print_freq=10):
        batch_time = AverageMeter()
        data_time = AverageMeter()
        losses = AverageMeter()
        accuracy = AverageMeter()

        model.train()

        end = time.time()
        for i, (input, target) in enumerate(data_loader):
                # measure data loading time
                data_time.update(time.time() - end)

                if isinstance(input, tuple):
                        input = tuple([e.to(device) if type(e) == torch.Tensor else e for e in input])
                else:
                        input = input.to(device)
                target = target.to(device)

                optimizer.zero_grad()
                output = model(input)
                loss = criterion(output, target)
                assert not np.isnan(loss.item()), 'Model diverged with loss = NaN'

                loss.backward()
                optimizer.step()

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

                losses.update(loss.item(), target.size(0))
                accuracy.update(compute_batch_accuracy(output, target).item(), target.size(0))

                if i % print_freq == 0:
                        print('Epoch: [{0}][{1}/{2}]\t'
                                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                                  'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
                                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                                  'Accuracy {acc.val:.3f} ({acc.avg:.3f})'.format(
                                epoch, i, len(data_loader), batch_time=batch_time,
                                data_time=data_time, loss=losses, acc=accuracy))

        return losses.avg, accuracy.avg


def evaluate(model, device, data_loader, criterion, print_freq=10):
        batch_time = AverageMeter()
        losses = AverageMeter()
        accuracy = AverageMeter()

        results = []

        model.eval()

        with torch.no_grad():
                end = time.time()
                for i, (input, target) in enumerate(data_loader):

                        if isinstance(input, tuple):
                                input = tuple([e.to(device) if type(e) == torch.Tensor else e for e in input])
                        else:
                                input = input.to(device)
                        target = target.to(device)

                        output = model(input)
                        loss = criterion(output, target)

                        # measure elapsed time
                        batch_time.update(time.time() - end)
                        end = time.time()

                        losses.update(loss.item(), target.size(0))
                        accuracy.update(compute_batch_accuracy(output, target).item(), target.size(0))

                        y_true = target.detach().to('cpu').numpy().tolist()
                        y_pred = output.detach().to('cpu').max(1)[1].numpy().tolist()
                        results.extend(list(zip(y_true, y_pred)))

                        if i % print_freq == 0:
                                print('Test: [{0}/{1}]\t'
                                          'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                                          'Accuracy {acc.val:.3f} ({acc.avg:.3f})'.format(
                                        i, len(data_loader), batch_time=batch_time, loss=losses, acc=accuracy))

        return losses.avg, accuracy.avg, results

def plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies):
        # TODO: Make plots for loss curves and accuracy curves.
        # TODO: You do not have to return the plots.
        # TODO: You can save plots as files by codes here or an interactive way according to your preference.
        plt.figure()
        plt.plot(np.arange(len(train_losses)), train_losses, label = 'Training Loss')
        plt.plot(np.arange(len(valid_losses)), valid_losses, label = 'Validation Loss')
        plt.ylabel('Loss')
        plt.xlabel('epoch')
        plt.legend(loc = "best")
        plt.title("Loss Curve")

        plt.figure()
        plt.plot(np.arange(len(train_accuracies)), train_accuracies, label = 'Training Accuracy')
        plt.plot(np.arange(len(valid_accuracies)), valid_accuracies, label = 'Validation Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('epoch')
        plt.legend(loc = "best")
        plt.title("Accuracy Curve")



best_val_acc = 0.0
train_losses, train_accuracies = [], []
valid_losses, valid_accuracies = [], []

start_time = time.time()
for epoch in range(NUM_EPOCHS):
        train_loss, train_accuracy = train(model, device, train_loader, criterion, optimizer, epoch)
        valid_loss, valid_accuracy, valid_results = evaluate(model, device, valid_loader, criterion)

        train_losses.append(train_loss)
        valid_losses.append(valid_loss)

        train_accuracies.append(train_accuracy)
        valid_accuracies.append(valid_accuracy)

        is_best = valid_accuracy > best_val_acc  # let's keep the model that has the best accuracy, but you can also use another metric.
        if is_best:
                best_val_acc = valid_accuracy
                #torch.save(model, os.path.join(PATH_OUTPUT, save_file))
                torch.save(model.state_dict(),os.path.join(PATH_OUTPUT, save_file))

        print('Time elapsed: %.2f min' % ((time.time() - start_time)/60))
plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies)
plt.show()

best_model = ConvNet()
best_model.load_state_dict(torch.load(os.path.join(PATH_OUTPUT, save_file)))
best_model.to(device)
#torch.save(model.state_dict(), filepath)

#Later to restore:
#model.load_state_dict(torch.load(filepath))


#best_model = torch.load(os.path.join(PATH_OUTPUT, save_file))
test_loss, test_accuracy, test_results = evaluate(best_model, device, test_loader, criterion)
print("test_loss:", test_loss)   
print("test_accuracy:", test_accuracy)
print("test_results:", test_results)


# running on colab
from google.colab import files
files.download( "../output/mymodel.pth" )
