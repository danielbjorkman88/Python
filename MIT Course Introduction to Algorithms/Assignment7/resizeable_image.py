import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    
    def best_seam(self):
        
        
        
        j = self.height
        guess = int(self.width*0.75)
#        for i in range(self.width):
#            pass
        
        self.dp(guess,j)
            
            #self.dp(i,j) = min(self.dp(i,j-1),self.dp(i-1,j-1),self.dp(i+1,j-1)) + self.energy(i,j)
        
        # width, height = self.width , self.height
        #self.energy(i,j)
        
        return self.path

    def dp(self, i , j):
        
        if j == 0:
            return  self.energy(i,j)
        else:
            a = self.dp(i,j-1) + self.energy(i,j)
            b = self.dp(i-1,j-1) + self.energy(i,j)
            c = self.dp(i+1,j-1) + self.energy(i,j)
            
            
            
            return min(self.dp(i,j-1),self.dp(i-1,j-1),self.dp(i+1,j-1)) + self.energy(i,j)
        


    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
