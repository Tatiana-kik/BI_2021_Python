#!/usr/bin/env python
# coding: utf-8

# In[1]:


###############################################################################
# Task 1 - make a histogram of A, C, T and G
###############################################################################

import pandas as pd
import pandas_profiling
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import re

df = pd.read_csv('train.csv')

# Numbre of ACTG for each position we already have in Data Frame.
# Therefore draw BarPlot (not Histogram) to show count of ACTG in
# each position.
df.plot(x='pos', y=['A', 'C', 'T', 'G'], kind="bar", width=0.7,
        alpha=0.8, figsize=(15, 7))


# In[2]:


###############################################################################
# Task 2 - store subframe
###############################################################################

# Just do a query and store result as CSV-file
df = pd.read_csv('train.csv')
sub_df = df.query('matches > @df["matches"].mean()')[
    ['pos', 'reads_all', 'mismatches', 'deletions', 'insertions']]
sub_df.to_csv('train_part.csv')
# sub_df


# In[3]:


###############################################################################
# Task 3 - make EDA of some dataset
###############################################################################

mpl.rcParams.update(mpl.rcParamsDefault)

# Make EDA of Pokemon dataset
df = pd.read_csv('Pokemon.csv')
df


# In[4]:


# Look through ...
df.info()
# Dataset contains numerical and categorical parameters.


# In[5]:


# Look at NULL data
df.isnull().sum()
# We can see that 'Type 2' has a lot of (~50%) NULL values,
# therefore ignore them.


# ### Univariate Analysis

# In[6]:


# Look at distribution of 'Type 1'
sns.set_style('darkgrid')
sns.countplot(y='Type 1', data=df, palette='colorblind')
plt.xlabel('Count')
plt.ylabel('Type 1')
plt.show()
# We can see that Water and Normal pokemon's type prevail,
# while Flying is the smallest type


# In[7]:


# Look at distribution of 'Generation'
sns.set_style('whitegrid')
sns.countplot(x='Generation', data=df, palette='colorblind')
plt.xlabel("Generation")
plt.ylabel("Count")
plt.show()
# We can see that number of Pokemons interchange throught the generations


# In[8]:


# Look at distribution of 'Score'
sns.set_style('whitegrid')
sns.countplot(x='Total', data=df, palette='colorblind')
plt.xlabel('Total scores')
plt.ylabel('Count')
# plt.show()
# We can see thar there are a lot of pokemons with differents scores.


# ### Multivariate analysis

# In[9]:


# Look at dependencies between Type and Total
sns.set_style('darkgrid')
plt.title('Dependencies between Type and Score', size=16)
plt.xlabel('Total', size=12)
plt.ylabel('Type 1', size=12)
sns.scatterplot(x='Total', y='Type 1', data=df, hue='Type 1',
                edgecolor='black', palette='cubehelix')
plt.show()
# We can not see any significant dependencies between Type and Total.


# In[10]:


# Look at dependencies between Generation and Total
sns.set_style('darkgrid')
plt.title('Dependencies between Generation and Score', size=16)
plt.xlabel('Total', size=12)
plt.ylabel('Generation', size=12)
sns.scatterplot(x='Total', y='Generation', data=df, hue='Type 1',
                edgecolor='black', palette='cubehelix')
plt.show()
# We can not see any significant dependencies between Generation and Score.


# In[11]:


# Look at dependencies between Generation and Legendary
sns.set_style('darkgrid')
plt.title('Dependencies between Generation and Legendary', size=16)
plt.xlabel('Generation', size=12)
plt.ylabel('Legendary', size=12)
sns.scatterplot(x='Generation', y='Legendary', data=df, hue='Type 1',
                edgecolor='black', palette='cubehelix')
plt.show()
# We can not see any significant dependencies between Generation and Legendary.


# In[12]:


# Look at dependencies between Attack and Speed
sns.set_style('darkgrid')
plt.title('Dependencies between Attack and Speed', size=16)
plt.xlabel('Attack', size=12)
plt.ylabel('Speed', size=12)
sns.scatterplot(x='Attack', y='Speed', data=df, hue='Type 1',
                edgecolor='black', palette='cubehelix')
plt.show()
# We can see moderate dependency between Attack and Speed.


# In[13]:


# Look at dependencies between Attack and Defense
sns.set_style('darkgrid')
plt.title('Dependencies between Attack and Defense', size=16)
plt.xlabel('Attack', size=12)
plt.ylabel('Defense', size=12)
sns.scatterplot(x='Attack', y='Defense', data=df, hue='Type 1',
                edgecolor='black', palette='cubehelix')
plt.show()
# We can see moderate dependency between Attack and Defense.


# In[14]:


# Let's estimate the distribution of several combat parameters
kde_data = df[['Defense', 'Attack', 'Speed', 'Total']]

sns.set_style("darkgrid")
sns.kdeplot(data=kde_data, shade=True, palette='colorblind')
# plt.show()

# We see that the values of combat parameters are symmetrically distributed
# (with one peak) in range 0-200 and the Total score is in the range 0-800
# with two pronounced peaks at 300 and 500.


# #### Summary for EDA with Pandas:
# Using Univariate and Multivariate analysis and 'manual' selection of
# several parameters failed to identify clear features of the data and
# correlations between the values.

# ### Pandas profiling

# In[15]:


# For a more complete overview of possible dependencies,
# let's try using the pandas_profiling library

pandas_profiling.ProfileReport(df)


