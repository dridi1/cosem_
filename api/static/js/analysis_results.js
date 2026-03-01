document.addEventListener("DOMContentLoaded", () => {
    initializeNavbar();
    initializeCharts();
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

function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        types: JSON.parse(decodeURIComponent(params.get("types")) || "[]"),
        superficie: JSON.parse(decodeURIComponent(params.get("superficie")) || "[]"),
        quantites: JSON.parse(decodeURIComponent(params.get("quantites")) || "[]"),
        rendement: JSON.parse(decodeURIComponent(params.get("rendement")) || "[]"),
    };
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

function initializeCharts() {
    if (!document.getElementById("pieChart")) {
        return;
    }

    const { types, superficie, quantites, rendement } = getQueryParams();
    const colorMap = getColorMap();
    const colors = types.map((type) => colorMap[type] || "#d3d3d3");

    Plotly.newPlot("pieChart", [{
        values: superficie,
        labels: types,
        type: "pie",
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true,
        marker: { colors },
    }], {
        title: "Share of sown area (ha)",
        showlegend: true,
    });

    Plotly.newPlot("barChart", [{
        x: types,
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
        title: "Collected quantities by crop",
        xaxis: { title: "Crop type" },
        yaxis: { title: "Collected quantities (q)" },
        barmode: "group",
    });

    Plotly.newPlot("pieChart1", [{
        values: quantites,
        labels: types,
        type: "pie",
        textinfo: "label+percent",
        textposition: "outside",
        automargin: true,
        marker: { colors },
    }], {
        title: "Share of collected quantities (q)",
        showlegend: true,
    });

    const normalizedRendement = normalizeValues(rendement);
    const rendementColors = normalizedRendement.map((value) => {
        const red = Math.floor((1 - value) * 255);
        const green = Math.floor(value * 255);
        return `rgb(${red}, ${green}, 0)`;
    });

    Plotly.newPlot("barChart1", [{
        x: types,
        y: rendement,
        type: "bar",
        marker: {
            color: rendementColors,
            colorscale: "Viridis",
            colorbar: { title: "Yield (q/ha)" },
        },
        text: rendement.map((value) => `Yield (q/ha): ${value}`),
        hoverinfo: "x+y+text",
    }], {
        title: "Yield by crop",
        xaxis: { title: "Crop type" },
        yaxis: { title: "Yield (q/ha)" },
        barmode: "group",
    });
}

function normalizeValues(values) {
    if (!values.length) {
        return [];
    }

    const maxValue = Math.max(...values);
    const minValue = Math.min(...values);

    if (maxValue === minValue) {
        return values.map(() => 0.5);
    }

    return values.map((value) => (value - minValue) / (maxValue - minValue));
}
