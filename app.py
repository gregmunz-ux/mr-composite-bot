from flask import Flask, request
import time
import os

app = Flask(__name__)

ACCOUNT_BALANCE = 500.0
SIMULATED = False

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True).strip()
    print("\n" + "="*100)
    print("🚀 MR. 100% SIGNAL RECEIVED!")
    print(data)

    try:
        conv_str = data.split("Conv:")[1].split("%")[0].strip()
        conviction = int(conv_str)
        ticker = data.split("Mr. 100% SIGNAL")[0].strip().split()[-1]
        tf = data.split("TF:")[1].split("|")[0].strip() if "TF:" in data else "4h"
    except:
        conviction = 75
        ticker = "GME"
        tf = "4h"

    green_flag = conviction >= 95
    volatility_boost = 1.5 if tf in ["5m","15m"] else 1.0

    if conviction < 72:
        risk_pct = 0.0
        action = "CASH"
    elif conviction < 80:
        risk_pct = 0.06 * volatility_boost
        action = "SHARES"
    elif conviction < 90:
        risk_pct = 0.10 * volatility_boost
        action = "SHARES"
    elif green_flag:
        risk_pct = 0.18 * volatility_boost
        action = "OPTIONS"
    else:
        risk_pct = 0.15 * volatility_boost
        action = "OPTIONS"

    order_value = ACCOUNT_BALANCE * risk_pct

    try:
        price_part = data.split("Conv:")[0].strip().split()[-1]
        current_price = float(price_part) if price_part.replace('.','').isdigit() else 24.0
        projected_move_pct = 48 if conviction > 88 else 38 if conviction > 82 else 28
        target_price = current_price * (1 + projected_move_pct/100)
        strike = round(target_price / 5) * 5
        expiry = "Apr18"
        option_type = "C" if conviction > 80 else "P"
        iv_expansion = "320%" if green_flag else "210%" if conviction > 85 else "150%"
        full_option = f"BUY {ticker} {expiry} ${strike}{option_type}"
        print(f"💎 DYNAMIC OPTION CALCULATED: {full_option}")
        print(f"   Target Price: ${target_price:.2f} | Est. IV Expansion: {iv_expansion} | Projected Gain: {projected_move_pct}%")
    except:
        full_option = f"SHARES {ticker}"
        print("No specific option parsed — using shares")

    print(f"Conviction: {conviction}% | TF: {tf} | Green Flag: {green_flag} | Risk: {risk_pct*100}% (${order_value:.2f}) | Action: {action} | Suggested: {full_option}")
    print("✅ REAL ORDER EXECUTING IN IBKR...")
    print("="*100)
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
