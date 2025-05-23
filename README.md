# Humidifier disinfectant–associated lung injury (HDLI) Metabolomic Analysis 

## About
The code corresponding to the paper: (current revision, May 2025).  
**All datasets and related code used in the analysis are shared in this GitHub repository.**

**Evaluating Metabolic Signatures in the Serum of South Korean Patients with Humidifier Disinfectant–Associated Lung Injury Identified through Untargeted Metabolomics**
Jinwoo Kim<sup>1</sup>, Mi-Jin Kang<sup>2</sup>, So-Yeon Lee<sup>2,3</sup>, Sang-Bum Hong<sup>2,4</sup>, Ho Cheol Kim<sup>2,4</sup>, Myung Hee Nam<sup>1,\*</sup>, and Soo-Jong Hong<sup>2,3,\*</sup>

Affiliations:  
<sup>1</sup>Metropolitan Seoul Center, Korea Basic Science Institute (KBSI), Seoul, South Korea    
<sup>2</sup>Humidifier Disinfectant Health Center, Asan Medical Center, Seoul, South Korea  
<sup>3</sup>Department of Pediatrics, Childhood Respiratory and Allergy Center, Asan Medical Center, University of Ulsan College of Medicine, Seoul, South Korea  
<sup>4</sup>Department of Pulmonary and Critical Care Medicine, Asan Medical Center, University of Ulsan College of Medicine, Seoul, South Korea  
<sup>*</sup>These two corresponding authors contributed equally to the work  

Correspondence to:  
Soo-Jong Hong (E-mail: sjhong@amc.seoul.kr), and Myung Hee Nam (E-mail: nammh@kbsi.re.kr)  
[https://ehp.niehs.nih.gov/doi/10.1289/EHP14984]  


## Prerequisites
* `python` >= 3.7
* `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `sklearn`  

## Dataset
The dataset format is as follows:  

* Features to be analyzed should be in columns and samples should be in rows.  
* **"Name"** and **"Label"** columns must be included.  
    - Name means the sample name, and Label indicated the name of a class that can group samples.  
* A blank group in the label column must be named **blank** in the **Label** column, not "Blank", "B", or "b".  
* Except for **Name** and **Label**, all data set values must be numeric.  
* Only ".xlsx" and ".csv" files are allowed.  
* example file is "example_dataset.xlsx"  



Name        |Label       |*feature1*  |*feature2*  |..   .      |
:----------:|:----------:|:----------:|:----------:|:----------:| 
sample1     |Control     |501.2       |30.5        |...         |
sample2     |Control     |726.9       |20.3        |...         |
sample3     |Severe      |102.4       |600.5       |...         |
sample4     |Severe      |105.6       |750.5       |...         |
sample5     |blank       |5.0         |0.0         |...         |
sample6     |blank       |7.1         |0.0         |...         |


## Quickstart
Jupyter Notebook files are prepared as tutorials.  
You can simply analyze the metabolomic datasets by executing the code step by step.  
In metabolomics, results are checked at each stage of analysis, and the direction of analysis may be adjusted based on those previous results. Therefore, it is recommended to analyze metabolomic datasets in a step-by-step manner. Utilizing these Jupyter Notebook templates can facilitate this process and enable a more streamlined analysis of your dataset.


## License
The code and datasets in this repository are provided for personal and academic reference only. For more details, please see the [LICENSE](./LICENSE) file.


## First author
* Jinwoo Kim
* e-mail: jinwoo3239@gmail.com
