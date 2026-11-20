// Interactive Client Logic for Biplab Da's Gomati Milk Order Planner

const RAW_OBSERVATION_DATA = [
  { id: 1, date: "2026-11-18", time: "07:00-08:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 16, tetra: 0, surplus: 0, note: "Stall opened at 6:45 AM; morning walkers & sweepers" },
  { id: 2, date: "2026-11-18", time: "08:00-09:00", weather: "Clear", schedule: "Regular", pouches: 4, cups: 35, tetra: 0, surplus: 0, note: "Morning class rush; students arriving Gate 1" },
  { id: 3, date: "2026-11-18", time: "09:00-10:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 19, tetra: 0, surplus: 0, note: "Lectures underway; lull period" },
  { id: 4, date: "2026-11-18", time: "10:00-11:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 17, tetra: 0, surplus: 0, note: "Campus guards & auto drivers" },
  { id: 5, date: "2026-11-18", time: "11:00-12:00", weather: "Clear", schedule: "Regular", pouches: 3, cups: 26, tetra: 0, surplus: 0, note: "Mid-morning break; steady queue" },
  { id: 6, date: "2026-11-18", time: "12:00-13:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 18, tetra: 0, surplus: 0, note: "Lunch break starts" },
  { id: 7, date: "2026-11-18", time: "13:00-14:00", weather: "Clear", schedule: "Regular", pouches: 3, cups: 27, tetra: 0, surplus: 0, note: "Mechanical workshop crowd" },
  { id: 8, date: "2026-11-18", time: "14:00-15:00", weather: "Clear", schedule: "Regular", pouches: 1, cups: 11, tetra: 0, surplus: 0, note: "Afternoon lab started" },
  { id: 9, date: "2026-11-18", time: "15:00-16:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 19, tetra: 0, surplus: 0, note: "Day scholars leaving campus" },
  { id: 10, date: "2026-11-18", time: "16:00-17:00", weather: "Clear", schedule: "Regular", pouches: 6, cups: 52, tetra: 2, surplus: 0, note: "Lab exit rush; milk ran dry at 16:40; 2 emergency tetra bought" },
  { id: 11, date: "2026-11-18", time: "17:00-18:00", weather: "Clear", schedule: "Regular", pouches: 4, cups: 36, tetra: 2, surplus: 0, note: "Evening rush; 2 more tetra packs bought (total 4 tetra)" },
  { id: 12, date: "2026-11-18", time: "18:00-19:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 17, tetra: 0, surplus: 0, note: "Closing at 19:15; zero milk left; Rs 40 retail loss" },
  { id: 13, date: "2026-11-19", time: "07:00-08:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 15, tetra: 0, surplus: 0, note: "Biplab over-ordered 32 packets due to yesterday's shortage" },
  { id: 14, date: "2026-11-19", time: "08:00-09:00", weather: "Clear", schedule: "Regular", pouches: 4, cups: 33, tetra: 0, surplus: 0, note: "Morning lectures arrive" },
  { id: 15, date: "2026-11-19", time: "09:00-10:00", weather: "Clear", schedule: "Regular", pouches: 2, cups: 18, tetra: 0, surplus: 0, note: "Standard morning sales" },
  { id: 16, date: "2026-11-19", time: "10:00-11:00", weather: "Overcast", schedule: "Regular", pouches: 2, cups: 16, tetra: 0, surplus: 0, note: "Sky turned dark over Jirania" },
  { id: 17, date: "2026-11-19", time: "11:00-12:00", weather: "Overcast", schedule: "Regular", pouches: 3, cups: 28, tetra: 0, surplus: 0, note: "Administrative staff break" },
  { id: 18, date: "2026-11-19", time: "12:00-13:00", weather: "Overcast", schedule: "Regular", pouches: 2, cups: 17, tetra: 0, surplus: 0, note: "Lunch interval" },
  { id: 19, date: "2026-11-19", time: "13:00-14:00", weather: "Overcast", schedule: "Regular", pouches: 2, cups: 19, tetra: 0, surplus: 0, note: "Steady tea" },
  { id: 20, date: "2026-11-19", time: "14:00-15:00", weather: "Overcast", schedule: "Regular", pouches: 1, cups: 10, tetra: 0, surplus: 0, note: "Slow afternoon lab period" },
  { id: 21, date: "2026-11-19", time: "15:00-16:00", weather: "Overcast", schedule: "Regular", pouches: 2, cups: 16, tetra: 0, surplus: 0, note: "Overcast humid air" },
  { id: 22, date: "2026-11-19", time: "16:00-17:00", weather: "Rain Shower", schedule: "Regular", pouches: 2, cups: 14, tetra: 0, surplus: 0, note: "Heavy downpour at 16:15; road flooded; students stayed inside" },
  { id: 23, date: "2026-11-19", time: "17:00-18:00", weather: "Rain Shower", schedule: "Regular", pouches: 1, cups: 9, tetra: 0, surplus: 0, note: "Rain continued; evening crowd absent" },
  { id: 24, date: "2026-11-19", time: "18:00-19:00", weather: "Clear", schedule: "Regular", pouches: 1, cups: 8, tetra: 0, surplus: 5, note: "5 surplus packets: 2 sold to sweet shop at Rs 22, 3 soured overnight" }
];

function calculatePlan() {
  const dayType = document.getElementById("daySelect").value;
  const weather = document.getElementById("weatherSelect").value;
  const academic = document.getElementById("academicSelect").value;
  const leftover = parseInt(document.getElementById("iceboxInput").value, 10) || 0;

  // Baseline
  let baseline = 28;
  if (dayType === "friday") baseline = 24;
  else if (dayType === "weekend") baseline = 16;

  // Academic multiplier
  let acadMult = 1.0;
  if (academic === "exam_week") acadMult = 1.15;
  else if (academic === "vacation") acadMult = 0.45;

  // Weather multiplier
  let weatherMult = 1.0;
  if (weather === "afternoon_rain") weatherMult = 0.75;
  else if (weather === "morning_rain") weatherMult = 1.12;
  else if (weather === "heavy_rain") weatherMult = 0.65;

  const expectedDemand = baseline * acadMult * weatherMult;
  const netRequired = Math.max(4, expectedDemand - leftover);

  // Discrete 2-pouch dekschi batch rounding
  const recommendedPouches = Math.max(4, Math.round(netRequired / 2) * 2);
  const totalDekschis = Math.floor(recommendedPouches / 2);
  const estimatedCups = totalDekschis * 18;
  const milkCost = recommendedPouches * 26;
  const projectedRevenue = estimatedCups * 10;
  const netMargin = projectedRevenue - milkCost;

  // Risk exposure
  const spoilageRisk = Math.max(0, (recommendedPouches - expectedDemand) * 18.5);
  const shortageRisk = Math.max(0, (expectedDemand - recommendedPouches) * 10);

  // Update UI Elements
  document.getElementById("pouchOrderCount").textContent = recommendedPouches;
  document.getElementById("litersText").textContent = `(${ (recommendedPouches * 0.5).toFixed(1) } Liters)`;
  document.getElementById("dekschiCount").textContent = `${totalDekschis} Dekschis`;
  document.getElementById("cupsOutput").textContent = `~${estimatedCups} Cups`;
  document.getElementById("milkCost").textContent = `₹${milkCost}`;
  document.getElementById("projectedRevenue").textContent = `₹${projectedRevenue}`;
  document.getElementById("netMargin").textContent = `₹${netMargin}`;
  document.getElementById("spoilageRisk").textContent = `₹${Math.round(spoilageRisk)}`;
  document.getElementById("shortageRisk").textContent = `₹${Math.round(shortageRisk)}`;
}

function renderTable() {
  const tbody = document.getElementById("dataBody");
  tbody.innerHTML = "";
  RAW_OBSERVATION_DATA.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.date}</td>
      <td>${row.time}</td>
      <td>${row.weather}</td>
      <td>${row.pouches}</td>
      <td>${row.cups}</td>
      <td>${row.tetra > 0 ? `<strong style="color:#f87171">${row.tetra}</strong>` : 0}</td>
      <td>${row.surplus > 0 ? `<strong style="color:#fbbf24">${row.surplus}</strong>` : 0}</td>
      <td>${row.note}</td>
    `;
    tbody.appendChild(tr);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderTable();
  calculatePlan();

  document.getElementById("daySelect").addEventListener("change", calculatePlan);
  document.getElementById("weatherSelect").addEventListener("change", calculatePlan);
  document.getElementById("academicSelect").addEventListener("change", calculatePlan);
  document.getElementById("iceboxInput").addEventListener("input", calculatePlan);

  const toggleBtn = document.getElementById("toggleDataBtn");
  const dataWrap = document.getElementById("dataTableWrap");
  toggleBtn.addEventListener("click", () => {
    dataWrap.classList.toggle("hidden");
    toggleBtn.textContent = dataWrap.classList.contains("hidden") 
      ? "Show Raw Observation Table" 
      : "Hide Observation Table";
  });
});
