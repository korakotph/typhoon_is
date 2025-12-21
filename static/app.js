async function upload() {
  const fileInput = document.getElementById("fileInput");
  const loading = document.getElementById("loading");
  const btn = document.getElementById("analyzeBtn");
  const jsonBox = document.getElementById("jsonResult");

  if (!fileInput.files.length) {
    alert("กรุณาเลือกไฟล์");
    return;
  }

  // UI: เริ่มวิเคราะห์
  loading.style.display = "block";
  btn.disabled = true;
  btn.textContent = "กำลังวิเคราะห์...";
  jsonBox.textContent = "";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Server error: " + res.status);
    }

    const data = await res.json();

    // แสดง JSON ดิบ
    jsonBox.textContent = JSON.stringify(data, null, 2);

    // แสดงผลในตาราง
    renderResult(data.analysis);

  } catch (err) {
    jsonBox.textContent = "❌ ERROR:\n" + err.message;
  } finally {
    // UI: เสร็จแล้ว
    loading.style.display = "none";
    btn.disabled = false;
    btn.textContent = "วิเคราะห์";
  }
}

function renderResult(data) {
  const tbody = document.querySelector("#itemsTable tbody");
  tbody.innerHTML = "";

  let calcSubtotal = 0;

  data.items.forEach(item => {
    calcSubtotal += item.total;

    tbody.innerHTML += `
      <tr>
        <td>${item.name}</td>
        <td>${item.quantity}</td>
        <td>${item.unit_price.toLocaleString()}</td>
        <td>${item.total.toLocaleString()}</td>
      </tr>
    `;
  });

  const vatCalc = calcSubtotal * data.vat_rate / 100;
  const vatDiff = Math.abs(vatCalc - data.vat);

  document.getElementById("subtotal").textContent =
    calcSubtotal.toLocaleString() + " บาท";

  document.getElementById("vat").textContent =
    data.vat.toLocaleString() + " บาท";

  document.getElementById("grand").textContent =
    data.grand_total.toLocaleString() + " บาท";

  const alertBox = document.getElementById("alert");

  if (vatDiff > 1) {
    alertBox.className = "alert-error";
    alertBox.textContent =
      `⚠️ VAT ไม่ตรง (คำนวณได้ ${vatCalc.toFixed(2)} บาท)`;
  } else {
    alertBox.className = "alert-ok";
    alertBox.textContent = "✅ VAT ถูกต้อง";
  }
}
