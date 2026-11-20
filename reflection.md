# Step 4: Reflection — Engineering Mistakes, Cuts, and Field Reality

## 1. What I Got Wrong at the Start
When I first picked the problem, I modeled tea production as a continuous fluid problem. I thought I would track milk consumption in milliliters per hour and write a continuous linear regression predicting fractional liters.

Twenty minutes sitting next to Biplab Da's tawa proved that idea was disconnected from reality. Biplab never measures milk in milliliters. He brews in a brass *dekschi* (pot). Each pot requires exactly two 500ml pouches of Gomati milk, 250ml of water, and four spoonfuls of CTC tea dust, yielding 18 cutting glasses. A single leftover pouch is practically unusable on its own because he cannot brew half a pot without scorching the bottom of the vessel. My continuous math was useless. I had to scrap the formula and rebuild the entire tool around discrete even-integer packet batches.

I also misjudged the penalty for under-ordering. I initially assumed running out of milk meant losing customers permanently. But because Sarkar Grocery Store is right across the road, Biplab simply walks over and buys retail Amul tetra-packs. The real penalty is not zero sales; it is a direct ₹10 per pack margin haircut (₹36 retail vs ₹26 wholesale). Recognizing that converted a nebulous customer-churn problem into a clean, solvable asymmetric loss equation.

---

## 2. What I Would Cut
If I had to compress this build down to two hours, I would cut the academic calendar dropdown entirely. 

While exam weeks and semester breaks do affect footfall, NIT Agartala runs on a predictable 14-week semester calendar that rarely changes on short notice. Biplab already knows when the campus is on vacation because the entire station road empties out. The only factor that actually causes sharp day-to-day unpredictability is the local Jirania weather—specifically whether rain hits at 16:30 when afternoon lab students are deciding whether to walk outside or stay in their hostel rooms.

---

## 3. Where AI Helped and Where It Wasted Time

### Where AI Helped
AI was fast and effective for two things:
1. Translating the asymmetric Newsvendor formula ($p^* = \frac{C_u}{C_u + C_o}$) into clean, bug-free Python rounding logic that maps unrounded demands to discrete 2-pouch *dekschi* multiples.
2. Generating the responsive mobile web interface (`index.html` and `style.css`) with clean CSS variables and high-contrast night styling so Biplab can tap options on a cheap smartphone screen with wet hands.

### Where AI Wasted Time
AI repeatedly pushed to over-engineer the tool. In the first architecture pass, it suggested:
- Setting up a PostgreSQL or SQLite database to store customer timestamps.
- Integrating a commercial weather API (OpenWeatherMap) with background polling cron jobs.
- Training an ARIMA or Random Forest time-series regression on 24 data points.

All three suggestions were distractions. A roadside vendor with no Wi-Fi does not need a background daemon polling global weather APIs—especially when satellite weather forecasts for Jirania are notoriously lagged compared to looking up at the sky at 8:30 PM. I had to repeatedly tell the model to strip away frameworks and keep the core logic to a standalone script and a zero-dependency web page.

---

## 4. Screen Recording Demo
- **Demonstration Video**: `demo_walkthrough.mp4` (or unlisted demo link in `README.md`)
- A 3-minute end-to-end recording demonstrating:
  1. Running `python milk_order_planner.py` with different schedule flags.
  2. Opening `index.html` in a mobile-view browser and dynamically adjusting the icebox count.
  3. Verifying the financial exposure calculation matches the raw rows in `data.csv`.
