const API_BASE = "http://127.0.0.1:5000/api";

const cardBrandEl = document.getElementById("cardBrand");
const statusEl = document.getElementById("status");
const declineReasonEl = document.getElementById("declineReasonCode");
const declineContainer = document.getElementById("declineReasonContainer");

const mtdSummaryEl = document.getElementById("mtdSummary");
const monthlySummaryEl = document.getElementById("monthlySummary");
const applyBtn = document.getElementById("applyFilters");

// Show/hide decline reason filter
statusEl.addEventListener("change", () => {
  declineContainer.style.display =
    statusEl.value === "Declined" ? "inline-block" : "none";
});

// Build query string
function buildQueryParams() {
  const params = new URLSearchParams();

  if (cardBrandEl.value) params.append("cardBrand", cardBrandEl.value);
  if (statusEl.value) params.append("status", statusEl.value);
  if (statusEl.value === "Declined" && declineReasonEl.value) {
    params.append("declineReasonCode", declineReasonEl.value);
  }

  return params.toString();
}

async function fetchMTDSummary() {
  const res = await fetch(`${API_BASE}/summary/mtd`);
  const data = await res.json();
  mtdSummaryEl.textContent = JSON.stringify(data, null, 2);
}

async function fetchMonthlySummary() {
  const res = await fetch(`${API_BASE}/summary/monthly`);
  const data = await res.json();
  monthlySummaryEl.textContent = JSON.stringify(data, null, 2);
}

async function applyFilters() {
  const query = buildQueryParams();

  const res = await fetch(`${API_BASE}/transactions?${query}`);
  const transactions = await res.json();

  // For now, re-aggregate on the backend results
  mtdSummaryEl.textContent = `Filtered Transactions Count: ${transactions.length}`;
}

// Initial load
fetchMTDSummary();
fetchMonthlySummary();

// Apply filters
applyBtn.addEventListener("click", applyFilters);
