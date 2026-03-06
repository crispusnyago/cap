"""
Uganda administrative divisions data
Source: Based on official Uganda districts and counties
"""

UGANDA_DIVISIONS = {
    'kampala': {
        'name': 'Kampala',
        'counties': {
            'kampala_central': {
                'name': 'Kampala Central',
                'subcounties': ['Kampala Central Division', 'Kawempe Division', 'Makindye Division', 'Nakawa Division', 'Rubaga Division']
            },
            'nakawa': {
                'name': 'Nakawa',
                'subcounties': ['Nakawa', 'Kyambogo', 'Naguru', 'Bukoto', 'Kisaasi']
            },
            'makindye': {
                'name': 'Makindye',
                'subcounties': ['Makindye', 'Kabalagala', 'Nsambya', 'Ggaba', 'Lukuli']
            }
        }
    },
    'wakiso': {
        'name': 'Wakiso',
        'counties': {
            'kyadondo': {
                'name': 'Kyadondo',
                'subcounties': ['Wakiso', 'Nansana', 'Kira', 'Makindye', 'Kasangati', 'Gayaza', 'Bweyogerere']
            },
            'busiro': {
                'name': 'Busiro',
                'subcounties': ['Entebbe', 'Kajjansi', 'Ssisa', 'Nabweru', 'Nangabo', 'Masulita']
            }
        }
    },
    'mukono': {
        'name': 'Mukono',
        'counties': {
            'mukono_central': {
                'name': 'Mukono Central',
                'subcounties': ['Mukono Town', 'Goma', 'Nakisunga', 'Kyetume', 'Seeta']
            },
            'nakifuma': {
                'name': 'Nakifuma',
                'subcounties': ['Nakifuma', 'Kasawo', 'Nagojje', 'Kimenyedde']
            }
        }
    },
    'jinja': {
        'name': 'Jinja',
        'counties': {
            'jinja_municipality': {
                'name': 'Jinja Municipality',
                'subcounties': ['Jinja Central', 'Masese', 'Walukuba', 'Mpumudde', 'Bugembe']
            },
            'kagoma': {
                'name': 'Kagoma',
                'subcounties': ['Busede', 'Buyengo', 'Butagaya', 'Budondo']
            }
        }
    },
    'mbale': {
        'name': 'Mbale',
        'counties': {
            'mbale_municipality': {
                'name': 'Mbale Municipality',
                'subcounties': ['Mbale Central', 'Industrial Division', 'Northern Division', 'Wanale']
            },
            'bubulo': {
                'name': 'Bubulo',
                'subcounties': ['Bubulo', 'Busoba', 'Bukokho', 'Bumasikye']
            }
        }
    },
    'gulu': {
        'name': 'Gulu',
        'counties': {
            'gulu_municipality': {
                'name': 'Gulu Municipality',
                'subcounties': ['Gulu Central', 'Laroo', 'Bar-dege', 'Pece', 'Kasubi']
            },
            'omoro': {
                'name': 'Omoro',
                'subcounties': ['Omoro', 'Lalogi', 'Odek', 'Koro']
            }
        }
    },
    'mbarara': {
        'name': 'Mbarara',
        'counties': {
            'mbarara_municipality': {
                'name': 'Mbarara Municipality',
                'subcounties': ['Mbarara Central', 'Nyamitanga', 'Kakoba', 'Kamukuzi']
            },
            'kashari': {
                'name': 'Kashari',
                'subcounties': ['Bubaare', 'Rubaya', 'Kagongi', 'Kakyeeka']
            }
        }
    },
    'masaka': {
        'name': 'Masaka',
        'counties': {
            'masaka_municipality': {
                'name': 'Masaka Municipality',
                'subcounties': ['Masaka Central', 'Katwe', 'Kimaanya', 'Nyendo']
            },
            'bukoto': {
                'name': 'Bukoto',
                'subcounties': ['Bukoto', 'Kyanamukaka', 'Kyabakuza', 'Mukungwe']
            }
        }
    },
    'tororo': {
        'name': 'Tororo',
        'counties': {
            'tororo_municipality': {
                'name': 'Tororo Municipality',
                'subcounties': ['Tororo Central', 'Northern', 'Southern', 'Eastern']
            },
            'west_budama': {
                'name': 'West Budama',
                'subcounties': ['West Budama', 'Mulanda', 'Nagongera', 'Kwapa']
            }
        }
    },
    'busia': {
        'name': 'Busia',
        'counties': {
            'busia_municipality': {
                'name': 'Busia Municipality',
                'subcounties': ['Busia Central', 'Northern', 'Southern']
            },
            'samia_bugwe': {
                'name': 'Samia-Bugwe',
                'subcounties': ['Samia-Bugwe', 'Masaba', 'Bulumbi', 'Lumino']
            }
        }
    },
    'arua': {
        'name': 'Arua',
        'counties': {
            'arua_municipality': {
                'name': 'Arua Municipality',
                'subcounties': ['Arua Central', 'River Oli', 'Arua Hill']
            },
            'terego': {
                'name': 'Terego',
                'subcounties': ['Terego', 'Katrini', 'Omugo', 'Uriama']
            },
            'ayivu': {
                'name': 'Ayivu',
                'subcounties': ['Ayivu', 'Pajulu', 'Mvara', 'Oluko']
            }
        }
    },
    'lira': {
        'name': 'Lira',
        'counties': {
            'lira_municipality': {
                'name': 'Lira Municipality',
                'subcounties': ['Lira Central', 'Adyel', 'Bar', 'Ojwina']
            },
            'erute': {
                'name': 'Erute',
                'subcounties': ['Erute', 'Amach', 'Ogur', 'Barr']
            }
        }
    },
    'soroti': {
        'name': 'Soroti',
        'counties': {
            'soroti_municipality': {
                'name': 'Soroti Municipality',
                'subcounties': ['Soroti Central', 'Eastern', 'Western']
            },
            'serere': {
                'name': 'Serere',
                'subcounties': ['Serere', 'Ongaja', 'Pingire']
            }
        }
    },
    'kabale': {
        'name': 'Kabale',
        'counties': {
            'kabale_municipality': {
                'name': 'Kabale Municipality',
                'subcounties': ['Kabale Central', 'Southern', 'Northern']
            },
            'nkore': {
                'name': 'Nkore',
                'subcounties': ['Nkore', 'Kamuganguzi', 'Kitumba']
            }
        }
    },
    'fort_portal': {
        'name': 'Fort Portal',
        'counties': {
            'fort_portal_municipality': {
                'name': 'Fort Portal Municipality',
                'subcounties': ['Fort Portal Central', 'Southern', 'Western']
            },
            'bunyangabu': {
                'name': 'Bunyangabu',
                'subcounties': ['Bunyangabu', 'Kibiito', 'Rwimi']
            }
        }
    }
}

def get_districts():
    """Return list of all districts for dropdown"""
    return [(code, data['name']) for code, data in UGANDA_DIVISIONS.items()]

def get_counties(district_code):
    """Return counties for selected district"""
    district = UGANDA_DIVISIONS.get(district_code)
    if district:
        return [(code, county['name']) for code, county in district['counties'].items()]
    return []

def get_subcounties(district_code, county_code):
    """Return subcounties for selected district and county"""
    district = UGANDA_DIVISIONS.get(district_code)
    if district:
        county = district['counties'].get(county_code)
        if county:
            return county['subcounties']
    return []