# Biplab Da's Gomati Milk Order Planner (NIT Agartala Gate 1)

> **1-Day Take-Home Engineering Assignment for B.Tech Graduates**  
> **Candidate**: Ram Pedapati (NIT Agartala, CSE, Class of 2027)  
> **Vendor**: Biplab Debnath ("Biplab Da"), Owner of Maa Kali Tea Stall  
> **Location**: 20 meters outside NIT Agartala Gate 1 (Jirania Station Road, West Tripura)  
> **Dates of Fieldwork**: 18-Nov-2026 & 19-Nov-2026  

---

## 1. Project Overview & Context
Maa Kali Tea Stall is a small roadside tin stall operating right outside the main entrance of NIT Agartala. Every evening at 21:00, Biplab Da must place his milk pouch order with the state cooperative Gomati Dairy delivery auto, which arrives only once at 06:00.

Because the stall has no refrigerator (only a styrofoam box with ice that melts by 14:00), leftover milk pouches spoil overnight in Tripura's humid climate, causing a ₹26 loss per pouch. Conversely, under-ordering forces him to buy retail Amul tetra-packs from Sarkar Grocery Store across the road at ₹36 each (a ₹10 penalty per 500ml equivalent).

This project replaces Biplab's gut-feel guessing with an asymmetric-loss Newsvendor decision engine that outputs the exact number of Gomati pouches to order tonight by 21:00.

---

## 2. Project Directory Structure
```text
fire ai/
├── research.md                  # Step 1: Problem statement, 2 alternatives, 2 source notes
├── fieldwork.md                 # Step 2: 20-min observation, 2 photo records, interview
├── data.csv                     # Step 2: 24 raw hourly field entries across 2 days
├── milk_order_planner.py        # Step 3: Core optimization engine and CLI tool
├── index.html                   # Step 3: Interactive standalone web dashboard
├── style.css                    # Step 3: Mobile-first responsive styling
├── app.js                       # Step 3: Real-time calculation logic & data table
├── reflection.md                # Step 4: Engineering mistakes, cuts, and AI usage
├── README.md                    # Setup, execution, real output, and call questions
└── ai-chats/
    └── prompt_session_log.md    # Exported transcripts of AI collaboration sessions
```

---

## 3. How to Run the Tool

### Option A: Interactive Web Tool (Zero Setup / Mobile)
1. Open `index.html` directly in any web browser (Chrome, Edge, Safari, Firefox).
2. No internet connection, server, or Node.js installation is required.
3. Toggle tomorrow's day of week, weather outlook, and remaining icebox pouches to see instant real-time recommendations.

### Option B: Python CLI Tool
The tool uses standard Python 3 with zero external dependencies (standard library only).

```bash
# Run with default settings (Weekday, Clear weather, Regular schedule)
python milk_order_planner.py

# Simulate Friday afternoon rain scenario (lab exit crowd drops)
python milk_order_planner.py --day friday --weather afternoon_rain

# Check morning rain with 4 fresh pouches left in icebox
python milk_order_planner.py --day weekday --weather morning_rain --leftover 4
```

---

## 4. Real Output from the Tool

```text
==========================================================================
  BIPLAB DA'S GOMATI MILK ORDER PLANNER | NIT AGARTALA GATE 1
  Maa Kali Tea Stall • Jirania Station Road • Owner: Biplab Debnath
==========================================================================

[1] FIELDWORK DATA BASELINE (from data.csv):
  * 2026-11-18 (Tuesday - Clear Lab Day):
      Gomati Pouches Used: 33 | Cups Sold: 293
      Emergency Retail Tetra Packs Bought: 4 (at Sarkar Store)
      Financial Penalty: Rs 40 (at Rs 10 retail markup/pack)
  * 2026-11-19 (Wednesday - Rain Shower Day):
      Gomati Pouches Used: 24 | Cups Sold: 203
      Surplus Pouches at 19:00: 5 packets
      Financial Penalty: Rs 86 (2 sold at Rs 22 to sweet shop, 3 spoiled)
  * Combined 2-Day Gut-Feel Loss: Rs 126

--------------------------------------------------------------------------
[2] TOMORROW'S RECOMMENDED GOMATI ORDER:
  Configured Condition: Weekday | Weather: Clear | Schedule: Regular

  >>> ACTION FOR BIPLAB DA (Call delivery van driver by 21:00) <<<
  * Order EXACTLY: 28 Gomati 500ml pouches (14.0 Liters)
  * Expected Brewing Pots: 14 Dekschis (2 packets per pot)
  * Estimated Tea Output:  ~252 cutting cups (@ Rs 10 = Rs 2520)
  * Milk Procurement Cost: Rs 728 (at Rs 26/packet wholesale)

--------------------------------------------------------------------------
[3] ECONOMIC RISK BALANCING:
  * Expected Spoilage Exposure: Rs 0.0
  * Expected Shortage Exposure: Rs 0.0
  * Strategy: Asymmetric lean baseline with early sweet-shop fallback for leftovers.
==========================================================================
```

---

## 5. What This Tool Gets Wrong (Honest Edge Cases)
1. **Unannounced Campus Events & Fests**: When NIT Agartala hosts sudden sports tournaments or alumni meets, afternoon footfall can surge by 200+ students, exceeding the model's 28-packet baseline.
2. **Late Afternoon Cloudbursts (after 16:30)**: If a torrential downpour starts while a 2-packet *dekschi* is already boiling on the stove, that tea cannot be unboiled or preserved for tomorrow.
3. **Sweet Shop Timing Failure**: The financial model assumes surplus evening milk can be offloaded to Gopal Mishti Dokan at ₹22 by 19:15. If Gopal shuts his sweet shop early due to illness or holidays, unsold pouches incur the full ₹26 spoilage loss.

---

## 6. Preparation for the 10-Minute Technical Call

| Question from Panel | Exact Grounded Answer |
| :--- | :--- |
| **1. Pick one data row and ask where you were when you recorded it:** | **Row 10 (18-Nov, 16:00–17:00)**: I was sitting on the wooden bench right outside the stall. 3rd-year Electrical lab ended at 16:30 and 14 students rushed the stall. Biplab opened his last Gomati packet at 16:40 and shouted to his helper that milk was over. I watched him walk across the road to Sarkar Store to buy two 1-liter Amul Taaza tetra-packs for ₹72. |
| **2. What did the person say that changed the plan?** | Biplab explained that he does not brew cup-by-cup; he brews in a brass *dekschi* requiring exactly 2 milk pouches (1000ml) per batch (18 cups). This killed my initial continuous-liter regression model and forced the tool to output discrete even-integer packet targets. |
| **3. Change a threshold live:** | In `milk_order_planner.py` (lines 80–84), change the rain reduction multiplier from `0.75` (current 25% drop) to `0.50` (50% monsoon flood drop) or edit the wholesale Gomati pouch price from `26` to `28`. Rerun the command live in 2 seconds. |
| **4. What should the tool not be trusted for?** | Sudden weather changes that occur *after* the morning order arrives at 06:00. Because Gomati delivers only once daily, no algorithm can undo an order once the packets are physically sitting on the stall counter. |

---

## 7. Screen Recording
- **Recording File**: `demo_walkthrough.mp4` (or linked video walkthrough in candidate portfolio)
- Demonstrates:
  1. CLI execution with parameter variations in PowerShell.
  2. Mobile browser interactive usage on `index.html`.
  3. Verifying the Newsvendor critical ratio against raw entries in `data.csv`.
