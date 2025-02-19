# -*- coding: utf-8 -*-
#thanks to Alexander Haber..
import numpy as np
class RecursiveLeastSquares(object):
    
    # x0 - initial estimate used to initialize the estimator
    # P0 - initial estimation error covariance matrix
    # R  - covariance matrix of the measurement noise
    def __init__(self,w0,P0,R):
        
        # initialize the values
        self.wprev=w0
        self.Pprev=P0
        self.R=R
        self.I = np.eye(len(self.wprev))
                           
        self.weightmatrix=[]
        self.weightmatrix.append(self.wprev)
                
        self.estimationErrorCovarianceMatrices=[]
        self.estimationErrorCovarianceMatrices.append(self.Pprev)
               
        self.gainMatrices=[]
                 
        self.errors=[]
        self.estimated_measurements = []
             
    
    def predict(self,measurementValue,data_matris):
        
        
        Lmatrix = self.R + (data_matris @ (self.Pprev @ data_matris.T))
        Lmatrixinv = np.linalg.inv(Lmatrix)
        
        self.Gmatrix = self.Pprev @ (data_matris.T * Lmatrixinv)
                        
        self.estimated_measurement = data_matris @ self.wprev
        self.error = measurementValue - self.estimated_measurement
        
        self.wnew = self.wprev + (self.Gmatrix*self.error)
       
        self.Pnew = (self.I - (self.Gmatrix @ data_matris)) @ self.Pprev
        #self.Pnew = self.Pnew / self.R

        self.Pprev = self.Pnew
        self.wprev = self.wnew
        
        
    def trackvalues(self, track=False):
        if track == True:
            self.weightmatrix.append(self.wnew)
            self.estimationErrorCovarianceMatrices.append(self.Pnew)
            self.gainMatrices.append(self.Gmatrix)
            self.errors.append(self.error)
            self.estimated_measurements.append(self.estimated_measurement)
            
        
        
        
        
       
        
            
  
        
           
            
    
    
    
    
