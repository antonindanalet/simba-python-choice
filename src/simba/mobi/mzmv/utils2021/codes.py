dict_mobi_names2mzmv_codes_zp_2021 = {
    "has_ga": "f41600_01a",
    "has_hta": "f41600_01b",
    "has_va": "f41600_01c",
    "has_driving_licence": "f20400a",
    "day_of_the_week": "Tag",
    "employment_status": "f40800_01",
    "highest_education": "f40120",
    "other_activity_1_on_top_of_job": "f41000a",
    "other_activity_2_on_top_of_job": "f41000b",
    "other_activity_3_on_top_of_job": "f41000c",
    "activity_1_if_not_working": "f41001a",
    "activity_2_if_not_working": "f41001b",
    "activity_3_if_not_working": "f41001c",
    "total_work_percentage": "f40920",
}

dict_mobi_names2mzmv_codes_hh_2021 = {
    "nb_of_cars": "f30100",
    "has_ebike45": "f32200c",
}

dict_main_mode2mobi_mode_2021 = {
    1: "other",  # Flugzeug
    2: "pt",  # Bahn
    3: "pt",  # Schiff
    4: "pt",  # Tram
    5: "pt",  # Bus, Postauto
    6: "pt",  # sonstiger OeV
    7: "other",  # Reisecar
    8: "car",  # Auto
    9: "car",  # Lastwagen
    10: "ride",  # Taxi
    11: "ride",  # Taxi-ähnliche Fahrdienste (z.B. Uber)
    12: "car",  # Motorrad
    13: "car",  # Mofa
    14: "bike",  # E-Bike
    15: "bike",  # Velo
    16: "walk",  # zu Fuss
    17: "other",  # Fahrzeugaehnliche Geraete
    18: "other",  # Anderes
    -99: "other",  # enthält Pseudoetappe
}

dict_detailed_mode2mobi_mode_2021 = {
    1: "walk",  # Zu Fuss -> LV
    2: "bike",  # Velo -> LV
    3: "bike",  # E-Bike ohne Kontrollschild
    4: "bike",  # E-Bike mit gelbem Kontrollschild
    5: "car",  # Mofa, Motorfahrrad
    6: "car",  # Kleinmotorrad
    7: "car",  # Motorrad als Fahrer
    8: "ride",  # Motorrad als Mitfahrer
    9: "car",  # Auto als Fahrer
    10: "ride",  # Auto als Mitfahrer
    11: "pt",  # Bahn/Zug
    12: "pt",  # Bus/PostAuto/Schulbus
    13: "pt",  # Tram/Metro
    14: "ride",  # Taxi (im "klassischen" Sinn)
    15: "ride",  # Taxi-ähnliche Fahrdienste (z.B. Uber)
    16: "other",  # Reisecar
    17: "car",  # Lastwagen
    18: "other",  # Schiff, Boot
    19: "other",  # Flugzeug / Luftfahrzeug
    20: "other",  # Zahnradbahn, Standseilbahn, Seilbahn, Sessellift, Skilift
    21: "other",  # Fahrzeugaehnliche Geraete
    95: "other",  # Anderes
    -99: "other",  # Pseudoetappe
    -98: "other",  # Keine Antwort
    -97: "other",  # Weiss nicht
}
