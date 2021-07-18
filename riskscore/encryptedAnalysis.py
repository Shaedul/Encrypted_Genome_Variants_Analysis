#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 05:10:24 2021

@author: shahed
"""

# =============================================================================
# Imported all necessary basic and PySeal library 
# =============================================================================

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


# =============================================================================
# The first task is to set up an instance of the EncryptionParameters class. 
# It is critical to understand how these different parameters behave, how how they
# affect the encryption scheme, performance, and the security level. There are
# three encryption parameters that are necessary to set: size of polynomial modulus,
# coefficient modulus (ciphertext), plain modulus (plaintext modulus). 
# There are many range of value can be assign based on desired computation. For 
#more details https://github.com/Lab41/PySEAL/blob/master/SEALPythonExamples/examples.py   
# =============================================================================
    
parms = EncryptionParameters()
parms.set_poly_modulus("1x^2048 + 1")
parms.set_coeff_modulus(seal.coeff_modulus_128(2048))
parms.set_plain_modulus(1 << 8)

# =============================================================================
# Now that all parameters are set, we are ready to construct a SEALContext
# object. This is a heavy class that checks the validity and properties of
# the parameters we just set, and performs and stores several important
# pre-computations.
# =============================================================================

context = SEALContext(parms)



# =============================================================================
# Setup a integer value encoder and fractionaql value encoder 
# =============================================================================

iEncoder = IntegerEncoder(context.plain_modulus())
fEncoder = FractionalEncoder(context.plain_modulus(), context.poly_modulus(), 64, 32, 3)

# =============================================================================
# We are now ready to generate the secret and public keys. For this purpose we need
# an instance of the KeyGenerator class. Constructing a KeyGenerator automatically
# generates the public and secret key
# =============================================================================

keygen = KeyGenerator(context)
public_key = keygen.public_key()
secret_key = keygen.secret_key()

# =============================================================================
# To be able to encrypt, we need to construct an instance of Encryptor. Note that 
# the Encryptor only requires the public key.
# =============================================================================
encryptor = Encryptor(context, public_key)

# =============================================================================
# Computations on the ciphertexts are performed with the Evaluator class.
# So now we will setup a evaluator.
# =============================================================================

evaluator = Evaluator(context)

# =============================================================================
# We will of course want to decrypt our results to verify that everything worked,
# so we need to also construct an instance of Decryptor. Note that the Decryptor
# requires the secret key.
# =============================================================================

decryptor = Decryptor(context, secret_key)
    


print("====================================================================\n")
print(context)
print("========================================-----------================ \n")


print("====================================================================\n")
    
print(public_key,"\n",secret_key)
print("=================================================================== \n")
    
# =============================================================================
# Here we implemented some handy functions for different pourpouse.  
# =============================================================================

# =============================================================================
#The draw_z score () is used to draw z score 

def draw_z_score(x, cond, mu, sigma, title):
    y = norm.pdf(x, mu, sigma)
    z = x[cond]
    plt.plot(x, y)
    plt.fill_between(z, 0, norm.pdf(z, mu, sigma))
    plt.title(title)
    return plt.show()
# =============================================================================


# =============================================================================
#This plianEncode() function is to encode fractional number to fractional plaintext polynomial

def plianEncode(value):
    fplain = fEncoder.encode(value)
    return fplain
# =============================================================================


# =============================================================================
#This iencrypt() function is used to encrypt interger value and return the output 
#encrypted value. Here first the integer value will encode to plaintext polynomial 
#then create a ciphertext variable to store the encrypted result then encrypt the 
#integer.

def iencrypt(ivalue):
    iplain = iEncoder.encode(ivalue)
    out = Ciphertext()
    encryptor.encrypt(iplain, out)
    return out
# =============================================================================


# =============================================================================
#This fencrypt() function is used to encrypt fractional number and return the 
#output encrypted value

def fencrypt(fvalue):
    fplain = fEncoder.encode(fvalue)
    out = Ciphertext()
    encryptor.encrypt(fplain, out)
    return out
# =============================================================================


# =============================================================================
#This fdecrypt() function is used to decrypt fractional number and return the 
#fractional value.This is the reverse function of encryption. First a plaintext 
#variable will be created the decrypt the encrypted value and store o plaintext 
#variable. Then decode the plaintext polynomial to fractional number.

def fdecrypt(encvalue):
    result = Plaintext()
    decryptor.decrypt(encvalue,result)
    return fEncoder.decode(result)
# =============================================================================


# =============================================================================
#This idecrypt() function will decrypt the integer encrypted value and return 
#the integer value result

def idecrypt(encvalue):
    result = Plaintext()
    decryptor.decrypt(encvalue,result)
    return iEncoder.decode_int32(result)
# =============================================================================


# =============================================================================
# addition() function will perform encrypted addition operation and store the
#result to cipertext variable out then return

def addition(value1,value2):
    out = Ciphertext()
    evaluator.add(value1,value2,out)
    return out
# =============================================================================


# =============================================================================
# substraction() function will perform encrypted substraction operation and store the
#result to cipertext variable out then return

def substraction(value1,value2):
    out = Ciphertext()
    evaluator.sub(value1,value2,out)
    return out
# =============================================================================


# =============================================================================
# multipication() function will perform encrypted multipication operation and store the
#result to cipertext variable out then return

def multipication(value1,plainTwo,plainOne):
 
    evaluator.multiply_plain(value1,plainTwo)
    evaluator.multiply_plain(value1,plainOne)
    return value1
# =============================================================================


# =============================================================================
# additionall() function will used to add a column of value cumulatively which
# is used to SNPnormalized column

def additionall(enc_df):
    result = Ciphertext()
    result = fencrypt(0)
    for i in range(len(enc_df)):
        
        #print(i)
        #row = encryptedaddtion(i)
        evaluator.add(result, enc_df.loc[i]['SNPnormalized'])
    
    return result
# =============================================================================


# =============================================================================
def main():
    
    time_start = time.time() # Hold starting time
    print("Script running,,,,,,,,,,,,,")
    
# =============================================================================
    #random number will use as a confusion to make a comparison 
    #between encrypted value
    print("Enter a random number : ")
    random = input()
# =============================================================================   

# =============================================================================
    #User genome variants Information read. Here we read only some specific 
    #fields which we need to analysis
    GenomeVariantsInput = allel.read_vcf('quartet_variants_annotated.vcf', samples=['ISDBM322015'],fields=[ 'variants/CHROM', 'variants/ID', 'variants/REF',
    'variants/ALT','calldata/GT'])
    
    #Retrive SNP information from user genome variant file
    SNPdataframe = pd.DataFrame(GenomeVariantsInput['variants/ID'])
    
    #remove prefix "rs" from SNP ID number 
    SNPdataframe = SNPdataframe.apply(lambda S:S.str.strip('rs'))
    SNPdataframe.columns = ['SNP']
    SNPdataframe.drop(SNPdataframe.loc[SNPdataframe['SNP']=='.'].index, inplace = True)
    patternDel = "[0-9]+;rs[0-9]+" # remove unnecessary pattern from rs SNP id number
    filter = SNPdataframe['SNP'].str.contains(patternDel)

    SNPdataframe = SNPdataframe[~filter]
    
    #datatype changing
    SNPdataframe = SNPdataframe.astype(str).astype(int)
   
    #Genotype retrive from user genome variants
    genotype =  allel.GenotypeArray(GenomeVariantsInput['calldata/GT'])
    genotype2D = np.reshape(genotype,(-1,2))
    genotypeDataFrame = pd.DataFrame(genotype2D)
    genotypeDataFrame.columns=['A','B']
    individualSNPs = pd.concat((SNPdataframe, genotypeDataFrame), axis=1)
    
    #print(" \n Individual SNP and Genotype \n")
# =============================================================================


# =============================================================================
#One specific disease selection for risk calculation . Then load reference data
#for this disease
    
    print("Select one specefic diseases to calculate risk score :\n 1. Type1 Diabetes\n 2. Alzheimer Disease and Age of Onset\n 3. Biplolar Disorder\n 4. Breast Cancer\n 5. Celiac Disease\n   ")
    
    diseasesSelection = int(input())
    
    if(diseasesSelection == 1):
        identifiedSNP = pd.read_csv('Type1-diabetes.csv')
    elif(diseasesSelection == 2):
        identifiedSNP = pd.read_csv('Alzheimer_disease_and_age_of_onset.csv')
    elif(diseasesSelection == 3):
        identifiedSNP = pd.read_csv('Biplolar_disorder.csv')
    elif(diseasesSelection == 4):
        identifiedSNP = pd.read_csv('Breast_Cancer.csv')
    elif(diseasesSelection == 5):
        identifiedSNP = pd.read_csv('celiac_disease.csv')

# =============================================================================


# =============================================================================
# Filter identified SNP for selected disease from User genomic variants   
    filterSNP = pd.merge(identifiedSNP, individualSNPs, on="SNP", how="inner")
    
    if filterSNP.empty:
        print('There is no genomic variants for this desease!')
        quit()   
        
    filterSNP['randomaddition'] = filterSNP['A'] + filterSNP['B'] + int(random)
# =============================================================================
    


# =============================================================================
#Encryption part of the dataframe of user genomic information 
    enc_df = pd.DataFrame(dict(
        SNP = filterSNP['SNP'].apply(iencrypt),
        EffectSize = filterSNP['Effect size'].apply(fencrypt),
        MinorAlleleFrequency = filterSNP['Minor/ Allele Frequency'].apply(fencrypt),
        A = filterSNP['A'].apply(iencrypt),
        B = filterSNP['B'].apply(iencrypt),
        randomaddition = filterSNP['randomaddition']
        ))
# =============================================================================
    

# =============================================================================
    print("Encrypted User genome varinats which is identified for the specific desease:")
    print(enc_df.head())
# =============================================================================


# =============================================================================
#Some fractional zero, one, two value in encrypted form and plain module form
# to use in our analysis      
    encryptedZero = fencrypt(0.0)
    encryptedOne = fencrypt(1.0)
    plainOne = plianEncode(1.0)
    plainTwo = plianEncode(2.0)
# =============================================================================     


# =============================================================================
#Finding genoytpe comapring with random number becasue before add the genotype 
#with the random number. This part is : if genotype is 0/0
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
# =============================================================================       
    

# =============================================================================
# This analysis is for : if genotype is 0/1
    indexes = enc_df[(enc_df["randomaddition"] == int(random)+1)] 
    for i in range(len(indexes)):       
        row = indexes.index[i]
        enc_df.loc[row,'score']= enc_df.loc[row]["EffectSize"]
        plainEffectSize = Plaintext()
        decryptor.decrypt(enc_df.loc[row]["EffectSize"],plainEffectSize)
        enc_df.loc[row,"EffectAlleleFrequency"] = substraction(encryptedOne, enc_df.loc[row]['MinorAlleleFrequency']) 
        enc_df.loc[row, "AVGPopulationScore"] = multipication(enc_df.loc[row]["EffectAlleleFrequency"], plainEffectSize, plainTwo)
        enc_df.loc[row,"SNPnormalized"] = substraction(enc_df.loc[row]["score"], enc_df.loc[row]['AVGPopulationScore'])
# =============================================================================   
    

# ============================================================================= 
# This analysis is for : if genotype is 1/1   
    indexes = enc_df[(enc_df["randomaddition"] == int(random) + 2)]
    for i in range(len(indexes)):
        row = indexes.index[i]
        enc_df.loc[row,'score']=    addition(enc_df.loc[row]["EffectSize"], enc_df.loc[row]["EffectSize"])
        plainEffectSize = Plaintext()
        decryptor.decrypt(enc_df.loc[row]["EffectSize"],plainEffectSize)
        enc_df.loc[row,"EffectAlleleFrequency"] = substraction(encryptedOne, enc_df.loc[row]['MinorAlleleFrequency'])       
        enc_df.loc[row, "AVGPopulationScore"] = multipication(enc_df.loc[row]["EffectAlleleFrequency"], plainEffectSize, plainTwo)
        enc_df.loc[row,"SNPnormalized"] = substraction(enc_df.loc[row]["score"], enc_df.loc[row]['AVGPopulationScore'])
# ============================================================================= 
    

# ============================================================================= 
#Finally calculated dataframe of user genome analysis on encrypted data 
    print("Analyzed user genome for the specific desease on encrypted mode \n",enc_df)
# ============================================================================= 


# =============================================================================
# clean the SNPnormalized column, before perform the Normalization 
    enc_df = enc_df.dropna( how='any',subset=['SNPnormalized'])   
    enc_df.reset_index(drop=True, inplace=True)
    print("After clean the unnecessary data \n",enc_df)
# =============================================================================


# =============================================================================
#the inverse fractional value of Universel standard deviation value for the 
#European population
    stnd = plianEncode(1.17)  #0.85
# =============================================================================
 

# =============================================================================  
#perform the summation of SNPnormalized column to calculate the z score
    total = additionall(enc_df)       
    Z = multipication(total, stnd, plainOne)
    print("Encrypted Risk Score : ",Z) 
    riskScore = fdecrypt(Z) 
    print("Decrypted Risk Score : ",riskScore) 
# =============================================================================


# =============================================================================
# Z score draw   
    x = np.arange(-3,3,0.001)
    z0 = riskScore
    draw_z_score(x, x<z0, 0, 1, 'Disease Risk Score')
# =============================================================================


# =============================================================================
# Execution time 
    time_end = time.time()
    time_diff = time_end - time_start
    print("Execution time : [" + (str)(time_diff) + " seconds]") 
# =============================================================================


if __name__ == '__main__':
	main()
