$(function () {
    // Inicializar o Sortable
    $("#sortable").sortable({
        items: "> div:not(#header-preset)",
        update: function (event, ui) {
            saveOrderAutomatically();
        }
    });
    $("#sortable").disableSelection();

    // Associar função ao clique nos itens do setor
    $(".dropdown-item-sector").on("click", function () {
        // ... seu código atual para atualizar o setor ...
    });

    // Associar função ao clique nos itens do header
    $(".dropdown-item-head").on("click", function () {
        // ... seu código atual para atualizar o header ...
    });

    // Função para salvar automaticamente a ordem dos cards
    function saveOrderAutomatically() {
        var newOrder = [];
        $("#sortable > div").each(function () {
            newOrder.push($(this).data("id"));
        });

        var csrftoken = Cookies.get('csrftoken');

        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });

        // Enviar a nova ordem para o servidor
        $.ajax({
            url: updatePositionsUrl,
            type: "POST",
            data: JSON.stringify(newOrder),
            contentType: "application/json",
        });
    }
});

$(function () {
    $(".dropdown-item-sector").on("click", function () {
        var newWidth = $(this).data("width");
        var sectorId = $(this).closest(".draggable-card").data("id");

        var csrftoken = Cookies.get('csrftoken');

        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });

        $.ajax({
            url: `${updateSectorWidthUrl}/${sectorId}/${newWidth}/`,
            type: "POST",
            success: function (data) {
                window.location.reload();
            },
        });
    });
});

$(function () {
    $(".dropdown-item-head").on("click", function () {
        var newWidth = $(this).data("width");
        var presetId = preset_id;

        var csrftoken = Cookies.get('csrftoken');

        console.log("Preset ID:", presetId);  // Verifique se o valor está correto

        $.ajaxSetup({
            headers: { "X-CSRFToken": csrftoken }
        });

        $.ajax({
            url: `${updateHeaderWidthUrl}/${presetId}/${newWidth}/`,
            type: "POST",
            success: function (data) {
                console.log(data);  // Adicione este console.log para verificar a resposta do servidor
                window.location.reload();
            },
            error: function (xhr, status, error) {
                console.error("Erro ao atualizar a largura do header:", error);
            }
        });
    });
});