import json
import csv
import pandas as pd
import openai
import yaml
 #2-13

#step back for factors; intial prompt inspired by https://arxiv.org/pdf/2306.05685
#  https://chat.openai.com/share/43894089-c8b4-48c5-b7f8-7a89f74083e7

singles_1=[
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'B', 'A', 'B',
    'A', 'A', 'B', 'B', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'B', 'B',
    'B', 'B', 'A', 'B', 'B',
    'B', 'B', 'A', 'B', 'A',
    'B', 'B', 'A', 'B', 'A',
    'A', 'A', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'A',
    'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'A', 'B', 'A', 'B',
    'B', 'A', 'B', 'A', 'A',
    'A', 'A', 'B', 'A', 'B',
    'B', 'B', 'A', 'B', 'B',
    'A', 'B', 'A', 'B', 'B'
]
print(len(singles_1))
count_A_1 = singles_1.count('A')
#https://chat.openai.com/share/93cca684-c6b6-418a-aecb-98ca43b82b47


singles_2=[
    "B", "A", "B", "B", "B", "A", "A", "A", "A", "B",
    "A", "A", "A", "B", "A", "A", "B", "A", "B", "B",
    "A", "B", "A", "B", "B", "A", "B", "A", "B", "B",
    "B", "A", "B", "A", "A", "B", "A", "A", "B", "B",
    "B", "A", "B", "B", "B", "A", "A", "B", "A", "B",
    "A", "B", "A", "B", "A", "A", "B", "B", "A", "A",
    "B", "A", "B", "B", "A", "A", "B", "B", "A", "B",
    "B", "A", "B", "B", "A", "B", "B", "B", "B", "A",
    "B", "B", "B", "A", "A", "B", "A", "A", "B", "B",
    "A", "A", "B", "B", "A", "B", "B", "A", "B", "B"
]
print(len(singles_2))
count_A_2 = singles_2.count('A')
#https://chat.openai.com/share/356aa522-619c-40e5-b24b-68403918e321



singles_3=[
    'A', 'B', 'A', 'B', 'B',  # Judgments for rows 0-4
    'A', 'B', 'B', 'A', 'A',  # Judgments for rows 5-9
    'B', 'A', 'A', 'B', 'A',  # Judgments for rows 10-14
    'A', 'A', 'B', 'B', 'A',  # Judgments for rows 15-19
    'A', 'B', 'A', 'A', 'A',  # Judgments for rows 20-24
    'B', 'B', 'A', 'A', 'B',  # Judgments for rows 25-29
    'A', 'B', 'B', 'A', 'A',  # Judgments for rows 30-34
    'A', 'B', 'A', 'B', 'A',  # Judgments for rows 35-39
    'B', 'B', 'A', 'B', 'A',  # Judgments for rows 40-44
    'A', 'A', 'B', 'A', 'B',  # Judgments for rows 45-49
    'A', 'A', 'B', 'A', 'B',  # Judgments for rows 50-54
    'A', 'B', 'A', 'B', 'A',  # Judgments for rows 55-59
    'A', 'B', 'A', 'B', 'B',  # Judgments for rows 60-64
    'B', 'A', 'A', 'B', 'A',  # Judgments for rows 65-69
    'B', 'A', 'A', 'B', 'A',  # Judgments for rows 70-74
    'B', 'A', 'B', 'A', 'B',  # Judgments for rows 75-79
    'A', 'A', 'B', 'B', 'A',  # Judgments for rows 80-84
    'B', 'A', 'B', 'A', 'B',  # Judgments for rows 85-89
    'A', 'B', 'A', 'A', 'B',  # Judgments for rows 90-94
    'B', 'A', 'B', 'A', 'A'   # Judgments for rows 95-99
]
print(len(singles_3))
count_A_3 = singles_3.count('A')
#https://chat.openai.com/share/f7a551b5-89ca-4aa4-815c-d2f56c4fac09



