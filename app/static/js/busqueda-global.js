const searchInput =
    document.getElementById("global-search");

const resultsBox =
    document.getElementById("search-results");

searchInput?.addEventListener("input", async function () {

    const q = this.value.trim();

    if (q.length < 2) {
        resultsBox.innerHTML = "";
        return;
    }

    const response =
        await fetch(`/buscar-global?q=${encodeURIComponent(q)}`);

    const data = await response.json();

    resultsBox.innerHTML = data.map(item => `
        <a href="${item.url}" class="search-item">
            <small>${item.tipo}</small>
            <strong>${item.texto}</strong>
        </a>
    `).join("");

});

