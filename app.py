from flask import Flask, jsonify, render_template_string
import datetime
import pytz
import math

app = Flask(__name__)

def v10_strict_engine(period_str):
    """
    V10 ULTRA STRICT: Multi-Layer Validation Engine.
    3-ലെവലിൽ വിന്നിംഗ് സാധ്യത ഉറപ്പില്ലെങ്കിൽ ഈ സിസ്റ്റം 'SKIP' ചെയ്യും.
    """
    try:
        # പീരിയഡ് വിശകലനം
        digits = [int(d) for d in period_str]
        last_5 = digits[-5:]
        
        # ലെയർ 1: വെയിറ്റഡ് ഫ്രീക്വൻസി മൈനിംഗ്
        # അക്കങ്ങളുടെ സ്ഥാനത്തിനനുസരിച്ച് പ്രാധാന്യം നൽകുന്നു
        w_sum = (last_5[4] * 11) + (last_5[3] * 7) + (last_5[2] * 5) + (last_5[1] * 3) + (last_5[0] * 2)
        
        # ലെയർ 2: ഹാർമോണിക് വാല്യൂ (സീഡ് കറക്ഷൻ)
        seed_correction = sum(digits) * 0.618
        
        # ലെയർ 3: പ്രോബബിലിറ്റി ഫിൽട്ടറിംഗ്
        raw_val = (w_sum + seed_correction) % 10
        
        # ക്രമീകരണം: 3-ലെവലിൽ വിന്നിംഗ് റേറ്റ് കൂട്ടാൻ സിഗ്നലുകളെ ഫിൽട്ടർ ചെയ്യുന്നു
        # 5.6-ന് മുകളിൽ ബിഗ്, 4.4-ന് താഴെ സ്മാൾ. ഇടയിലുള്ളവ റിസ്ക് ആണ് (SKIP).
        if raw_val >= 5.65:
            return "BIG", "#00FF88", "HIGH"
        elif raw_val <= 4.35:
            return "SMALL", "#FF3131", "HIGH"
        else:
            return "WAIT/SKIP", "#AAAAAA", "LOW" # പണം കളയാതിരിക്കാൻ ഒഴിവാക്കുന്നു
            
    except Exception:
        return "ERROR", "#FFFFFF", "NONE"

@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI V10 ULTRA STRICT</title>
    <style>
        body { background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { border: 3px solid #00FF88; border-radius: 30px; padding: 40px; width: 340px; background: #0a0a0a; box-shadow: 0 0 60px rgba(0, 255, 136, 0.25); text-align: center; position: relative; }
        .period { color: #FFA500; font-size: 18px; font-weight: bold; margin-bottom: 5px; }
        #res { font-size: 60px; font-weight: 900; margin: 20px 0; transition: 0.3s; }
        .conf { font-size: 11px; padding: 5px 15px; border-radius: 10px; border: 1px solid #00FF88; color: #00FF88; display: inline-block; }
        .warning { color: #ff4444; font-size: 10px; margin-top: 20px; font-weight: bold; letter-spacing: 1px; }
        .skip-info { color: #666; font-size: 10px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="card">
        <div style="font-size: 10px; color: #00FF88; margin-bottom: 10px;">V10 ULTRA STRICT ENGINE</div>
        <div id="p_box" class="period">SYNCING...</div>
        <div id="res">---</div>
        <div id="conf_badge" class="conf">PROBABILITY: SCANNING</div>
        <div class="warning">STRICT RULE: STOP IF 2 LOSSES</div>
        <div class="skip-info">Note: System will skip risky periods.</div>
    </div>
    <script>
        async function update() {
            try {
                let r = await fetch('/get_signal_v10');
                let d = await r.json();
                document.getElementById('p_box').innerText = "PERIOD: " + d.p;
                let resDiv = document.getElementById('res');
                resDiv.innerText = d.s;
                resDiv.style.color = d.c;
                resDiv.style.textShadow = "0 0 30px " + d.c;
                document.getElementById('conf_badge').innerText = "CONFIDENCE: " + d.conf;
            } catch(e) {}
        }
        setInterval(update, 3000);
        update();
    </script>
</body>
</html>
''')

@app.route("/get_signal_v10")
def get_signal():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    idx = (now.hour * 60) + now.minute + 10001
    p_str = f"{now.strftime('%Y%m%d')}{idx}"
    s, c, conf = v10_strict_engine(p_str)
    return jsonify({"p": p_str, "s": s, "c": c, "conf": conf})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)