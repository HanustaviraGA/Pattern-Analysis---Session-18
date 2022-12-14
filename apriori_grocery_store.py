# -*- coding: utf-8 -*-
"""Apriori - Grocery Store.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kMpjVCAazbLYPm0IYzldh4HP_bDfnVaU

Mengimport library yang dibutuhkan dan menautkan Google Drive
"""

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from google.colab import drive
drive.mount('/content/drive')

"""Membuka dan memproses dataset"""

data = pd.read_excel('/content/drive/My Drive/PatternAnalysis/Online_Retail.xlsx')
data.head()

"""Mengeksplorasi kolom pada dataset"""

data.columns

"""Mengeksplorasi region/negara yang unik di setiap transaksinya"""

data.Country.unique()

"""Data cleaning"""

# Menghapus spasi tambahan pada deskripsi
data['Description'] = data['Description'].str.strip()
  
# Menghapus baris yang tidak terdapat nomor invoice
data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True)
data['InvoiceNo'] = data['InvoiceNo'].astype('str')
  
# Menghapus transaksi yang dilakukan secara kredit
data = data[~data['InvoiceNo'].str.contains('C')]

"""Splitting data berdasarkan region/negara asal transaksi"""

# Transaksi yang dilakukan di Perancis / France
basket_France = (data[data['Country'] =="France"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

# Transaksi yang dilakukan di Inggris / United Kingdom
basket_UK = (data[data['Country'] =="United Kingdom"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

# Transaksi yang dilakukan di Portugis / Portugal
basket_Por = (data[data['Country'] =="Portugal"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

# Transaksi yang dilakukan di Swedia / Sweden
basket_Sweden = (data[data['Country'] =="Sweden"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

"""Data encoding"""

# Membuat hot encode untuk menyesuaikan dengan library yang digunakan
def hot_encode(x):
	if(x<= 0):
		return 0
	if(x>= 1):
		return 1

# Encoding dataset
basket_encoded = basket_France.applymap(hot_encode)
basket_France = basket_encoded

basket_encoded = basket_UK.applymap(hot_encode)
basket_UK = basket_encoded

basket_encoded = basket_Por.applymap(hot_encode)
basket_Por = basket_encoded

basket_encoded = basket_Sweden.applymap(hot_encode)
basket_Sweden = basket_encoded

"""Membuat model dan analisa hasil

Perancis / France
"""

# Bentuk model
frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True)
  
# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Dari hasil diatas dapat terlihat bahwa cangkir kertas dan kertas, serta piring dibeli secara bersamaan di Perancis. Mengingat budaya Perancis yang sering berkumpul bersama keluarga setidaknya sekali dalam seminggu. Dan juga pemerintah Perancis telah melarang penggunaan plastik di negara tersebut, sehingga warga harus membeli dengan bahan kertas sebagai alternatif

Inggris / United Kingdom
"""

# Bentuk model
frq_items = apriori(basket_UK, min_support = 0.01, use_colnames = True)

# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Jika aturan transaksi Inggris dianalisis lebih dalam, terlihat bahwa orang Inggris membeli piring teh berwarna berbeda secara bersamaan. Alasan di balik ini mungkin karena biasanya orang Inggris sangat menikmati teh dan sering mengumpulkan piring teh dengan warna berbeda untuk berbagai kesempatan.

Portugis / Portugal
"""

# Bentuk model
frq_items = apriori(basket_Por, min_support = 0.05, use_colnames = True)

# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Saat menganalisis aturan asosiasi untuk transaksi Portugis, diamati bahwa set Tiffin (Knick Knack Tins) dan pensil warna. Kedua produk ini biasanya milik anak sekolah dasar. Kedua produk ini dibutuhkan oleh anak-anak di sekolah untuk membawa bekal dan untuk berkreasi masing-masing sehingga secara logis masuk akal untuk dipasangkan bersama.

Swedia / Sweden
"""

# Bentuk model
frq_items = apriori(basket_Sweden, min_support = 0.05, use_colnames = True)

# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Setelah menganalisis aturan di atas, ditemukan bahwa peralatan makan anak laki-laki dan perempuan dipasangkan bersama. Ini masuk akal karena ketika orang tua pergi berbelanja peralatan makan untuk anak-anaknya, dia ingin produknya sedikit disesuaikan dengan keinginan anak."""