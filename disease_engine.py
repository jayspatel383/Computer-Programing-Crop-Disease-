"""
Disease Prediction Engine - Rule-Based Expert System
No Machine Learning - Pure threshold-based logic
"""

from datetime import datetime

try:
    from crop_database import DISEASE_CONDITIONS, TREATMENT_DATABASE, find_matching_outbreaks
except ImportError:
    DISEASE_CONDITIONS = {}
    TREATMENT_DATABASE = {}
    def find_matching_outbreaks(crop, temp, hum):
        return []


class DiseasePredictor:
    """Main disease prediction engine"""
    
    def __init__(self):
        self.risk_weights = {
            'temperature': 0.30,
            'humidity': 0.35,
            'rainfall': 0.15,
            'consecutive': 0.15,
            'historical': 0.05
        }
    
    def predict_all_diseases(self, crop, weather_data):
        """Predict risk for all diseases of a crop"""
        print(f"\n🔍 Analyzing {crop.upper()} diseases...")
        print(f"   Temp: {weather_data.get('temperature')}°C | "
              f"Humidity: {weather_data.get('humidity')}% | "
              f"Rain: {weather_data.get('rainfall_24h', 0):.1f}mm")
        
        if crop not in DISEASE_CONDITIONS:
            return self._no_data_prediction(crop)
        
        predictions = []
        diseases = DISEASE_CONDITIONS[crop]
        
        for disease_name, disease_info in diseases.items():
            pred = self._predict_single(crop, disease_name, disease_info, weather_data)
            predictions.append(pred)
        
        # Sort highest risk first
        predictions.sort(key=lambda x: x['risk_score'], reverse=True)
        
        # Print summary
        for p in predictions[:3]:
            print(f"   {p['risk_emoji']} {p['disease_display_name']}: {p['risk_score']}% - {p['risk_level']}")
        
        return predictions
    
    def _predict_single(self, crop, disease_name, disease_info, weather_data):
        """Calculate risk for one disease"""
        conditions = disease_info['favorable_conditions']
        temp = weather_data.get('temperature', 25)
        humidity = weather_data.get('humidity', 50)
        rainfall = weather_data.get('rainfall_24h', 0)
        
        scores = {
            'temperature': 0,
            'humidity': 0,
            'rainfall': 0,
            'consecutive': 0,
            'historical': 0
        }
        
        conditions_met = []
        conditions_not_met = []
        
        # --- TEMPERATURE CHECK (30% weight) ---
        if 'temperature' in conditions:
            t_min = conditions['temperature']['min']
            t_max = conditions['temperature']['max']
            
            if t_min <= temp <= t_max:
                scores['temperature'] = 100
                conditions_met.append(f"✅ Temperature {temp}°C (ideal: {t_min}-{t_max}°C)")
            elif abs(temp - t_min) <= 3 or abs(temp - t_max) <= 3:
                scores['temperature'] = 50
                conditions_not_met.append(f"⚠️ Temperature {temp}°C (near range {t_min}-{t_max}°C)")
            else:
                scores['temperature'] = 10
                conditions_not_met.append(f"❌ Temperature {temp}°C (outside {t_min}-{t_max}°C)")
        
        # --- HUMIDITY CHECK (35% weight - MOST IMPORTANT) ---
        if 'humidity' in conditions:
            h_min = conditions['humidity']['min']
            
            if humidity >= h_min:
                # Higher humidity = higher score
                ratio = min(humidity / h_min, 2.0)
                scores['humidity'] = min(100, 50 + (ratio - 1) * 100)
                conditions_met.append(f"✅ Humidity {humidity}% (needs ≥{h_min}%)")
            elif humidity >= h_min * 0.8:
                scores['humidity'] = 40
                conditions_not_met.append(f"⚠️ Humidity {humidity}% (near threshold {h_min}%)")
            else:
                scores['humidity'] = 10
                conditions_not_met.append(f"❌ Humidity {humidity}% (needs ≥{h_min}%)")
        
        # --- RAINFALL CHECK (15% weight) ---
        if 'rainfall_24h_mm' in conditions:
            r_threshold = conditions['rainfall_24h_mm']
            if rainfall >= r_threshold:
                scores['rainfall'] = 100
                conditions_met.append(f"✅ Rainfall {rainfall:.1f}mm (≥{r_threshold}mm)")
            elif rainfall > 0:
                scores['rainfall'] = 50
            else:
                scores['rainfall'] = 10
        elif 'rainfall_weekly_mm' in conditions:
            r_weekly = weather_data.get('total_rainfall_5day', 0)
            r_threshold = conditions['rainfall_weekly_mm']
            if r_weekly >= r_threshold:
                scores['rainfall'] = 100
                conditions_met.append(f"✅ Weekly rain {r_weekly:.0f}mm (≥{r_threshold}mm)")
            elif r_weekly > 0:
                scores['rainfall'] = 50
            else:
                scores['rainfall'] = 10
        elif 'rainfall_trigger_mm' in conditions:
            r_threshold = conditions['rainfall_trigger_mm']
            if rainfall >= r_threshold:
                scores['rainfall'] = 100
                conditions_met.append(f"✅ Rainfall {rainfall:.1f}mm (trigger ≥{r_threshold}mm)")
            elif rainfall > 0:
                scores['rainfall'] = 50
            else:
                scores['rainfall'] = 10
        else:
            scores['rainfall'] = 50  # Neutral if no rainfall condition
        
        # --- CONSECUTIVE CONDITIONS (15% weight) ---
        if 'consecutive_favorable_hours' in conditions:
            hours = weather_data.get('consecutive_favorable_hours', 0)
            required = conditions['consecutive_favorable_hours']
            if hours >= required:
                scores['consecutive'] = 100
                conditions_met.append(f"✅ Favorable for {hours}h (need {required}h)")
            elif hours >= required * 0.5:
                scores['consecutive'] = 50
            else:
                scores['consecutive'] = 10
        elif 'consecutive_favorable_days' in conditions:
            days = weather_data.get('consecutive_condition_days', 0)
            required = conditions['consecutive_favorable_days']
            if days >= required:
                scores['consecutive'] = 100
                conditions_met.append(f"✅ Favorable for {days:.1f} days (need {required})")
            elif days >= required * 0.5:
                scores['consecutive'] = 50
            else:
                scores['consecutive'] = 10
        else:
            scores['consecutive'] = 50
        
        # --- HISTORICAL MATCH (5% weight) ---
        matches = find_matching_outbreaks(crop, temp, humidity)
        if matches and matches[0]['similarity'] > 50:
            scores['historical'] = matches[0]['similarity']
            if matches[0]['similarity'] > 70:
                conditions_met.append(f"⚠️ Similar to {matches[0]['outbreak']['year']} outbreak")
        else:
            scores['historical'] = 0
        
        # --- CALCULATE FINAL SCORE ---
        risk_score = round(
            scores['temperature'] * self.risk_weights['temperature'] +
            scores['humidity'] * self.risk_weights['humidity'] +
            scores['rainfall'] * self.risk_weights['rainfall'] +
            scores['consecutive'] * self.risk_weights['consecutive'] +
            scores['historical'] * self.risk_weights['historical']
        )
        
        risk_level = self._get_level(risk_score)
        
        return {
            'crop': crop,
            'disease': disease_name,
            'disease_display_name': disease_name.replace('_', ' ').title(),
            'scientific_name': disease_info.get('scientific_name', 'Unknown'),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_emoji': self._get_emoji(risk_score),
            'scores_breakdown': scores,
            'conditions_met': conditions_met,
            'conditions_partially_met': [],
            'conditions_not_met': conditions_not_met,
            'advisory': self._get_advisory(risk_score, risk_level, disease_name),
            'treatment': self._get_treatment(crop, disease_name, risk_score),
            'matching_outbreaks': matches[:2],
            'prediction_timestamp': datetime.now().isoformat()
        }
    
    def _get_level(self, score):
        if score >= 80: return 'CRITICAL'
        elif score >= 60: return 'HIGH'
        elif score >= 40: return 'MODERATE'
        elif score >= 20: return 'LOW'
        else: return 'MINIMAL'
    
    def _get_emoji(self, score):
        if score >= 80: return '🔴'
        elif score >= 60: return '🟠'
        elif score >= 40: return '🟡'
        elif score >= 20: return '🟢'
        else: return '⚪'
    
    def _get_advisory(self, score, level, disease_name):
        name = disease_name.replace('_', ' ').title()
        
        if level == 'CRITICAL':
            return {
                'summary': f'🚨 IMMEDIATE ACTION! {name} risk is critically high. Conditions are perfect for rapid disease development.',
                'urgency': 'URGENT - Act within 12-24 hours',
                'actions': [
                    'Apply recommended fungicide IMMEDIATELY',
                    'Notify all farm workers',
                    'Monitor field every 12 hours',
                    'Begin spraying adjacent fields'
                ],
                'estimated_loss': '40-70% crop loss if untreated'
            }
        elif level == 'HIGH':
            return {
                'summary': f'⚠️ High risk of {name}. Disease could develop within 48-72 hours.',
                'urgency': 'HIGH - Act within 24-48 hours',
                'actions': [
                    'Apply preventive fungicide',
                    'Monitor field twice daily',
                    'Ensure proper drainage',
                    'Remove infected plants'
                ],
                'estimated_loss': '20-40% crop loss if untreated'
            }
        elif level == 'MODERATE':
            return {
                'summary': f'📊 Moderate risk of {name}. Conditions are developing.',
                'urgency': 'MODERATE - Prepare in 3-5 days',
                'actions': [
                    'Begin weekly monitoring',
                    'Prepare fungicides and equipment',
                    'Check weather forecast daily'
                ],
                'estimated_loss': '10-20% crop loss if unmanaged'
            }
        elif level == 'LOW':
            return {
                'summary': f'✅ Low risk of {name}. Conditions mostly unfavorable.',
                'urgency': 'LOW - Routine monitoring',
                'actions': [
                    'Continue regular monitoring',
                    'Maintain general crop health'
                ],
                'estimated_loss': '<10% crop loss risk'
            }
        else:
            return {
                'summary': f'✅ Minimal risk of {name}. Conditions unfavorable for disease.',
                'urgency': 'NONE - No action needed',
                'actions': ['Continue normal practices'],
                'estimated_loss': 'Negligible risk'
            }
    
    def _get_treatment(self, crop, disease, score):
        try:
            treatment_db = TREATMENT_DATABASE.get(crop, {}).get(disease, {})
            if not treatment_db:
                return {'available': False, 'message': 'No specific treatment data.'}
            
            if score >= 60:
                t = treatment_db.get('curative', treatment_db.get('preventive', {}))
                return {'available': True, 'type': 'CURATIVE/PREVENTIVE', 'treatment': t}
            elif score >= 30:
                t = treatment_db.get('preventive', {})
                return {'available': True, 'type': 'PREVENTIVE', 'treatment': t}
            else:
                return {'available': True, 'type': 'MONITORING', 'treatment': {}}
        except:
            return {'available': False, 'message': 'Error loading treatment.'}
    
    def _no_data_prediction(self, crop):
        return [{
            'disease': 'no_data',
            'disease_display_name': f'No disease data for {crop}',
            'scientific_name': 'N/A',
            'risk_score': 0,
            'risk_level': 'NO DATA',
            'risk_emoji': '⚪',
            'scores_breakdown': {},
            'conditions_met': [],
            'conditions_partially_met': [],
            'conditions_not_met': [],
            'advisory': {
                'summary': f'Disease database not available for {crop}.',
                'urgency': 'N/A',
                'actions': ['Add disease data'],
                'estimated_loss': 'Unknown'
            },
            'treatment': {'available': False},
            'matching_outbreaks': []
        }]


class DiseaseTrendAnalyzer:
    """Simple trend analyzer"""
    
    def __init__(self):
        self.predictor = DiseasePredictor()
    
    def generate_trend_data(self, crop, historical_data):
        trend = []
        for day_data in historical_data:
            predictions = self.predictor.predict_all_diseases(crop, day_data['weather'])
            trend.append({
                'date': day_data['date'],
                'overall_risk': sum(p['risk_score'] for p in predictions) / max(len(predictions), 1),
                'highest_risk': predictions[0]['risk_score'] if predictions else 0,
                'predictions': predictions
            })
        return trend