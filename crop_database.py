"""
Crop Disease Knowledge Base
Data from ICAR, FAO, CPRI, IIWBR, DRR
"""

CROP_DATABASE = {
    'potato': {
        'scientific_name': 'Solanum tuberosum',
        'crop_type': 'Tuber crop',
        'season': 'Rabi (Winter)',
        'crop_duration_days': 90,
        'vulnerable_stages': ['tuber_formation', 'flowering'],
        'major_producing_states': ['Punjab', 'UP', 'Bihar', 'West Bengal'],
        'area_million_hectares': 2.2,
        'production_million_tonnes': 53,
        'average_yield_tonnes_per_hectare': 24,
        'economic_value_crores': 55000,
    },
    'wheat': {
        'scientific_name': 'Triticum aestivum',
        'crop_type': 'Cereal grain',
        'season': 'Rabi (Winter)',
        'crop_duration_days': 120,
        'vulnerable_stages': ['heading', 'grain_filling'],
        'major_producing_states': ['Punjab', 'Haryana', 'UP', 'MP'],
        'area_million_hectares': 31,
        'production_million_tonnes': 110,
        'average_yield_tonnes_per_hectare': 3.5,
        'economic_value_crores': 210000,
    },
    'rice': {
        'scientific_name': 'Oryza sativa',
        'crop_type': 'Cereal grain',
        'season': 'Kharif (Monsoon)',
        'crop_duration_days': 120,
        'vulnerable_stages': ['tillering', 'panicle_initiation'],
        'major_producing_states': ['West Bengal', 'Punjab', 'UP', 'AP'],
        'area_million_hectares': 45,
        'production_million_tonnes': 125,
        'average_yield_tonnes_per_hectare': 2.8,
        'economic_value_crores': 230000,
    },
    'tomato': {
        'scientific_name': 'Solanum lycopersicum',
        'crop_type': 'Vegetable',
        'season': 'All seasons',
        'crop_duration_days': 90,
        'vulnerable_stages': ['flowering', 'fruiting'],
        'major_producing_states': ['Maharashtra', 'Karnataka', 'Gujarat'],
        'area_million_hectares': 0.8,
        'production_million_tonnes': 20,
        'average_yield_tonnes_per_hectare': 25,
        'economic_value_crores': 35000,
    },
    'cotton': {
        'scientific_name': 'Gossypium hirsutum',
        'crop_type': 'Fiber crop',
        'season': 'Kharif (Monsoon)',
        'crop_duration_days': 180,
        'vulnerable_stages': ['boll_formation', 'flowering'],
        'major_producing_states': ['Gujarat', 'Maharashtra', 'Telangana'],
        'area_million_hectares': 12,
        'production_million_tonnes': 36,
        'average_yield_tonnes_per_hectare': 0.5,
        'economic_value_crores': 70000,
    }
}

