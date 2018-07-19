# Importing the fuzzy package
import fuzzy as fz

# Exploring the output of fuzzy.nysiis
fz.nysiis('color')

# Testing equivalence of similar sounding words
fz.nysiis('Tufoule') == fz.nysiis('Tufool')


get_ipython().run_cell_magic('nose', '', "import sys\n\ndef test_fuzzy_is_loaded():\n    assert 'fuzzy' in sys.modules, \\\n    'The fuzzy module should be loaded'")


# Importing the pandas module
import pandas as pd

# Reading in python/py projects/datasets/nytkids_yearly.csv, which is semicolon delimited.
author_df = pd.read_csv('python/py projects/datasets/nytkids_yearly.csv', sep=';')

# Looping through author_df['Author'] to extract the authors first names
first_name = []
for name in author_df['Author']:
    first_name.append(name.split()[0])

# Adding first_name as a column to author_df
author_df['first_name'] = first_name

# Checking out the first few rows of author_df
author_df.head()

get_ipython().run_cell_magic('nose', '', "    \ndef test_check_authors():\n    len_auth = len(author_df['first_name'])\n    all_names = list(author_df['first_name'])\n    assert ('Shel' in all_names and len_auth==603), \\\n    'first_name column does not contan the correct first names of authors'")

# Importing numpy
import numpy as np

# Looping through author's first names to create the nysiis (fuzzy) equivalent
nysiis_name = []
for name in author_df['first_name']:
    nysiis_name.append(fz.nysiis(name))

# Adding nysiis_name as a column to author_df
author_df['nysiis_name'] = nysiis_name

# Printing out the difference between unique firstnames and unique nysiis_names:
print(len(np.unique(author_df['first_name'])) - len(np.unique(author_df['nysiis_name'])))



get_ipython().run_cell_magic('nose', '', "\nimport numpy as np\n\ndef test_check_nysiis_list():\n    assert len( np.unique(author_df['nysiis_name']) ) == 145, \\\n        'The nysiis_name column does not contan the correct entries'")


# Reading in python/py projects/datasets/babynames_nysiis.csv, which is semicolon delimited.
babies_df = pd.read_csv('python/py projects/datasets/babynames_nysiis.csv', sep=';')

# Looping through babies_df to and filling up gender
gender = []
for x,y in zip(babies_df['perc_female'], babies_df['perc_male']):
    if x>y:
        gender.append('F')
    elif x<y:
        gender.append('M')
    else:
        gender.append("N")
# Adding a gender column to babies_df
babies_df['gender'] = gender
# Printing out the first few rows of babies_df
babies_df.head()



get_ipython().run_cell_magic('nose', '', "\ndef test_gender_distribution():\n    assert len([i for i, x in enumerate(babies_df['gender']) if x == 'N']) == 1170,\\\n        'gender column does not contain the correct number of Male, Female and Neutral names, which are 7031, 8939 and 1170 respectively'")


# This function returns the location of an element in a_list.
# Where an item does not exist, it returns -1.
def locate_in_list(a_list, element):
    loc_of_name = a_list.index(element) if element in a_list else -1
    return(loc_of_name)

# Looping through author_df['nysiis_name'] and appending the gender of each
# author to author_gender.
author_gender = []
for name in author_df['nysiis_name']:
    ind = locate_in_list(list(babies_df['babynysiis']), name)
    if ind<0:
         author_gender.append('Unknown')
    else:
        author_gender.append(babies_df['gender'][locate_in_list(list(babies_df['babynysiis']), name)])
print(author_gender)
# Adding author_gender to the author_df
author_df['author_gender']=author_gender
# Counting the author's genders
author_df.head()



get_ipython().run_cell_magic('nose', '', '\ndef len_authors():\n    return len(author_df[author_df.author_gender == "M"])\n\ndef test_num_males():\n    assert len_authors() == 191, \\\n        \'The number of Males (M) and Females (F) appear to be wrong. These are 191 and 395 respectively\'')

# Creating a list of unique years, sorted in ascending order.
years = sorted(author_df['Year'].unique())

# Initializing lists
males_by_yr = []
females_by_yr = []
unknown_by_yr = []

# Looping through years to find the number of male, female and unknown authors per year
for year in years:
    df= author_df[author_df['Year']==year]
    males_by_yr.append(len( df[ df['author_gender']=='M' ] ))
    females_by_yr.append(len( df[ df['author_gender']=='F' ] ))
    unknown_by_yr.append(len( df[ df['author_gender']=='Unknown' ] ))

# Printing out yearly values to examine changes over time
print(males_by_yr, females_by_yr, unknown_by_yr)


get_ipython().run_cell_magic('nose', '', '\ndef test_years():\n    correct_years = list(np.unique(author_df.Year))\n    assert list(years) == correct_years, \\\n    \'years should be the unique years in author_df["Year"] sorted in ascending order.\'\n\ndef test_gender_by_yr():\n    assert sum(males_by_yr)==191, \\\n    \'At least one of the lists (males_by_yr, females_by_yr, unknown_by_yr) contains an incorrect value.\'')


# Importing matplotlib
import matplotlib.pyplot as plt

# This makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Plotting the bar chart
plt.bar(years, unknown_by_yr)
# [OPTIONAL] - Setting a title, and axes labels
plt.title('unknown in each year')
plt.xlabel('year')
plt.ylabel('no. of unknowns')


get_ipython().run_cell_magic('nose', '', '\n# It\'s hard to test plots.\ndef test_nothing():\n    assert True, ""\n\n#def test_pos():\n#    assert  pos ==list(range(len(unknown_by_yr))) or pos== range(len(unknown_by_yr)) or pos==years, \\\n#    \'pos should be a list containing integer values with the same length as unknown_by_yr \'')


# Creating a new list, where 0.25 is added to each year
years_shifted = [x+0.25 for x in years]
print(years_shifted)

# Plotting males_by_yr by year
plt.bar(years, males_by_yr,width=0.25, color='blue')

# Plotting females_by_yr by years_shifte
plt.bar(years_shifted, females_by_yr,width=0.25, color='red')
# [OPTIONAL] - Adding relevant Axes labels and Chart Title
plt.title('Gender prediction using sound')
plt.xlabel('Years')
plt.ylabel('Nr of unknowns')



get_ipython().run_cell_magic('nose', '', "\ndef test_years_shifted():\n    correct_years_shifted = [year + 0.25 for year in years]\n    assert list(years_shifted) == correct_years_shifted, \\\n    'years_shifted should be like years but with 0.25 added to each year.'")

