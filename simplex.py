import numpy as np
import math as mth

def set_simplex():
    simplex[0]['r']='Z0'
    
    sign=-1
    if(Z['type']):
        sign=sign*-1
        
    simplex[0]['row']=np.concatenate( ( np.array(Z['C_i'])*sign , np.zeros(len(A))) ,   axis=0 )
    simplex[0]['RHS']=0
    
    
    for i in range (len(A)):
        if(A[i]['type']=='>='):
            A[i]['v']=np.array(A[i]['v'])*-1
            b[i]=b[i]*-1
            
        A[i]['s']=np.zeros((len(A)))
        A[i]['s'][i]=1    
        
        simplex.append({'r':'S'+str(i+1),'row':np.concatenate((A[i]['v'],A[i]['s']),axis=0) , 'RHS':b[i]})
        
        
    
    n=len(simplex[0]['row'])
    n_x=len(Z['C_i'])
    for i in range(n):
        if (i<n_x):
            row_simplex.append("X"+str(i+1))
        else:
            row_simplex.append("S"+str(i-n_x+1))
                        
def arr_txt(arr):
    tmp=""
    for i in range(len(arr)):
        tmp=tmp+"%.2f"%arr[i]+"    "
    return tmp

def pr(simplex,row_simplex):
    r=''
    for i in range(len(row_simplex)):
        r=r+row_simplex[i]+"      "    
    print("--------------------------------------------------------------")
    print("      "+r+"      RHS")
    print("--------------------------------------------------------------")
    for i in range(len(simplex)):
        tmp=arr_txt(simplex[i]['row'])    
        print(simplex[i]['r']+"    "+tmp+"     %.2f"%simplex[i]['RHS'])
    print("\n")    

def min_rhs(simplex):
    tmp=[-0.0000001,-1]
    for i in range(len(simplex)-1):
        if (simplex[1+i]['RHS']<tmp[0]):            
            tmp[0]=simplex[1+i]['RHS']
            tmp[1]=i+1
    
    return tmp[1]

def input_var_d(simplex,pivot_line):
    tmp= [-1,-1]
    for i in range(len(row_simplex)):
        if (simplex[pivot_line]['row'][i]<-0.0000001):
            if (tmp[0]!=-1):
                a=abs(simplex[0]['row'][i] / simplex[pivot_line]['row'][i])
                if(a<tmp[0]):
                    tmp=[a,i]                
            else:
                a=abs(simplex[0]['row'][i] / simplex[pivot_line]['row'][i])
                tmp=[a,i]
    return (tmp[1])    

def update_simplex(simplex,pivot_line,inp_var):
    y=simplex[pivot_line]['row'][inp_var]
    for i in range(len(simplex)):
        tmp=(simplex[i]['row'][inp_var]/y)*-1
        if(i!=pivot_line):
            simplex[i]['row']=np.round(simplex[i]['row']+simplex[pivot_line]['row']*tmp,4)
            simplex[i]['RHS']=round(simplex[i]['RHS']+tmp*simplex[pivot_line]['RHS'],4)
    simplex[pivot_line]['row']=np.round(simplex[pivot_line]['row']/y,4)
    simplex[pivot_line]['RHS']=round(simplex[pivot_line]['RHS']/y,4)
    
def dual_simplex():
    print("---------------Dual Simplex method---------------")
    while(True):
        pr(simplex,row_simplex)        
        pivot_line=min_rhs(simplex)
        if(pivot_line == -1 ):
            break
        inp_var=input_var_d(simplex,pivot_line)
        if(inp_var == -1 ):
            break
        simplex[pivot_line]['r']=row_simplex[inp_var]
        update_simplex(simplex,pivot_line,inp_var)
    
def min_z0(simplex):
    tmp=[-0.0001,-1]
    for i in range(len(simplex[0]['row'])):
        if(simplex[0]['row'][i]<tmp[0]):
            tmp[0]=simplex[0]['row'][i]
            tmp[1]=i

    return tmp[1]

def input_var_s(simplex,pivot_column):
    tmp= [-1,-1]
    for i in range(1,len(simplex)):
        if (simplex[i]['row'][pivot_column]>0.0000001):
            if (tmp[0]!=-1):
                a=simplex[i]['RHS'] / simplex[i]['row'][pivot_column]
                if(a<tmp[0]):
                    tmp=[a,i]
            else:
                a=simplex[i]['RHS'] / simplex[i]['row'][pivot_column]
                tmp=[a,i]
    return (tmp[1])
        
def s_simplex():
    while (True):
        print("--------------- Simplex method ---------------")
        pr(simplex,row_simplex)
        pivot_column=min_z0(simplex)
        if(pivot_column == -1 ):
            break
        
        inp_var=input_var_s(simplex,pivot_column)    
        
        if(inp_var == -1 ):
                break
        simplex[inp_var]['r']=row_simplex[pivot_column]
        update_simplex(simplex,inp_var,pivot_column)

def find_row_U():
    tmp=[0.000001,-1]
    for i in range (len(simplex)):
        rhs=round(simplex[i]['RHS'],2)
        floor=mth.floor(rhs)
        delta=round(rhs-floor,4)
        if (delta>tmp[0]):
            tmp=[delta,i]
    return (tmp[1])
            
def set_U(simplex,r):
    global I
    arr=[]
    for i in range(len(simplex[r]['row'])):
        tmp=round(mth.floor(simplex[r]['row'][i])-simplex[r]['row'][i],4)
        arr.append(tmp)
    arr.append(1)
    for i in range(len(simplex)):
        simplex[i]['row']=np.append(simplex[i]['row'],0)
        
    rhs=round(mth.floor(simplex[r]['RHS'])-simplex[r]['RHS'],4)
    
    u_i='U'+str(I)
    row={'r':u_i,'row':np.array(arr),'RHS':rhs}
    I+=1
    simplex.append(row)
    row_simplex.append(u_i)

        
I=1
simplex=[{}]
row_simplex=[]     



#True if minimize
type_obj_func = False

       
C_i=[4,5,6]

Z={"type":type_obj_func,"C_i":C_i}

A=[
   {"type":'<=','v':[2,3,3] },
   {"type":'<=','v':[3,1,4] },  
   ]

b=[45,50]

set_simplex()

dual_simplex()
s_simplex()

input()