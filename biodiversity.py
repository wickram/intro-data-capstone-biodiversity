
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

#Inspecing Species DataFrame

species = pd.read_csv('species_info.csv')

species_count = species.scientific_name.nunique()

species_type = species.category.unique()

#Analysis of Species Conversation Status

conservation_statuses = species.conservation_status.unique()

conservation_counts = species.groupby('conservation_status').scientific_name.nunique().reset_index()

species.fillna('No Intervention', inplace=True)

conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print conservation_counts_fixed

protection_counts = species.groupby('conservation_status') \
    .scientific_name.nunique().reset_index() \
    .sort_values(by='scientific_name')

print protection_counts


#Plotting Conservation Status by Species

plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts.conservation_status)), protection_counts.scientific_name)
ax.set_xticks(range(len(protection_counts.conservation_status)))
ax.set_xticklabels(protection_counts.conservation_status)
plt.ylabel("Number of Species")
plt.title("Conservation Status by Species")
plt.show()

#Investigating Endangered Species

species['is_protected'] = species.conservation_status != 'No Intervention'

category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

category_pivot = category_counts.pivot(columns='is_protected',
                                       index='category',
                                       values='scientific_name') \
    .reset_index()

category_pivot.columns = ['category', 'not_protected', 'protected']

category_pivot['percent_protected'] = category_pivot.protected / (
category_pivot.protected + category_pivot.not_protected)

print category_pivot

#Chi-Squared Test for Significance


contingency = [[30, 146], [75, 413]]

chi2, pval, dof, expected = chi2_contingency(contingency)

print pval

contingency2 = [[30, 146], [5, 73]]

chi2, pval_reptile_mammal, dof, expected = chi2_contingency(contingency2)

print pval_reptile_mammal

#Inpecting Observations DataFrame

observations = pd.read_csv('observations.csv')

print observations.head(10)

#Analysis of observations of Sheep

species['is_sheep'] = species['common_names'].apply(lambda x: True if x.find('Sheep') >= 0 else False)

species_is_sheep = species[species.is_sheep == True]

print species_is_sheep.head(5)

sheep_species = species_is_sheep = species[(species.is_sheep == True) & (species.category == 'Mammal')]

print sheep_species

#Merging Sheep and Observation DataFrames

sheep_observations = pd.merge(sheep_species, observations)

print sheep_observations.head(5)

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

print obs_by_park

print obs_by_park.head(5)

#Plotting Sheep Sightings

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park.park_name)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park.park_name)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel("Number of Observations")
plt.title("Observations of Sheep per Week")
plt.show()

print obs_by_park.observations.sum()
