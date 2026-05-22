async function updateStatus() {
  try {
    const res = await fetch("/status.json?t=" + Date.now());
    const data = await res.json();

    document.getElementById("food").innerText = data.zh || data.food || "--";
    document.getElementById("confidence").innerText =
      data.confidence ? (data.confidence * 100).toFixed(1) + "%" : "--";
    document.getElementById("weight").innerText = data.weight_g ?? "--";
    document.getElementById("time").innerText = data.time || "--";
    document.getElementById("kcal").innerText = data.kcal ?? "--";
    document.getElementById("protein").innerText = data.protein ?? "--";
    document.getElementById("fat").innerText = data.fat ?? "--";
    document.getElementById("carbs").innerText = data.carbs ?? "--";
  } catch (e) {
    console.log("waiting for status.json...");
  }
}

setInterval(updateStatus, 1000);
updateStatus();
