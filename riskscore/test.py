#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 05:10:24 2021

@author: shahed
"""
import pandas as pd
import os
import numpy as np
import allel
#import cairo
#import tkinter as tk
#from tkinter import filedialog
import matplotlib
#matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
#plt.switch_backend('TkAgg')
from scipy.stats import norm
import time
import random
import pickle
import threading
import seal
from seal import ChooserEvaluator, \
	Ciphertext, \
	Decryptor, \
	Encryptor, \
	EncryptionParameters, \
	Evaluator, \
	IntegerEncoder, \
	FractionalEncoder, \
	KeyGenerator, \
	MemoryPoolHandle, \
	Plaintext, \
	SEALContext, \
	EvaluationKeys, \
	GaloisKeys, \
	PolyCRTBuilder, \
	ChooserEncoder, \
	ChooserEvaluator, \
	ChooserPoly




 # Parameters setupp
parms = EncryptionParameters()
parms.set_poly_modulus("1x^2048 + 1")
parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
parms.set_plain_modulus(1 << 8)
context = SEALContext(parms)

# Key's setup amd encoder, encryptor, decryptopr,evaluator

iEncoder = IntegerEncoder(context.plain_modulus())
fEncoder = FractionalEncoder(context.plain_modulus(), context.poly_modulus(), 64, 32, 3)

keygen = KeyGenerator(context)
public_key = keygen.public_key()
secret_key = keygen.secret_key()

# =============================================================================
# outFileName="/SEAL/SEAL/rikscalculate/secretkey.txt"
# outFile=open(outFileName, "w")
# outFile.write(secret_key)
# outFile.close()ISDBM322015
# 
# =============================================================================

encryptor = Encryptor(context, public_key)
evaluator = Evaluator(context)
decryptor = Decryptor(context, secret_key)
    


print("============================================================================= \n")
print(context)
print("========================================ISDBM322015===================================== \n")


print("============================================================================= \n")
    
print(public_key,"\n",secret_key)
print("============================================================================= \n")
    
    



def draw_z_score(x, cond, mu, sigma, title):
    y = norm.pdf(x, mu, sigma)
    z = x[cond]
    plt.plot(x, y)
    plt.fill_between(z, 0, norm.pdf(z, mu, sigma))
    plt.title(title)
    return plt.show()


def plianEncode(value):
    fplain = fEncoder.encode(value)
    return fplain


def iencrypt(ivalue):
    iplain = iEncoder.encode(ivalue)
    out = Ciphertext()
    encryptor.encrypt(iplain, out)
    return out

def fencrypt(fvalue):
    fplain = fEncoder.encode(fvalue)
    out = Ciphertext()
    encryptor.encrypt(fplain, out)
    return out

def fdecrypt(encvalue):
    result = Plaintext()
    decryptor.decrypt(encvalue,result)
    return fEncoder.decode(result)

def idecrypt(encvalue):
    result = Plaintext()
    decryptor.decrypt(encvalue,result)
    return iEncoder.decode_int32(result)


def addition(value1,value2):
    out = Ciphertext()
    evaluator.add(value1,value2,out)
    return out


def substraction(value1,value2):
    out = Ciphertext()
    evaluator.sub(value1,value2,out)
    return out

def multipication(value1,plainTwo,plainOne):
 
    evaluator.multiply_plain(value1,plainTwo)
    evaluator.multiply_plain(value1,plainOne)
    return value1

def additionall(enc_df):
    result = Ciphertext()
    result = fencrypt(0)
    for i in range(len(enc_df)):
        
        #print(i)
        #row = encryptedaddtion(i)
        evaluator.add(result, enc_df.loc[i]['SNPnormalized'])
    
    return result

def main():
    time_start = time.time()
    
    print("Script running,,,,,,,,,,,,,")
    
    #User genome variants Information read
    
    print("Enter a random number : ")
    random = input()
    
# =============================================================================
#     GenomeVariantsInput = pd.read_csv('Type1-diabetes.csv')
#     
#     SNPdataframe = pd.DataFrame(GenomeVariantsInput['variants/ID'])
#     SNPdataframe = SNPdataframe.apply(lambda S:S.str.strip('rs'))
#     SNPdataframe.columns=['SNP']
#     SNPdataframe.drop(SNPdataframe.loc[SNPdataframe['SNP']=='.'].index, inplace=True)
#     patternDel = "[0-9]+;rs[0-9]+"
#     filter = SNPdataframe['SNP'].str.contains(patternDel)
# 
#     SNPdataframe = SNPdataframe[~filter]
#     
#     SNPdataframe = SNPdataframe.astype(str).astype(int)
#     #print(SNPdataframe.dtypes)
#     
#     genotype =  allel.GenotypeArray(GenomeVariantsInput['calldata/GT'])
# 
#     genotype2D = np.reshape(genotype,(-1,2))
# 
#     genotypeDataFrame = pd.DataFrame(genotype2D)
#     genotypeDataFrame.columns=['A','B']
#     
#     
#     individualSNPs = pd.concat((SNPdataframe, genotypeDataFrame), axis=1)
#     
#     print(" \n Individual SNP and Genotype \n")
#     print(individualSNPs.head(5))
#     #print(individualSNPs.dtypes)
#     #print(individualSNPs.head(5))
# =============================================================================
    
    
    GenomeVariantsInput = pd.read_csv('imputeme.csv')
    #Load Type1-imputed analysis vlaue for type1- diabetes
    Type1identifiedSNP = pd.read_csv('Type1-diabetes.csv')
    print("\n Type 1 daibates SNP EffectSize and Allele frquencey \n ")
    print(Type1identifiedSNP.head(5))
    
    filterSNP = pd.merge(Type1identifiedSNP, GenomeVariantsInput, on="SNP", how="inner")
    
    filterSNP['randomaddition'] = filterSNP['genotype'] ++ int(random)
    
    
    
    
    
    print("\n Type 1 daibates SNP of indivuduals \n ")
    print(filterSNP.head(100))
    #print(enc_df.dtypes)
    

    
    
    
    

    
    encryptedZero = fencrypt(0.0)
    encryptedOne = fencrypt(1.0)
    plainOne = plianEncode(1.0)
    plainTwo = plianEncode(2.0)
    

   
#Encryption part of dataframe
    enc_df = pd.DataFrame(dict(
        SNP = filterSNP['SNP'].apply(iencrypt),
        EffectSize = filterSNP['Effect size'].apply(fencrypt),
        MinorAlleleFrequency = filterSNP['Minor/ Allele Frequency'].apply(fencrypt),
        A = filterSNP['genotype'].apply(iencrypt),
        
        randomaddition = filterSNP['randomaddition']
        ))

    

    print("Encrypted Values:")
    print(enc_df.head())

    

    
    indexes = enc_df[(enc_df["randomaddition"] == int(random))]
   
    for i in range(len(indexes)):
        
        row = indexes.index[i]
        enc_df.loc[row,'score']= encryptedZero
        enc_df.loc[row,"EffectAlleleFrequency"] = enc_df.loc[row]['MinorAlleleFrequency']
        plainEffectSize = Plaintext()
        decryptor.decrypt(enc_df.loc[row]["EffectSize"],plainEffectSize)
        #print(plainEffectSize)
        enc_df.loc[row, "AVGPopulationScore"] = multipication(enc_df.loc[row]["EffectAlleleFrequency"], plainEffectSize, plainTwo)
        enc_df.loc[row,"SNPnormalized"] = substraction(enc_df.loc[row]["score"], enc_df.loc[row]['AVGPopulationScore'])
        
    
    indexes = enc_df[(enc_df["randomaddition"] == int(random)+1)]
   
    for i in range(len(indexes)):
        
        row = indexes.index[i]
        enc_df.loc[row,'score']= enc_df.loc[row]["EffectSize"]
        plainEffectSize = Plaintext()
        decryptor.decrypt(enc_df.loc[row]["EffectSize"],plainEffectSize)
        enc_df.loc[row,"EffectAlleleFrequency"] = substraction(encryptedOne, enc_df.loc[row]['MinorAlleleFrequency']) 
        enc_df.loc[row, "AVGPopulationScore"] = multipication(enc_df.loc[row]["EffectAlleleFrequency"], plainEffectSize, plainTwo)
        enc_df.loc[row,"SNPnormalized"] = substraction(enc_df.loc[row]["score"], enc_df.loc[row]['AVGPopulationScore'])
    
    
    
    indexes = enc_df[(enc_df["randomaddition"] == int(random) + 2)]
    for i in range(len(indexes)):
        row = indexes.index[i]
        enc_df.loc[row,'score']=    addition(enc_df.loc[row]["EffectSize"], enc_df.loc[row]["EffectSize"])
        plainEffectSize = Plaintext()
        decryptor.decrypt(enc_df.loc[row]["EffectSize"],plainEffectSize)
        enc_df.loc[row,"EffectAlleleFrequency"] = substraction(encryptedOne, enc_df.loc[row]['MinorAlleleFrequency']) 
        enc_df.loc[row, "AVGPopulationScore"] = multipication(enc_df.loc[row]["EffectAlleleFrequency"], plainEffectSize, plainTwo)
        enc_df.loc[row,"SNPnormalized"] = substraction(enc_df.loc[row]["score"], enc_df.loc[row]['AVGPopulationScore'])
    
    #evaluator.multiply(enc_df["EffectAlleleFrequency"], enc_df["EffectSize"])
    print(enc_df)





# =============================================================================
    
    enc_df = enc_df.dropna( how='any',subset=['SNPnormalized'])
    
    enc_df.reset_index(drop=True, inplace=True)
    print(enc_df)

    stnd = plianEncode(1.17)  #0.85
    
    #print(enc_df)
    total = additionall(enc_df)
    
    
    Z = multipication(total, stnd, plainOne)
    print("Encrypted Risk Score : ",Z) 
    riskScore = fdecrypt(Z)
    
    print("Decrypted Risk Score : ",riskScore) 
    
    x = np.arange(-3,3,0.001)
    z0 = riskScore
    draw_z_score(x, x<z0, 0, 1, 'Genetic Score for type1 diabetes')
# =============================================================================

    time_end = time.time()
    time_diff = time_end - time_start
    print("Execution time : [" + (str)(time_diff) + " seconds]") 


if __name__ == '__main__':
	main()
