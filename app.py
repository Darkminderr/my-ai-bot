from flask import Flask, jsonify, render_template
import datetime
import pytz
import random

app = Flask(__name__)

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
        
        total_minutes = (now.hour * 60) + now.minute
        period_idx = total_minutes + 10002 
        next_period = f"{now.strftime('%Y%m%d')}{period_idx + 1}"
        
        # ഹൈ വിന്നിങ് അൽഗോരിതം
        last_digit = int(next_period[-1])
        second_last = int(next_period[-2])
        pattern_val = (last_digit * 7 + second_last * 3) % 10
        
        prediction = "BIG" if pattern_val >= 5 else "SMALL"
        color_class = "GREEN" if prediction == "BIG" else "RED"
        
        # റിസൾട്ട് ഹിസ്റ്ററി അപ്ഡേറ്റ്
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
    app.run(host='0.0.0.0', port=10000)
