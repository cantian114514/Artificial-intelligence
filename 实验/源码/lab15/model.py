import torch
import torch.nn as nn

class AutoEncoder(nn.Module):
    def __init__(self, dims):
        super().__init__()
        encoders = []
        for i in range(len(dims) - 1):
            encoders.append(nn.Linear(dims[i], dims[i + 1]))
            encoders.append(nn.ReLU())
        self.encoders = nn.Sequential(*encoders)
        
        decoders = []
        for i in range(len(dims) - 1, 0, -1):
            decoders.append(nn.Linear(dims[i], dims[i - 1]))
            decoders.append(nn.ReLU())
        self.decoders = nn.Sequential(*decoders)
    
    def forward(self, X):
        h = self.encoders(X)
        X_hat = self.decoders(h)
        return h, X_hat