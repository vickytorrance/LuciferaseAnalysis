# LuciferaseAnalysis
Firefly and Renilla luciferases are widely used as reporter genes for studying gene regulation and function. The use of two reporters genes allows for one to be used as a control. The dual luciferase assay is performed by sequentially measuring the firefly and renilla luciferase activities of the same sample. Results are expressed as the ratio of firefly to renilla luciferase activity (Fluc/Rluc), if renilla is used as the control, or (Rluc/Fluc) if firefly is used as the control. 

Plasmids are typically transformed into cells of different genotypes to study the effect of a given genotype on the expression of the reporter gene. Each sample will therefore have a ‘Genotype’ ID, a ‘Plasmid’ ID, a ‘Firefly’ reading and a ‘Renilla’ reading. Background is measured using a sample containing only cells.

ProcessDualLuciferase.py reads an excel file containing luciferase readings labelled with the Genotype ID and plasmid ID of the sample and plots renilla (or firefly if renilla is the control) levels as stripplots. A bar graph containing the ‘raw data’ ie the firefly and luciferase levels is also generated. 


Note – Within the excel sheet there should only be one cell which contains the background Renilla luciferase and one cell containing background Firefly luciferase and this sample should be labelled ‘blank’.  


Dependencies:


•	Pandas 
•	Xlrd
•	seaborn 
•	matplotlib



TO DO

Finish README.md – upload some sample plots

upload script to plot fold changes