singles_4=[
    'B', 'B', 'B', 'B', 'B',
    'B', 'A', 'B', 'B', 'A',
    'B', 'A', 'A', 'A', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'A', 'A', 'B',
    'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'B',
    'B', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'A',
    'A', 'A', 'B', 'B', 'A',
    'B', 'B', 'A', 'B', 'A',
    'B', 'A', 'A', 'B', 'B',
    'A', 'A', 'B', 'B', 'A',
    'A', 'A', 'A', 'B', 'A',
    'B', 'B', 'B', 'B', 'B',
    'B', 'B', 'B', 'A', 'A',
    'A', 'B', 'B', 'B', 'B',
    'B', 'B', 'A', 'B', 'B'
]
print(len(singles_4))
count_A_4 = singles_4.count('A')
#https://chat.openai.com/share/3e59c144-ee13-4c51-8c3c-224bd73a51a5


singles_5=[
    'A', 'A', 'B', 'A', 'A', # 1-5
    'A', 'B', 'B', 'A', 'A', # 6-10
    'A', 'A', 'B', 'A', 'A', # 11-15
    'B', 'A', 'B', 'A', 'A', # 16-20
    'A', 'A', 'A', 'B', 'B', # 21-25
    'A', 'A', 'A', 'A', 'B', # 26-30
    'A', 'B', 'B', 'A', 'B', # 31-35
    'A', 'A', 'A', 'A', 'A', # 36-40
    'A', 'A', 'B', 'A', 'B', # 41-45
    'A', 'A', 'A', 'A', 'B', # 46-50
    'A', 'A', 'A', 'A', 'B', # 51-55
    'A', 'A', 'A', 'A', 'A', # 56-60
    'B', 'A', 'A', 'A', 'B', # 61-65
    'A', 'B', 'B', 'A', 'A', # 66-70
    'B', 'B', 'A', 'A', 'A', # 71-75
    'A', 'A', 'A', 'A', 'B', # 76-80
    'A', 'A', 'B', 'A', 'B', # 81-85
    'A', 'A', 'A', 'A', 'B', # 86-90
    'A', 'A', 'B', 'A', 'B', # 91-95
    'A', 'B', 'A', 'B', 'A'  # 96-100
]
print(len(singles_5))
count_A_5 = singles_5.count('A')
#https://chat.openai.com/share/eb9735a6-9713-4e40-8978-28e26fa51f4e


singles_6= [
    'A', 'A', 'B', 'A', 'A',
    'A', 'A', 'A', 'A', 'B',
    'A', 'A', 'B', 'B', 'B',
    'B', 'B', 'A', 'B', 'A',
    'A', 'A', 'A', 'A', 'A',
    'B', 'A', 'B', 'A', 'B',
    'A', 'A', 'A', 'B', 'B',
    'B', 'B', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'A', 'A', 'B', 'A', 'A',
    'A', 'B', 'B', 'B', 'B',
    'A', 'B', 'B', 'B', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'B', 'B', 'A',
    'A', 'A', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'B',
    'A', 'B', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'B',
    'A', 'B', 'A', 'B', 'B'
]
print(len(singles_6))
count_A_6 = singles_6.count('A')
#https://chat.openai.com/share/fc201b81-e464-4eb8-8193-8dda7b3cfc9c


singles_7=[
    "A", "B", "A", "B", "A",
    "B", "B", "A", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "A", "A", "B", "B",
    "A", "A", "B", "B", "A",
    "B", "A", "A", "B", "A",
    "A", "A", "B", "B", "A",
    "B", "A", "B", "A", "A",
    "A", "A", "A", "A", "B",
    "A", "A", "B", "A", "A",
    "B", "A", "A", "A", "A",
    "B", "B", "B", "A", "A",
    "A", "B", "A", "B", "A",
    "A", "B", "A", "A", "B",
    "B", "B", "B", "A", "A",
    "A", "B", "B", "B", "B",
    "B", "A", "B", "A", "A",
    "B", "A", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "A", "A", "A", "B"
]
print(len(singles_7))
count_A_7 = singles_7.count('A')
#https://chat.openai.com/share/e9b82ab2-38de-40d9-a3f5-ec8760a1e705

singles_8= [
    'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'A',
    'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'A',
    'B', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'B', 'A',
    'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B',
    'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'A', 'B',
    'B', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A',
    'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B'
]
print(len(singles_8))
count_A_8 = singles_8.count('A')
#https://chat.openai.com/share/86c883db-fc85-4a24-91e1-afb34159b0df

