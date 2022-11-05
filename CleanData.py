import pandas as pd
from itertools import permutations

food = pd.read_csv('./data/Food.csv')[['id', 'name', 'name_scientific', 'description', 'food_group', 'food_subgroup']]
content = pd.read_csv('./data/Content.csv')[['source_type', 'food_id', 'orig_food_common_name', 'orig_food_part', 'orig_source_name',
       'orig_content', 'orig_min','orig_max', 'orig_unit']]
content.rename(columns={'food_id':'id'}, inplace= True)
# print(content.columns)
content2=content.query("source_type == 'Nutrient'")
count = content2[['orig_source_name']].nunique() #55 de valori unice la orig_source_name cand source_type = Nutrient ;                           
# print(content2)                                #10000 de valori unice la orig_source_name cand source_type = Compound
# print(count)
# print(content2.orig_source_name.unique())  #unique nutrients  ; din 56 numai vreo 5-6 sunt cunoscuti
freq = content2['orig_source_name'].value_counts()
print(freq)
freq.to_excel('frequencytableNutrients.xlsx')

# # creaza un for care sa i-a valorile unice ale source type si face frecventele pentru orig_source_name
# for source_type.unique() in source_type :
#     content2 = content.query(f"source_type == {source_type.unique()}")
#     freq= content2['orig_source_name'].value_counts()
#     freq.to_excel(f'frequencytable{source_type.unique()}.xlsx')
# Ceva de genul de mai sus


dataset = content.join(food, on='id', how='outer', lsuffix='l_', rsuffix='r_')

ds_final = pd.DataFrame()
ds_final['ID'] = dataset['id']
ds_final['Name'] = dataset['orig_food_common_name']
ds_final['Category'] = dataset['food_group']
ds_final['Sub-Category'] = dataset['food_subgroup']
ds_final['Nutrient'] = dataset['orig_source_name']
ds_final['Quantity'] = dataset['orig_content'] / 1000
ds_final['Description'] = dataset['description']

ds_final = ds_final.reset_index(drop=True)
ds_final['Nutrient'] = ds_final['Nutrient'].str.lower()
ds_final = ds_final.dropna(how='any')

accepted = ['protein', 'carbohydrate', 'vitamin', 'energy','fat','fatty', '16:0', 'fiber', 'calcium', 'copper', 'fluoride', 'iron', 'magnesium', 'riboflavin','folic acid', 'folate', 'sugars', 'retinol', 'carotene', 'sucrose', 'fructose', 'glucose', 'Maltose', 'Lactose', 'phosphorus', 'potassium', 'selenium', 'sodium', 'zinc', 'ash', 'cholesterol','niacin', 'water']
rejected = ['carbohydrate, by difference', 'protein, total-n', 'carbohydrates, total available, ']
accepted = '|'.join(accepted)
rejected = '|'.join(rejected)

ds_final = ds_final.loc[ds_final['Nutrient'].str.contains(accepted)]
ds_final = ds_final.loc[~ds_final['Nutrient'].str.contains(rejected)]

ds_final.to_csv('FinalData.csv')
# unique_nutr_vals = ds_final['Nutrient'].unique()
# for perm in permutations(unique_nutr_vals, 2):
# 	print(perm)

print(ds_final)

print(ds_final['Nutrient'].value_counts())
ds_final['Nutrient'].value_counts().to_excel('NewNutri.xlsx')
# if ds_final['Nutrient'].value_counts() <50:
#     delete