document.addEventListener("DOMContentLoaded", () => {
    initializeNavbar();
    initializeStaticDashboard();
    initializeAnalyzePage();
    initializeAnalyzeButton();
});

function initializeNavbar() {
    const toggle = document.getElementById("header-toggle");
    const nav = document.getElementById("nav-bar");
    const body = document.getElementById("body-pd");
    const header = document.getElementById("header");

    if (toggle && nav && body && header) {
        toggle.addEventListener("click", () => {
            nav.classList.toggle("show");
            toggle.classList.toggle("bx-x");
            body.classList.toggle("body-pd");
            header.classList.toggle("body-pd");
        });
    }

    document.querySelectorAll(".nav_link").forEach((link) => {
        link.addEventListener("click", function colorLink() {
            document.querySelectorAll(".nav_link").forEach((item) => item.classList.remove("active"));
            this.classList.add("active");
        });
    });
}

function hasRequiredElements(ids) {
    return ids.every((id) => document.getElementById(id));
}

async function loadKribData() {
    const response = await fetch("/static/Firme_de_Krib.csv");
    const csvText = await response.text();
    return Papa.parse(csvText, { header: true, skipEmptyLines: true }).data;
}

function getColorMap() {
    return {
        "BlÃ© dur": "#00441b",
        "BlÃ© tendre": "#006d2c",
        "Orge": "#31a354",
        Triticale: "#a1d99b",
        Autres: "#c2c2c2",
    };
}

async function initializeStaticDashboard() {
    if (!hasRequiredElements(["pieChart", "barChart", "pieChart1", "barChart1", "myTable1"])) {
        return;
    }

    const rows = await loadKribData();
    const colorMap = getColorMap();
    const labels = rows.map((item) => item["Type Groupe"]);
    const superficie = rows.map((item) => parseFloat(item["Superficie semÃ©e (ha)"]) || 0);
    const quantites = rows.map((item) => parseFloat(item["QuantitÃ©s collectÃ©es (q)"]) || 0);
    const rendement = rows.map((item) => parseFloat(item["Rendement (q/ha)"]) || 0);
    const colors = labels.map((label) => colorMap[label] || "#d3d3d3");

    Plotly.newPlot("pieChart", [{
        values: superficie,
        labels,
        type: "pie",
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true,
        marker: { colors },
    }], { title: "COSEM 2023: Sown area by crop", showlegend: true });

    Plotly.newPlot("barChart", [{
        x: labels,
        y: quantites,
        type: "bar",
        marker: {
            color: superficie,
            colorscale: "Greens",
            colorbar: { title: "Sown area (ha)" },
        },
        text: superficie.map((value) => `Sown area (ha): ${value}`),
        hoverinfo: "x+y+text",
    }], {
        title: "COSEM 2023: Collected quantities by crop",
        xaxis: { title: "Crop type" },
        yaxis: { title: "Collected quantities (q)" },
        barmode: "group",
    });

    Plotly.newPlot("pieChart1", [{
        values: quantites,
        labels,
        type: "pie",
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true,
        marker: { colors },
    }], { title: "COSEM 2023: Share of collected quantities", showlegend: true });

    Plotly.newPlot("barChart1", [{
        x: labels,
        y: rendement,
        type: "bar",
        marker: {
            color: rendement,
            colorscale: "Reds",
            colorbar: { title: "Yield (q/ha)" },
        },
        text: rendement.map((value) => `Yield (q/ha): ${value}`),
        hoverinfo: "x+y+text",
    }], {
        title: "COSEM 2023: Yield by crop",
        xaxis: { title: "Crop type" },
        yaxis: { title: "Yield (q/ha)" },
        barmode: "group",
    });

    renderDataTable(rows, "myTable1", "tableHeader1", "tableBody1");
}

function renderDataTable(rows, tableId, headerId, bodyId) {
    const tbody = document.getElementById(bodyId);
    const thead = document.getElementById(headerId);

    if (!tbody || !thead || rows.length === 0) {
        return;
    }

    const headers = Object.keys(rows[0]);
    thead.innerHTML = "";
    tbody.innerHTML = "";

    const headerRow = document.createElement("tr");
    headers.forEach((header) => {
        const th = document.createElement("th");
        th.innerText = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    rows.forEach((row) => {
        const tr = document.createElement("tr");
        headers.forEach((header) => {
            const td = document.createElement("td");
            td.innerText = row[header];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    if (window.$ && $.fn.DataTable) {
        const tableSelector = `#${tableId}`;
        if ($.fn.DataTable.isDataTable(tableSelector)) {
            $(tableSelector).DataTable().destroy();
        }
        $(tableSelector).DataTable();
    }
}

function initializeAnalyzePage() {
    const form = document.getElementById("dataForm");
    const mapElement = document.getElementById("map");

    if (!form || !mapElement || !window.L) {
        return;
    }

    const savePolygonUrl = form.dataset.savePolygonUrl || "/save_polygon";
    const resultsUrl = form.dataset.resultsUrl || "/yourdash";
    const map = L.map("map").setView([33.8869, 9.5375], 6);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
        edit: { featureGroup: drawnItems },
        draw: {
            polygon: true,
            polyline: false,
            rectangle: false,
            circle: false,
            marker: false,
            circlemarker: false,
        },
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, async (event) => {
        const layer = event.layer;
        drawnItems.addLayer(layer);

        const polygonCoordinates = layer.getLatLngs()[0].map((coord) => [coord.lat, coord.lng]);

        try {
            const response = await fetch(savePolygonUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ coordinates: polygonCoordinates }),
            });
            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Failed to register polygon");
            }

            alert("Polygon has been successfully registered.");
        } catch (error) {
            console.error("Error saving polygon:", error);
            alert("An error occurred while saving the polygon. Please try again.");
        }
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const types = Array.from(form.querySelectorAll("tbody tr td:first-child")).map((cell) => cell.textContent.trim());
        const superficie = Array.from(form.querySelectorAll('input[name="superficie[]"]')).map((input) => parseFloat(input.value) || 0);
        const quantites = Array.from(form.querySelectorAll('input[name="quantites[]"]')).map((input) => parseFloat(input.value) || 0);
        const rendement = Array.from(form.querySelectorAll('input[name="rendement[]"]')).map((input) => parseFloat(input.value) || 0);

        const queryString = new URLSearchParams({
            types: JSON.stringify(types),
            superficie: JSON.stringify(superficie),
            quantites: JSON.stringify(quantites),
            rendement: JSON.stringify(rendement),
        }).toString();

        window.location.assign(`${resultsUrl}?${queryString}`);
    });
}

function initializeAnalyzeButton() {
    const button = document.getElementById("analyze-button");
    if (!button) {
        return;
    }

    button.addEventListener("click", () => {
        if (button.classList.contains("loading")) {
            return;
        }

        button.classList.add("loading");

        window.setTimeout(() => {
            window.location.assign(button.dataset.targetUrl);
        }, 500);
    });
}
