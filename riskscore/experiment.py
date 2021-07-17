import pandas as pd
import os
import numpy as np
import allel
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.stats import norm


#pd.options.mode.chained_assignment = None 


def draw_z_score(x, cond, mu, sigma, title):
    y = norm.pdf(x, mu, sigma)
    z = x[cond]
    plt.plot(x, y)
    plt.fill_between(z, 0, norm.pdf(z, mu, sigma))
    plt.title(title)
    return plt.show()




def main():

    GenomeVariantsInput = allel.read_vcf('/home/shahed/riskScore/quartet.variants.annotated.vcf', samples=['ISDBM322015'],fields=[ 'variants/CHROM', 'variants/ID', 'variants/REF',
 'variants/ALT','calldata/GT'])

    #print(GenomeVariantsInput)
    SNP = GenomeVariantsInput['variants/ID']

    genotype = GenomeVariantsInput['calldata/GT']

    SNPdataframe = pd.DataFrame(SNP)
    SNPdataframe.columns=['SNP']

    genotype =  allel.GenotypeArray(GenomeVariantsInput['calldata/GT'])

    genotype2D = np.reshape(genotype,(-1,2))

    genotypeDataFrame = pd.DataFrame(genotype2D)
    genotypeDataFrame.columns=['A','B']

    individualSNPs = pd.concat((SNPdataframe, genotypeDataFrame), axis=1)
    #Load Type1-imputed analysis vlaue for type1- diabetes
    Type1identifiedSNP = pd.read_csv('/home/shahed/riskScore/Type1-diabetes.csv')
    
   
    
    Type1identifiedSNP.drop(['Your Genotype','Risk/non-risk Allele','SNP score','SNP-score(population normalized)','P-value','Major/minor Allele','Reported Gene'], axis='columns', inplace=True)
    
    new_df = pd.merge(Type1identifiedSNP, individualSNPs, on="SNP", how="inner")
    
    index= new_df[(new_df["A"] == 0) & (new_df["B"] == 0)].index
    new_df.loc[index,'SNP Score'] = 0
    new_df.loc[index,'effectAlleleFrequency'] = new_df['Minor/ Allele Frequency']
    new_df.loc[index,"AVGPopulationScore"] = new_df["effectAlleleFrequency"] * new_df["Effect size"]*2
    new_df.loc[index,"SNPnormalized"] = new_df["SNP Score"] - new_df['AVGPopulationScore']
    
 
    index= new_df[(new_df["A"] == 0) & (new_df["B"] == 1)].index
    new_df.loc[index,'SNP Score'] = new_df["Effect size"] * 1
    new_df.loc[index,'effectAlleleFrequency'] = 1 - new_df['Minor/ Allele Frequency']
    new_df.loc[index,"AVGPopulationScore"] = new_df["effectAlleleFrequency"] * new_df["Effect size"]*2
    new_df.loc[index,"SNPnormalized"] = new_df["SNP Score"] - new_df['AVGPopulationScore']
    
    
    
    index= new_df[(new_df["A"] == 1) & (new_df["B"] == 1)].index
    new_df.loc[index,'SNP Score'] = new_df["Effect size"] * 2
    new_df.loc[index,'effectAlleleFrequency'] = 1 - new_df['Minor/ Allele Frequency']
    new_df.loc[index,"AVGPopulationScore"] = new_df["effectAlleleFrequency"] * new_df["Effect size"]*2
    new_df.loc[index,"SNPnormalized"] = new_df["SNP Score"] - new_df['AVGPopulationScore']
    
    zScore = new_df.loc[:, 'SNPnormalized'].sum() / 0.85
    
    print(zScore)
    x = np.arange(-3,3,0.001)
    z0 = zScore
    draw_z_score(x, x<z0, 0, 1, 'Genetic Score for type1 diabetes')
 
  


# =============================================================================
# individualSNPs = pd.concat((SNPdataframe, genotypeDataFrame), axis=1)
# 
# 
# df = pd.merge(Type1identifiedSNP, individualSNPs, on="SNP", how="inner")
# =============================================================================
  
# =============================================================================
# =============================================================================
# # 
# #     new_df1 =df[(df["A"] == 0) & (df["B"] == 0)]
# # 
# #     new_df1["score"]=0
# #     new_df1["effectAlleleFrequency"] = new_df1['Minor/ Allele Frequency']
# #     new_df1["AVGPopulationScore"] = new_df1["effectAlleleFrequency"] * new_df1["Effect size"]*2
# #     new_df1["SNPnormalized"] = new_df1["score"] - new_df1['AVGPopulationScore']
# # 
# #     new_df2=df[(df["A"] == 0) & (df["B"] == 1)]
# #     new_df2["score"]= new_df2["Effect size"]*1
# #     new_df2["effectAlleleFrequency"] = 1 - new_df2['Minor/ Allele Frequency']
# #     new_df2["AVGPopulationScore"] = new_df2["effectAlleleFrequency"] * new_df2["Effect size"]*2
# #     new_df2["SNPnormalized"] = new_df2["score"] - new_df2['AVGPopulationScore']
# # 
# #     new_df3=df[(df["A"] == 1) & (df["B"] == 1)]
# #     new_df3["score"]= new_df3["Effect size"]*2
# #     new_df3["effectAlleleFrequency"] = 1 - new_df3['Minor/ Allele Frequency']
# #     new_df3["AVGPopulationScore"] = new_df3["effectAlleleFrequency"] * new_df3["Effect size"]*2
# #     new_df3["SNPnormalized"] = new_df3["score"] - new_df3['AVGPopulationScore']
# # 
# # 
# # 
# #     frames = [new_df1, new_df2, new_df3]
# #     result = pd.concat(frames)
# #     print(result)
# #     total = result.loc[:, 'SNPnormalized'].sum()
# #     z = total/0.85
# #     print("Z score = ",z)
# #     
# #     x = np.arange(-3,3,0.001)
# #     z0 = z
# #     draw_z_score(x, x<z0, 0, 1, 'Genetic Score for type1 diabetes')
# =============================================================================
# 
# =============================================================================

if __name__ == '__main__':
	main()

# sum = result.['SNPnormalized'].sum()
# print(sum)



# =============================================================================
# #print(indexes)
# #dataFrame1=pd.DataFrame(indexes)
# #new_df.iloc[indexes, "score"] = new_df["Minor/ Allele Frequency"] * new_df["Effect size"]
# =============================================================================






#print(individualSNPs.loc[1])





#Conditional part

#print(SNPdataframe.head(5))
#a = Type1identifiedSNP.loc[Type1identifiedSNP['SNP'].isin(SNPdataframe[0])].head()

#b = SNPdataframe.loc[SNPdataframe[0].isin(Type1identifiedSNP['SNP'])].head()







# =============================================================================
# print(Type1identifiedSNP['Minor/ Allele Frequency'])
# 
# print(SNPdataframe.loc[8])
# 
# print(genotypeDataFrame.loc[8][0])
# =============================================================================






# =============================================================================
# data3= np.array(genotype)
# data = pd.DataFrame(GenomeVariantsInput)
# #data2 = pd.DataFrame(data3)
# print(data.head(5))
# print(data)
# =============================================================================

