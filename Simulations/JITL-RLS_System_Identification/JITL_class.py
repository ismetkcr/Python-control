"""
A new data-based methodology for nonlinear process modeling
Cheng Cheng, Min-Sen Chiu∗
"""


import numpy as np
def create_delta_xi_matrix(x_matrix):    
    x_matrix = np.array(x_matrix)    
    # Calculate the differences between consecutive rows
    delta_xi = np.diff(x_matrix, axis=0)
    
    return delta_xi

def euclidean_norm(matrix):
    """
    Calculate the Euclidean (Frobenius) norm of a matrix.
    
    :param matrix: A 2D numpy array or nested list representing the matrix
    :return: The Euclidean norm of the matrix
    """
    matrix = np.array(matrix)
    return np.sqrt(np.sum(np.square(matrix)))

def radial_func(x):
    """
    e^-(x^2) sigmoid fonksiyonunu hesaplar.
    
    :param x: Girdi değeri veya numpy dizisi
    :return: Sigmoid fonksiyonunun sonucu
    """
    sigmo = np.exp(-np.square(x))
    return sigmo
def check_conditions(input1, input2):
    # Check the matrix inequality condition
    left_side_1 = input1 + input2
    left_side_2 = -input1 + input2
    condition1 = left_side_1 < 1 and left_side_2 < 1
    # Check the range condition for input2
    condition2 = -1 <= input2 <= 1    
    # Combined condition
    condition3 = condition1 and condition2
    
    # Return all three conditions
    return condition1, condition2, condition3


class JITL(object):
    def __init__(self, y0, u0):
        self.data_base = np.load('database.npy')
        self.y_minus_3 =  y0
        self.y_minus_2 =  y0
        self.y_minus_1 =  y0
        self.u_minus_1 = u0
        self.gamma = 0.55
        self.N = 200
        self.learning_rate = 1e-6
        self.cross_valid_errors = {j: 0 for j in range(self.N)}
        self.cross_valid_a = {j: 0 for j in range(self.N)}
        self.cross_valid_b = {j: 0 for j in range(self.N)} 
        
    def predict(self,y,u):
        x_q = np.array([[self.y_minus_2, self.y_minus_1, self.u_minus_1]])  # query_data
        # Step 1: Compute delta_xi and delta_xq
        xi = self.data_base[:, 1:]
        delta_xi = create_delta_xi_matrix(xi)
        delta_xq = np.array([[(self.y_minus_3 - self.y_minus_2), (self.y_minus_2 - self.y_minus_1), (self.y_minus_1 - y)]])
        # Step 2: Compute cos_fi
        cos_fi = (delta_xq.dot(delta_xi.T)) / (euclidean_norm(delta_xq) * euclidean_norm(delta_xi) + 1e-8)
        # Step 3: Find indices where cos_fi >= 0
        positive_indices = np.where(cos_fi >= 0)[1]
        # Step 4: Calculate distances similarity for these indices
        distances = {}
        similarity = {}
        for idx in positive_indices:
            d_i = euclidean_norm(xi[idx] - x_q)
            distances[idx] = d_i
            similarity[idx] = self.gamma * np.sqrt(radial_func(d_i)) + ((1 - self.gamma) * cos_fi[0, idx])
        # Step 5: Sort similarity in descending order and get the corresponding indices
        sorted_similarity = sorted(similarity.items(), key=lambda item: item[1], reverse=True)
        sorted_indices = [item[0] for item in sorted_similarity]
        similarity_num_descending = [item[1] for item in sorted_similarity]
        top_N_indices = sorted_indices[:self.N]    
        # Step 6. Extract data from database
        top_N_values = self.data_base[top_N_indices]
        top_N_similarities = similarity_num_descending[:self.N]        
        y_l = top_N_values[:, 0]
        fi_l = top_N_values[:, 1:]
        # Step 7. Transform data using similarities
        W = np.diag(top_N_similarities)
        v_l = W.dot(y_l)
        P_l = W.dot(fi_l)
        # Step 8. Calculate Model Parameters
        P_l_T = P_l.T
        # Calculate (P_l.T * P_l)
        P_l_T_P_l = np.dot(P_l_T, P_l)    
        # Calculate the inverse of (P_l.T * P_l)
        try:
            P_l_T_P_l_inv = np.linalg.inv(P_l_T_P_l)
            # Calculate (P_l.T * P_l)^-1 * P_l.T
            temp = np.dot(P_l_T_P_l_inv, P_l_T)
            # calculate the parameters
            self.parameters = np.dot(temp, v_l)
            for j in range(self.N):
                self.cross_valid_a[j] += 1 / top_N_similarities[j]**2 
                self.cross_valid_b[j] += top_N_similarities[j] *  (
                (y_l[j] - fi_l[j].T.dot(self.parameters))
                / (1 - (P_l[j].T @ P_l_T_P_l_inv @ P_l[j]))
                )
                self.cross_valid_errors[j] = (self.cross_valid_a[j] * self.cross_valid_b[j])
                     
        except np.linalg.LinAlgError:
            # If the matrix is not invertible, use the previous parameters
            print("Warning: Matrix is not invertible. Using last known parameters.")
            
         # Step 9 Calculate cross-validation errors and N_opt
            
          
        N_opt = min(self.cross_valid_errors.items(), key=lambda x: x[1])[0]
        N_opt = max(150, N_opt)
        # print("CROSS_VALID_ERRORS",cross_valid_errors)
        # print("N_opt", N_opt)
        # Update N to the new N_opt value
        self.N = N_opt
        # Reinitialize cross_valid_errors, cross_valid_a, and cross_valid_b with the new size N_opt
        self.cross_valid_errors = {j: 0 for j in range(self.N)}
        self.cross_valid_a = {j: 0 for j in range(self.N)}
        self.cross_valid_b = {j: 0 for j in range(self.N)}
        #print(f"Key with minimum value: {N_opt}")    
        # Step 10 Verify stability
        _, _, c3 = check_conditions(self.parameters[1], self.parameters[0])
        if c3 == False:
            #print(c3)
            #print('parameters before gradient',parameters)
            #USE Stochastic gradient for soln. of opt. problem
            for p in range(1):
                for l in range(N_opt):
                    Yhat = P_l[l,:].dot(self.parameters)
                    delta = Yhat - v_l[l]
                    self.parameters -= self.learning_rate*P_l[l,:].T.dot(delta)                              
            #print('parameters after gradient',parameters)
            _, _, c5 = check_conditions(self.parameters[1], self.parameters[0])
            #print('stability criteria after gradient,',c5)
        # Step 11 Calculate predicted output, updata states
        y_hat = self.parameters.dot(x_q.T)
        
        self.y_minus_3 = self.y_minus_2
        self.y_minus_2 = self.y_minus_1
        self.y_minus_1 = y
        self.u_minus_1 = u
        # Step 12 return predicted output
        return y_hat
    























    