singles_9=[
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'A', 'A', 'A',
    'B', 'A', 'A', 'B', 'B',
    'A', 'B', 'A', 'B', 'A',
    'A', 'A', 'B', 'A', 'A',
    'B', 'B', 'A', 'A', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'A', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'A', 'B', 'A',
    'B', 'B', 'B', 'B', 'B',
    'B', 'A', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'A', 'A',
    'B', 'B', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'A',
    'A', 'A', 'A', 'B', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'A', 'A'
]
print(len(singles_9))
count_A_9 = singles_9.count('A')
#https://chat.openai.com/share/246a2b45-b499-4ab5-a5b6-7896f07457d9

singles_10=[
    "B", "A", "A", "B", "A",
    "A", "A", "B", "A", "B",
    "A", "A", "B", "A", "A",
    "B", "B", "A", "B", "A",
    "B", "B", "B", "B", "B",
    "A", "A", "A", "B", "A",
    "B", "A", "B", "B", "A",
    "B", "A", "A", "A", "B",
    "B", "B", "A", "A", "A",
    "A", "B", "B", "A", "B",
    "B", "A", "A", "A", "B",
    "A", "B", "B", "B", "B",
    "A", "B", "A", "A", "A",
    "B", "A", "B", "B", "A",
    "A", "A", "B", "A", "B",
    "B", "A", "B", "B", "B",
    "B", "A", "B", "A", "B",
    "B", "A", "A", "B", "A",
    "A", "B", "A", "A", "B",
    "B", "A", "A", "B", "B"
]

print(len(singles_10))
count_A_10 = singles_10.count('A')
#https://chat.openai.com/share/0982086a-82c9-4376-8a21-9b62a51237ab


singles_11=[
    'A', 'A', 'A', 'A', 'A', # 1-5
    'A', 'B', 'B', 'A', 'B', # 6-10
    'A', 'A', 'B', 'B', 'A', # 11-15
    'A', 'B', 'B', 'B', 'A', # 16-20
    'A', 'B', 'A', 'A', 'B', # 21-25
    'A', 'B', 'A', 'B', 'A', # 26-30
    'B', 'A', 'B', 'B', 'A', # 31-35
    'A', 'A', 'A', 'B', 'B', # 36-40
    'A', 'A', 'B', 'B', 'B', # 41-45
    'B', 'A', 'B', 'A', 'B', # 46-50
    'A', 'B', 'A', 'A', 'A', # 51-55
    'A', 'B', 'B', 'A', 'A', # 56-60
    'B', 'B', 'A', 'A', 'A', # 61-65
    'B', 'A', 'B', 'A', 'B', # 66-70
    'A', 'B', 'A', 'A', 'A', # 71-75
    'A', 'B', 'A', 'A', 'B', # 76-80
    'A', 'A', 'B', 'B', 'A', # 81-85
    'B', 'B', 'A', 'B', 'A', # 86-90
    'B', 'A', 'A', 'B', 'B', # 91-95
    'A', 'B', 'B', 'B', 'B'  # 96-100
]
print(len(singles_11))
count_A_11 = singles_11.count('A')
#https://chat.openai.com/share/c40158d0-f59a-438d-bc65-b719eea99771


singles_12=[
    'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'B', 'A', 'B', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'B', 'A',
    'A', 'A', 'B', 'B', 'B',
    'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'A', 'B', 'A',
    'A', 'A', 'A', 'B', 'B',
    'B', 'A', 'B', 'A', 'A',
    'A', 'A', 'A', 'B', 'A',
    'A', 'B', 'B', 'B', 'B',
    'B', 'A', 'B', 'B', 'A',
    'B', 'B', 'B', 'B', 'A',
    'A', 'A', 'B', 'A', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'B', 'A', 'B',
    'B', 'B', 'A', 'A', 'B',
    'A', 'A', 'B', 'B', 'A',
    'B', 'B', 'B', 'B', 'A'
]
print(len(singles_12))
count_A_12 = singles_12.count('A')
#https://chat.openai.com/share/aec9f10e-9f70-460f-9899-7353828a4278


singles_13=[
    'B', 'A', 'B', 'A', 'A',
    'B', 'B', 'B', 'A', 'B',
    'A', 'B', 'A', 'B', 'B',
    'B', 'A', 'B', 'B', 'A',
    'B', 'B', 'A', 'B', 'B',
    'A', 'B', 'B', 'B', 'B',
    'A', 'B', 'A', 'B', 'A',
    'A', 'A', 'B', 'A', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'A', 'A', 'B', 'A',
    'B', 'B', 'B', 'B', 'B',
    'A', 'B', 'B', 'A', 'A',
    'A', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'B', 'B',
    'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'B'
]
print(len(singles_13))
count_A_13 = singles_13.count('A')
#https://chat.openai.com/share/45efc8b7-c250-4f9e-ac13-96cd7f683c96




