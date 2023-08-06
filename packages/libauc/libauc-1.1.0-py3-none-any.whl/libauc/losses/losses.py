import torch 
import torch.nn.functional as F

class AUCMLoss(torch.nn.Module):
    """
    AUCM Loss
    Reference: https://arxiv.org/abs/2012.03173
    """
    def __init__(self, margin=1.0, imratio=0.1):
        super(AUCMLoss, self).__init__()
        self.margin = margin
        self.p = imratio
        self.a = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        self.b = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        self.alpha = torch.zeros(1, dtype=torch.float32, device="cuda", requires_grad=True).cuda()
        
    def forward(self, y_pred, y_true):
        loss = (1-self.p)*torch.mean((y_pred - self.a)**2*(1==y_true).float()) + \
                    self.p*torch.mean((y_pred - self.b)**2*(0==y_true).float())   + \
                    2*self.alpha*(self.p*(1-self.p) + \
                    torch.mean((self.p*y_pred*(0==y_true).float() - (1-self.p)*y_pred*(1==y_true).float())) )- \
                    self.p*(1-self.p)*self.alpha**2
        return loss
    

class CrossEntropyLoss(torch.nn.Module):
    """
    Cross Entropy Loss with Sigmoid Function
    Reference: https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html
    """
    def __init__(self):
        super(CrossEntropyLoss, self).__init__()
        self.criterion = F.binary_cross_entropy_with_logits  # with sigmoid

    def forward(self, y_pred, y_true):
        return self.criterion(y_pred, y_true)
    

class FocalLoss(torch.nn.Module):
    """
    Focal Loss
    Reference: https://amaarora.github.io/2020/06/29/FocalLoss.html
    """
    def __init__(self, alpha=.25, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = torch.tensor([alpha, 1-alpha]).cuda()
        self.gamma = gamma

    def forward(self, inputs, targets):
        BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        targets = targets.type(torch.long)
        at = self.alpha.gather(0, targets.data.view(-1))
        pt = torch.exp(-BCE_loss)
        F_loss = at*(1-pt)**self.gamma * BCE_loss
        return F_loss.mean()
