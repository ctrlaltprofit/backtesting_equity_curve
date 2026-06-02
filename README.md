# ORB Backtesting + Risk Management + Real Trading Charges

A Python backtesting project for an **Opening Range Breakout (ORB)** strategy with a strong focus on realistic trading simulation.

Unlike most beginner backtests, this project includes:

* Risk-based position sizing
* Slippage simulation
* Brokerage simulation
* STT
* Transaction charges
* SEBI fees
* GST
* IPFT charges
* Stamp duty
* Realistic PnL calculations

Most traders focus only on entries.

But in actual trading:

> Risk management and execution costs decide survival.

This project demonstrates how the same strategy can look profitable on paper but behave very differently once real-world trading costs are included.

---

# Why This Project Exists

Most strategy videos show:

```text
Perfect Entry
Perfect Exit
Zero Costs
```

Reality is different.

Every trade includes:

```text
Brokerage
STT
Transaction Charges
SEBI Fees
GST
IPFT
Stamp Duty
Slippage
```

Ignoring these costs can completely distort a backtest.

This project exists to demonstrate why:

```text
Backtest Realism

>

Backtest Profit
```

---

# Example Result

Before realistic costs:

```text
Trades: 81

Wins: 45

Losses: 36

Win Rate: 55.56%

PnL: ₹16,077
```

After adding:

```text
Slippage
Brokerage
Taxes
Exchange Charges
```

Result:

```text
Trades: 81

Wins: 39

Losses: 42

Win Rate: 48.15%

PnL: ₹5,198
```

Same strategy.

Same entries.

Same exits.

Only realism changed.

---

# Strategy Overview

The script calculates an Opening Range from:

```text
09:15 AM → 09:29 AM
```

Then waits for a breakout.

Only one trade is taken per day.

---

# Opening Range Calculation

Opening High:

```text
Highest High
between
09:15–09:29
```

Opening Low:

```text
Lowest Low
between
09:15–09:29
```

---

# BUY Entry

Enter BUY when:

```text
Current Candle High

>

Opening High
```

Parameters:

```text
Entry = Breakout Candle Close

SL = Opening Low

Risk Per Share

=

Entry − SL

Target

=

Entry + (Risk × RR)
```

---

# SELL Entry

Enter SELL when:

```text
Current Candle Low

<

Opening Low
```

Parameters:

```text
Entry = Breakdown Candle Close

SL = Opening High

Risk Per Share

=

SL − Entry

Target

=

Entry − (Risk × RR)
```

---

# Exit Rules

BUY exits when:

* Target Hit
* Stop Loss Hit
* End Of Day (3:15 PM)

SELL exits when:

* Target Hit
* Stop Loss Hit
* End Of Day (3:15 PM)

---

# Risk Management

Position sizing is based on risk.

Formula:

```text
Quantity

=

Allowed Risk

÷

Risk Per Share
```

Example:

Capital:

```text
₹100,000
```

Risk:

```text
1%
```

Maximum Loss:

```text
₹1,000
```

Trade:

```text
Entry = 1705

SL = 1695
```

Risk Per Share:

```text
10
```

Quantity:

```text
1000 ÷ 10

=

100 Shares
```

This ensures every trade risks approximately the same amount.

---

# Slippage Simulation

The project simulates execution slippage.

Configuration:

```python
SLIPPAGE = 0.0005
```

Equivalent:

```text
0.05%
```

Applied as:

BUY Entry:

```text
Price × (1 + Slippage)
```

SELL Entry:

```text
Price × (1 - Slippage)
```

BUY Exit:

```text
Price × (1 - Slippage)
```

SELL Exit:

```text
Price × (1 + Slippage)
```

This simulates imperfect fills found in real markets.

---

# Trading Charges Simulation

The project simulates realistic Indian Equity Intraday charges.

Included:

```text
Brokerage
STT
Transaction Charges
SEBI Fees
GST
IPFT
Stamp Duty
```

---

## Brokerage

```text
0.03%

or

₹5

whichever is lower
```

Per executed order.

---

## STT

Applied on sell side:

```text
0.025%
```

---

## Transaction Charges

Applied on turnover:

```text
0.00307%
```

---

## SEBI Charges

```text
₹10 per Crore
```

---

## GST

```text
18%
```

Applied on:

```text
Brokerage
+
Transaction Charges
+
SEBI Fees
```

---

## IPFT

```text
₹0.01 per Crore
```

Applied on traded value.

---

## Stamp Duty

Applied only on buy side.

```text
0.0003%
```

---

# Charge Calculation

Each trade calculates:

```text
Entry Charges

+

Exit Charges
```

Formula:

```text
Net PnL

=

Gross PnL

−

Total Charges
```

This provides a much more realistic estimate of strategy performance.

---

# Folder Structure

```text
project/

│
├── backtest.py

│
└── back_data/
    │
    └── JIOFIN-EQ/
        │
        ├── 2026-01-01.json
        ├── 2026-01-02.json
        ├── 2026-01-03.json
        └── ...
```

---

# Expected JSON Format

```json
[
  {
    "stat":"Ok",
    "time":"01-01-2026 09:15:00",
    "into":"1700",
    "inth":"1705",
    "intl":"1698",
    "intc":"1702"
  }
]
```

---

# Config Variables

```python
DATA_DIR="./back_data"

SYMBOL="JIOFIN-EQ"

START_DATE=datetime(2026,1,1)

END_DATE=datetime(2026,5,13)

TARGET_RR=2

CAPITAL=100000

RISK_PERCENT=1

SLIPPAGE=0.0005
```

---

# Metrics Tracked

The script tracks:

* Total Trades
* Wins
* Losses
* Win Rate
* Total PnL
* Profitable Days
* Losing Days
* Flat Days
* Trading Charges Paid

---

# Current Features

✓ ORB Strategy

✓ One Trade Per Day

✓ Risk Based Position Sizing

✓ Slippage Simulation

✓ Brokerage Simulation

✓ STT Calculation

✓ Transaction Charges

✓ GST Calculation

✓ SEBI Fees

✓ IPFT Charges

✓ Stamp Duty

✓ End Of Day Exit

✓ Performance Statistics

---

# Planned Improvements

* Equity Curve
* Drawdown Analysis
* Tradebook CSV Export
* Portfolio Backtesting
* Multi-Symbol Testing
* Multiple Trades Per Day
* Trailing Stop Loss
* Portfolio Risk Limits

---

# Key Lesson

Many traders think:

```text
Entry Strategy

=

Profit
```

Reality:

```text
Strategy

+

Risk Management

+

Execution

+

Charges

+

Slippage

=

Reality
```

Backtesting should not sell dreams.

It should move as close to reality as possible.
