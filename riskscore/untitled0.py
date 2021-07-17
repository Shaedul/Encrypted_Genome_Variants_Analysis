import pandas as pd
import os
import numpy as np
import allel
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.stats import norm


pd.options.mode.chained_assignment = None 


def draw_z_score(x, cond, mu, sigma, title):
    y = norm.pdf(x, mu, sigma)
    z = x[cond]
    plt.plot(x, y)
    plt.fill_between(z, 0, norm.pdf(z, mu, sigma))
    plt.title(title)
    return plt.show()


 

def main():

# =============================================================================
#     GenomeVariantsInput = allel.read_vcf('/home/shahed/riskScore/quartet.variants.annotated.vcf', samples=['ISDBM322015'],fields=[ 'variants/CHROM', 'variants/ID', 'variants/REF',
#  'variants/ALT','calldata/GT'])
# 
#     print(GenomeVariantsInput)
#     SNP = GenomeVariantsInput['variants/ID']
# 
#     genotype = GenomeVariantsInput['calldata/GT']
# 
#     SNPdataframe = pd.DataFrame(SNP)
#     SNPdataframe.columns=['SNP']
# 
#     genotype =  allel.GenotypeArray(GenomeVariantsInput['calldata/GT'])
# 
#     genotype2D = np.reshape(genotype,(-1,2))
# 
#     genotypeDataFrame = pd.DataFrame(genotype2D)
#     genotypeDataFrame.columns=['A','B']
# 
# =============================================================================

    GenomeVariantsInput = pd.read_csv('imputeme.csv')
    #Load Type1-imputed analysis vlaue for type1- diabetes
    Type1identifiedSNP = pd.read_csv('Type1-diabetes.csv')
    print("\n Type 1 daibates SNP EffectSize and Allele frquencey \n ")
    print(Type1identifiedSNP.head(5))
    
    df1 = pd.merge(Type1identifiedSNP, GenomeVariantsInput, on="SNP", how="inner")
    print("Individuals available SNP for Type1 Diabetes",df1)

    df1['Multipication'] = (df1['Effect size'] * 1000).astype(int)
    
    print(df1)
    
    indexes =df1[(df1["A"] == 0) & (df1["B"] == 0)]
    #row= indexes.index
    #print(indexes)w
    df1.loc[indexes.index,'score']= 0
    df1.loc[indexes.index]
    df1.loc[indexes.index,"EffectAlleleFrequency"] = df1['Minor/ Allele Frequency']
    df1.loc[indexes.index, "AVGPopulationScore"] = df1["EffectAlleleFrequency"] * df1["Effect size"] * 2
    df1.loc[indexes.index,"SNPnormalized"] = df1["score"] - df1['AVGPopulationScore']
    
    
    indexes = df1[(df1["A"] == 0) & (df1["B"] == 1)]
    df1.loc[indexes.index,'score']= df1["Effect size"] 
    df1.loc[indexes.index,"EffectAlleleFrequency"] = 1 - df1['Minor/ Allele Frequency']
    df1.loc[indexes.index, "AVGPopulationScore"] = df1["EffectAlleleFrequency"] * df1["Effect size"] * 2
    df1.loc[indexes.index,"SNPnormalized"] = df1["score"] - df1['AVGPopulationScore']


    indexes = df1[(df1["A"] == 1) & (df1["B"] == 1)]
    df1.loc[indexes.index,'score']= df1["Effect size"] * 2
    df1.loc[indexes.index,"EffectAlleleFrequency"] = 1 - df1['Minor/ Allele Frequency']
    df1.loc[indexes.index, "AVGPopulationScore"] = df1["EffectAlleleFrequency"] * df1["Effect size"] * 2
    df1.loc[indexes.index,"SNPnormalized"] = df1["score"] - df1['AVGPopulationScore']
    
    print(df1)


    #frames = [new_df1, new_df2, new_df3]
    #result = pd.concat(frames)
    print(df1.loc[1])
    
    
    
    
    
    
    
    total = df1.loc[:, 'SNPnormalized'].sum()
    print(total)
    z = total/0.85
    print("Z score = ",z)
    
    x = np.arange(-3,3,0.001)
    z0 = z
    draw_z_score(x, x<z0, 0, 1, 'Genetic Score for type1 diabetes')


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