singles_14= [
    'A', 'A', 'B', 'A', 'A',
    'B', 'B', 'A', 'A', 'A',
    'A', 'B', 'A', 'B', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'B', 'B', 'A', 'A',
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'B',
    'B', 'B', 'B', 'A', 'B',
    'A', 'A', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'A', 'A', 'B',
    'B', 'B', 'A', 'A', 'B',
    'B', 'A', 'A', 'A', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'B',
    'A', 'A', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'A',
    'B', 'B', 'A', 'B', 'A'
]
print(len(singles_14))
count_A_14 = singles_14.count('A')
#https://chat.openai.com/share/2f141469-41ea-4d42-8457-5bf2775dd4fa


singles_15= [
    'B', 'B', 'A', 'A', 'A',
    'B', 'A', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'B',
    'B', 'A', 'B', 'A', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'A', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'B',
    'B', 'B', 'B', 'B', 'B',
    'B', 'B', 'A', 'A', 'A',
    'A', 'A', 'A', 'B', 'A',
    'B', 'A', 'A', 'B', 'B',
    'A', 'A', 'A', 'A', 'B',
    'B', 'B', 'A', 'B', 'B'
]

print(len(singles_15))
count_A_15 = singles_15.count('A')
#https://chat.openai.com/share/3e2e1537-2d9d-4f37-8bd2-d3472421f39e

singles_16= [
    'A', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'A', 'B',
    'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B',
    'A', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'A',
    'A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B',
    'A', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'A'
]
print(len(singles_16))
count_A_16 = singles_16.count('A')
#https://chat.openai.com/share/79f27185-bfac-4820-86ef-999d458d7fca

singles_17= [
    'A', 'A', 'B', 'A', 'B', # 1-5
    'B', 'A', 'B', 'B', 'A', # 6-10
    'B', 'A', 'B', 'B', 'A', # 11-15
    'A', 'A', 'B', 'A', 'B', # 16-20
    'A', 'B', 'B', 'A', 'A', # 21-25
    'B', 'A', 'A', 'B', 'B', # 26-30
    'A', 'B', 'A', 'B', 'A', # 31-35
    'A', 'B', 'A', 'B', 'A', # 36-40
    'B', 'A', 'B', 'A', 'B', # 41-45
    'A', 'B', 'A', 'A', 'B', # 46-50
    'B', 'A', 'A', 'B', 'A', # 51-55
    'B', 'A', 'B', 'A', 'B', # 56-60
    'A', 'A', 'B', 'B', 'A', # 61-65
    'A', 'B', 'B', 'A', 'B', # 66-70
    'A', 'B', 'A', 'A', 'B', # 71-75
    'A', 'B', 'B', 'A', 'A', # 76-80
    'B', 'A', 'B', 'B', 'A', # 81-85
    'B', 'A', 'B', 'A', 'B', # 86-90
    'A', 'B', 'A', 'B', 'A', # 91-95
    'B', 'A', 'B', 'A', 'B'  # 96-100
]
print(len(singles_17))
count_A_17 = singles_17.count('A')
#https://chat.openai.com/share/a8036b38-1563-4722-b4a4-2f4954355902


singles_18=  [
    'B', 'B', 'A', 'A', 'B', # 1-5
    'A', 'A', 'B', 'A', 'A', # 6-10
    'B', 'B', 'A', 'B', 'B', # 11-15
    'A', 'A', 'B', 'A', 'B', # 16-20
    'B', 'B', 'A', 'B', 'A', # 21-25
    'B', 'A', 'A', 'A', 'A', # 26-30
    'B', 'A', 'A', 'B', 'A', # 31-35
    'B', 'B', 'B', 'A', 'B', # 36-40
    'A', 'B', 'A', 'A', 'B', # 41-45
    'B', 'B', 'A', 'A', 'A', # 46-50
    'A', 'A', 'B', 'B', 'A', # 51-55
    'A', 'B', 'A', 'A', 'B', # 56-60
    'A', 'A', 'A', 'B', 'B', # 61-65
    'A', 'B', 'B', 'A', 'A', # 66-70
    'A', 'B', 'A', 'B', 'B', # 71-75
    'A', 'A', 'B', 'B', 'B', # 76-80
    'A', 'B', 'A', 'B', 'A', # 81-85
    'B', 'A', 'A', 'A', 'B', # 86-90
    'A', 'A', 'B', 'A', 'A', # 91-95
    'B', 'B', 'A', 'B', 'A'  # 96-100
]
print(len(singles_18))
count_A_18 = singles_18.count('A')
#https://chat.openai.com/share/a18735e6-5953-48e3-9847-f086c3ff4ffe


