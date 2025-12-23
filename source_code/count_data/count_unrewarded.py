import pandas as pd

# 读取 summerOly_athletes_sorted.csv 文件
athletes_data = pd.read_csv("summerOly_athletes_sorted.csv")

# 给定的 NOC 列值列表
noc_values = [
    "SaintVincentandtheGrenadines", "SriLanka", "FederatedStatesofMicronesia", "Oman", "Bangladesh",
    "MarshallIslands", "Vanuatu", "SanMarino", "BurkinaFaso", "Aruba", "CaboVerde", "Guam", "Bhutan",
    "Guinea", "Czechia", "Somalia", "Mali", "PuertoRico", "Myanmar", "Palau", "SaudiArabia", "Rwanda",
    "SaintLucia", "BritishVirginIslands", "RepublicofMoldova", "CookIslands", "Belize", "Nicaragua",
    "Lesotho", "Eswatini", "Malawi", "UnitedStates", "CentralAfricanRepublic", "PapuaNewGuinea",
    "CzechRepublic", "Comoros", "Maldives", "Liberia", "Nauru", "UnitedArabEmirates", "AmericanSamoa",
    "BosniaandHerzegovina", "Benin", "Seychelles", "Yemen", "SaintKittsandNevis",
    "SolomonIslands", "SouthAfrica", "EquatorialGuinea", "NorthMacedonia", "AntiguaandBarbuda", "Malta",
    "Tuvalu", "SaoTomeandPrincipe", "Congo", "SierraLeone", "NewZealand", "Gambia", "Mauritania", "Angola",
    "Libya", "BruneiDarussalam", "CostaRica", "Cambodia", "Andorra", "DominicanRepublic", "CaymanIslands",
    "El Salvador", "SouthSudan", "Honduras", "Madagascar", "Nepal", "TrinidadandTobago", "Liechtenstein",
    "Monaco", "Kiribati", "RepublicoftheCongo", "Chad","Bolivia"
]

# 保留 NOC 列值在给定列表中的数据
filtered_data = athletes_data[athletes_data['Team'].isin(noc_values)]

# 保存结果到新的 CSV 文件
filtered_data.to_csv("filtered_summerOly_athletes_sorted.csv", index=False)

print("过滤完成，结果保存在 filtered_summerOly_athletes_sorted.csv 文件中。")