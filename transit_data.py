"""
Chennai Multimodal Transit Network
===================================
Sources: CMRL (Chennai Metro Rail Limited), Southern Railway,
         MTC (Metropolitan Transport Corporation) — approximate public data.

Coverage:
  - CMRL Metro Blue Line  (Wimco Nagar ↔ Chennai Airport, ~20 key stations)
  - CMRL Metro Green Line (Chennai Central ↔ St. Thomas Mount, ~10 stations)
  - Suburban Railway South Line (Central → Tambaram → Perungalathur)
  - Suburban Railway Main Line  (Central → Avadi)
  - Suburban MRTS           (Chennai Beach → Velachery)
  - Suburban Harbour Line   (Chennai Beach → Tondiarpet)
  - Major MTC Bus Hubs (~20 key interchange points)

All EDGES are bidirectional by default.
Coordinates accurate to ±200 m.
"""

NODES = {

    # ─────────────────────────────────────────────────────────────
    # CMRL METRO — BLUE LINE (Corridor 1)
    # Wimco Nagar ↔ Chennai Airport
    # ─────────────────────────────────────────────────────────────

    "Wimco Nagar Metro":              {"lat": 13.1739, "lng": 80.3063, "type": "METRO"},
    "Thiruvottiyur Metro":            {"lat": 13.1618, "lng": 80.3002, "type": "METRO"},
    "Kaladipet Metro":                {"lat": 13.1499, "lng": 80.2967, "type": "METRO"},
    "Tollgate Metro":                 {"lat": 13.1400, "lng": 80.2928, "type": "METRO"},
    "Washermanpet Metro":             {"lat": 13.1063, "lng": 80.2878, "type": "METRO"},
    "Mannadi Metro":                  {"lat": 13.0912, "lng": 80.2852, "type": "METRO"},
    "High Court Metro":               {"lat": 13.0813, "lng": 80.2836, "type": "METRO"},
    "Chennai Central Metro":          {"lat": 13.0831, "lng": 80.2721, "type": "METRO"},
    "Government Estate Metro":        {"lat": 13.0694, "lng": 80.2737, "type": "METRO"},
    "LIC Metro":                      {"lat": 13.0658, "lng": 80.2569, "type": "METRO"},
    "Thousand Lights Metro":          {"lat": 13.0573, "lng": 80.2567, "type": "METRO"},
    "AG-DMS Metro":                   {"lat": 13.0476, "lng": 80.2500, "type": "METRO"},
    "Nandanam Metro":                 {"lat": 13.0285, "lng": 80.2310, "type": "METRO"},
    "Saidapet Metro":                 {"lat": 13.0213, "lng": 80.2231, "type": "METRO"},
    "Little Mount Metro":             {"lat": 13.0142, "lng": 80.2281, "type": "METRO"},
    "Guindy Metro":                   {"lat": 13.0067, "lng": 80.2206, "type": "METRO"},
    "Alandur Metro":                  {"lat": 13.0022, "lng": 80.2040, "type": "METRO"},
    "Nanganallur Road Metro":         {"lat": 13.0100, "lng": 80.1950, "type": "METRO"},
    "Meenambakkam Metro":             {"lat": 13.0090, "lng": 80.1866, "type": "METRO"},
    "Meenambakkam":                 {"lat": 13.0090, "lng": 80.1866, "type": "SUBURBAN"},
    "Chennai Airport Metro":          {"lat": 13.0002, "lng": 80.1793, "type": "METRO"},

    # ─────────────────────────────────────────────────────────────
    # CMRL METRO — GREEN LINE (Corridor 2)
    # Chennai Central ↔ St. Thomas Mount (via Anna Nagar, Koyambedu)
    # Chennai Central Metro node is shared with Blue Line above
    # ─────────────────────────────────────────────────────────────

    "Nehru Park Metro":               {"lat": 13.0863, "lng": 80.2568, "type": "METRO"},
    "Kilpauk Medical College Metro":  {"lat": 13.0919, "lng": 80.2480, "type": "METRO"},
    "Arumbakkam Metro":               {"lat": 13.0801, "lng": 80.2099, "type": "METRO"},
    "Koyambedu Metro":                {"lat": 13.0730, "lng": 80.1960, "type": "METRO"},
    "CMBT Metro":                     {"lat": 13.0700, "lng": 80.2010, "type": "METRO"},
    "Vadapalani Metro":               {"lat": 13.0503, "lng": 80.2122, "type": "METRO"},
    "Ashok Nagar Metro":              {"lat": 13.0301, "lng": 80.2137, "type": "METRO"},
    "Ekkattuthangal Metro":           {"lat": 13.0147, "lng": 80.2154, "type": "METRO"},
    "St. Thomas Mount Metro":         {"lat": 13.0152, "lng": 80.2124, "type": "METRO"},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN RAILWAY — SOUTH LINE
    # Chennai Central → Egmore → Tambaram → Perungalathur
    # ─────────────────────────────────────────────────────────────

    "Chennai Central":     {"lat": 13.0827, "lng": 80.2707, "type": "SUBURBAN"},
    "Chennai Egmore":      {"lat": 13.0782, "lng": 80.2607, "type": "SUBURBAN"},
    "Chetpet":             {"lat": 13.0746, "lng": 80.2432, "type": "SUBURBAN"},
    "Nungambakkam":        {"lat": 13.0651, "lng": 80.2393, "type": "SUBURBAN"},
    "Kodambakkam":         {"lat": 13.0505, "lng": 80.2243, "type": "SUBURBAN"},
    "Mambalam":            {"lat": 13.0368, "lng": 80.2181, "type": "SUBURBAN"},
    "Saidapet":            {"lat": 13.0209, "lng": 80.2229, "type": "SUBURBAN"},
    "Guindy":              {"lat": 13.0067, "lng": 80.2206, "type": "SUBURBAN"},
    "Pallavaram":          {"lat": 12.9731, "lng": 80.1502, "type": "SUBURBAN"},
    "Tirusulam":           {"lat": 12.9900, "lng": 80.1680, "type": "SUBURBAN"},
    "Chromepet":           {"lat": 12.9507, "lng": 80.1450, "type": "SUBURBAN"},
    "Tambaram":            {"lat": 12.9249, "lng": 80.1298, "type": "SUBURBAN"},
    "Vandalur":            {"lat": 12.8940, "lng": 80.0980, "type": "SUBURBAN"},
    "Perungalathur":       {"lat": 12.8599, "lng": 80.0877, "type": "SUBURBAN"},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN RAILWAY — MAIN LINE
    # Chennai Central → Perambur → Ambattur → Avadi
    # ─────────────────────────────────────────────────────────────

    "Perambur":            {"lat": 13.1160, "lng": 80.2485, "type": "SUBURBAN"},
    "Villivakkam":         {"lat": 13.1192, "lng": 80.2173, "type": "SUBURBAN"},
    "Ambattur":            {"lat": 13.0982, "lng": 80.1614, "type": "SUBURBAN"},
    "Pattabiram":          {"lat": 13.1171, "lng": 80.1386, "type": "SUBURBAN"},
    "Avadi":               {"lat": 13.1149, "lng": 80.1042, "type": "SUBURBAN"},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN RAILWAY — MRTS
    # Chennai Beach → Chepauk → Mylapore → Adyar → Velachery
    # ─────────────────────────────────────────────────────────────

    "Chennai Beach":       {"lat": 13.0913, "lng": 80.2917, "type": "SUBURBAN"},
    "Fort":                {"lat": 13.0873, "lng": 80.2838, "type": "SUBURBAN"},
    "Park Town":           {"lat": 13.0827, "lng": 80.2769, "type": "SUBURBAN"},
    "Chepauk":             {"lat": 13.0605, "lng": 80.2805, "type": "SUBURBAN"},
    "Triplicane":          {"lat": 13.0581, "lng": 80.2784, "type": "SUBURBAN"},
    "Thiruvallikeni":      {"lat": 13.0523, "lng": 80.2754, "type": "SUBURBAN"},
    "Mylapore MRTS":       {"lat": 13.0339, "lng": 80.2692, "type": "SUBURBAN"},
    "Luz":                 {"lat": 13.0267, "lng": 80.2651, "type": "SUBURBAN"},
    "Adyar":               {"lat": 13.0067, "lng": 80.2572, "type": "SUBURBAN"},
    "Thiruvanmiyur":       {"lat": 12.9885, "lng": 80.2586, "type": "SUBURBAN"},
    "Perungudi":           {"lat": 12.9618, "lng": 80.2437, "type": "SUBURBAN"},
    "Taramani":            {"lat": 12.9845, "lng": 80.2357, "type": "SUBURBAN"},
    "Velachery":           {"lat": 12.9786, "lng": 80.2208, "type": "SUBURBAN"},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN RAILWAY — HARBOUR LINE
    # Chennai Beach → Washermanpet → Tondiarpet
    # ─────────────────────────────────────────────────────────────

    "Washermanpet":        {"lat": 13.1063, "lng": 80.2978, "type": "SUBURBAN"},
    "Tondiarpet":          {"lat": 13.1182, "lng": 80.2980, "type": "SUBURBAN"},

    # ─────────────────────────────────────────────────────────────
    # MAJOR MTC BUS HUBS
    # ─────────────────────────────────────────────────────────────

    "CMBT":                    {"lat": 13.0693, "lng": 80.2005, "type": "BUS_HUB"},
    "Broadway":                {"lat": 13.0912, "lng": 80.2796, "type": "BUS_HUB"},
    "T Nagar":                 {"lat": 13.0418, "lng": 80.2341, "type": "BUS_HUB"},
    "Anna Nagar":              {"lat": 13.0849, "lng": 80.2090, "type": "BUS_HUB"},
    "Adyar Bus Stand":         {"lat": 13.0070, "lng": 80.2578, "type": "BUS_HUB"},
    "Tambaram Bus Stand":      {"lat": 12.9253, "lng": 80.1302, "type": "BUS_HUB"},
    "Guindy Bus Stand":        {"lat": 13.0070, "lng": 80.2213, "type": "BUS_HUB"},
    "Besant Nagar":            {"lat": 12.9990, "lng": 80.2655, "type": "BUS_HUB"},
    "Thiruvanmiyur Bus Stand": {"lat": 12.9883, "lng": 80.2590, "type": "BUS_HUB"},
    "Sholinganallur":          {"lat": 12.9007, "lng": 80.2274, "type": "BUS_HUB"},
    "Porur":                   {"lat": 13.0363, "lng": 80.1566, "type": "BUS_HUB"},
    "Poonamallee":             {"lat": 13.0476, "lng": 80.1148, "type": "BUS_HUB"},
    "Velachery Bus Stand":     {"lat": 12.9790, "lng": 80.2212, "type": "BUS_HUB"},
    "Mylapore":                {"lat": 13.0339, "lng": 80.2695, "type": "BUS_HUB"},
    "Vadapalani":              {"lat": 13.0503, "lng": 80.2125, "type": "BUS_HUB"},
    "Egmore Bus Stand":        {"lat": 13.0783, "lng": 80.2612, "type": "BUS_HUB"},
    "Ambattur Bus Stand":      {"lat": 13.0985, "lng": 80.1617, "type": "BUS_HUB"},
    "Avadi Bus Stand":         {"lat": 13.1151, "lng": 80.1044, "type": "BUS_HUB"},
    "Pallavaram Bus Stand":    {"lat": 12.9734, "lng": 80.1505, "type": "BUS_HUB"},
    "OMR Toll":                {"lat": 12.9007, "lng": 80.2274, "type": "BUS_HUB"},
}


