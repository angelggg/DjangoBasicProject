function CreateEntityAjax()
    {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var entity_id = $("#entity_id").val();

        if (isNaN(entity_id)) {
            alert("Please insert a numeric value: " + entity_id);
            return false;
        }

        $.ajax({
            headers:{"X-CSRFToken": csrftoken},
            type: "POST",
            url: "/create_entities/",
            data: {"entity_id": entity_id},
            context: document.body,
            statusCode: {
                400: function() {
                    $("#create_entity_result").html("<span class='glyphicon glyphicon-print'></span> Failed ");
                }
            },

            success: function(response){
                console.log(response);
                $("#create_entity_result").html("<span class='glyphicon glyphicon-print'></span> Added " + response.created + " records");
            }
        })
    }