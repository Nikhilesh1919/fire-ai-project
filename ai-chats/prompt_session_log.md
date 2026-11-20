# AI Collaboration Chat Log: Biplab Da's Milk Order Planner

*Exported as required by assignment guidelines for audit & grading.*

---

## Session 1: Problem Selection & Scoping
**User Prompt:**
> "I have 24 hours to find a real problem near NIT Agartala and build a tool for one real person. I'm thinking of Biplab Da's tea stall outside Gate 1. He buys Gomati milk packets in the morning and either runs out at 4:30 PM lab exit or wastes milk. What should the tool do?"

**Assistant Response:**
> "Focus strictly on his 21:00 nightly ordering decision. The Gomati delivery van only comes once at 06:00. He cannot order midday. The tool should not try to be a full point-of-sale system. It should simply answer: 'How many 500ml pouches should Biplab tell the delivery driver tonight?'"

---

## Session 2: Rejecting Machine Learning & API Bloat
**User Prompt:**
> "Should I fetch the OpenWeatherMap API for Jirania weather forecasts, and use an ARIMA model to predict cup counts?"

**Assistant Response:**
> "No, avoid APIs and ML regressions here. The dataset is ~24 entries collected over two days. Fitting ARIMA or XGBoost on 24 rows will drastically overfit. Moreover, an API requires internet and an API key that can break or expire. A simple rule-based asymmetric loss model based on the Newsvendor formula ($p^* = C_u / (C_u + C_o)$) with weather multipliers is transparent, debuggable, and won't fail when the vendor has no network."

---

## Session 3: Incorporating Fieldwork Insights (Dekschis & Sweet Shop Offload)
**User Prompt:**
> "I just spent 20 minutes at Gate 1 talking to Biplab Da. Two surprises:
> 1. He doesn't measure in liters; he brews in a brass dekschi which takes exactly 2 Gomati pouches (1000ml) and gives 18 glasses.
> 2. If he under-orders, he buys retail Amul tetra-packs from Sarkar Store across the road for Rs 36 instead of Rs 26.
> 3. If he has leftovers at 6:45 PM, he sells them to Gopal's sweet shop for Rs 22 instead of throwing them away.
> How do we adapt the code?"

**Assistant Response:**
> "This makes the math much cleaner:
> - $C_u$ (underage penalty) = ₹36 retail - ₹26 wholesale = ₹10 penalty per pouch.
> - $C_o$ (overage penalty) = ₹26 - ₹22 = ₹4 if sold to sweet shop, or ₹26 if spoiled. Weighted average $C_o \approx ₹18.50$.
> - All pouch recommendations must be even integers (`recommended = round(demand / 2) * 2`) so they map directly to full dekschi brewing pots."

---

## Session 4: Code & Web UI Generation
**User Prompt:**
> "Generate `milk_order_planner.py` with CLI flags and an `index.html` + `style.css` + `app.js` dashboard that Biplab can view on his mobile screen without needing to install Node.js or run servers."

**Assistant Response:**
> [Delivered zero-dependency Python script with `argparse` and single-directory HTML/CSS/JS web application].
