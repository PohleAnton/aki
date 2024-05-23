import csv
import pandas as pd

singles_1=['B', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
print(len(singles_1))
count_A_1 = singles_1.count('A')
#https://chat.openai.com/share/7c7f7aad-89e8-46f5-8517-426044bb1b77

singles_2=['A', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'B', 'B']

print(len(singles_2))
count_A_2 = singles_2.count('A')
#https://chat.openai.com/share/b9a7da3e-9ddf-43d0-9577-6780e04227b2


singles_3=[
    'A', 'A', 'A', 'B', 'A',  # Entries 1-5
    'B', 'A', 'B', 'A', 'B',  # Entries 6-10
    'B', 'A', 'A', 'B', 'A',  # Entries 11-15
    'B', 'A', 'B', 'A', 'B',  # Entries 16-20
    'B', 'A', 'B', 'A', 'B',  # Entries 21-25
    'A', 'B', 'A', 'B', 'A',  # Entries 26-30
    'A', 'B', 'A', 'B', 'A',  # Entries 31-35
    'B', 'A', 'B', 'A', 'B',  # Entries 36-40
    'A', 'A', 'B', 'B', 'A',  # Entries 41-45
    'B', 'A', 'B', 'A', 'B',  # Entries 46-50
    'A', 'B', 'A', 'B', 'A',  # Entries 51-55
    'B', 'A', 'B', 'A', 'B',  # Entries 56-60
    'A', 'B', 'A', 'B', 'A',  # Entries 61-65
    'B', 'A', 'B', 'A', 'B',  # Entries 66-70
    'A', 'B', 'A', 'B', 'A',  # Entries 71-75
    'A', 'B', 'A', 'B', 'A',  # Entries 76-80
    'B', 'A', 'B', 'A', 'B',  # Entries 81-85
    'A', 'B', 'A', 'B', 'A',  # Entries 86-90
    'B', 'A', 'B', 'A', 'B',  # Entries 91-95
    'A', 'A', 'B', 'B', 'A'   # Entries 96-100
]
print(len(singles_3))
count_A_3 = singles_3.count('A')
#https://chat.openai.com/share/f62548fd-4ec7-4e16-9dd9-f834eaa3c130

singles_4= [
    "A", "A", "A", "B", "B",  # 1-5
    "B", "A", "B", "B", "A",  # 6-10
    "A", "A", "B", "B", "A",  # 11-15
    "A", "B", "A", "B", "B",  # 16-20
    "A", "B", "B", "A", "B",  # 21-25
    "A", "B", "B", "B", "B",  # 26-30
    "A", "A", "A", "B", "B",  # 31-35
    "B", "A", "B", "B", "A",  # 36-40
    "A", "A", "B", "B", "A",  # 41-45
    "A", "B", "A", "B", "B",  # 46-50
    "A", "B", "B", "A", "B",  # 51-55
    "A", "B", "B", "B", "B",  # 56-60
    "A", "A", "A", "B", "B",  # 61-65
    "B", "A", "B", "B", "A",  # 66-70
    "A", "A", "B", "B", "A",  # 71-75
    "A", "B", "A", "B", "B",  # 76-80
    "A", "B", "B", "A", "B",  # 81-85
    "A", "B", "B", "B", "B",  # 86-90
    "A", "A", "A", "B", "B",  # 91-95
    "B", "A", "B", "B", "A"   # 96-100
]
print(len(singles_4))
count_A_4 = singles_4.count('A')
#https://chat.openai.com/share/2dbc4964-b5c3-4e1c-bdce-99c3456a0285


singles_5= [
    'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'A',
    'B', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'A',
    'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'A'
]

print(len(singles_5))
count_A_5 = singles_5.count('A')
#https://chat.openai.com/share/751ebc88-6dff-499e-9835-f51e6311709e


singles_6= [
    "B", "A", "A", "B", "B", "B", "B", "A", "A", "A",
    "A", "A", "A", "B", "B", "B", "B", "A", "B", "B",
    "B", "B", "A", "B", "A", "A", "B", "A", "B", "A",
    "A", "B", "B", "B", "B", "B", "A", "A", "B", "B",
    "A", "B", "A", "B", "B", "B", "B", "B", "A", "A",
    "B", "A", "B", "A", "B", "B", "A", "A", "B", "A",
    "A", "A", "A", "B", "A", "B", "A", "A", "B", "A",
    "B", "A", "A", "B", "B", "B", "A", "B", "A", "B",
    "A", "A", "A", "A", "A", "B", "B", "A", "B", "B",
    "B", "A", "A", "B", "B", "A", "B", "B", "B", "A"
]



print(len(singles_6))
count_A_6 = singles_6.count('A')
#https://chat.openai.com/share/adcdbd52-0358-4691-984b-52098f21cb3a




singles_7= ['B', 'A', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', # 1-10
             'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', # 11-20
             'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', # 21-30
             'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', # 31-40
             'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', # 41-50
             'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', # 51-60
             'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', # 61-70
             'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', # 71-80
             'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', # 81-90
             'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B']

print(len(singles_7))
count_A_7 = singles_7.count('A')
#https://chat.openai.com/share/2a1f6ef5-52e5-4e56-83e1-f3dca6ef3a54

singles_8= [
    'B', 'A', 'B', 'B', 'B', # 1-5
    'A', 'B', 'A', 'A', 'B', # 6-10
    'A', 'A', 'B', 'A', 'B', # 11-15
    'B', 'B', 'B', 'B', 'A', # 16-20
    'A', 'A', 'B', 'B', 'B', # 21-25
    'A', 'A', 'A', 'B', 'B', # 26-30
    'B', 'B', 'A', 'B', 'A', # 31-35
    'B', 'A', 'A', 'A', 'B', # 36-40
    'B', 'A', 'B', 'B', 'A', # 41-45
    'A', 'B', 'B', 'A', 'B', # 46-50
    'B', 'A', 'A', 'A', 'B', # 51-55
    'A', 'B', 'B', 'A', 'B', # 56-60
    'A', 'A', 'A', 'B', 'B', # 61-65
    'A', 'B', 'B', 'B', 'A', # 66-70
    'A', 'B', 'A', 'B', 'B', # 71-75
    'A', 'B', 'A', 'A', 'B', # 76-80
    'A', 'A', 'B', 'A', 'A', # 81-85
    'B', 'B', 'B', 'B', 'A', # 86-90
    'A', 'B', 'A', 'A', 'A', # 91-95
    'A', 'B', 'B', 'A', 'B'  # 96-100
]

print(len(singles_8))
count_A_8 = singles_8.count('A')
#https://chat.openai.com/share/0da8f786-ad88-4c42-8ac2-468ac3768a56


singles_9= [
    'B', 'B', 'A', 'B', 'B',  # Pairs 1-5
    'B', 'A', 'B', 'A', 'A',  # Pairs 6-10
    'A', 'B', 'A', 'B', 'A',  # Pairs 11-15
    'B', 'A', 'B', 'A', 'B',  # Pairs 16-20
    'B', 'A', 'B', 'A', 'A',  # Pairs 21-25
    'B', 'A', 'B', 'A', 'B',  # Pairs 26-30
    'A', 'B', 'A', 'B', 'A',  # Pairs 31-35
    'B', 'A', 'B', 'A', 'B',  # Pairs 36-40
    'A', 'B', 'A', 'B', 'A',  # Pairs 41-45
    'B', 'A', 'B', 'A', 'B',  # Pairs 46-50
    'A', 'B', 'A', 'B', 'A',  # Pairs 51-55
    'B', 'A', 'B', 'A', 'B',  # Pairs 56-60
    'A', 'B', 'A', 'B', 'A',  # Pairs 61-65
    'B', 'A', 'B', 'A', 'B',  # Pairs 66-70
    'A', 'B', 'A', 'B', 'A',  # Pairs 71-75
    'B', 'A', 'B', 'A', 'B',  # Pairs 76-80
    'A', 'B', 'A', 'B', 'A',  # Pairs 81-85
    'B', 'A', 'B', 'A', 'B',  # Pairs 86-90
    'A', 'B', 'A', 'B', 'A',  # Pairs 91-95
    'B', 'A', 'B', 'A', 'B'   # Pairs 96-100
]

print(len(singles_9))
count_A_9 = singles_9.count('A')
#https://chat.openai.com/share/13346d16-ee79-4551-9c3b-b6a6e3c0b6f5

singles_10= [
    "A", "B", "A", "A", "B",  # 1-5
    "B", "A", "B", "B", "A",  # 6-10
    "B", "A", "A", "A", "B",  # 11-15
    "A", "B", "A", "B", "A",  # 16-20
    "B", "B", "B", "B", "A",  # 21-25
    "A", "A", "B", "A", "B",  # 26-30
    "A", "B", "A", "B", "B",  # 31-35
    "A", "A", "B", "A", "A",  # 36-40
    "A", "B", "A", "A", "A",  # 41-45
    "B", "A", "A", "A", "B",  # 46-50
    "A", "B", "B", "B", "A",  # 51-55
    "A", "B", "A", "B", "B",  # 56-60
    "B", "B", "A", "A", "B",  # 61-65
    "B", "A", "A", "B", "A",  # 66-70
    "A", "A", "B", "A", "B",  # 71-75
    "A", "A", "B", "B", "B",  # 76-80
    "A", "A", "A", "A", "A",  # 81-85
    "B", "A", "A", "B", "A",  # 86-90
    "B", "A", "B", "B", "A",  # 91-95
    "B", "A", "B", "A", "A"   # 96-100
]
print(len(singles_10))
count_A_10 = singles_10.count('A')
#https://chat.openai.com/share/d998c967-37da-40e3-94c4-a4c12f90a991




singles_11 = [
    'B', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'A', 'A',
    'B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A',
    'A', 'B', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'B',
    'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'B',
    'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B',
    'B', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'A',
    'A', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'A',
    'B', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'B',
    'A', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'B', 'B'
]
print(len(singles_11))
count_A_11 = singles_11.count('A')
#https://chat.openai.com/share/9a247479-cf10-4358-b961-fafc134e02d1


singles_12 = ['B', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'A']

print(len(singles_12))
count_A_12 = singles_12.count('A')
#https://chat.openai.com/share/9a247479-cf10-4358-b961-fafc134e02d1