singles_19= ['B', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'A',
 'A', 'B', 'A', 'A', 'B', 'B', 'A', 'B', 'A', 'B',
 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'A',
 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'B',
 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'A',
 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'B', 'A', 'B',
 'A', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'B']

print(len(singles_19))
count_A_19 = singles_19.count('A')
#https://chat.openai.com/share/a47cd107-c916-411c-827b-1ed1e5ca758c


singles_20= [
    'A', 'A', 'B', 'A', 'A',
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'A',
    'A', 'A', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'B',
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'B',
    'A', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'B',
    'A', 'A', 'B', 'A', 'B'
]


print(len(singles_20))
count_A_20 = singles_20.count('A')
#https://chat.openai.com/share/ff9091e9-1e16-412b-8779-55fd91ae506d

singles_21= [
    'B', 'A', 'A', 'B', 'B',  # 1-5
    'A', 'B', 'A', 'B', 'A',  # 6-10
    'B', 'B', 'A', 'A', 'B',  # 11-15
    'A', 'A', 'A', 'A', 'B',  # 16-20
    'A', 'A', 'B', 'A', 'A',  # 21-25
    'B', 'B', 'A', 'B', 'B',  # 26-30
    'A', 'B', 'B', 'A', 'A',  # 31-35
    'B', 'B', 'B', 'B', 'A',  # 36-40
    'A', 'B', 'A', 'A', 'A',  # 41-45
    'B', 'A', 'B', 'B', 'A',  # 46-50
    'B', 'B', 'A', 'A', 'B',  # 51-55
    'A', 'B', 'A', 'B', 'A',  # 56-60
    'A', 'B', 'A', 'B', 'A',  # 61-65
    'A', 'B', 'B', 'B', 'A',  # 66-70
    'B', 'A', 'A', 'A', 'B',  # 71-75
    'A', 'B', 'B', 'B', 'A',  # 76-80
    'B', 'A', 'B', 'A', 'A',  # 81-85
    'B', 'A', 'A', 'B', 'B',  # 86-90
    'B', 'B', 'B', 'B', 'A',  # 91-95
    'B', 'A', 'A', 'A', 'A'   # 96-100
]


print(len(singles_21))
count_A_21 = singles_21.count('A')
#https://chat.openai.com/share/4d31d3f4-3fc5-4d14-b47d-f43cf359be2b


