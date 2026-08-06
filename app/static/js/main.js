const form = document.getElementById("uploadForm");
const message = document.getElementById("message");
const loading = document.getElementById("loading");
const button = form.querySelector("button");
const downloadBtn = document.getElementById("downloadBtn");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const files = document.getElementById("codeFile").files;

    if (files.length === 0) {
        alert("Please select at least one supported source code file or ZIP file.");
        return;
    }

    message.innerHTML = "";
    downloadBtn.style.display = "none";

    loading.style.display = "block";

    button.disabled = true;
    button.innerText = "Analyzing...";

    const steps = [
        "📤 Uploading files...",
        "📦 Processing project...",
        "💻 Detecting programming languages...",
        "🤖 AI is reviewing code...",
        "🔍 Checking code quality...",
        "🛡️ Running security analysis...",
        "📄 Generating report..."
    ];

    let index = 0;

    loading.querySelector("p").innerText = steps[0];

    const interval = setInterval(() => {

        index = (index + 1) % steps.length;

        loading.querySelector("p").innerText = steps[index];

    }, 1500);

    try {

        const formData = new FormData();

        for (const file of files) {
            formData.append("files", file);
        }

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();

        clearInterval(interval);

        loading.style.display = "none";

        button.disabled = false;
        button.innerText = "Analyze Code";

        const project = data.project;

        let html = `

        <div class="history-card">

            <h2>📁 Project Summary</h2>

            <p><strong>Total Files:</strong> ${project.total_files}</p>

            <p><strong>Average Score:</strong> ⭐ ${project.average_score}/10</p>

            <p><strong>Total Bugs:</strong> 🐞 ${project.total_bugs}</p>

            <p><strong>Security Issues:</strong> 🔒 ${project.total_security}</p>

            <p><strong>Performance Issues:</strong> ⚡ ${project.total_performance}</p>

            <p><strong>Style Issues:</strong> 📏 ${project.total_pep8}</p>

        </div>

        <hr>

        <h2>📄 Individual File Reviews</h2>

        `;

        data.reviews.forEach(item => {

            const review = item.review;

            html += `

            <div class="history-card">

                <h2>💻 ${item.language}</h2>

                <h3>📄 ${item.filename}</h3>

                <h3>⭐ Score : ${review.score}/10</h3>

                <p><strong>Summary</strong></p>

                <p>${review.summary}</p>

                <h4>✅ Strengths</h4>

                <ul>
                    ${review.strengths.map(i => `<li>${i}</li>`).join("")}
                </ul>

                <h4>⚠ Weaknesses</h4>

                <ul>
                    ${review.weaknesses.map(i => `<li>${i}</li>`).join("")}
                </ul>

                <h4>💡 Suggestions</h4>

                <ul>
                    ${review.suggestions.map(i => `<li>${i}</li>`).join("")}
                </ul>

                <details>

                    <summary><strong>More Details</strong></summary>

                    <h4>🐞 Bugs</h4>

                    <ul>
                        ${review.bugs.map(i => `<li>${i}</li>`).join("")}
                    </ul>

                    <h4>🔒 Security</h4>

                    <ul>
                        ${review.security.map(i => `<li>${i}</li>`).join("")}
                    </ul>

                    <h4>⚡ Performance</h4>

                    <ul>
                        ${review.performance.map(i => `<li>${i}</li>`).join("")}
                    </ul>

                    <h4>📏 Style Issues</h4>

                    <ul>
                        ${review.pep8.map(i => `<li>${i}</li>`).join("")}
                    </ul>

                </details>

            </div>

            <br>

            `;

        });

        message.innerHTML = html;

        downloadBtn.style.display = "inline-block";

    }

    catch (error) {

        clearInterval(interval);

        loading.style.display = "none";

        button.disabled = false;

        button.innerText = "Analyze Code";

        message.innerHTML = `

        <h2 style="color:red;">❌ Error</h2>

        <pre>${error.message}</pre>

        `;

        console.error(error);

    }

});