import seaborn as sns
import pandas as pd

f = open('data', 'r')
d = {}
tot,v1,v2,v3,v4,v5 = [], [], [], [], [], []
v6,v7,v8,v9,v10 = [], [], [], [], []

for line in f:
    line=line.split()
    tot.append(int(line[0]))
    v1.append(int(line[1])/int(line[0])*100)
    v2.append(int(line[2])/int(line[0])*100)
    v3.append(int(line[3])/int(line[0])*100)
    v4.append(int(line[4])/int(line[0])*100)
    v5.append(int(line[5])/int(line[0])*100)
    v6.append(int(line[6])/int(line[0])*100)
    v7.append(int(line[7])/int(line[0])*100)
    v8.append(int(line[8])/int(line[0])*100)
    v9.append(int(line[9])/int(line[0])*100)
    v10.append(int(line[10])/int(line[0])*100)
    
df = pd.DataFrame(list(zip(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10)),                        columns = ['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10'])
df2 = pd.DataFrame(list(zip(v3,v4,v5,v6,v7,v8,v9,v10)),                        columns = ['V3','V4','V5','V6','V7','V8','V9','V10'])

sns.set_style('whitegrid')
df = df.melt(var_name='groups', value_name='Percentage(%)')
ax = sns.violinplot(x=df['groups'], y=df['Percentage(%)'], palette='Set3')
ax.figure.savefig('violine.png')