EDGES = [

    # ─────────────────────────────────────────────────────────────
    # CMRL METRO — BLUE LINE (all bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Wimco Nagar Metro",       "to": "Thiruvottiyur Metro",         "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "Thiruvottiyur Metro",     "to": "Kaladipet Metro",             "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Kaladipet Metro",         "to": "Tollgate Metro",              "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Tollgate Metro",          "to": "Washermanpet Metro",          "type": "METRO",    "route": "Blue Line", "time": 6,  "fare": 10},
    {"from": "Washermanpet Metro",      "to": "Mannadi Metro",               "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Mannadi Metro",           "to": "High Court Metro",            "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "High Court Metro",        "to": "Chennai Central Metro",       "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Chennai Central Metro",   "to": "Government Estate Metro",     "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Government Estate Metro", "to": "LIC Metro",                   "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "LIC Metro",               "to": "Thousand Lights Metro",       "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Thousand Lights Metro",   "to": "AG-DMS Metro",                "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "AG-DMS Metro",            "to": "Nandanam Metro",              "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "Nandanam Metro",          "to": "Saidapet Metro",              "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Saidapet Metro",          "to": "Little Mount Metro",          "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Little Mount Metro",      "to": "Guindy Metro",                "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},
    {"from": "Guindy Metro",            "to": "Alandur Metro",               "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "Alandur Metro",           "to": "Nanganallur Road Metro",      "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "Nanganallur Road Metro",  "to": "Meenambakkam Metro",          "type": "METRO",    "route": "Blue Line", "time": 4,  "fare": 10},
    {"from": "Meenambakkam Metro",      "to": "Chennai Airport Metro",       "type": "METRO",    "route": "Blue Line", "time": 3,  "fare": 10},

    # ─────────────────────────────────────────────────────────────
    # CMRL METRO — GREEN LINE (all bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Chennai Central Metro",         "to": "Nehru Park Metro",              "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "Nehru Park Metro",              "to": "Kilpauk Medical College Metro",  "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "Kilpauk Medical College Metro", "to": "Arumbakkam Metro",              "type": "METRO", "route": "Green Line", "time": 5,  "fare": 10},
    {"from": "Arumbakkam Metro",              "to": "Koyambedu Metro",               "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "Koyambedu Metro",               "to": "CMBT Metro",                    "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "CMBT Metro",                    "to": "Vadapalani Metro",              "type": "METRO", "route": "Green Line", "time": 5,  "fare": 10},
    {"from": "Vadapalani Metro",              "to": "Ashok Nagar Metro",             "type": "METRO", "route": "Green Line", "time": 4,  "fare": 10},
    {"from": "Ashok Nagar Metro",             "to": "Ekkattuthangal Metro",          "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "Ekkattuthangal Metro",          "to": "Alandur Metro",                 "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},
    {"from": "Alandur Metro",                 "to": "St. Thomas Mount Metro",        "type": "METRO", "route": "Green Line", "time": 3,  "fare": 10},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN — SOUTH LINE (bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Chennai Central", "to": "Chennai Egmore",  "type": "SUBURBAN", "route": "South Line", "time": 5,  "fare": 5},
    {"from": "Chennai Egmore",  "to": "Chetpet",         "type": "SUBURBAN", "route": "South Line", "time": 4,  "fare": 5},
    {"from": "Chetpet",         "to": "Nungambakkam",    "type": "SUBURBAN", "route": "South Line", "time": 3,  "fare": 5},
    {"from": "Nungambakkam",    "to": "Kodambakkam",     "type": "SUBURBAN", "route": "South Line", "time": 4,  "fare": 5},
    {"from": "Kodambakkam",     "to": "Mambalam",        "type": "SUBURBAN", "route": "South Line", "time": 3,  "fare": 5},
    {"from": "Mambalam",        "to": "Saidapet",        "type": "SUBURBAN", "route": "South Line", "time": 4,  "fare": 5},
    {"from": "Saidapet",        "to": "Guindy",          "type": "SUBURBAN", "route": "South Line", "time": 4,  "fare": 5},
    {"from": "Guindy",          "to": "Tirusulam",       "type": "SUBURBAN", "route": "South Line", "time": 5,  "fare": 5},
    {"from": "Tirusulam",       "to": "Meenambakkam",    "type": "SUBURBAN", "route": "South Line", "time": 4,  "fare": 5},
    {"from": "Meenambakkam",    "to": "Pallavaram",      "type": "SUBURBAN", "route": "South Line", "time": 5,  "fare": 5},
    {"from": "Pallavaram",      "to": "Chromepet",       "type": "SUBURBAN", "route": "South Line", "time": 5,  "fare": 5},
    {"from": "Chromepet",       "to": "Tambaram",        "type": "SUBURBAN", "route": "South Line", "time": 5,  "fare": 5},
    {"from": "Tambaram",        "to": "Vandalur",        "type": "SUBURBAN", "route": "South Line", "time": 8,  "fare": 10},
    {"from": "Vandalur",        "to": "Perungalathur",   "type": "SUBURBAN", "route": "South Line", "time": 7,  "fare": 10},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN — MAIN LINE (bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Chennai Central", "to": "Perambur",    "type": "SUBURBAN", "route": "Main Line", "time": 6,  "fare": 5},
    {"from": "Perambur",        "to": "Villivakkam", "type": "SUBURBAN", "route": "Main Line", "time": 4,  "fare": 5},
    {"from": "Villivakkam",     "to": "Ambattur",    "type": "SUBURBAN", "route": "Main Line", "time": 10, "fare": 10},
    {"from": "Ambattur",        "to": "Pattabiram",  "type": "SUBURBAN", "route": "Main Line", "time": 7,  "fare": 10},
    {"from": "Pattabiram",      "to": "Avadi",       "type": "SUBURBAN", "route": "Main Line", "time": 5,  "fare": 5},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN — MRTS (bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Chennai Beach",  "to": "Fort",           "type": "SUBURBAN", "route": "MRTS", "time": 3, "fare": 5},
    {"from": "Fort",           "to": "Park Town",      "type": "SUBURBAN", "route": "MRTS", "time": 3, "fare": 5},
    {"from": "Park Town",      "to": "Chepauk",        "type": "SUBURBAN", "route": "MRTS", "time": 4, "fare": 5},
    {"from": "Chepauk",        "to": "Triplicane",     "type": "SUBURBAN", "route": "MRTS", "time": 3, "fare": 5},
    {"from": "Triplicane",     "to": "Thiruvallikeni", "type": "SUBURBAN", "route": "MRTS", "time": 3, "fare": 5},
    {"from": "Thiruvallikeni", "to": "Mylapore MRTS",  "type": "SUBURBAN", "route": "MRTS", "time": 4, "fare": 5},
    {"from": "Mylapore MRTS",  "to": "Luz",            "type": "SUBURBAN", "route": "MRTS", "time": 3, "fare": 5},
    {"from": "Luz",            "to": "Adyar",          "type": "SUBURBAN", "route": "MRTS", "time": 5, "fare": 5},
    {"from": "Adyar",          "to": "Thiruvanmiyur",  "type": "SUBURBAN", "route": "MRTS", "time": 6, "fare": 5},
    {"from": "Thiruvanmiyur",  "to": "Perungudi",      "type": "SUBURBAN", "route": "MRTS", "time": 4, "fare": 5},
    {"from": "Perungudi",      "to": "Taramani",       "type": "SUBURBAN", "route": "MRTS", "time": 4, "fare": 5},
    {"from": "Taramani",       "to": "Velachery",      "type": "SUBURBAN", "route": "MRTS", "time": 5, "fare": 5},

    # ─────────────────────────────────────────────────────────────
    # SUBURBAN — HARBOUR LINE (bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Chennai Beach", "to": "Washermanpet", "type": "SUBURBAN", "route": "Harbour Line", "time": 6, "fare": 5},
    {"from": "Washermanpet",  "to": "Tondiarpet",   "type": "SUBURBAN", "route": "Harbour Line", "time": 4, "fare": 5},

    # ─────────────────────────────────────────────────────────────
    # MTC BUS — Major Corridors (bidirectional)
    # ─────────────────────────────────────────────────────────────

    {"from": "Broadway",          "to": "T Nagar",              "type": "BUS", "route": "MTC",     "time": 30, "fare": 20},
    {"from": "Broadway",          "to": "Egmore Bus Stand",     "type": "BUS", "route": "MTC",     "time": 10, "fare": 10},
    {"from": "Broadway",          "to": "Anna Nagar",           "type": "BUS", "route": "MTC",     "time": 35, "fare": 25},
    {"from": "CMBT",              "to": "T Nagar",              "type": "BUS", "route": "MTC",     "time": 15, "fare": 15},
    {"from": "CMBT",              "to": "Anna Nagar",           "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "CMBT",              "to": "Porur",                "type": "BUS", "route": "MTC",     "time": 30, "fare": 20},
    {"from": "CMBT",              "to": "Poonamallee",          "type": "BUS", "route": "MTC",     "time": 50, "fare": 30},
    {"from": "CMBT",              "to": "Ambattur Bus Stand",   "type": "BUS", "route": "MTC",     "time": 30, "fare": 20},
    {"from": "CMBT",              "to": "Avadi Bus Stand",      "type": "BUS", "route": "MTC",     "time": 55, "fare": 30},
    {"from": "T Nagar",           "to": "Adyar Bus Stand",      "type": "BUS", "route": "MTC",     "time": 25, "fare": 15},
    {"from": "T Nagar",           "to": "Guindy Bus Stand",     "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "T Nagar",           "to": "Mylapore",             "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "T Nagar",           "to": "Egmore Bus Stand",     "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "T Nagar",           "to": "Vadapalani",           "type": "BUS", "route": "MTC",     "time": 15, "fare": 15},
    {"from": "Guindy Bus Stand",  "to": "Tambaram Bus Stand",   "type": "BUS", "route": "MTC",     "time": 30, "fare": 20},
    {"from": "Guindy Bus Stand",  "to": "Velachery Bus Stand",  "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "Adyar Bus Stand",   "to": "Besant Nagar",         "type": "BUS", "route": "MTC",     "time": 10, "fare": 10},
    {"from": "Adyar Bus Stand",   "to": "Thiruvanmiyur Bus Stand","type":"BUS","route": "MTC",     "time": 15, "fare": 10},
    {"from": "Besant Nagar",      "to": "Thiruvanmiyur Bus Stand","type":"BUS","route": "MTC",     "time": 10, "fare": 10},
    {"from": "Thiruvanmiyur Bus Stand","to": "Sholinganallur",  "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "Mylapore",          "to": "Adyar Bus Stand",      "type": "BUS", "route": "MTC",     "time": 15, "fare": 10},
    {"from": "Mylapore",          "to": "Broadway",             "type": "BUS", "route": "MTC",     "time": 25, "fare": 15},
    {"from": "Tambaram Bus Stand","to": "Velachery Bus Stand",  "type": "BUS", "route": "MTC",     "time": 30, "fare": 20},
    {"from": "Tambaram Bus Stand","to": "Pallavaram Bus Stand", "type": "BUS", "route": "MTC",     "time": 15, "fare": 10},
    {"from": "Anna Nagar",        "to": "Vadapalani",           "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "Anna Nagar",        "to": "Ambattur Bus Stand",   "type": "BUS", "route": "MTC",     "time": 25, "fare": 15},
    {"from": "Porur",             "to": "Poonamallee",          "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "Vadapalani",        "to": "Guindy Bus Stand",     "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},
    {"from": "Sholinganallur",    "to": "Velachery Bus Stand",  "type": "BUS", "route": "MTC",     "time": 25, "fare": 15},
    {"from": "Egmore Bus Stand",  "to": "Broadway",             "type": "BUS", "route": "MTC",     "time": 10, "fare": 10},
    {"from": "Ambattur Bus Stand","to": "Avadi Bus Stand",      "type": "BUS", "route": "MTC",     "time": 20, "fare": 15},

    # ─────────────────────────────────────────────────────────────
    # WALK CONNECTIONS — between co-located / adjacent transit nodes
    # These are short walks to transfer between transport modes
    # ─────────────────────────────────────────────────────────────

    # Metro ↔ Suburban interchange
    {"from": "Chennai Central Metro",  "to": "Chennai Central",      "type": "WALK", "route": "", "time": 3,  "fare": 0},
    # Airport area connections
    {"from": "Chennai Airport Metro",  "to": "Tirusulam",            "type": "WALK", "route": "", "time": 8,  "fare": 0},
    {"from": "Meenambakkam Metro",     "to": "Meenambakkam",         "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Tirusulam",              "to": "Meenambakkam",         "type": "WALK", "route": "", "time": 6,  "fare": 0},
    {"from": "Chennai Central Metro",  "to": "Park Town",            "type": "WALK", "route": "", "time": 5,  "fare": 0},
    {"from": "Chennai Central",        "to": "Park Town",            "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Chennai Central",        "to": "Chennai Egmore",       "type": "WALK", "route": "", "time": 8,  "fare": 0},
    {"from": "Chennai Beach",          "to": "Broadway",             "type": "WALK", "route": "", "time": 5,  "fare": 0},
    {"from": "Washermanpet Metro",     "to": "Washermanpet",         "type": "WALK", "route": "", "time": 5,  "fare": 0},
    {"from": "Saidapet Metro",         "to": "Saidapet",             "type": "WALK", "route": "", "time": 5,  "fare": 0},
    {"from": "Guindy Metro",           "to": "Guindy",               "type": "WALK", "route": "", "time": 5,  "fare": 0},
    # Blue ↔ Green Line interchange at Alandur
    {"from": "Alandur Metro",          "to": "St. Thomas Mount Metro","type": "WALK", "route": "", "time": 3,  "fare": 0},
    # Metro ↔ Bus Hub
    {"from": "CMBT Metro",             "to": "CMBT",                 "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Koyambedu Metro",        "to": "CMBT",                 "type": "WALK", "route": "", "time": 6,  "fare": 0},
    {"from": "Vadapalani Metro",       "to": "Vadapalani",           "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Guindy Metro",           "to": "Guindy Bus Stand",     "type": "WALK", "route": "", "time": 5,  "fare": 0},
    {"from": "Guindy",                 "to": "Guindy Bus Stand",     "type": "WALK", "route": "", "time": 3,  "fare": 0},
    # Suburban ↔ Bus Hub
    {"from": "Chennai Egmore",         "to": "Egmore Bus Stand",     "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Tambaram",               "to": "Tambaram Bus Stand",   "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Pallavaram",             "to": "Pallavaram Bus Stand", "type": "WALK", "route": "", "time": 4,  "fare": 0},
    {"from": "Ambattur",               "to": "Ambattur Bus Stand",   "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Avadi",                  "to": "Avadi Bus Stand",      "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Perambur",               "to": "Broadway",             "type": "BUS",  "route": "MTC", "time": 20, "fare": 15},
    # MRTS ↔ Bus Hub
    {"from": "Velachery",              "to": "Velachery Bus Stand",  "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Thiruvanmiyur",          "to": "Thiruvanmiyur Bus Stand","type":"WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Adyar",                  "to": "Adyar Bus Stand",      "type": "WALK", "route": "", "time": 3,  "fare": 0},
    {"from": "Mylapore MRTS",          "to": "Mylapore",             "type": "WALK", "route": "", "time": 5,  "fare": 0},
]
