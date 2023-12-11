<script>
$(document).ready(function() {
// Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
$("#delete-selected-establishment-button").click(function() {
// Crie um array para armazenar os IDs dos itens selecionados
var selectedItemsEst = [];

// Encontre todos os checkboxes marcados
$("input[name='selected_items_establishment']:checked").each(function() {
selectedItemsEst.push($(this).val());
});

// Verifique se pelo menos um item foi selecionado
if (selectedItemsEst.length > 0) {
// Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
$.post('{% url "delete_selected_establishments" %}', { 'selected_items_establishment[]': selectedItemsEst, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
// Recarregar a página ou atualizar a lista de itens na página, se necessário
location.reload();
});
} else {
alert("Nenhum item selecionado.");
}
});
});

$(document).ready(function() {
// Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
$("#delete-selected-sector-button").click(function() {
// Crie um array para armazenar os IDs dos itens selecionados
var selectedItemsSec = [];

// Encontre todos os checkboxes marcados
$("input[name='selected_items_sector']:checked").each(function() {
selectedItemsSec.push($(this).val());
});

// Verifique se pelo menos um item foi selecionado
if (selectedItemsSec.length > 0) {
// Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
$.post('{% url "delete_selected_sectors" %}', { 'selected_items_sector[]': selectedItemsSec, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
    // Recarregar a página ou atualizar a lista de itens na página, se necessário
    location.reload();
});
} else {
alert("Nenhum item selecionado.");
}
});
});
</script>
<script>
$(document).ready(function() {
// Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
$("#delete-selected-sub-sector-button").click(function() {
// Crie um array para armazenar os IDs dos itens selecionados
var selectedItemsSec = [];

// Encontre todos os checkboxes marcados
$("input[name='selected_items_sub_sector']:checked").each(function() {
    selectedItemsSec.push($(this).val());
});

// Verifique se pelo menos um item foi selecionado
if (selectedItemsSec.length > 0) {
    // Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
    $.post('{% url "delete_selected_sub_sectors" %}', { 'selected_items_sub_sector[]': selectedItemsSec, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
        // Recarregar a página ou atualizar a lista de itens na página, se necessário
        location.reload();
    });
} else {
    alert("Nenhum item selecionado.");
}
});
});
</script>
<script>
$(document).ready(function() {
// Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
$("#delete-selected-position-button").click(function() {
    // Crie um array para armazenar os IDs dos itens selecionados
    var selectedItemsEst = [];

    // Encontre todos os checkboxes marcados
    $("input[name='selected_items_position']:checked").each(function() {
        selectedItemsEst.push($(this).val());
    });

    // Verifique se pelo menos um item foi selecionado
    if (selectedItemsEst.length > 0) {
        // Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
        $.post('{% url "delete_selected_positions" %}', { 'selected_items_position[]': selectedItemsEst, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
            // Recarregar a página ou atualizar a lista de itens na página, se necessário
            location.reload();
        });
    } else {
        alert("Nenhum item selecionado.");
    }
});
});
</script>
<script>
$(document).ready(function() {
    // Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
    $("#delete-selected-shift-button").click(function() {
        // Crie um array para armazenar os IDs dos itens selecionados
        var selectedItemsEst = [];

        // Encontre todos os checkboxes marcados
        $("input[name='selected_items_shift']:checked").each(function() {
            selectedItemsEst.push($(this).val());
        });

        // Verifique se pelo menos um item foi selecionado
        if (selectedItemsEst.length > 0) {
            // Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
            $.post('{% url "delete_selected_shifts" %}', { 'selected_items_shift[]': selectedItemsEst, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
                // Recarregar a página ou atualizar a lista de itens na página, se necessário
                location.reload();
            });
        } else {
            alert("Nenhum item selecionado.");
        }
    });
});
</script>
<script>
    $(document).ready(function() {
        // Quando o botão "<span><i class="nf nf-fa-remove"></i></span> Remover" é clicado
        $("#delete-selected-status-button").click(function() {
            // Crie um array para armazenar os IDs dos itens selecionados
            var selectedItemsEst = [];

            // Encontre todos os checkboxes marcados
            $("input[name='selected_items_status']:checked").each(function() {
                selectedItemsEst.push($(this).val());
            });

            // Verifique se pelo menos um item foi selecionado
            if (selectedItemsEst.length > 0) {
                // Enviar os IDs dos itens selecionados para a view do Django para deletar os itens
                $.post('{% url "delete_selected_statuss" %}', { 'selected_items_status[]': selectedItemsEst, csrfmiddlewaretoken: '{{ csrf_token }}' }, function(data) {
                    // Recarregar a página ou atualizar a lista de itens na página, se necessário
                    location.reload();
                });
            } else {
                alert("Nenhum item selecionado.");
            }
        });
    });
</script>

<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#establishment-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de establishment
                    $('#establishment-list').replaceWith($(response).find('#establishment-list'));
                    $('#id_establishment_name').val('');
                }
            });
        });
    });
</script>
<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#sector-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de sector
                    $('#sector-list').replaceWith($(response).find('#sector-list'));
                    $('#id_sector_name').val('');
                }
            });
        });
    });
</script>
<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#sub-sector-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de sub-sector
                    $('#sub-sector-list').replaceWith($(response).find('#sub-sector-list'));
                    $('#id_subSector_name').val('');
                }
            });
        });
    });
</script>
<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#position-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de position
                    $('#position-list').replaceWith($(response).find('#position-list'));
                    $('#id_position_name').val('');
                }
            });
        });
    });
</script>
<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#shift-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de shift
                    $('#shift-list').replaceWith($(response).find('#shift-list'));
                    $('#id_shift_name').val('');
                }
            });
        });
    });
</script>
<script>
    $(document).ready(function() {
        // Captura o evento de envio do formulário
        $('#status-form').on('submit', function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário
    
            $.ajax({
                type: 'POST',
                url: '{% url 'settings' %}', // Substitua pelo URL correto
                data: $(this).serialize(), // Serializa o formulário
                success: function(response) {
                    // Atualiza apenas o elemento da lista de status
                    $('#status-list').replaceWith($(response).find('#status-list'));
                    $('#status-list-color').replaceWith($(response).find('#status-list-color'));
                    $('#id_status_name').val('');
                }
            });
        });
    });
</script>    
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const colorInputs = document.querySelectorAll('input[type="color"]');
        
        colorInputs.forEach(input => {
            input.addEventListener('change', function() {
                const selectedColor = this.value;
                this.style.backgroundColor = selectedColor;
            });
        });
    });
    </script>