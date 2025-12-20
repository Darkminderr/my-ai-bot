from flask import Flask, jsonify, render_template
from datetime import datetime
import math

app = Flask(__name__)

def get_raja_5min_mining():
    now = datetime.now()
    # 5 മിനിറ്റ് വിംഗോ പീരിയഡ് ഐഡി നിർമ്മാണം
    total_min = now.hour * 60 + now.minute
    period_count = total_min // 5+1
    period_id = now.strftime("%Y%m%d1000") + str(1000 + period_count)
    
    # --- ADVANCED DATA MINING LOGIC ---
    # പീരിയഡ് നമ്പറിലെ അക്കങ്ങളുടെ സ്വാധീനം അളക്കുന്നു (Weighted Digits)
    p_str = str(period_id)
    d1 = int(p_str[-1])
    d2 = int(p_str[-2])
    d3 = int(p_str[-3])
    
    # 3-ലെവൽ വിന്നിംഗിനായി നമ്പറുകളുടെ തീവ്രത കണക്കാക്കുന്നു
    # കൂടുതൽ പ്രിസിഷൻ കിട്ടാൻ പ്രൈം നമ്പറുകൾ (7, 3) ഉപയോഗിച്ചുള്ള മൈനിംഗ്
    mining_val = (d1 * 7) + (d2 * 3) + (d3 * 1)
    
    # ലളിതമായ ശരാശരിക്ക് പകരം മോഡുലോ ലോജിക് ഉപയോഗിക്കുന്നു
    if (mining_val % 10) >= 5:
        prediction, cls = "BIG", "big-glow"
    else:
        prediction, cls = "SMALL", "small-glow"
        
    return {
        "period": period_id,
        "prediction": prediction,
        "class": cls
    }

@app.route("/api/signal")
def signal():
    return jsonify(get_raja_5min_mining())

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)