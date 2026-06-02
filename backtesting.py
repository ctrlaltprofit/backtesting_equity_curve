import os
import json
import pandas as pd
from datetime import datetime, time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


DATA_DIR = "./back_data"

SYMBOL = "JIOFIN-EQ"

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 2)

TARGET_RR = 2

CAPITAL = 100000
RISK_PERCENT = 1

SLIPPAGE = 0.0005  #0.05%

def calculate_charges(price, qty, side):
    turnover = price*qty
    
    brokerage = min(0.0003 * turnover, 5)

    stt = 0
    if side == 'SELL':
        stt = 0.00025 * turnover
    
    txn = 0.0000307 * turnover

    sebi = turnover * 0.000001

    gst = 0.18 * (brokerage + sebi + txn)

    ipft = 0.000000001 * turnover

    stamp = 0
    if side == 'BUY':
        stamp = 0.000003 * turnover

    total = brokerage + stt + txn + sebi + gst + ipft + stamp

    return total




def load_single_day(symbol, date):

    path = os.path.join(
        DATA_DIR,
        symbol,
        date.strftime("%Y-%m-%d") + ".json"
    )

    if not os.path.exists(path):
        return pd.DataFrame()

    with open(path) as f:
        data = json.load(f)

    rows = []

    for c in data:

        if c.get("stat") != "Ok":
            continue

        rows.append({

            "time": pd.to_datetime(
                c["time"],
                format="%d-%m-%Y %H:%M:%S"
            ),

            "open": float(c["into"]),
            "high": float(c["inth"]),
            "low": float(c["intl"]),
            "close": float(c["intc"])

        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df.set_index(
        "time",
        inplace=True
    )

    df.sort_index(
        inplace=True
    )

    return df


# =========================================
# BACKTEST
# =========================================

def run_backtest(
    start_date,
    end_date
):

    total_pnl = 0

    total_trades = 0

    winning = 0
    losing = 0

    profitable_days = 0
    loss_days = 0
    flat_days = 0

    equity = CAPITAL

    equity_curve = [
        equity
    ]

    equity_dates = [start_date]


    for date in pd.date_range(
        start_date,
        end_date
    ):

        print(
            f"\n===== {date.date()} ====="
        )

        df = load_single_day(
            SYMBOL,
            date
        )

        if df.empty:

            print("No Data")

            continue




        opening_df = df.between_time(
            "09:15",
            "09:29"
        )

        if opening_df.empty:
            continue


        opening_high = (
            opening_df["high"]
            .max()
        )

        opening_low = (
            opening_df["low"]
            .min()
        )


        print(
            "Opening High:",
            round(
                opening_high,
                2
            )
        )

        print(
            "Opening Low:",
            round(
                opening_low,
                2
            )
        )


        position = None

        entry = 0
        sl = 0
        target = 0
        trade_qty = 0

        day_pnl = 0


        # ============================
        # LOOP
        # ============================

        for i in range(
            len(df)
        ):

            candle = df.iloc[i]

            current_time = (
                candle.name.time()
            )


            if current_time <= time(
                9,
                29
            ):
                continue


            high = candle["high"]
            low = candle["low"]
            close = candle["close"]


            # ========================
            # ENTRY
            # ========================

            if position is None:


                # BUY

                if high > opening_high:

                    position = "BUY"
                    raw_entry = close
                    entry = raw_entry * (1+SLIPPAGE)

                    sl = opening_low

                    risk_per_stock = raw_entry - sl

                    if risk_per_stock <= 0:
                        continue


                    # =========================
                    # RISK MANAGEMENT
                    # =========================

                    total_risk = (

                        equity *

                        (
                            RISK_PERCENT / 100
                        )

                    )

                    qty_risk = (

                        total_risk /

                        risk_per_stock

                    )

                    qty_capital = (

                        equity /

                        entry

                    )

                    trade_qty = int(

                        min(
                            qty_risk,
                            qty_capital
                        )

                    )

                    if trade_qty <= 0:
                        continue


                    target = (

                        raw_entry +

                        (
                            risk_per_stock *
                            TARGET_RR
                        )

                    )


                    print(
                        f"BUY : {entry:.2f}"
                    )

                    print(
                        f"SL : {sl:.2f}"
                    )

                    print(
                        f"TARGET : {target:.2f}"
                    )

                    print(
                        f"QTY : {trade_qty}"
                    )



                # SELL

                elif low < opening_low:

                    position = "SELL"
                    raw_entry = close
                    entry = raw_entry * (1-SLIPPAGE)

                    sl = opening_high

                    risk_per_stock = sl - raw_entry

                    if risk_per_stock <= 0:
                        continue


                    # =========================
                    # RISK MANAGEMENT
                    # =========================

                    total_risk = (

                        equity *

                        (
                            RISK_PERCENT / 100
                        )

                    )

                    qty_risk = (

                        total_risk /

                        risk_per_stock

                    )

                    qty_capital = (

                        equity /

                        entry

                    )

                    trade_qty = int(

                        min(
                            qty_risk,
                            qty_capital
                        )

                    )

                    if trade_qty <= 0:
                        continue

                    target = (

                        raw_entry -

                        (
                            risk_per_stock *
                            TARGET_RR
                        )

                    )


                    print(
                        f"SELL : {entry:.2f}"
                    )

                    print(
                        f"SL : {sl:.2f}"
                    )

                    print(
                        f"TARGET : {target:.2f}"
                    )

                    print(
                        f"QTY : {trade_qty}"
                    )


            # ========================
            # EXIT
            # ========================

            elif position:


                exit_reason = None

                exit_price = None


                # BUY EXIT

                if position=="BUY":

                    if high >= target:

                        exit_reason="TARGET"

                        exit_price=target * (1-SLIPPAGE)


                    elif low <= sl:

                        exit_reason="SL"

                        exit_price=sl * (1-SLIPPAGE)


                # SELL EXIT

                else:

                    if low <= target:

                        exit_reason="TARGET"

                        exit_price=target * (1+SLIPPAGE)


                    elif high >= sl:

                        exit_reason="SL"

                        exit_price=sl * (1+SLIPPAGE)


                # EOD EXIT

                if (

                    exit_reason is None

                    and

                    current_time >= time(
                        15,
                        15
                    )

                ):

                    exit_reason="EOD"
                    if position == "BUY":
                        exit_price=close * (1-SLIPPAGE)
                    elif position == "SELL":
                        exit_price = close *(1+SLIPPAGE)


                # ====================
                # CLOSE TRADE
                # ====================

                if exit_reason:


                    if position=="BUY":

                        pnl = (

                            exit_price -
                            entry

                        ) * trade_qty


                    else:

                        pnl = (

                            entry -
                            exit_price

                        ) * trade_qty

                    entry_charges = calculate_charges(entry, trade_qty, "BUY")
                    exit_charges = calculate_charges(exit_price, trade_qty, "SELL")

                    total_charges = entry_charges + exit_charges

                    pnl -=total_charges

                    total_pnl += pnl

                    day_pnl += pnl

                    equity += pnl

                    equity_curve.append(
                        equity
                    )
                    equity_dates.append(
                        date
                    )
                    total_trades += 1


                    if pnl > 0:

                        winning += 1

                    else:

                        losing += 1


                    print(
                        f"EXIT: "
                        f"{exit_reason}"
                    )

                    print(
                        f"PnL: "
                        f"{round(pnl,2)}"
                    )

                    print(
                        f"Total Charges: "
                        f"{round(total_charges,2)}"
                    )

                    break


        print(
            f"Day PnL: "
            f"{round(day_pnl,2)}"
        )


        if day_pnl > 0:

            profitable_days += 1

        elif day_pnl < 0:

            loss_days += 1

        else:

            flat_days += 1



    print(
        "\n===== FINAL ====="
    )

    print(
        "Trades:",
        total_trades
    )

    print(
        "Wins:",
        winning
    )

    print(
        "Losses:",
        losing
    )


    if total_trades:

        winrate = (

            winning /
            total_trades

        ) * 100


        print(
            "Win Rate:",
            round(
                winrate,
                2
            ),
            "%"
        )

    print(
        "Final Equity:",
        round(equity, 2)
    )

    print(
        "PnL:",
        round(
            total_pnl,
            2
        )
    )


    print(
        "\n===== DAYS ====="
    )

    print(
        "Profitable:",
        profitable_days
    )

    print(
        "Loss:",
        loss_days
    )

    print(
        "Flat:",
        flat_days
    )

    plt.figure(figsize=(12,6))

    plt.plot(
        equity_dates,
        equity_curve
    )

    plt.title("Equity Curve")

    plt.xlabel("Date")

    plt.ylabel("Account Value")

    plt.grid(True)

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%b")
    )

    plt.gca().xaxis.set_major_locator(
        mdates.MonthLocator()
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "equity_curve.png",
        dpi=300
    )



if __name__=="__main__":

    run_backtest(
        START_DATE,
        END_DATE
    )