# Disease conditions - Temperature and Humidity thresholds
DISEASE_CONDITIONS = {
    'potato': {
        'late_blight': {
            'scientific_name': 'Phytophthora infestans',
            'favorable_conditions': {
                'temperature': {'min': 10, 'max': 24},
                'humidity': {'min': 75},
                'rainfall_24h_mm': 0.2,
                'consecutive_favorable_hours': 48,
            },
            'description': 'Cool nights (10-15°C) + warm days (20-24°C) + high humidity'
        },
        'early_blight': {
            'scientific_name': 'Alternaria solani',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 32},
                'humidity': {'min': 31},
                'consecutive_favorable_days': 3,
            },
            'description': 'Warm temperatures with alternating wet/dry periods'
        },
        'black_scurf': {
            'scientific_name': 'Rhizoctonia solani',
            'favorable_conditions': {
                'temperature': {'min': 15, 'max': 25},
                'humidity': {'min': 60},
                'consecutive_favorable_days': 7,
            },
            'description': 'Cool soil with high moisture at planting'
        },
        'bacterial_wilt': {
            'scientific_name': 'Ralstonia solanacearum',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 80},
                'rainfall_weekly_mm': 50,
            },
            'description': 'High temperature + waterlogged soil'
        },
        'common_scab': {
            'scientific_name': 'Streptomyces scabies',
            'favorable_conditions': {
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 40},
                'consecutive_favorable_days': 14,
            },
            'description': 'Warm, dry soil during tuber formation'
        },
        'potato_virus_y': {
            'scientific_name': 'Potato Virus Y (PVY)',
            'favorable_conditions': {
                'temperature': {'min': 18, 'max': 28},
                'humidity': {'min': 60},
                'consecutive_favorable_days': 5,
            },
            'description': 'Warm conditions + aphid population growth'
        }
    },
    'wheat': {
        'rust': {
            'scientific_name': 'Puccinia spp.',
            'favorable_conditions': {
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 70},
                'consecutive_favorable_days': 3,
            },
            'description': 'Warm temps + 6+ hours leaf wetness'
        },
        'powdery_mildew': {
            'scientific_name': 'Blumeria graminis',
            'favorable_conditions': {
                'temperature': {'min': 15, 'max': 22},
                'humidity': {'min': 85},
                'consecutive_favorable_days': 5,
            },
            'description': 'Cool, humid + reduced sunlight'
        },
        'karnal_bunt': {
            'scientific_name': 'Tilletia indica',
            'favorable_conditions': {
                'temperature': {'min': 15, 'max': 22},
                'humidity': {'min': 80},
                'rainfall_24h_mm': 5,
            },
            'description': 'Cool, cloudy at ear emergence + light rain'
        },
        'loose_smut': {
            'scientific_name': 'Ustilago tritici',
            'favorable_conditions': {
                'temperature': {'min': 18, 'max': 25},
                'humidity': {'min': 60},
            },
            'description': 'Moderate temp + humidity at flowering'
        },
        'leaf_blight': {
            'scientific_name': 'Bipolaris sorokiniana',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 80},
                'consecutive_favorable_days': 4,
            },
            'description': 'High temp + humidity + rainfall'
        }
    },
    'rice': {
        'blast': {
            'scientific_name': 'Magnaporthe oryzae',
            'favorable_conditions': {
                'temperature': {'min': 22, 'max': 30},
                'humidity': {'min': 90},
                'consecutive_favorable_hours': 24,
            },
            'description': 'High humidity + overcast skies 2+ days'
        },
        'bacterial_leaf_blight': {
            'scientific_name': 'Xanthomonas oryzae',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 34},
                'humidity': {'min': 70},
                'rainfall_trigger_mm': 20,
            },
            'description': 'Warm + heavy rainfall + flooding'
        },
        'sheath_blight': {
            'scientific_name': 'Rhizoctonia solani',
            'favorable_conditions': {
                'temperature': {'min': 28, 'max': 32},
                'humidity': {'min': 85},
            },
            'description': 'High temp + humidity + dense canopy'
        },
        'false_smut': {
            'scientific_name': 'Ustilaginoidea virens',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 30},
                'humidity': {'min': 90},
                'rainfall_24h_mm': 10,
            },
            'description': 'High humidity at heading + rainfall'
        },
        'brown_spot': {
            'scientific_name': 'Bipolaris oryzae',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 30},
                'humidity': {'min': 80},
                'consecutive_favorable_days': 4,
            },
            'description': 'Warm, humid + nutrient-deficient soil'
        }
    },
    'tomato': {
        'early_blight': {
            'scientific_name': 'Alternaria solani',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 32},
                'humidity': {'min': 31},
                'consecutive_favorable_days': 3,
            },
            'description': 'Warm + alternating wet/dry periods'
        },
        'late_blight': {
            'scientific_name': 'Phytophthora infestans',
            'favorable_conditions': {
                'temperature': {'min': 10, 'max': 24},
                'humidity': {'min': 75},
                'rainfall_24h_mm': 0.2,
                'consecutive_favorable_hours': 48,
            },
            'description': 'Cool nights + warm days + high humidity'
        },
        'leaf_curl_virus': {
            'scientific_name': 'Tomato Leaf Curl Virus',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 60},
                'consecutive_favorable_days': 5,
            },
            'description': 'Hot + humid + high whitefly population'
        },
        'bacterial_wilt': {
            'scientific_name': 'Ralstonia solanacearum',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 80},
                'rainfall_weekly_mm': 50,
            },
            'description': 'High temp + waterlogged soil'
        },
        'powdery_mildew': {
            'scientific_name': 'Oidium neolycopersici',
            'favorable_conditions': {
                'temperature': {'min': 20, 'max': 28},
                'humidity': {'min': 50},
                'consecutive_favorable_days': 5,
            },
            'description': 'Warm + moderate humidity + dry leaves'
        }
    },
    'cotton': {
        'leaf_curl_virus': {
            'scientific_name': 'Cotton Leaf Curl Virus',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 60},
                'consecutive_favorable_days': 5,
            },
            'description': 'Hot + humid + high whitefly population'
        },
        'bacterial_blight': {
            'scientific_name': 'Xanthomonas campestris',
            'favorable_conditions': {
                'temperature': {'min': 28, 'max': 35},
                'humidity': {'min': 80},
                'rainfall_24h_mm': 5,
            },
            'description': 'Hot + humid + rain splashing'
        },
        'wilt': {
            'scientific_name': 'Fusarium oxysporum',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 32},
                'humidity': {'min': 60},
                'consecutive_favorable_days': 7,
            },
            'description': 'Warm soil + moderate moisture'
        },
        'root_rot': {
            'scientific_name': 'Rhizoctonia spp.',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 35},
                'humidity': {'min': 80},
                'rainfall_weekly_mm': 50,
            },
            'description': 'Hot + waterlogged soil'
        },
        'grey_mildew': {
            'scientific_name': 'Ramularia areola',
            'favorable_conditions': {
                'temperature': {'min': 25, 'max': 32},
                'humidity': {'min': 75},
                'consecutive_favorable_days': 5,
            },
            'description': 'Warm + high humidity + dense canopy'
        }
    }
}