# #### Summary for EDA with Pandas_profiling library:
# In this large report (especially in the Correlations section) we can see:
# 1. All combat characteristics correlate with each other to an average degree
#     - the higher one characteristic - the higher the other.
# 2. The Total parameter is in high correlation with all other combat
# properties
#     - this is logical - Total is the sum of all combat properties.
# 3. Generation - does not correlate with other characteristics.
# 4. Legendaries - significantly correlates with combat characteristics,
# which is also logical.
#
# ### Conclusion
# It is more convenient to do the initial analysis of the data using the
# pandas_profiling library.
#
# This will allow to see explicit dependencies and, if necessary, examine
# them in more details. Data analysis "manually" using Pandas on this data
# set turned out to be poorly informative, since in most cases dependencies
# between variables are weakly expressed.

# In[16]:


###############################################################################
# Task 4 - Extra task (extra 25 points)
###############################################################################

# reading data from .gff file to pandas.DataFrame
def read_gff(path):
    # line format has view:
    #   Reference_10\t barrnap:0.9\t rRNA\t 67122\t 68652\t 0.0\t +\t .\t
    #   Name=16S_rRNA;product=16S ribosomal RNA
    return pd.read_csv(path, sep='\t', skiprows=1,
                       names=['chromosome', 'source', 'type', 'start', 'end',
                              'score', 'strand', 'phase', 'attributes'])


df_gff = read_gff('rrna_annotation.gff')
df_gff


# In[17]:


# reading data from .bed6 file to pandas.DataFrame
def read_bed6(path):
    # line format has view:
    #   Reference_1/t 197681/t 200286\t NODE_1445_length_2603_cov_1135/t
    #   593799/t  41/t -
    return pd.read_csv(path, sep='\t',
                       names=['chromosome', 'start', 'end', 'name',
                              'score', 'strand'])


df_bed = read_bed6('alignment.bed')
df_bed


# In[18]:


# modifying of values in 'attributes' column

def make_attr_shoter(attr_str):
    m = re.search('product=(.+?) ', attr_str)
    if m:
        return m.group(1)
    return None


df_gff = read_gff('rrna_annotation.gff')
df_gff['attributes'] = df_gff['attributes'].apply(make_attr_shoter)
df_gff


# In[19]:


# Make a table where for each chromosome (in fact, these are not chromosomes,
# but reference genomes) shows the amount of rRNA of each type.
# We can build a barplot that displays this data

df_gff['attributes'].value_counts()
# There are only 3 types - 23S, 16S and 5S


# In[20]:


# Look through types of chromosome
df_gff['chromosome'].value_counts().sort_index()
# There are 26 types of chromosome: [Reference_1 .. Reference_26]


# In[21]:


# make new DF with counting of RNA for each type
df_counts = pd.DataFrame(columns=['chromosome', '5S', '16S', '23S'])
for i in range(26):
    ref = 'Reference_' + str(i + 1)
    cnts = df_gff.query('chromosome == @ref')['attributes'].value_counts()
    df_counts.loc[i] = [ref, cnts.get('5S', 0), cnts.get('16S', 0),
                        cnts.get('23S', 0)]

df_counts


# In[22]:


# make bar plot for count_df
df_counts.plot.barh(x='chromosome', y=['5S', '16S', '23S'], rot=1)


# In[23]:


# Task:
# We want to know how much rRNA was successfully assembled during
# assembly. To do this, you can use the bedtools intersect program
# and intersect these two files. As a result, only rRNA records are
# saved, the interval of which overlapped with the contig interval
# in the alignment, which means that this gene is in the assembly.
# But forget the bedtools! We actually have a pandas here! So let's
# get the same result in it. Output a table containing the original
# records about the rRNAs completely included in the assembly
# (not a fragment), as well as a record about the contig in which
# this RNA fell. The resulting table should look something like Example2.
# Please note that several rRNAs can fall into one contig.

# Look again at the data frames

df_gff = read_gff('rrna_annotation.gff')
df_gff


# In[24]:


df_bed = read_bed6('alignment.bed')
df_bed


# In[25]:


# Go through df_gff and check for existing in df_bed

# resulr DF will be based on original GFF dataframe
df_res = df_gff

# rename several coulumns
df_res.rename(inplace=True,
              columns={'start': 'start_x', 'end': 'end_x',
                       'score': 'score_x', 'strand': 'strand_x'})

# prepare some lists to add them to DF after
drops = []
start_y = []
end_y = []
name_y = []
score_y = []
strand_y = []

# go through DF, prepare lists with aditional info,
# remove lines without intersection
for i in range(df_res.shape[0]):
    # print(f'### {i} ###')
    row = df_res.iloc[i]
    match = df_bed.query('chromosome == @row["chromosome"] and ' +
                         'start <= @row["start_x"] and ' +
                         'end >= @row["end_x"]')
    if match.shape[0] == 1:  # one intersection
        start_y.append(match['start'].iloc[0])
        end_y.append(match['end'].iloc[0])
        name_y.append(match['name'].iloc[0])
        score_y.append(match['score'].iloc[0])
        strand_y.append(match['strand'].iloc[0])
    elif match.shape[0] == 0:  # no intersections
        drops.append(i)
    else:
        raise BaseException('More then 1 intersections. What can I do?')

df_res.drop(drops, inplace=True)
df_res['start_y'] = start_y
df_res['end_y'] = end_y
df_res['name_y'] = name_y
df_res['score_y'] = score_y
df_res['strand_y'] = strand_y

# And we got result dataframe with intersections!
df_res
