const API_BASE = "http://127.0.0.1:5000/api";

// DOM Elements
const cardBrandEl = document.getElementById("cardBrand");
const statusEl = document.getElementById("status");
const declineReasonEl = document.getElementById("declineReasonCode");
const declineContainer = document.getElementById("declineReasonContainer");
const mtdCardsEl = document.getElementById("mtdCards");
const applyBtn = document.getElementById("applyFilters");

// Chart instance (so we can update it)
let monthlyChart = null;

// Show/hide decline reason filter based on status selection
statusEl.addEventListener("change", () => {
  declineContainer.style.display =
    statusEl.value === "Declined" ? "inline-block" : "none";
});

// Build query string from current filter selections
function buildQueryParams() {
  const params = new URLSearchParams();

  if (cardBrandEl.value) params.append("cardBrand", cardBrandEl.value);
  if (statusEl.value) params.append("status", statusEl.value);
  if (statusEl.value === "Declined" && declineReasonEl.value) {
    params.append("declineReasonCode", declineReasonEl.value);
  }

  return params.toString();
}

// Render MTD summary as cards
function renderMTDCards(data) {
  const approvalRate = data.totalTransactions > 0
    ? ((data.totalApproved / data.totalTransactions) * 100).toFixed(1)
    : 0;

  mtdCardsEl.innerHTML = `
    <div class="card">
      <div class="card-value">${data.totalTransactions}</div>
      <div class="card-label">Total Transactions</div>
    </div>
    <div class="card approved">
      <div class="card-value">${data.totalApproved}</div>
      <div class="card-label">Approved</div>
    </div>
    <div class="card declined">
      <div class="card-value">${data.totalDeclined}</div>
      <div class="card-label">Declined</div>
    </div>
    <div class="card rate">
      <div class="card-value">${approvalRate}%</div>
      <div class="card-label">Approval Rate</div>
    </div>
    <div class="card">
      <div class="card-value">$${data.totalAmount.toLocaleString()}</div>
      <div class="card-label">Total Amount</div>
    </div>
  `;
}

// Render monthly bar chart
function renderMonthlyChart(data) {
  const ctx = document.getElementById("monthlyChart").getContext("2d");

  // Sort months by sortKey and extract labels/values
  const sortedMonths = Object.entries(data)
    .sort((a, b) => a[1].sortKey.localeCompare(b[1].sortKey));

  const labels = sortedMonths.map(([month]) => month);
  const approvedData = sortedMonths.map(([, d]) => d.totalApproved);
  const declinedData = sortedMonths.map(([, d]) => d.totalDeclined);

  // Destroy existing chart if it exists
  if (monthlyChart) {
    monthlyChart.destroy();
  }

  // Create new chart
  monthlyChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Approved",
          data: approvedData,
          backgroundColor: "#28a745"
        },
        {
          label: "Declined",
          data: declinedData,
          backgroundColor: "#dc3545"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: false
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Transactions"
          }
        }
      },
      plugins: {
        legend: {
          position: "top"
        }
      }
    }
  });
}

// Fetch and display MTD summary
async function fetchMTDSummary(query = "") {
  const url = query ? `${API_BASE}/summary/mtd?${query}` : `${API_BASE}/summary/mtd`;
  const res = await fetch(url);
  const data = await res.json();
  renderMTDCards(data);
}

// Fetch and display monthly summary
async function fetchMonthlySummary(query = "") {
  const url = query ? `${API_BASE}/summary/monthly?${query}` : `${API_BASE}/summary/monthly`;
  const res = await fetch(url);
  const data = await res.json();
  renderMonthlyChart(data);
}

// Apply filters and refresh both views
async function applyFilters() {
  const query = buildQueryParams();
  await fetchMTDSummary(query);
  await fetchMonthlySummary(query);
}

// Initial load
fetchMTDSummary();
fetchMonthlySummary();

// Apply filters button
applyBtn.addEventListener("click", applyFilters);
