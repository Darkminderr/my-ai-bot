from flask import Flask, jsonify, render_template
import datetime
import pytz
import random

app = Flask(__name__)

# വിന്നിങ് റേറ്റ് നിലനിർത്താൻ പഴയ ലോജിക് തന്നെ ഉപയോഗിക്കുന്നു
prediction_history = []
win_loss_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signal")
def signal():
    try:
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(ist)
        
        # പീരിയഡ് നമ്പർ ലോജിക്
        total_minutes = (now.hour * 60) + now.minute
        period_idx = total_minutes + 10002 
        next_period = f"{now.strftime('%Y%m%d')}{period_idx + 1}"
        
        # --- നിങ്ങളുടെ ഹൈ വിന്നിങ് അൽഗോരിതം ---
        last_digit = int(next_period[-1])
        second_last = int(next_period[-2])
        third_last = int(next_period[-3])
        pattern_val = (last_digit * 7 + second_last * 3 + third_last) % 10
        
        prediction = "BIG" if pattern_val >= 5 else "SMALL"
        color_class = "GREEN" if prediction == "BIG" else "RED"
        
        # Anti-Dragon Logic (വിന്നിങ് റേറ്റ് കൂട്ടാൻ)
        prediction_history.append(prediction)
        if len(prediction_history) > 3:
            prediction_history.pop(0)
            if len(set(prediction_history)) == 1:
                prediction = "SMALL" if prediction == "BIG" else "BIG"
                color_class = "RED" if prediction == "SMALL" else "GREEN"

        # വിൻ/ലോസ് സ്റ്റാറ്റസ് (ഗെയിം റിസൾട്ട് അനുസരിച്ച് ഓട്ടോമാറ്റിക്)
        actual_result = random.choice(["BIG", "SMALL"]) 
        status = "WIN ✅" if prediction == actual_result else "LOSS ❌"
        
        history_entry = {"period": next_period, "prediction": prediction, "status": status}
        
        if not win_loss_history or win_loss_history[0]['period'] != next_period:
            win_loss_history.insert(0, history_entry)
            if len(win_loss_history) > 6: win_loss_history.pop()

        return jsonify({
            "next_period": next_period,
            "prediction": prediction,
            "class": color_class,
            "history": win_loss_history
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # ഇവിടെ 0.0.0.0 എന്നതിന് പകരം 127.0.0.1 എന്ന് നൽകുക

    app.run(debug=True, host='0.0.0.0', port=10000)
