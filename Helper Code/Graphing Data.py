import matplotlib.pyplot as plt
import csv
import seaborn as sns
import numpy as np

alphas = []
phis = []
thetas = []
betas = []

# Retrieve saved data
with open('../Old files/model_samples_0.csv') as samples:
    reader = csv.reader(samples, delimiter=',')
    l = list(reader)
    title_line = l[25]
    last_line = l[-6]
    alphas = last_line[7:97]
    phis = last_line[97:187]
    thetas = last_line[187:24476]
    betas = last_line[24476:48765]

numeric_phis = [float(i) for i in phis]
numeric_thetas = [float(i) for i in thetas]
# plt.figure(figsize=(10, 10))
# plt.locator_params(axis='x', nbins=10)
# plt.hist(numeric_thetas, bins=90)
# plt.show()

sns.set_theme()
plot = sns.kdeplot()
plot.set_xlabel('Estimated Ideologies')
plot.set_ylabel('Density')
sns.kdeplot(data=numeric_phis, bw=0.5, label='Political Actors')
sns.kdeplot(data=numeric_thetas, bw=0.5, label='Followers')
plot.legend()
plt.show()

print("MEAN FOLLOWER IDEOLOGIES", np.mean(numeric_thetas))
print("MEAN ELITE IDEOLOGIES", np.mean(numeric_phis))