# Treatment database
TREATMENT_DATABASE = {
    'potato': {
        'late_blight': {
            'preventive': {
                'chemical': 'Mancozeb 75% WP',
                'dosage_per_acre': '1 kg',
                'cost_per_acre_inr': 500,
                'efficacy_percent': 85,
                'repeat_interval_days': 7
            },
            'curative': {
                'chemical': 'Cymoxanil 8% + Mancozeb 64% WP',
                'dosage_per_acre': '800 gm',
                'cost_per_acre_inr': 1200,
                'efficacy_percent': 92
            }
        },
        'early_blight': {
            'preventive': {
                'chemical': 'Chlorothalonil 75% WP',
                'dosage_per_acre': '800 gm',
                'cost_per_acre_inr': 650,
                'efficacy_percent': 80
            }
        },
        'bacterial_wilt': {
            'preventive': {
                'chemical': 'Streptomycin Sulphate + Copper Oxychloride',
                'dosage_per_acre': 'As per label',
                'cost_per_acre_inr': 300,
                'efficacy_percent': 65
            }
        }
    },
    'wheat': {
        'rust': {
            'preventive': {
                'chemical': 'Propiconazole 25% EC',
                'dosage_per_acre': '200 ml',
                'cost_per_acre_inr': 240,
                'efficacy_percent': 90
            }
        },
        'powdery_mildew': {
            'preventive': {
                'chemical': 'Sulfur 80% WP',
                'dosage_per_acre': '1 kg',
                'cost_per_acre_inr': 180,
                'efficacy_percent': 78
            }
        }
    },
    'rice': {
        'blast': {
            'preventive': {
                'chemical': 'Tricyclazole 75% WP',
                'dosage_per_acre': '0.6 g/L water',
                'cost_per_acre_inr': 400,
                'efficacy_percent': 88
            }
        },
        'bacterial_leaf_blight': {
            'preventive': {
                'chemical': 'Streptomycin Sulphate + Copper Oxychloride',
                'dosage_per_acre': 'As per label',
                'cost_per_acre_inr': 350,
                'efficacy_percent': 65
            }
        }
    }
}

# Historical outbreak data for pattern matching
HISTORICAL_OUTBREAKS = [
    {'year': 2019, 'state': 'Punjab', 'crop': 'potato', 'disease': 'late_blight',
     'severity': 'Severe', 'crop_loss_percent': 45,
     'conditions': {'temperature': 22, 'humidity': 85, 'rainfall': 0.4}},
    {'year': 2020, 'state': 'UP', 'crop': 'potato', 'disease': 'late_blight',
     'severity': 'Moderate', 'crop_loss_percent': 25,
     'conditions': {'temperature': 20, 'humidity': 82, 'rainfall': 0.3}},
    {'year': 2021, 'state': 'Punjab', 'crop': 'wheat', 'disease': 'rust',
     'severity': 'Severe', 'crop_loss_percent': 35,
     'conditions': {'temperature': 26, 'humidity': 75, 'rainfall': 0.1}},
    {'year': 2022, 'state': 'West Bengal', 'crop': 'rice', 'disease': 'blast',
     'severity': 'Severe', 'crop_loss_percent': 40,
     'conditions': {'temperature': 28, 'humidity': 92, 'rainfall': 15}},
    {'year': 2023, 'state': 'Maharashtra', 'crop': 'tomato', 'disease': 'leaf_curl_virus',
     'severity': 'Moderate', 'crop_loss_percent': 20,
     'conditions': {'temperature': 30, 'humidity': 78, 'rainfall': 5}},
]

def get_crop_list():
    return list(CROP_DATABASE.keys())

def get_diseases_for_crop(crop):
    if crop in DISEASE_CONDITIONS:
        return list(DISEASE_CONDITIONS[crop].keys())
    return []

def get_crop_statistics(crop):
    if crop in CROP_DATABASE:
        return CROP_DATABASE[crop]
    return {}

def find_matching_outbreaks(crop, current_temp, current_humidity):
    matches = []
    for outbreak in HISTORICAL_OUTBREAKS:
        if outbreak['crop'] == crop:
            temp_diff = abs(outbreak['conditions']['temperature'] - current_temp)
            humidity_diff = abs(outbreak['conditions']['humidity'] - current_humidity)
            if temp_diff <= 3 and humidity_diff <= 10:
                similarity = 100 - (temp_diff * 5 + humidity_diff * 2)
                matches.append({
                    'outbreak': outbreak,
                    'similarity': max(0, min(100, similarity))
                })
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    return matches[:3]