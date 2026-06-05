import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
import os

os.makedirs('reports', exist_ok=True)

df = pd.read_csv('raw_data.csv')

plt.figure(figsize=(10, 6))
plt_sns.boxplot(x=df['Price'])
plt.title('Price Distribution Before Cleaning')
plt.savefig('reports/1_outliers_before.png')
plt.close()

df = df.drop_duplicates()

df['Category'] = df['Category'].fillna(df['Category'].mode()[0])
df['Price'] = df['Price'].fillna(df['Price'].median())
df['CustomerAge'] = df['CustomerAge'].fillna(df['CustomerAge'].median())

Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]

Q1_q = df['Quantity'].quantile(0.25)
Q3_q = df['Quantity'].quantile(0.75)
IQR_q = Q3_q - Q1_q
lower_bound_q = Q1_q - 1.5 * IQR_q
upper_bound_q = Q3_q + 1.5 * IQR_q
df = df[(df['Quantity'] >= lower_bound_q) & (df['Quantity'] <= upper_bound_q)]

df.to_csv('cleaned_data.csv', index=False)

plt.figure(figsize=(10, 6))
plt_sns.boxplot(x=df['Price'])
plt.title('Price Distribution After Cleaning')
plt.savefig('reports/2_outliers_after.png')
plt.close()

plt.figure(figsize=(10, 6))
plt_sns.countplot(data=df, x='Category', order=df['Category'].value_counts().index)
plt.title('Sales Count by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/3_sales_by_category.png')
plt.close()

plt.figure(figsize=(10, 6))
df['TotalSales'] = df['Quantity'] * df['Price']
plt_sns.barplot(data=df, x='Region', y='TotalSales', estimator=sum)
plt.title('Total Sales by Region')
plt.tight_layout()
plt.savefig('reports/4_sales_by_region.png')
plt.close()

plt.figure(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
numeric_df = df[numeric_cols].drop('TransactionID', axis=1, errors='ignore')
corr = numeric_df.corr()
plt_sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('reports/5_correlation_heatmap.png')
plt.close()
