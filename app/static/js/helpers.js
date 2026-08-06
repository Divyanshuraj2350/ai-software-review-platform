/*
========================================
AI Software Review Platform
Helpers
========================================
*/


// -----------------------------
// Language Icons
// -----------------------------

function getLanguageIcon(language) {

    const icons = {

        "Python": "🐍",

        "Java": "☕",

        "JavaScript": "🟨",

        "TypeScript": "🔷",

        "HTML": "🌐",

        "CSS": "🎨",

        "C": "📘",

        "C++": "⚙️",

        "C#": "💜",

        "Go": "🐹",

        "Rust": "🦀",

        "PHP": "🐘",

        "Kotlin": "📱",

        "Swift": "🍎",

        "SQL": "🗄️",

        "Unknown": "📄"

    };

    return icons[language] || "📄";

}



// -----------------------------
// Score Formatter
// -----------------------------

function formatScore(score) {

    if (score === undefined || score === null) {
        return "0/10";
    }

    return `${Number(score).toFixed(1)}/10`;

}



// -----------------------------
// Safe List Generator
// -----------------------------

function createList(items) {

    if (!items || items.length === 0) {

        return `
            <p class="empty-list">
                Nothing found.
            </p>
        `;

    }

    return `

        <ul>

            ${items.map(item => `<li>${item}</li>`).join("")}

        </ul>

    `;

}



// -----------------------------
// Reset Analysis
// -----------------------------

function resetAnalysis() {

    const message = document.getElementById("message");

    const downloadBtn = document.getElementById("downloadBtn");

    const fileInput = document.getElementById("codeFile");

    message.innerHTML = "";

    downloadBtn.style.display = "none";

    fileInput.value = "";

}



// -----------------------------
// Loading
// -----------------------------

function showLoading(text) {

    const loading = document.getElementById("loading");

    loading.style.display = "block";

    loading.querySelector("p").innerText = text;

}



function hideLoading() {

    document.getElementById("loading").style.display = "none";

}



// -----------------------------
// Error Card
// -----------------------------

function renderError(error) {

    return `

        <div class="history-card">

            <h2 style="color:#ff4d4d;">
                ❌ Error
            </h2>

            <pre>${error}</pre>

        </div>

    `;

}