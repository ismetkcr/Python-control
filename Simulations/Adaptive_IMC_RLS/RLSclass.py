# -*- coding: utf-8 -*-
#thanks to Alexander Haber..
import numpy as np
class RecursiveLeastSquares(object):
    
    # x0 - initial estimate used to initialize the estimator
    # P0 - initial estimation error covariance matrix
    # R  - covariance matrix of the measurement noise
    def __init__(self,w0,P0,R):
        
        # Ensure inputs are numpy arrays with float64 type
        self.wprev = np.array(w0, dtype=np.float64)
        self.Pprev = np.array(P0, dtype=np.float64)
        self.R = np.array(R, dtype=np.float64)
        self.I = np.eye(len(self.wprev), dtype=np.float64)
                           
        self.weightmatrix=[]
        self.weightmatrix.append(self.wprev)
                
        self.estimationErrorCovarianceMatrices=[]
        self.estimationErrorCovarianceMatrices.append(self.Pprev)
               
        self.gainMatrices=[]
                 
        self.errors=[]
        self.estimated_measurements = []
             
    
    def predict(self,measurementValue,data_matris):
        data_matris = np.array(data_matris, dtype=np.float64)
        data_matris = data_matris.reshape(1,3)
        Lmatrix = self.R + (data_matris @ (self.Pprev @ data_matris.T))
        Lmatrixinv = np.linalg.inv(Lmatrix)
        
        self.Gmatrix = self.Pprev @ (data_matris.T * Lmatrixinv)
                        
        self.estimated_measurement = data_matris @ self.wprev
        self.error = measurementValue - self.estimated_measurement
        
        self.wnew = self.wprev + (self.Gmatrix*self.error)
       
        self.Pnew = (self.I - (self.Gmatrix @ data_matris)) @ self.Pprev
        self.Pnew = self.Pnew / self.R

        self.Pprev = self.Pnew
        self.wprev = self.wnew
        
        return self.estimated_measurement
        
    def trackvalues(self, track=False):
        if track == True:
            self.weightmatrix.append(self.wnew)
            self.estimationErrorCovarianceMatrices.append(self.Pnew)
            self.gainMatrices.append(self.Gmatrix)
            self.errors.append(self.error)
            self.estimated_measurements.append(self.estimated_measurement)
            
        
        
        
        
       
        
            
  
        
           
            
    
    
    
    
