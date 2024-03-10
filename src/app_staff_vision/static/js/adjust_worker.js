document.addEventListener("DOMContentLoaded", function() {
    const selectSector = document.getElementById("filtro-setor");
    const campoBusca = document.getElementById("campo-busca");
    const tabelaWorkers = document.getElementById("tabela-workers").getElementsByTagName("tbody")[0];
    const workers = tabelaWorkers.getElementsByTagName("tr");

    selectSector.addEventListener("change", function() {
        filterWorkers();
    });

    campoBusca.addEventListener("input", function() {
        filterWorkers();
    });

    function filterWorkers() {
        const selectedSector = selectSector.value.toLowerCase();
        const searchTerm = campoBusca.value.toLowerCase();

        for (let i = 0; i < workers.length; i++) {
            const worker = workers[i];
            const workerSector = worker.querySelector("td:nth-child(5)").textContent.trim().toLowerCase(); // Ajuste o índice conforme necessário
            const workerName = worker.querySelector("td:nth-child(3)").textContent.trim().toLowerCase(); // Ajuste o índice conforme necessário

            if ((selectedSector === "" || workerSector === selectedSector) &&
                (searchTerm === "" || workerName.includes(searchTerm))) {
                worker.style.display = "";
            } else {
                worker.style.display = "none";
            }
        }
    }

    // Disparar o evento 'change' para exibir todos os trabalhadores inicialmente
    selectSector.dispatchEvent(new Event('change'));
});

document.addEventListener("DOMContentLoaded", function() {
    const tabelaWorkers = document.getElementById("tabela-workers");
    const tableBody = tabelaWorkers.querySelector("tbody");
    const tableHeaders = tabelaWorkers.querySelectorAll("th");
    const rows = Array.from(tableBody.rows);

    tableHeaders.forEach(header => {
        header.addEventListener("click", () => {
            const columnIndex = header.cellIndex;
            const sortDirection = header.getAttribute("data-sort-direction") || "asc";

            const dataRows = rows.slice(); // Exclui a primeira linha (linha de cabeçalho)

            dataRows.sort((a, b) => {
                const cellA = a.cells[columnIndex].textContent.trim();
                const cellB = b.cells[columnIndex].textContent.trim();
                
                const numA = parseFloat(cellA);
                const numB = parseFloat(cellB);
                
                if (!isNaN(numA) && !isNaN(numB)) {
                    return numA - numB;
                } else {
                    return cellA.localeCompare(cellB);
                }
            });

            // Limpa a tabela
            while (tableBody.rows.length > 0) {
                tableBody.deleteRow(0);
            }

            // Adiciona as linhas classificadas de volta à tabela
            dataRows.forEach(row => {
                tableBody.appendChild(row);
            });

            // Remove a classe "bi-arrow-up" ou "bi-arrow-down" de todas as setas
            tableHeaders.forEach(th => {
                th.querySelector("i").classList.remove("bi-arrow-up", "bi-arrow-down");
                th.removeAttribute("data-sort-direction");
            });

            // Define a classe da seta e o atributo data-sort-direction no cabeçalho clicado
            header.querySelector("i").classList.add(sortDirection === "asc" ? "bi-arrow-up" : "bi-arrow-down");
            header.setAttribute("data-sort-direction", sortDirection === "asc" ? "desc" : "asc");
        });
    });
});

// Detecta o dispositivo móvel
var is_mobile = window.innerWidth <= 768; // Defina o valor apropriado para o ponto de corte entre celular e desktop