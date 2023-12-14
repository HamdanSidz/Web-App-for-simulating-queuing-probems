import streamlit as st
import math
from math import factorial
import numpy as np

np.bool = np.bool_
np.object = object   

def mmc(lambda_val,mu_val,num_servers=1):

    if num_servers < 1:
        st.warning("No server is present")

    elif num_servers == 1:

        flag = False

        if lambda_val >= mu_val:
            st.warning("Error: Lambda should be less than Mu (lambda < mu)")
            flag = True
        
        rho = lambda_val / mu_val 
        Ls = lambda_val / (mu_val - lambda_val)
        Lq = (lambda_val ** 2) / (mu_val * (mu_val - lambda_val))
        Ws = 1 / (mu_val - lambda_val)
        Wq = lambda_val / (mu_val * (mu_val - lambda_val))
        
        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000

        if rho > 1:
            st.warning("Error: Utilization rate exceeds 1")
            flag = True

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {rho:.3f}")
   
    elif num_servers > 1:

        flag = False

        rho = lambda_val / (mu_val * num_servers)
        Ls = ((rho ** num_servers) * (1 / factorial(num_servers)) / 
            (sum([(rho ** k) / factorial(k) for k in range(num_servers)]) + 
            ((rho ** num_servers) * (1 / factorial(num_servers)))))
        Lq = Ls - (lambda_val / (mu_val * num_servers))
        Ws = Ls / lambda_val
        Wq = Lq / lambda_val
        
       
        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000
        
        if rho > 1:
            st.warning("Error: Utilization rate exceeds 1")
            flag = True

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {rho:.3f}")
    

   
def mgc(exp_mean, maxval, minval, num_servers):
    
    if num_servers < 1:
        st.warning("No server is present")

    elif num_servers == 1:
        flag = False

        exp_mean= 1/exp_mean
        exp_var = (exp_mean)**2/(exp_mean)**2

        mean_uniform = (maxval+minval)/2
        variance_uniform = ((maxval-minval)**2)/12
        mean_uniform = 1/mean_uniform
        variance_uniform = 1/variance_uniform

        p=exp_mean/(mean_uniform)

        Lq = (exp_mean ** 2) / (2 * exp_var) + ((p ** 2) / (2 * (1 - p)))
        Wq = Lq/exp_mean
        Ws = Wq + (1/mean_uniform)
        Ls = exp_mean * Ws

        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000
        
        if p > 1:
            st.warning("Error: Utilization rate exceeds 1")
            flag = True

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {p:.3f}")

    elif num_servers > 1:
        flag = False

        exp_mean=1/exp_mean
        exp_var = (exp_mean)**2/(exp_mean)**2

        mean_uniform = (maxval+minval)/2
        variance_uniform = ((maxval-minval)**2)/12
        mean_uniform = 1/mean_uniform
        variance_uniform = 1/variance_uniform

        c= num_servers 
        p=exp_mean/(c*mean_uniform)
        

        Lq = (exp_mean ** 2) / (num_servers * (1 - p)) * (1 + (num_servers ** 2 * exp_var) / (2 * (1 - p) ** 2)) / (1 - exp_mean / (num_servers * p))
        Wq = Lq / exp_mean
        Ws = Wq + 1 / (num_servers * p - exp_mean)
        Ls = exp_mean * Ws
        

        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000
        
        if p > 1:
            st.warning("Error: Utilization rate exceeds 1")
            flag = True

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {p:.3f}")
    
    
        
def ggc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,num_servers):
   
    if num_servers < 1:
        st.warning("No server is present")

    elif num_servers > 1:
        flag = False

        lembda=1/Arrival_Mean
        meu=1/Service_Mean
        c=num_servers
        p=lembda/(c*meu)
       
        Lq = (lembda ** 2) / (2 * lembda) + ((p ** 2) / (2 * (1 - p)))
        Wq = Lq/lembda
        Ws = Wq + (1/meu)
        Ls = lembda * Ws

        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000
        
        if p > 1:
            st.warning("Error: Utilization rate exceeds 1")
            flag = True

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {p:.3f}")

    elif num_servers == 1:
        flag = False
            
        lembda=1/Arrival_Mean
        meu=1/Service_Mean
        c=num_servers
        p=lembda/(c*meu)
     
        Lq = (p ** (num_servers + 1)) / (np.math.factorial(num_servers - 1) * num_servers * (1 - p) ** 2)
        Wq = Lq / lembda
        Ws = Wq + 1 / (num_servers * lembda / 2 - lembda)
        Ls = lembda * Ws
      
        if Ls < 0 or Lq < 0 or Ws < 0 or Wq < 0:
            #st.warning("Error: Negative values encountered")
            if Ls < 0:
                Ls = 0.000
            if Lq < 0:
                Lq = 0.000
            if Ws < 0:
                Ws = 0.000
            if Wq < 0:
                Wq = 0.000
        
        if p > 1:
            p = 1.0
          

        if flag != True:
            st.write(f"Number of customers in the system (Ls): {Ls:.3f}")
            st.write(f"Number of customers in the queue (Lq): {Lq:.3f}")
            st.write(f"Average wait time in the system (Ws): {Ws:.3f}")
            st.write(f"Average wait time in the queue (Wq): {Wq:.3f}")
            st.write(f"Total utilization rate (P): {p:.2f}")
    



def main():

    st.title("Queuing Theory Calculator")

    selected = st.selectbox("Select queuing model:", ["M/M/C", "M/G/C","G/G/C"])
    
    if selected == "M/M/C":

        No_of_server = st.number_input("Number of servers",value=1)
        st.subheader(f"Poisson and Exponential Distributions M/M/{No_of_server}")
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=1.58)
        Service_Mean = st.number_input("Enter average service time:", value=2.56)
    
    elif selected == "M/G/C":

        No_of_server = st.number_input("Number of servers",value=1)
        st.subheader(f"Exponential and Uniform Distributions M/G/{No_of_server}")              
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=10)
        maxvalue = st.number_input("Enter maximum value:", value=9)
        minvalue = st.number_input("Enter minimum value:", value=7)
    
    elif selected == "G/G/C":

        No_of_server = st.number_input("Number of servers",value=1)
        st.subheader(f"Noraml and Uniform Distributions G/G/{No_of_server}")
        Arrival_Mean = st.number_input("Enter mean inter-arrival time:", value=10)
        Service_Mean = st.number_input("Enter average service time:", value=15)
        ArrivalVariance = st.number_input("Enter maximum value:", value=25)
        ServiceVariance = st.number_input("Enter minimum value:", value=20)

    
    
    if st.button("Run Calculator"):

        if selected == "M/M/C":
            mmc(Arrival_Mean,Service_Mean,No_of_server)
        elif selected == "M/G/C":
            mgc(Arrival_Mean,maxvalue,minvalue,No_of_server)    
        elif selected == "G/G/C":
            ggc(Arrival_Mean,Service_Mean,ArrivalVariance,ServiceVariance,No_of_server)    

        


            
            


main()
    