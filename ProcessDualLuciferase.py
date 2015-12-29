__author__ = 'victoriatorrance'


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


##### USER INPUT REQUIRED ########
control = 'firefly'
# first and last collumn containing data
first_col_last_col = range(2,8,1)
# which row in the spreadsheet does the data start?
row_skip = 1
##############


if control == 'Firefly' or control == 'firefly' or control == 'FIREFLY':
    reporter = 'Renilla'
else:
    reporter = 'Firefly'

f = pd.read_excel('/example_data.xlsx', skiprows= row_skip, parse_cols = first_col_last_col)

# Deducts the blank and then removes it from dataframe
x = f.loc[(f['Genotype'] == 'blank')]
blank_F, blank_R =  x['Firefly'], x['Renilla']
i = 0
for first, last, x, y in zip(f['Plasmid'], f['Genotype'], f['Firefly'], f['Renilla']):
    f['Firefly'][i] = x - blank_F
    f['Renilla'][i] = y - blank_R
    i = i+1
f = f[f.Plasmid != "blank"]


# returns a list of unique geneotypes within our dataframe
Genotypes = set(f['Genotype'])
Genotypes = sorted(Genotypes, reverse=False)
# loops through each of the unique geneotypes and returns for each a dataframe containing the only the values concerned
# with that geneotype. these are stored in a list which is zipped to its 'geneotype' name
dfs, Genes = [], []
for gene in Genotypes:
    data = f[f['Genotype'].isin([gene])]
    data =  data.drop('Genotype', 1)
    data = data.set_index(data.Plasmid)
    dfs.append((data))
    Genes.append((gene))
zipped = zip(Genes, dfs)

# raw data is plotted, each geneotype in a separate subplot
fig, axes = plt.subplots(nrows=1, ncols=len(zipped), sharey=True)
for i in range(0, len(zipped)):
    zipped[i][1].plot(ax=axes[i], kind='bar', color=['r','y']); axes[i].set_title('%s'%zipped[i][0]) #r'%s$\Delta$'

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


print Relative_values_reordered


ax = sns.factorplot(x = "Plasmid", y = "Relative Renilla", col = "Genotype", data = Relative_values_reordered, kind = "strip", jitter = 0.25, marker = 'D', edgecolor = 'gray')
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
