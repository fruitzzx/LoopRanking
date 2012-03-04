# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:33:40 2012

@author: St Elmo Wilken
"""

class rErr(Exception): #not going to use this for a while...
    def __init__(self,message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)


#the "gain" matrix i input here comes from that pagerank document you gave me
#I kind of started over in lieu of our conversation earlier today i.e. assume the gain matrix is given and then go from there. 
class gRanking:
    """ this class just needs an input gain matrix to work its magic. """
    
    def __init__(self,mat,var):
        from numpy import array        
        self.gMatrix = array(mat) #feed in a normalised gain matrix NB: no dangling nodes!!!
        self.gVariables = var #feed in ordered variables wrt gMatrix
        self.constructRankArray()        
        

    
    def constructRankArray(self):
        from numpy import ones, argmax
        from numpy import linalg as linCalc
        
        self.n = len(self.gMatrix) #length of gain matrix = number of nodes
        S = (1.0/self.n)*ones((self.n,self.n))
        m = 0.15
        self.M = (1-m)*self.gMatrix + m*S #basic page rank algorithm
        [eigVal, eigVec] = linCalc.eig(self.M) #calc eigenvalues, eigenvectors as usual
        
        maxeigindex = argmax(eigVal)
        self.maxeig = eigVal[maxeigindex].real # store value for downstream checking

        self.rankArray = eigVec[:,maxeigindex] #cuts array into the eigenvector corrosponding to the eigenvalue above
        self.rankArray = (1/sum(self.rankArray))*self.rankArray #this is the 1 dimensional array composed of rankings (normalised)
        self.rankArray = self.rankArray.real #to take away the useless +0j part...
        
    def showConnectRank(self):
        import networkx as nx
        import matplotlib.pyplot as plot

        rG = nx.DiGraph()
        for i in range(self.n):
            for j in range(self.n):
                if (self.gMatrix[i,j] != 0):
                    rG.add_edge(self.gVariables[j],self.gVariables[i]) #draws the connectivity graph to visualise rankArray

        
        #create a dictionary of the rankings with their respective nodes ie {NODE:RANKING}
        self.rankDict = dict(zip(self.gVariables,self.rankArray))
        #print(self.rankDict) this works. now need to rearrange the rank sizes to corrospond to the drawing...
        self.rearrange = rG.nodes()
        #print(self.rearrange)
        self.sizeArray = [self.rankDict[var]*10000 for var in self.rearrange]
        
        nx.draw_circular(rG,node_size = self.sizeArray) #took out the colour... for some reason the nodes rearrange themselves... need to fix this.. and hence the code changes above... 
        plot.show()


#manual testing: this part works
if __name__ == "__main__":

    #this is the new test plant...
    mat1 = [[0,0,0,0,0,0,0,0,0,0,0,0.5,0,0],[0,0,0,0,0,0,0,0,0,0,0.5,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0.5,0,0],[0,0,0,0,0,0,0,0,0,0,0.5,0,0,0],[1.0/3,0,1.0/3,0,0,0,1.0/3,0,0,0,0,0,0,1.0/3],[1.0/3,0,1.0/3,0,1,0,1.0/3,0,0,0,0,0,0,1.0/3],[0,1,0,1,0,0.5,0,0,0,0,0,0,1,0],[1.0/3,0,1.0/3,0,0,0.5,0,0,0,0,0,0,0,1.0/3],[0,0,0,0,0,0,1.0/3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0.5,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0.5,0,0,0,0],[0,0,0,0,0,0,0,0,0.5,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0.5,0,0,0,0]]   
    mat2 = ["T1","F1","T2","F2","R1","X1","F3","T3","F4","T4","F6","T6","F5","T5"]
        
    testOne = gRanking(mat1,mat2)
    print(testOne.rankArray)
    testOne.showConnectRank()
















