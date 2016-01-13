__author__ = 'victoriatorrance'

import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def getSpreadsheet():
    '''Finds a single Excel spreadsheet in the current directory.'''
    flist=glob.glob("./*.xls*")
    if len(flist)>1:
        print("Too many Excel files to choose from!")
        for f in flist:
            print f
        return()
    else:
        return(flist[0])

def getReporter(control):
    if control.upper() == 'FIREFLY':
        reporter = 'Renilla'
    else:
        reporter = 'Firefly'
    return(reporter)

##### USER INPUT REQUIRED ########
control = 'firefly'
# user can optionally specify a spreadsheet filename.  Specify a value of None to search for a spreadsheet automatically
spread_file = None
# first and last column containing data
first_col_last_col = range(2,8,1)
# which row in the spreadsheet does the data start?
row_skip = 1
##############

reporter=getReporter(control)

if spread_file is None:
    spread_file=getSpreadsheet()

f = pd.read_excel(spread_file, skiprows= row_skip, parse_cols = first_col_last_col)

# Deducts blank values from Firefly and Renilla columns and then removes blank values from dataframe
x = f.loc[(f['Genotype'] == 'blank')]
blank_F, blank_R =  x['Firefly'].values[0], x['Renilla'].values[0]
f["Firefly"]=f["Firefly"]-blank_F
f["Renilla"]=f["Renilla"]-blank_R
f = f[f.Plasmid != "blank"]

# subsets original dataframe to give dataframes with unique genotypes
Genotypes = set(f['Genotype'])
Genotypes = sorted(Genotypes, reverse=False)

grps=f.groupby("Genotype")

# raw data is plotted, each genotype in a separate subplot
fig, axes = plt.subplots(nrows=1, ncols=len(Genotypes), sharey=True)
for i,gene in enumerate(Genotypes):
    pltdf=grps.get_group(gene)[["Plasmid","Firefly","Renilla"]].set_index("Plasmid")
    pltdf.plot(ax=axes[i], kind='bar', color=['r','y']); axes[i].set_title('%s'%gene) #r'%s$\Delta$'
plt.show()

# creates a new dataframe containing only relative renilla values
raw_data = f
Relative_values = f
raw_data['plot_label'] = [x + ' ' + y for x, y in zip(raw_data.Genotype, raw_data.Plasmid)]
raw_data = raw_data.drop('Genotype', 1)
raw_data = raw_data.drop('Plasmid', 1)
raw_data = raw_data.set_index(raw_data.plot_label)
raw_data = raw_data.drop('plot_label', 1)
if control == 'Firefly' or control == 'firefly':
    Relative_values['Relative Renilla'] = Relative_values['Renilla']/Relative_values['Firefly']
else:
    Relative_values['Relative Firefly'] = Relative_values['Firefly']/Relative_values['Renilla']
Relative_values = Relative_values.drop('Renilla', 1)
Relative_values = Relative_values.drop('Firefly', 1)
Relative_values = Relative_values.drop('plot_label', 1)
Relative_values_reordered = Relative_values.sort(columns='Genotype', axis=0, ascending=True)

ax = sns.factorplot(x = "Plasmid", y = "Relative Renilla", col = "Genotype", data = Relative_values_reordered, kind = "strip", jitter = 0.25, marker = 'D', edgecolor = 'gray')
plt.legend()
plt.show()

ax2 = sns.factorplot(x = "Genotype", y = "Relative Renilla", col = "Plasmid", data = Relative_values_reordered, kind = "strip", jitter = 0.25, marker = 'D', edgecolor = 'gray')
plt.legend()
plt.show()


genNames, df_genotypes = [], []
for g in Genotypes:
    data = Relative_values_reordered[Relative_values_reordered['Genotype'].isin([g])]
    data =  data.drop('Genotype', 1)
    data = data.set_index(data.Plasmid)
    data =  data.drop('Plasmid', 1)
    data.rename(columns={'Relative Renilla':g}, inplace=True)
    genNames.append(g)
    df_genotypes.append((data))

dfs2Concat_bygenes = pd.concat(df_genotypes)

# returns a list of unique geneotypes within our dataframe
plasmids = set(Relative_values_reordered['Plasmid'])

dfs2, plasmidNames = [], []

# loops through unique names and appends to the list a dataframe containing only the values for that plasmid
for plasmid in plasmids:
    data = Relative_values_reordered[Relative_values_reordered['Plasmid'].isin([plasmid])]
    data =  data.drop('Plasmid', 1)
    data = data.set_index(data.Genotype)
    data =  data.drop('Genotype', 1)
    data.rename(columns={'Relative Renilla':plasmid}, inplace=True)
    plasmidNames.append(plasmid)
    dfs2.append((data))
relativeValueData = zip(dfs2, plasmidNames)

dfs2Concat = pd.concat(dfs2)

markers = ['o','d','v', '^', '<', 's', 'p', '*', 'h', 'H', '+', 'x', 'D']

for i in range (0, len(df_genotypes)):
    m = sns.stripplot(x = dfs2Concat_bygenes.index, y = Genotypes[i], data = dfs2Concat_bygenes, jitter = 0.18, marker = markers[i], edgecolor= 'gray')
    m.plot([],[], color = 'k',linewidth = 0, marker = markers[i],label = Genotypes[i] , markersize = 8)

plt.title('Relative %s activity'%(reporter))
plt.ylabel('Relative %s'%reporter)
plt.legend()
plt.show()

for i in range (0, len(dfs2)):
    n = sns.stripplot(x = dfs2Concat.index, y = plasmidNames[i], data = dfs2Concat, jitter = 0.18, marker = markers[i], edgecolor= 'gray')
    n.plot([],[], color = 'k',linewidth = 0, marker = markers[i],label = plasmidNames[i] , markersize = 8)


plt.title('Relative %s activity'%(reporter))
plt.ylabel('Relative %s'%reporter)
plt.legend()
plt.show()
