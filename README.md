# Genome Varinat Analysis: Genomic Disease Risk Score Analysis on Encrypted Genomic variants

The main goal of this repository is to establish a secure genome variants analysis platform. For this purpose, we have used the Fully Homomorphic Encryption (FHE) scheme to perform the genome variants analysis on encrypted mode, where FHE allows to perform Arithmetic Computation.
Here we used a Python wrapper docker image of PySeal library (Fork version of SEAL), which is a homomorphic encryption library developed by researchers in the Cryptography Research Group at Microsoft Research. Following instructions, you will guide to see our experiment result. In this experiment, 
we calculate disease risk scores from individual genome variants information (obtained in .vcf file) for five specific diseases, namely Alzheimer Disease and Age of Onset, Bipolar Disorder,  Breast Cancer, Celiac Disease, Type1 Diabetes. The guideline is structured by part 1 and Part 2: Part 1 leads to encrypted analysis, and Part 2 leads to Unecrypted analysis instructions.
## Pre-requisites
### System Configuration

* OS : Ubuntu (update) or windows 64-bit
* At least 16 GB RAM

### Software Setup

* Docker (v 19.03.13 or higher)
 [Instructions to install here](https://docs.docker.com/get-docker/)
 Check the installed version : `Docker --version`

* VirtualBox(v 6.0, or higher)
 [Instructions to install here](https://www.virtualbox.org/wiki/Downloads)
 
Note : VirtualBox is an optional. If you don't want to install docker in your main PC then you can use VirtualBox


# Part 1 :Setup SEAL Python wrapper

## Step 1 : Clone the repository or download 

1. Open a Terminal or PowerShell<br>
`git clone https://`

 or download the ZIP folder

**Notes :**
* The repository is a Docker Image SEAL Python wrapper (PySeal)
* Directory `~GenomeAnalysis_PySEAL-master/riskscore` obtain exp.py script for Encrypted Genomic variants analysis
* Directory `~GenomeAnalysis_PySEAL-master/riskscore` obtain exp2.py script for Unecrypted Genomic variants analysis
* Directory `~GenomeAnalysis_PySEAL-master/riskscore` obtain reference data (all csv file)for five specific disease
* Directory `~GenomeAnalysis_PySEAL-master/riskscore` obtain individual Genome varaints (.vcf file)


## Step 2 : Run the docker Image and create PySeal package

1. Get to the directory<br>
`cd ~/GenomeAnalysis_PySEAL-master`

2. Run the build-docker file to create the docker Image & Package<br>
`build-docker.sh`

3. Check the Docker Image<br>
`Docker images`
Image Name : seal-save will be visibile if the Image is successfully created

4. Run the  seal-save Image<br>
`docker run -it seal-save`

Expected :- then enter into the root directory : root@containerID:/SEAL$

5. view list of directory <br>
`ls` for ubuntu or `dir` for windows

## Step 3 : Run the Encrypted Analysis on Individuals Genomic variants to Calculate specific desease riskscore`

1. Get to the riskscore directory<br>
`cd ~/GenomeAnalysis_PySEAL-master/riskscore`

2. view list of file <br>
`ls` for ubuntu or `dir` for windows

3. Run the encrypted analysis script <br>
`python3 exp.py`

Expected :- you will see the all encrypted variant information, then finally get the riskscore and graphical view of risk score 

 **Notes :**
 --if want to modify the encrypted analysis script go to directory `cd ~/GenomeAnalysis_PySEAL-master/riskscore` then modify the exp.py. To execute the modified script you need to send script to your image container. you can send your script using following command
 `docker cp exp.py containerID:/SEAL/riskscore`.
 
# Part 2 : Run unencrypted Analysis

You can compare encrypted analysis risk score with unecrypted analysis result by executing exp2.py

1. Open Terminal or PowerShell <br>

2. Get to the directory outside of the docker <br>

`cd ~/GenomeAnalysis_PySEAL-master/riskscore`

3. Run the unecrypted analysis script <br>

`python3 exp2.py`

 **Notes :**
 --Make sure that you have installed all require library specially scikit-allel, scipy
, matplotlib outside of the docker.

### Congratualtion you have done successfully

References : 
[1]	 Folkersen L, Pain O, Ingason A, Werge T, Lewis CM and Austin J (2020) Impute.me: An Open-Source, Non-profit Tool for Using Data From Direct-to-Consumer Genetic Testing to Calculate and Interpret Polygenic Risk Scores. Front. Genet. 11:578. doi: 10.3389/fgene.2020.00578
[2]	 @article{Titus2018PySEALAP,
  title={PySEAL: A Python wrapper implementation of the SEAL homomorphic encryption library},
  author={A. Titus and S. Kishore and Todd Stavish and Stephanie M. Rogers and Karl S. Ni},
  journal={ArXiv},
  year={2018},
  volume={abs/1803.01891}
}


