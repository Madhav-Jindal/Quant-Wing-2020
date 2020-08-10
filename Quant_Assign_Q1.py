import numpy as np
import matplotlib.pyplot as plt 


# Function for option value calculation

def bapm(S0,vol,N,r,K,T,call='C'):

    """
        S0 - initial stock price
        vol - the volatility of the stock
        N - number of steps in the model
        r - risk-free interest rate
        K - strike price of the option
        T - time until expiry of the option
        call - Add P for put , by default set for call
    """
    
    dt=T/N 
    # u=np.exp(vol*np.sqrt(dt))
    # v=1/u
    # p=(np.exp(r*dt)-v)/(u-v)

    temp1 = np.exp((r + vol * vol)*dt)
    temp2 = 0.5 * (np.exp(-r*dt) + temp1)
    u = temp2 + np.sqrt(temp2 * temp2 - 1)
    v=1/u
    p=(np.exp(r*dt)-v)/(u-v)
 # Asset price tree 
    asset=np.zeros([N+1,N+1])
    for i in range(N+1):
        for j in range(i+1):
            asset[j,i]=S0*(u**(i-j)*(v**j))
    
    # print(asset)

# Option Value tree 
    option=np.zeros([N+1,N+1])
    #Final node calculation
    if call=='C':
        option[:,N]=np.maximum(np.zeros(N+1),(asset[:,N]-K))
    else:
        option[:,N]=np.maximum(np.zeros(N+1),(K-asset[:,N]))
    

    for i in range(N-1,-1,-1):    
        for j in range(0,i+1):
            # Modified for American verison
             if call=='C':
                option[j,i]=max(0,asset[i,j]-K,np.exp(-r*dt)*((p*option[j,i+1])+((1-p)*option[j+1,i+1])))
             else:
                 option[j,i]=max(0,K-asset[i,j],np.exp(-r*dt)*((p*option[j,i+1])+((1-p)*option[j+1,i+1])))
    
    
            
    return(option[0,0])

    
print("Option value is :{0:0.4}".format(bapm(100,0.2,4,0.1,100,0.33)))
#Modify here
# T to be entered in years
    # for ex-
    # 4 months is 1/3 years or 0.33 years
