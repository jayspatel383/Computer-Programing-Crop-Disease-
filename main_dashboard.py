"""
Crop Disease Early Warning System - Main Dashboard
Tkinter GUI with multiple tabs
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime

# Import modules with fallback
try:
    from crop_database import CROP_DATABASE, get_crop_list
    from disease_engine import DiseasePredictor, DiseaseTrendAnalyzer
    from data_fetcher import DataFetcher
    from config import APP_NAME, APP_VERSION, DEFAULT_LOCATIONS
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    APP_NAME = "Crop Disease Warning System"
    APP_VERSION = "1.0"
    DEFAULT_LOCATIONS = [
        {"name": "Germany", "city": "Berlin", "lat": 52.52, "lon": 13.40},
        {"name": "India", "city": "Ludhiana", "lat": 30.90, "lon": 75.85},
    ]
    CROP_DATABASE = {}
    
    def get_crop_list():
        return ['potato', 'wheat', 'rice', 'tomato', 'cotton']
    
    class DiseasePredictor:
        def predict_all_diseases(self, crop, weather):
            return [{'disease': 'error', 'disease_display_name': 'Error',
                     'risk_score': 0, 'risk_level': 'ERROR', 'risk_emoji': '⚪',
                     'scientific_name': 'N/A', 'scores_breakdown': {},
                     'conditions_met': [], 'conditions_partially_met': [],
                     'conditions_not_met': [],
                     'advisory': {'summary': 'Import error', 'urgency': 'N/A',
                                  'actions': [], 'estimated_loss': 'N/A'},
                     'treatment': {'available': False}, 'matching_outbreaks': []}]
    
    class DiseaseTrendAnalyzer:
        pass
    
    class DataFetcher:
        def quick_fetch(self, crop, loc):
            return {'temperature': 22, 'humidity': 85, 'rainfall_24h': 0.5,
                    'wind_speed': 10, 'cloud_cover': 75,
                    'consecutive_favorable_hours': 48, 'consecutive_condition_days': 4,
                    'total_rainfall_5day': 2.5, 'demo_data': True}


class CropDiseaseDashboard:
    """Main Dashboard Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')
        
        self.predictor = DiseasePredictor()
        self.trend_analyzer = DiseaseTrendAnalyzer()
        self.data_fetcher = DataFetcher()
        
        self.current_crop = tk.StringVar(value='potato')
        self.current_location = tk.StringVar(value=DEFAULT_LOCATIONS[0]['name'])
        self.current_city = tk.StringVar(value=DEFAULT_LOCATIONS[0]['city'])
        self.current_data = None
        self.current_predictions = None
        self.is_fetching = False
        
        self.setup_styles()
        self.setup_header()
        self.setup_notebook()
        self.setup_status_bar()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Action.TButton', font=('Arial', 12, 'bold'), padding=10)
    
    def setup_header(self):
        header = tk.Frame(self.root, bg='#2c3e50', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🌾 CROP DISEASE EARLY WARNING SYSTEM",
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=20, pady=18)
        
        self.time_label = tk.Label(header, text="", font=('Arial', 11),
                                   bg='#2c3e50', fg='#ecf0f1')
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=22)
        self.update_time()
    
    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_monitor = ttk.Frame(self.notebook)
        self.tab_details = ttk.Frame(self.notebook)
        self.tab_treatment = ttk.Frame(self.notebook)
        self.tab_trends = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_monitor, text='📊 Live Monitor')
        self.notebook.add(self.tab_details, text='🔍 Disease Details')
        self.notebook.add(self.tab_treatment, text='🧪 Treatment Plan')
        self.notebook.add(self.tab_trends, text='📈 Trends')
        
        self.setup_monitor_tab()
        self.setup_details_tab()
        self.setup_treatment_tab()
        self.setup_trends_tab()
    
    def setup_monitor_tab(self):
        # LEFT PANEL - Controls
        left = ttk.LabelFrame(self.tab_monitor, text="📍 Control Panel", padding=15)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        ttk.Label(left, text="Select Crop:", font=('Arial', 12)).pack(pady=5)
        crops = get_crop_list()
        crop_combo = ttk.Combobox(left, textvariable=self.current_crop,
                                  values=crops, state='readonly',
                                  font=('Arial', 12), width=20)
        crop_combo.pack(pady=5)
        crop_combo.bind('<<ComboboxSelected>>', self.on_crop_change)
        
        ttk.Label(left, text="Select Location:", font=('Arial', 12)).pack(pady=5)
        locations = [loc['name'] for loc in DEFAULT_LOCATIONS]
        loc_combo = ttk.Combobox(left, textvariable=self.current_location,
                                 values=locations, state='readonly',
                                 font=('Arial', 12), width=20)
        loc_combo.pack(pady=5)
        loc_combo.bind('<<ComboboxSelected>>', self.on_location_change)
        
        ttk.Label(left, text="City:", font=('Arial', 11)).pack(pady=2)
        self.city_label = ttk.Label(left, textvariable=self.current_city,
                                    font=('Arial', 12, 'bold'))
        self.city_label.pack(pady=2)
        
        self.fetch_btn = ttk.Button(left, text="🔍 Analyze Disease Risk",
                                    command=self.fetch_and_analyze,
                                    style='Action.TButton')
        self.fetch_btn.pack(pady=20)
        
        self.progress = ttk.Progressbar(left, mode='indeterminate')
        self.progress.pack(pady=5, fill=tk.X)
        
        ttk.Separator(left, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Crop info
        self.crop_info = scrolledtext.ScrolledText(left, height=10, width=35,
                                                    font=('Arial', 9), wrap=tk.WORD)
        self.crop_info.pack(pady=5, fill=tk.BOTH, expand=True)
        self.update_crop_info()
        
        # RIGHT PANEL - Results
        right = ttk.Frame(self.tab_monitor)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Risk meter + Conditions
        top = ttk.Frame(right)
        top.pack(fill=tk.X, pady=5)
        
        # Risk meter
        risk_frame = ttk.LabelFrame(top, text="🎯 OVERALL RISK", padding=15)
        risk_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.risk_score_label = tk.Label(risk_frame, text="--",
                                         font=('Arial', 64, 'bold'), fg='#95a5a6')
        self.risk_score_label.pack()
        self.risk_level_label = ttk.Label(risk_frame, text="Select crop & click Analyze",
                                          font=('Arial', 14))
        self.risk_level_label.pack()
        
        # Conditions
        cond_frame = ttk.LabelFrame(top, text="🌤️ CURRENT CONDITIONS", padding=15)
        cond_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.cond_labels = {}
        for cond, emoji in [('Temperature', '🌡️'), ('Humidity', '💧'),
                            ('Rainfall', '🌧️'), ('Wind', '💨'), ('Cloud', '☁️')]:
            f = ttk.Frame(cond_frame)
            f.pack(fill=tk.X, pady=6)
            ttk.Label(f, text=f"{emoji} {cond}:", font=('Arial', 11)).pack(side=tk.LEFT)
            lbl = ttk.Label(f, text="--", font=('Arial', 11, 'bold'))
            lbl.pack(side=tk.RIGHT)
            self.cond_labels[cond] = lbl
        
        # Disease table
        table_frame = ttk.LabelFrame(right, text="🦠 DISEASE RISK BREAKDOWN", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('disease', 'risk', 'level', 'action')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        self.tree.heading('disease', text='Disease')
        self.tree.heading('risk', text='Risk %')
        self.tree.heading('level', text='Level')
        self.tree.heading('action', text='Action Required')
        self.tree.column('disease', width=180)
        self.tree.column('risk', width=70)
        self.tree.column('level', width=100)
        self.tree.column('action', width=250)
        
        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Advisory
        adv_frame = ttk.LabelFrame(right, text="💡 QUICK ADVISORY", padding=10)
        adv_frame.pack(fill=tk.X, pady=5)
        self.advisory_text = tk.Text(adv_frame, height=4, font=('Arial', 10),
                                      wrap=tk.WORD, bg='#fff3cd')
        self.advisory_text.pack(fill=tk.X)
        self.advisory_text.insert('1.0', 'Click "Analyze Disease Risk" to begin...')
    
    def setup_details_tab(self):
        left = ttk.Frame(self.tab_details, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(left, text="Select Disease:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.disease_listbox = tk.Listbox(left, font=('Arial', 11), height=15, width=25)
        self.disease_listbox.pack(fill=tk.BOTH, expand=True)
        self.disease_listbox.bind('<<ListboxSelect>>', self.on_disease_select)
        
        right = ttk.Frame(self.tab_details, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.detail_text = scrolledtext.ScrolledText(right, font=('Arial', 10),
                                                      wrap=tk.WORD, bg='white')
        self.detail_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_treatment_tab(self):
        self.treatment_text = scrolledtext.ScrolledText(self.tab_treatment,
                                                         font=('Arial', 10),
                                                         wrap=tk.WORD, bg='white')
        self.treatment_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.treatment_text.insert('1.0', 'Treatment plan will appear after analysis...')
    
    def setup_trends_tab(self):
        frame = ttk.LabelFrame(self.tab_trends, text="📈 RISK TRENDS", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.trend_canvas = tk.Canvas(frame, bg='white', height=350)
        self.trend_canvas.pack(fill=tk.BOTH, expand=True)
        self.trend_canvas.create_text(400, 175, text="Run analysis multiple times\nto build trend data",
                                       font=('Arial', 14), fill='gray', justify=tk.CENTER)
    
    def setup_status_bar(self):
        bar = tk.Frame(self.root, bg='#34495e', height=28)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        self.status_label = tk.Label(bar, text="🟢 Ready | Select crop & location, click Analyze",
                                     font=('Arial', 9), bg='#34495e', fg='white')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=4)
        self.data_quality = tk.Label(bar, text="", font=('Arial', 9),
                                     bg='#34495e', fg='#ecf0f1')
        self.data_quality.pack(side=tk.RIGHT, padx=10, pady=4)
    
    def update_time(self):
        self.time_label.config(text=datetime.now().strftime("%d %B %Y | %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def update_crop_info(self):
        crop = self.current_crop.get()
        self.crop_info.delete('1.0', tk.END)
        if crop in CROP_DATABASE:
            info = CROP_DATABASE[crop]
            self.crop_info.insert('1.0', f"🌾 {crop.upper()}\n")
            self.crop_info.insert(tk.END, f"Scientific: {info.get('scientific_name', 'N/A')}\n")
            self.crop_info.insert(tk.END, f"Season: {info.get('season', 'N/A')}\n")
            self.crop_info.insert(tk.END, f"Duration: {info.get('crop_duration_days', 'N/A')} days\n\n")
            self.crop_info.insert(tk.END, "📊 Production:\n")
            area = info.get('area_million_hectares', 'N/A')
            if area != 'N/A':
                self.crop_info.insert(tk.END, f"Area: {area}M ha\n")
            yld = info.get('average_yield_tonnes_per_hectare', 'N/A')
            if yld != 'N/A':
                self.crop_info.insert(tk.END, f"Yield: {yld} t/ha\n")
            val = info.get('economic_value_crores', 'N/A')
            if val != 'N/A':
                self.crop_info.insert(tk.END, f"Value: ₹{val:,} Cr\n")
        else:
            self.crop_info.insert('1.0', f"{crop.title()}\nNo detailed data available.")
    
    def on_crop_change(self, event=None):
        self.update_crop_info()
        self.update_status("Crop changed. Click Analyze to update.")
    
    def on_location_change(self, event=None):
        name = self.current_location.get()
        for loc in DEFAULT_LOCATIONS:
            if loc['name'] == name:
                self.current_city.set(loc['city'])
                break
        self.update_status("Location changed. Click Analyze to update.")
    
    def fetch_and_analyze(self):
        if self.is_fetching:
            messagebox.showinfo("Busy", "Analysis in progress...")
            return
        thread = threading.Thread(target=self._fetch_thread, daemon=True)
        thread.start()
    
    def _fetch_thread(self):
        self.is_fetching = True
        self.root.after(0, self._start_loading)
        
        try:
            name = self.current_location.get()
            loc_data = DEFAULT_LOCATIONS[0]
            for loc in DEFAULT_LOCATIONS:
                if loc['name'] == name:
                    loc_data = loc
                    break
            
            self.root.after(0, self.update_status, "📡 Fetching weather data...")
            weather = self.data_fetcher.quick_fetch(self.current_crop.get(), loc_data)
            self.current_data = weather
            
            self.root.after(0, self.update_status, "🔍 Analyzing disease risk...")
            predictions = self.predictor.predict_all_diseases(self.current_crop.get(), weather)
            self.current_predictions = predictions
            
            self.root.after(0, self._update_dashboard, predictions, weather)
            self.root.after(0, self.update_status, "✅ Analysis complete!")
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.is_fetching = False
            self.root.after(0, self._stop_loading)
    
    def _start_loading(self):
        self.progress.start()
        self.fetch_btn.config(state='disabled', text='⏳ Analyzing...')
    
    def _stop_loading(self):
        self.progress.stop()
        self.fetch_btn.config(state='normal', text='🔍 Analyze Disease Risk')
    
    def _update_dashboard(self, predictions, weather):
        if predictions:
            top = predictions[0]
            self.risk_score_label.config(text=str(top['risk_score']),
                                         fg=self._risk_color(top['risk_score']))
            self.risk_level_label.config(text=top['risk_level'])
        
        # Update conditions
        self.cond_labels['Temperature'].config(text=f"{weather.get('temperature', '--')}°C")
        self.cond_labels['Humidity'].config(text=f"{weather.get('humidity', '--')}%")
        self.cond_labels['Rainfall'].config(text=f"{weather.get('rainfall_24h', '--'):.1f} mm")
        self.cond_labels['Wind'].config(text=f"{weather.get('wind_speed', '--')} km/h")
        self.cond_labels['Cloud'].config(text=f"{weather.get('cloud_cover', '--')}%")
        
        # Update table
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in predictions:
            self.tree.insert('', 'end', values=(
                p['disease_display_name'], f"{p['risk_score']}%",
                p['risk_level'], p['advisory']['urgency']
            ), tags=(p['risk_level'].lower(),))
        
        self.tree.tag_configure('critical', background='#ffcccc')
        self.tree.tag_configure('high', background='#ffe6cc')
        self.tree.tag_configure('moderate', background='#ffffcc')
        self.tree.tag_configure('low', background='#ccffcc')
        self.tree.tag_configure('minimal', background='#e6ffe6')
        
        # Update advisory
        self.advisory_text.delete('1.0', tk.END)
        if predictions:
            top = predictions[0]
            self.advisory_text.insert('1.0', f"{top['risk_emoji']} {top['disease_display_name']}: ")
            self.advisory_text.insert(tk.END, top['advisory']['summary'])
            if top['advisory']['actions']:
                self.advisory_text.insert(tk.END, f"\n\n📋 Action: {top['advisory']['actions'][0]}")
        
        # Update details tab
        self.disease_listbox.delete(0, tk.END)
        for p in predictions:
            self.disease_listbox.insert(tk.END, f"{p['risk_emoji']} {p['disease_display_name']} ({p['risk_score']}%)")
        self._detail_predictions = predictions
        
        # Update treatment tab
        self.treatment_text.delete('1.0', tk.END)
        self.treatment_text.insert('1.0', '🧪 TREATMENT ACTION PLAN\n')
        self.treatment_text.insert(tk.END, '='*60 + '\n\n')
        for i, p in enumerate(predictions):
            if p['treatment']['available']:
                t = p['treatment']['treatment']
                self.treatment_text.insert(tk.END, f"{p['risk_emoji']} {p['disease_display_name']} ({p['risk_score']}%)\n")
                self.treatment_text.insert(tk.END, f"  Priority: {i+1} | Type: {p['treatment']['type']}\n")
                self.treatment_text.insert(tk.END, f"  Urgency: {p['advisory']['urgency']}\n")
                if 'chemical' in t:
                    self.treatment_text.insert(tk.END, f"  Chemical: {t['chemical']}\n")
                    self.treatment_text.insert(tk.END, f"  Dosage: {t.get('dosage_per_acre', 'N/A')}\n")
                    self.treatment_text.insert(tk.END, f"  Cost: ₹{t.get('cost_per_acre_inr', 'N/A')}/acre\n")
                    self.treatment_text.insert(tk.END, f"  Efficacy: {t.get('efficacy_percent', 'N/A')}%\n")
                self.treatment_text.insert(tk.END, '\n')
        
        # Data quality
        q = "📊 REAL DATA" if not weather.get('demo_data') else "📦 DEMO DATA"
        self.data_quality.config(text=f"{q} | Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def on_disease_select(self, event=None):
        sel = self.disease_listbox.curselection()
        if not sel or not hasattr(self, '_detail_predictions'):
            return
        idx = sel[0]
        if idx < len(self._detail_predictions):
            p = self._detail_predictions[idx]
            self.detail_text.delete('1.0', tk.END)
            self.detail_text.insert('1.0', f"{'='*60}\n")
            self.detail_text.insert(tk.END, f"{p['risk_emoji']} {p['disease_display_name']}\n")
            self.detail_text.insert(tk.END, f"{'='*60}\n\n")
            self.detail_text.insert(tk.END, f"Scientific: {p['scientific_name']}\n")
            self.detail_text.insert(tk.END, f"Risk Score: {p['risk_score']}/100\n")
            self.detail_text.insert(tk.END, f"Risk Level: {p['risk_level']}\n\n")
            self.detail_text.insert(tk.END, "📊 SCORE BREAKDOWN:\n")
            self.detail_text.insert(tk.END, "-"*40 + "\n")
            for k, v in p['scores_breakdown'].items():
                bar = '█' * int(v/10) + '░' * (10 - int(v/10))
                self.detail_text.insert(tk.END, f"  {k:15s}: [{bar}] {v}%\n")
            self.detail_text.insert(tk.END, f"\n✅ Conditions Met:\n")
            for c in p['conditions_met']:
                self.detail_text.insert(tk.END, f"  {c}\n")
            if p['conditions_not_met']:
                self.detail_text.insert(tk.END, f"\n❌ Conditions Not Met:\n")
                for c in p['conditions_not_met']:
                    self.detail_text.insert(tk.END, f"  {c}\n")
            self.detail_text.insert(tk.END, f"\n💡 {p['advisory']['summary']}\n")
            self.detail_text.insert(tk.END, f"\n📋 Actions:\n")
            for i, a in enumerate(p['advisory']['actions'], 1):
                self.detail_text.insert(tk.END, f"  {i}. {a}\n")
            self.detail_text.insert(tk.END, f"\n💰 Est. Loss: {p['advisory']['estimated_loss']}\n")
    
    def update_status(self, msg):
        self.status_label.config(text=msg)
    
    def show_error(self, msg):
        messagebox.showerror("Error", f"An error occurred:\n\n{msg}")
    
    def _risk_color(self, score):
        if score >= 80: return '#e74c3c'
        elif score >= 60: return '#e67e22'
        elif score >= 40: return '#f1c40f'
        elif score >= 20: return '#2ecc71'
        return '#27ae60'


def main():
    root = tk.Tk()
    app = CropDiseaseDashboard(root)
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f'{w}x{h}+{x}+{y}')
    root.mainloop()

if __name__ == "__main__":
    print("="*60)
    print("🌾 Crop Disease Early Warning System")
    print("="*60)
    main()