import pandas as pd
import sqlite3
from database import init_db, import_df_to_db

data = [
    {"code": "A", "industry": "Agriculture, forestry, and fishing", "category": "Agriculture",
     "2018": 19708798, "2019": 19176988, "2020": 18737364, "2021": 17374858, "2022": 17432561, "2023": 18806745, "2024": 18516602, "2025": 18140918},

    {"code": "B", "industry": "Mining and quarrying", "category": "Industry",
     "2018": 246148, "2019": 178693, "2020": 158736, "2021": 166800, "2022": 179693, "2023": 181497, "2024": 198426, "2025": 205380},

    {"code": "C", "industry": "Manufacturing", "category": "Industry",
     "2018": 19977097, "2019": 19863802, "2020": 25522591, "2021": 22534272, "2022": 23213610, "2023": 21139584, "2024": 22343564, "2025": 22941731},

    {"code": "D-E", "industry": "Electricity, steam, water and waste management", "category": "Industry",
     "2018": 1061276, "2019": 1124432, "2020": 1239229, "2021": 1266646, "2022": 1229491, "2023": 1229970, "2024": 1314495, "2025": 1376844},

    {"code": "F", "industry": "Construction", "category": "Industry",
     "2018": 15129235, "2019": 14324717, "2020": 14575660, "2021": 14186003, "2022": 17223742, "2023": 19757593, "2024": 20256826, "2025": 18670110},

    {"code": "G", "industry": "Wholesale and retail trade; repair of motor vehicles and motorcycles", "category": "Services",
     "2018": 20612961, "2019": 21668655, "2020": 21300422, "2021": 21581253, "2022": 22677794, "2023": 24125124, "2024": 25118439, "2025": 28812668},

    {"code": "H", "industry": "Transportation and storage", "category": "Services",
     "2018": 3323679, "2019": 3712019, "2020": 2218896, "2021": 2153161, "2022": 2609020, "2023": 2910086, "2024": 3266582, "2025": 3491721},

    {"code": "I", "industry": "Accommodation and food service activities", "category": "Services",
     "2018": 1698804, "2019": 1968138, "2020": 1081510, "2021": 1102003, "2022": 1448303, "2023": 1704906, "2024": 1925663, "2025": 2032994},

    {"code": "J", "industry": "Information and communication", "category": "Services",
     "2018": 2168824, "2019": 2402877, "2020": 2533723, "2021": 2744117, "2022": 3028497, "2023": 3147811, "2024": 3335423, "2025": 3351382},

    {"code": "K", "industry": "Financial and insurance activities", "category": "Services",
     "2018": 2388247, "2019": 2824945, "2020": 3055636, "2021": 3275015, "2022": 3663276, "2023": 3990136, "2024": 4396529, "2025": 4718081},

    {"code": "L", "industry": "Real estate and ownership of dwellings", "category": "Services",
     "2018": 4471690, "2019": 4604662, "2020": 4487571, "2021": 4093993, "2022": 4155624, "2023": 4301690, "2024": 4493342, "2025": 4552207},

    {"code": "M", "industry": "Professional and business services", "category": "Services",
     "2018": 653295, "2019": 685932, "2020": 596468, "2021": 665886, "2022": 710201, "2023": 762763, "2024": 849420, "2025": 868511},

    {"code": "N", "industry": "Public administration and defense; compulsory social security", "category": "Services",
     "2018": 3755759, "2019": 4192149, "2020": 4546942, "2021": 4664140, "2022": 4773369, "2023": 5011939, "2024": 5275856, "2025": 5904499},

    {"code": "P", "industry": "Education", "category": "Services",
     "2018": 6784456, "2019": 7031650, "2020": 6981610, "2021": 8479728, "2022": 9238831, "2023": 9812897, "2024": 10188625, "2025": 11217999},

    {"code": "Q", "industry": "Human health and social work activities", "category": "Services",
     "2018": 1655980, "2019": 1791615, "2020": 2027145, "2021": 2297055, "2022": 2481143, "2023": 2644955, "2024": 2912452, "2025": 3230901},

    {"code": "S", "industry": "Other services", "category": "Services",
     "2018": 1147078, "2019": 1320155, "2020": 377761, "2021": 372898, "2022": 514303, "2023": 685932, "2024": 733234, "2025": 745278}
]

df = pd.DataFrame(data)
df.to_csv('zamboanga_gdp.csv', index=False)
init_db()
import_df_to_db(df)
print("Successfully updated zamboanga_gdp.csv and gdp_database.db with official 2018-2025 PSA dataset!")
