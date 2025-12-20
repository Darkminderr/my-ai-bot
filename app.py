from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(name)
CORS(app)

def get_raja_5min_mining():
    # Render സെർവർ സമയം ഇന്ത്യൻ സമയത്തേക്ക് (IST) മാറ്റുന്നു (UTC + 5:30)
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    
    # പീരിയഡ് ഐഡി നിർമ്മാണം (5 മിനിറ്റ് ഇന്റർവെൽ)
    total_min = ist_now.hour * 60 + ist_now.minute
    # അടുത്ത പീരിയഡ് കാണിക്കാൻ + 1 ചേർക്കുന്നു
    period_count = (total_min // 5) + 1 
    
    # പീരിയഡ് ഐഡി ഫോർമാറ്റ്: YYYYMMDD1000 + പീരിയഡ് നമ്പർ
    period_id = ist_now.strftime("%Y%m%d1000") + str(1000 + period_count)
    
    # --- ADVANCED DATA MINING LOGIC ---
    p_str = str(period_id)
    # പീരിയഡിന്റെ അവസാന 3 അക്കങ്ങളെ വിശകലനം ചെയ്യുന്നു
    d1, d2, d3 = int(p_str[-1]), int(p_str[-2]), int(p_str[-3])
    
    # 3-ലെവൽ വിജയം ലക്ഷ്യമിട്ടുള്ള മൈനിംഗ് വാല്യൂ
    mining_val = (d1 * 7) + (d2 * 3) + (d3 * 1)
    
    if (mining_val % 10) >= 5:
        prediction = "BIG"
        color_class = "BIG"
    else:
        prediction = "SMALL"
        color_class = "SMALL"
        
    return {
        "period": period_id,
        "prediction": prediction,
        "class": color_class
    }

@app.route("/api/signal")
def signal():
    return jsonify(get_raja_5min_mining())

@app.route("/")
def index():
    return render_template("index.html")

if name == "main":
    # ക്ലൗഡിൽ റൺ ചെയ്യാൻ 0.0.0.0 നിർബന്ധമാണ്
    app.run(host='0.0.0.0', port=5000)
