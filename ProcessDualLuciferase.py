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
    '''Sanitise user specification of control and deduce correct reporter'''
    if control.upper() == 'FIREFLY':
        reporter = 'Renilla'
    else:
        reporter = 'Firefly'
    return(reporter)

def readData(spread_file,reporter,row_skip,first_col_last_col):
    '''Reads in reporter signal data, adds extra columns and corrects for blanks, where present'''
    f = pd.read_excel(spread_file, skiprows= row_skip, parse_cols = first_col_last_col)
    f['plot_label'] = [x + ' ' + y for x, y in zip(f.Genotype, f.Plasmid)]
    if reporter=="Renilla":
        f[replab] = f['Renilla']/f['Firefly']
    else:
        f[replab] = f['Firefly']/f['Renilla']

    # Deducts blank values from Firefly and Renilla columns and then removes blank values from dataframe
    meanblank = f.loc[(f['Genotype'] == 'blank')].mean(axis=0)
    if not pd.isnull(meanblank["Firefly"]):
        f["Firefly"]=f["Firefly"]-meanblank['Firefly']
    if not pd.isnull(meanblank["Renilla"]):
        f["Renilla"]=f["Renilla"]-meanblank['Renilla']
    f = f[f.Plasmid != "blank"]
    return(f)

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
replab="Relative "+reporter

if spread_file is None:
    spread_file=getSpreadsheet()

f = readData(spread_file,reporter,row_skip,first_col_last_col)

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
Relative_values_reordered = f[["Plasmid","Genotype",replab]].sort(columns='Genotype', axis=0, ascending=True)

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
