const form = document.getElementById("uploadForm");
const message = document.getElementById("message");
const loading = document.getElementById("loading");
const button = form.querySelector("button");
const downloadBtn = document.getElementById("downloadBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = document.getElementById("codeFile").files[0];

    if (!file) {
        alert("Please select a Python file.");
        return;
    }

    // Reset UI
    message.innerHTML = "";
    downloadBtn.style.display = "none";

    loading.style.display = "block";

    button.disabled = true;
    button.innerText = "Analyzing...";

    const steps = [
        "📤 Uploading file...",
        "🤖 AI is understanding your code...",
        "🔍 Finding bugs...",
        "⚡ Checking performance...",
        "🛡️ Checking security issues...",
        "📝 Preparing report..."
    ];

    let index = 0;
    loading.querySelector("p").innerText = steps[0];

    const interval = setInterval(() => {
        index = (index + 1) % steps.length;
        loading.querySelector("p").innerText = steps[index];
    }, 1500);

    try {

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();

        const review = data.review;

        // Save review for PDF
       

        clearInterval(interval);

        loading.style.display = "none";

        button.disabled = false;
        button.innerText = "Analyze Code";

        message.innerHTML = `
<h2>⭐ Overall Score : ${review.score}/10</h2>

<h3>📄 Summary</h3>
<p>${review.summary}</p>

<h3>🐞 Bugs</h3>
<ul>
${review.bugs.map(item => `<li>${item}</li>`).join("")}
</ul>

<h3>🔒 Security Issues</h3>
<ul>
${review.security.map(item => `<li>${item}</li>`).join("")}
</ul>

<h3>⚡ Performance Improvements</h3>
<ul>
${review.performance.map(item => `<li>${item}</li>`).join("")}
</ul>

<h3>🧹 Code Quality</h3>
<ul>
${review.quality.map(item => `<li>${item}</li>`).join("")}
</ul>

<h3>📘 PEP8 Issues</h3>
<ul>
${review.pep8.map(item => `<li>${item}</li>`).join("")}
</ul>
`;

        // Show download button
        downloadBtn.style.display = "inline-block";

    } catch (error) {

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