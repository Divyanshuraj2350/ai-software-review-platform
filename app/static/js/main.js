const form = document.getElementById("uploadForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const file = document.getElementById("codeFile").files[0];

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch("/upload", {

        method: "POST",

        body: formData

    });

    const data = await response.json();

    document.getElementById("message").innerText = data.message;

});