singles_22= ['A', 'B', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B',
 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B',
 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'A',
 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'A',
 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B',
 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'A',
 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'A',
 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'B',
 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A']

print(len(singles_22))
count_A_22 = singles_22.count('A')
#https://chat.openai.com/share/54681926-caba-47cd-b902-036fcfbc3dfe

singles_23= [
    'A', 'B', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'A', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'A', 'B',
    'A', 'B', 'A', 'A', 'B',
    'A', 'B', 'A', 'B', 'A',
    'B', 'B', 'A', 'A', 'B',
    'A', 'B', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'A',
    'A', 'B', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'B',
    'A', 'B', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'B', 'A',
    'A', 'A', 'A', 'A', 'A',
    'B', 'A', 'B', 'A', 'B'
]

print(len(singles_23))
count_A_23 = singles_23.count('A')
#https://chat.openai.com/share/08e82c55-8032-4b76-a2e9-33b786de0caf

singles_24= [
    'A', 'B', 'A', 'A', 'A',
    'B', 'B', 'B', 'A', 'B',
    'A', 'B', 'A', 'A', 'A',
    'B', 'A', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'A', 'A', 'B', 'A',
    'A', 'A', 'A', 'A', 'A',
    'B', 'A', 'A', 'A', 'B',
    'B', 'B', 'A', 'B', 'A',
    'A', 'A', 'B', 'A', 'A',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'B', 'A',
    'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'A', 'A', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'A', 'A', 'B', 'A',
    'A', 'A', 'B', 'A', 'A'
]


print(len(singles_24))
count_A_24 = singles_24.count('A')
#https://chat.openai.com/share/9373196d-3af0-460c-b388-2904c87245f3



singles_25=[
    'B', 'B', 'A', 'B', 'A',
    'B', 'A', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'A',
    'B', 'A', 'A', 'B', 'B',
    'B', 'B', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'B', 'A', 'B',
    'B', 'B', 'B', 'A', 'A',
    'A', 'A', 'A', 'B', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'A',
    'A', 'A', 'A', 'A', 'A',
    'A', 'B', 'B', 'B', 'A',
    'A', 'B', 'B', 'B', 'B',
    'B', 'B', 'B', 'A', 'A',
    'A', 'B', 'A', 'B', 'B',
    'B', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'A', 'A',
    'A', 'A', 'A', 'B', 'A'
]
print(len(singles_25))
count_A_25 = singles_25.count('A')
#https://chat.openai.com/share/88baa8f7-b5d3-4dfe-b194-406f5e953281


singles_26= [
    'A', 'A', 'A', 'A', 'B',
    'A', 'A', 'A', 'A', 'A',
    'B', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B',
    'A', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'A', 'B',
    'B', 'A', 'B', 'B', 'A',
    'A', 'A', 'A', 'A', 'B',
    'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'B',
    'B', 'B', 'A', 'A', 'B',
    'A', 'B', 'A', 'B', 'A',
    'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'A', 'B', 'B',
    'A', 'B', 'B', 'B', 'A',
    'B', 'A', 'B', 'A', 'B',
    'B', 'A', 'A', 'A', 'A',
    'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'A'
]
print(len(singles_26))
count_A_26 = singles_26.count('A')
#https://chat.openai.com/share/aec9f10e-9f70-460f-9899-7353828a4278

singles_27= [
    'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A',
    'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'A',
    'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B',
    'B', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'A',
    'B', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'A',
    'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'A'
]
print(len(singles_27))
count_A_27 = singles_27.count('A')
#https://chat.openai.com/share/a9c5ee7c-349f-46f4-81ea-e1e5fb455908





list_count=27
all_singles = []

# Loop through lists dynamically
for i in range(1, list_count+ 1):
    list_name = f"singles_{i}"
    current_list = globals()[list_name]  # Accessing lists dynamically
    all_singles.extend(current_list)

count_A_all =all_singles.count('A')
count_B_all =all_singles.count('B')
#53,4% f. A (rules)
#46,6% f. B (llama3)


with open('LetAIEntertainYou/combined_strings.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Strings'])
    writer.writerows([[string] for string in all_singles])




df=pd.read_csv('LetAIEntertainYou/Posts/current/chunks/reverse_fullprompt/output_2.csv', sep=';', encoding='iso-8859-1')



functions = [
    {
        "name": "compare_subject_lines",
        "description": "A function asses which subject line is more engaging, meaning a user is more likely to click on: subject_line_a or subject_line_b. it evaluates like a human would and focuses on on factors like engagement, specificity, urgency, and relevance",
        "parameters": {
            "type": "object",
            "properties": {
                "letter": {
                    "type": "string",
                    "description": "the letter of the winning subject line, 'A' or 'B' only"
                }
            },
            "required": ["subject_line_a", "subject_line_b",'letter']
        }
        }
    ]

openai.api_key = yaml.safe_load(open("./LetAIEntertainYou/config.yml")).get('KEYS', {}).get('openai')
list_neu=[]
for r in df.values:
    print(r[0])
    subject_line_a =r[0]
    subject_line_b =r[1]
    response = openai.ChatCompletion.create(
        model='gpt-4-turbo',
        messages=[
            {'role': 'user',
            'content': f"compare_subject_lines {subject_line_a} and {subject_line_b}"}
             ],
             functions=functions,
             function_call={'name': 'compare_subject_lines'}
         )
    output = json.loads(response['choices'][0]['message']['function_call']['arguments'])
    try:
        letter = output['letter']
    except:
        print(output)
    print(letter)
    list_neu.append(letter)
print('fertig')

asa=0
for str in list_neu:
    if 'A' in str:
        asa=asa+1


