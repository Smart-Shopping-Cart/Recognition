import torch.nn as nn
import torch


class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.features = nn.Sequential(
            nn.BatchNorm2d(3),
            nn.Conv2d(3, 8, 5),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 8, 5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(8, 16, 5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 16, 5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2))
        self.features.apply(self.init_weights)
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(16 * 12 * 12, 120),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, 3))
        self.classifier.apply(self.init_weights)

    def init_weights(self, m):
        if type(m) == nn.Conv2d:
            nn.init.xavier_uniform_(m.weight)
        elif type(m) == nn.Linear:
            nn.init.xavier_uniform_(m.weight)
        elif type(m) == nn.BatchNorm2d:
            nn.init.normal_(m.weight.data, 1.0, 0.02)
            nn.init.constant_(m.bias.data, 0.0)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
