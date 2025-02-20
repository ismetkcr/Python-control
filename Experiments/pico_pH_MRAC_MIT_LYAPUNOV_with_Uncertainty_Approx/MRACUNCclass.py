# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:04:08 2024
Thanks to Tansel Yucelen and LazyProgrammer..
@author: ismt
"""
import numpy as np

class Lyap_UNC(object):
    def __init__(self, gamma):
        self.What_app = np.random.rand(6, 1) * 0
        self.P = 1
        self.b = 1
        self.dt = 0.5
        self.gamma = gamma
        self.weightmatrix = []
        self.weightmatrix.append(self.What_app.T.copy())
        
    def calculate_uhand(self, x, u_n):
        self.app_func = np.array([[1], [x], [x**2], [x*u_n], [x**3], [u_n]])  
        uhand = self.What_app.T @ self.app_func
        # uhand = max(0, min(uhand, 125))
        return uhand

    def update_weights(self, yprev, ymprev):
        self.What_app += self.dt * ((self.gamma * (yprev - ymprev) * self.P * self.b) * self.app_func)
        self.weightmatrix.append(self.What_app.T.copy())
        return self.What_app
    
class Radial_UNC(object):
    def __init__(self, gamma, M):
        self.gamma = gamma
        self.What_app = np.random.randn(M, 1)  
        self.kernels = np.random.randint(-10, 11, size=(M, 1))
        self.weights = np.random.rand(M, 1) * 10
        self.P = 1
        self.b = 1
        self.dt = 0.5
        self.weightmatrix = []
        self.weightmatrix.append(self.What_app.T.copy())
        
                    
     
    def calculate_uhand(self,x):
        self.app_func = np.exp(-self.weights *  (np.abs(x+self.kernels))**2)
        uhand = self.What_app.T @ self.app_func
        return uhand
    
    def update_weights(self,yprev, ymprev):
        self.What_app += self.dt*((self.gamma*(yprev-ymprev)*self.P*self.b) * self.app_func )
        self.weightmatrix.append(self.What_app.T.copy())
        return self.What_app
    
    
class ANN_UNC(object):
     def __init__(self, gamma, M):
        self.gamma = gamma
        self.M = M
        self.D = 1
        self.W1 = np.random.randn(self.D, self.M)  
        self.b1 = np.zeros(self.M)
        self.W2 = np.random.randn(self.M, 1)  
        self.b2 = 0
        self.reg = 0.0
        
        
     def forward(self, X):
        #sigmoid
        X = np.array([X])
        #self.Z = 1 / (1 + np.exp(X.dot(self.W1) + self.b1))
        #tanh
        self.Z = np.tanh(X.dot(self.W1) + self.b1)
        #relu
        
        # self.Z = X.dot(self.W1) + self.b1
        # self.Z = self.Z * (self.Z>0)
        self.uhand = self.Z.dot(self.W2) + self.b2
        return self.uhand
     
     def derivative_w2(self, T, Y):
        diff = T - Y                             
        return (diff * self.Z).reshape(-1, 1)
    
     def derivative_b2(self, T, Y):
        return np.array([T-Y]).sum()
    
     def derivative_w1(self, X, T, Y):
        X = np.array([X])
        
        self.dZw1= np.outer(T-Y, self.W2) * (1 - self.Z * self.Z) #tanh activation
        
        return X.T.dot(self.dZw1)
    
     def derivative_b1(self,T, Y):
        
        self.dZb1 = np.outer(T-Y, self.W2) * (1 - self.Z * self.Z)
        
        return self.dZb1.sum(axis=0)
    
     def calculate_uhand(self, X):
         return self.forward(X)
     
     
     def update_weights(self,ymprev, yprev):
         #get gradients
          self.gW2 = self.derivative_w2(ymprev, yprev) 
          self.gb2 = self.derivative_b2(ymprev, yprev) 
          self.gW1 = self.derivative_w1(yprev, ymprev, yprev) 
          self.gb1 = self.derivative_b1(ymprev, yprev) 

          self.W2 += self.gamma * (self.gW2 - self.reg * self.W2 )
          self.b2 += self.gamma * (self.gb2 - self.reg * self.b2)
          self.W1 += self.gamma * (self.gW1 - self.reg * self.W1)
          self.b1 += self.gamma * (self.gb1 - self.reg * self.b1)    
         
    
    