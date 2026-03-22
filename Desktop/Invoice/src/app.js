const statusEl = document.getElementById("status");
const rowsEl = document.getElementById("invoiceRows");
const statsEl = document.getElementById("stats");
const refreshBtn = document.getElementById("refreshBtn");

function formatMoney(value) {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2
    }).format(Number(value || 0));
}

function setStatus(text, isWarning = false) {
    statusEl.textContent = text;
    statusEl.classList.toggle("warn", isWarning);
}

function renderStats(invoices) {
    const totalInvoices = invoices.length;
    const totalAmount = invoices.reduce((sum, item) => sum + Number(item.total_amount || 0), 0);
    const totalAdvance = invoices.reduce((sum, item) => sum + Number(item.advance_paid || 0), 0);
    const totalBalance = invoices.reduce((sum, item) => sum + Number(item.balance || 0), 0);

    statsEl.innerHTML = `
        <article class="stat-card"><div class="label">Invoices</div><div class="value">${totalInvoices}</div></article>
        <article class="stat-card"><div class="label">Total Amount</div><div class="value">${formatMoney(totalAmount)}</div></article>
        <article class="stat-card"><div class="label">Advance Paid</div><div class="value">${formatMoney(totalAdvance)}</div></article>
        <article class="stat-card"><div class="label">Balance</div><div class="value">${formatMoney(totalBalance)}</div></article>
    `;
}

function renderRows(invoices) {
    if (!Array.isArray(invoices) || invoices.length === 0) {
        rowsEl.innerHTML = '<tr><td colspan="9" class="empty">No invoices found.</td></tr>';
        return;
    }

    rowsEl.innerHTML = invoices
        .map((invoice) => `
            <tr>
                <td>${invoice.id ?? "-"}</td>
                <td>${invoice.customer_name ?? "-"}</td>
                <td>${invoice.phone ?? "-"}</td>
                <td>${invoice.description ?? "-"}</td>
                <td>${formatMoney(invoice.total_amount)}</td>
                <td>${formatMoney(invoice.advance_paid)}</td>
                <td>${formatMoney(invoice.balance)}</td>
                <td>${invoice.type ?? "-"}</td>
                <td>${invoice.date ?? "-"}</td>
            </tr>
        `)
        .join("");
}

async function loadInvoices() {
    try {
        const cacheBuster = `t=${Date.now()}`;
        const response = await fetch(`/invoices_data.json?${cacheBuster}`);
        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const invoices = await response.json();
        renderStats(invoices);
        renderRows(invoices);
        setStatus(`Updated: ${new Date().toLocaleTimeString()}`);
    } catch (error) {
        setStatus(`Could not load invoices_data.json (${error.message})`, true);
    }
}

refreshBtn.addEventListener("click", loadInvoices);
loadInvoices();
setInterval(loadInvoices, 3000);