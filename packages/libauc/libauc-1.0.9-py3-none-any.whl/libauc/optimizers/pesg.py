import torch 
import copy

class PESG(torch.optim.Optimizer):
    '''
    Proximal Epoch Stochastic Method (PESG) 
    Reference:
        https://arxiv.org/abs/2006.06889
    '''
    def __init__(self, model, a=None, b=None, alpha=None, imratio=0.1, margin=1.0, lr=0.1, gamma=500, clip_value=1.0, weight_decay=1e-5, **kwargs):
       
        assert a is not None, 'Found no variable a!'
        assert b is not None, 'Found no variable b!'
        assert alpha is not None, 'Found no variable alpha!'
        
        self.p = imratio
        self.margin = margin
        self.model = model
        
        self.lr = lr
        self.gamma = gamma
        self.clip_value = clip_value
        self.weight_decay = weight_decay
        
        self.a = a 
        self.b = b 
        self.alpha = alpha 
    
        # TODO! 
        self.model_ref = []
        for name, var in model.named_parameters(): 
            self.model_ref.append(torch.empty(var.shape).normal_(mean=0, std=0.01).cuda())
        self.a_ref = torch.empty(self.a.shape).normal_(mean=0, std=0.01).cuda() 
        self.b_ref = torch.empty(self.b.shape).normal_(mean=0, std=0.01).cuda() 
        self.model_ref.append(self.a_ref)
        self.model_ref.append(self.b_ref)
        
        self.model_acc = [torch.zeros(var.shape, dtype=torch.float32, device="cuda", requires_grad=False).cuda() for var in model.parameters()] #list(copy.deepcopy(model).parameters())
        self.a_acc = self.a.clone().detach().requires_grad_(False)
        self.b_acc = self.b.clone().detach().requires_grad_(False)
        self.model_acc.append(self.a_acc)
        self.model_acc.append(self.b_acc)
        self.T = 0
        self.step_counts = 0
    
        def get_parameters(params):
            for p in params:
                yield p
        self.params = get_parameters(list(model.parameters())+[a,b])
        self.defaults = dict(lr=self.lr, 
                             margin=margin, 
                             gamma=gamma, 
                             p=imratio, 
                             a=self.a, 
                             b=self.b,
                             alpha=self.alpha,
                             clip_value=clip_value,
                             weight_decay=weight_decay,
                             model_ref = self.model_ref,
                             model_acc = self.model_acc
                             )
        
        super(PESG, self).__init__(self.params, self.defaults)
     
    @property    
    def optim_steps(self):
        return self.step_counts

    def update_lr(self, lr):
        self.param_groups[0]['lr']=lr

    @torch.no_grad()
    def step(self):
        """Performs a single optimization step.
        """
        for group in self.param_groups:
            weight_decay = group['weight_decay']
            clip_value = group['clip_value']
            self.lr =  group['lr']
            
            p = group['p']
            gamma = group['gamma']
            m = group['margin']
           
            model_ref = group['model_ref']
            model_acc = group['model_acc']

            a = group['a']
            b = group['b']
            alpha = group['alpha']
            
            # updates
            for i, p in enumerate(group['params']):
                if p.grad is None:
                    continue  
                p.data = p.data - group['lr']*( torch.clamp(p.grad.data , -clip_value, clip_value) + 1/gamma*(p.data - model_ref[i].data) ) - group['lr']*weight_decay*p.data
                model_acc[i].data = model_acc[i].data + p.data

            alpha.data = alpha.data + group['lr']*(2*(m + b.data - a.data)-2*alpha.data)
            alpha.data  = torch.clamp(alpha.data,  0, 999)

        self.T += 1  
        self.step_counts += 1

    def zero_grad(self):
        self.model.zero_grad()
        self.a.grad = None
        self.b.grad = None
        self.alpha.grad =None
        
    def update_regularizer(self, decay_factor=None):
        if decay_factor != None:
            self.param_groups[0]['lr'] = self.param_groups[0]['lr']/decay_factor
            print ('Reducing learning rate to %.5f @ T=%s!'%(self.param_groups[0]['lr'], self.T))

        print ('Updating regularizer @ T=%s!'%(self.T))
        for i, param in enumerate(self.model.parameters()):
            self.model_ref[i].data = self.model_acc[i].data/self.T
        self.a_ref.data = self.a_acc.data/self.T
        self.b_ref.data = self.b_acc.data/self.T

        self.model_acc = [torch.zeros(var.shape, dtype=torch.float32, device="cuda", requires_grad=False).cuda() for var in self.model.parameters()] #list(copy.deepcopy(self.model).parameters())
        self.a_acc = torch.zeros(self.a.shape, dtype=torch.float32, device="cuda", requires_grad=False).cuda() #self.a.clone().detach().requires_grad_(False)
        self.b_acc =torch.zeros(self.a.shape, dtype=torch.float32, device="cuda", requires_grad=False).cuda() #self.b.clone().detach().requires_grad_(False)
        self.model_acc.append(self.a_acc)
        self.model_acc.append(self.b_acc)
        self.T = 0
        
    