function initializeTomSelect(config){

    new TomSelect(config.selector,{

        create:function(input,callback){

            Swal.fire({

                title:config.title,

                html:
                "<b>"+input+"</b><br><br>"+
                "Do you want to add this to the database?",

                icon:"question",

                showCancelButton:true,

                confirmButtonText:"➕ Yes, Add",

                cancelButtonText:"Cancel"

            }).then(function(result){

                if(!result.isConfirmed){

                    callback();

                    return;

                }

                $.ajax({

                    url:config.url,

                    type:"POST",

                    headers:{
                        "X-CSRFToken":getCookie("csrftoken")
                    },

                    data:{
                        [config.field]:input
                    },

                    success:function(response){

                        let ts = document.querySelector(config.selector).tomselect;

                        ts.addOption({
                            value: response.id,
                            text: response.name
                        });

                        ts.addItem(response.id);

                        reloadTomSelect(
                            config.selector,
                            config.field === "faculty_name"
                                ? "/faculty-list/"
                                : "/activity-list/"
                        );

                        Swal.fire({
                            icon:"success",
                            title:"Added Successfully",
                            timer:1200,
                            showConfirmButton:false
                        });

                        callback();

                        Swal.fire({

                            icon:"success",

                            title:"Added Successfully",

                            timer:1200,

                            showConfirmButton:false

                        });

                    }

                });

            });

        },

        createOnBlur:false,

        persist:false,

        maxItems:config.multiple ? null : 1,

        plugins: config.multiple
            ? ["remove_button"]
            : (config.plugins || []),

        placeholder:config.placeholder,

        onItemAdd:function(){

            this.close();
            this.blur();

        }

    });

}

function reloadTomSelect(selector, url){

    let ts = document.querySelector(selector).tomselect;

    $.get(url, function(data){

        ts.clearOptions();

        data.forEach(function(item){

            ts.addOption({
                value: item.id,
                text: item.name
            });

        });

        ts.refreshOptions(false);

    });

}

function initializeFacultyForm() {

    initializeTomSelect({

        selector:"#faculty",

        placeholder:"Search Faculty",

        title:"Add Faculty?",

        url:"/add-faculty/",

        field:"faculty_name",

        multiple:true

    });

    initializeTomSelect({

        selector:"#activity",

        placeholder:"Search Activity",

        title:"Add Activity?",

        url:"/add-activity/",

        field:"activity_name",

        multiple:false,

        plugins:["clear_button"]

    });

    $(document)
    .off("submit", "#activityForm")
    .on("submit", "#activityForm", function(e){

        e.preventDefault();

        var formData = new FormData(this);

        let editId=$("#activityForm").attr("data-edit-id");

        let url="/submit/";

        if(editId){

            url="/update-activity/"+editId+"/";

        }

        $.ajax({

            url:url,

            type: "POST",

            data: formData,

            processData: false,

            contentType: false,

            success: function(response){

                showToast(response.message);
                $("#activityForm").removeAttr("data-edit-id");

                $(".primaryButton").text("🚀 Submit Activity");

                $("#cancelEditButton")
                    .text("Reset")
                    .removeClass("cancelEdit");

                selectedFiles = new DataTransfer();
                document.querySelector("#faculty").tomselect.setValue(data.faculty);

                document.querySelector("#activity").tomselect.setValue(data.activity);
                $("#activityForm")[0].reset();
                $("#fileList").empty();

            },

            error: function(xhr){

                let message = "Unknown Error";

                if(xhr.responseJSON && xhr.responseJSON.message){
                    message = xhr.responseJSON.message;
                }else{
                    message = xhr.responseText;
                }

                $("#message").html(`
                    <div class="alert alert-danger">
                        ${message}
                    </div>
                `);

            }

        });

    });

    let selectedFiles = new DataTransfer();

    $(document)
    .off("change", "#attachments")
    .on("change", "#attachments", function(){

        Array.from(this.files).forEach(file => {
            selectedFiles.items.add(file);
        });

        this.files = selectedFiles.files;

        renderFiles();
    });

    const uploadArea = $(".upload-area");

    /* Prevent browser opening PDF */

    uploadArea.on("dragenter dragover", function(e){

        e.preventDefault();
        e.stopPropagation();

        $(this).addClass("dragging");

    });

    uploadArea.on("dragleave", function(e){

        e.preventDefault();
        e.stopPropagation();

        $(this).removeClass("dragging");

    });

    uploadArea.on("drop", function(e){

        e.preventDefault();
        e.stopPropagation();

        $(this).removeClass("dragging");

        const files = e.originalEvent.dataTransfer.files;

        Array.from(files).forEach(file => {

            if(file.type !== "application/pdf"){

                Swal.fire({

                    icon:"warning",

                    title:"Only PDF Files",

                    text:"Please drop PDF files only."

                });

                return;
            }

            selectedFiles.items.add(file);

        });

        $("#attachments")[0].files = selectedFiles.files;

        renderFiles();

    });

    function renderFiles() {

        $("#fileList").empty();

        Array.from(selectedFiles.files).forEach((file, index) => {

            $("#fileList").append(`
            <li class="file-item">
                <span>📄 ${file.name}</span>
                <button
                    type="button"
                    class="remove-file"
                    data-index="${index}"
                    title="Remove">
                    ✖
                </button>
            </li>
            `);

        });

    }

    $(document)
    .off("click",".remove-file")
    .on("click",".remove-file",function(){

        let index = $(this).data("index");

        let dt = new DataTransfer();

        Array.from(selectedFiles.files).forEach((file, i) => {

            if (i != index) {

                dt.items.add(file);

            }

        });

        selectedFiles = dt;

        $("#attachments")[0].files = selectedFiles.files;

        renderFiles();

    });

    $(document)
    .off("click","#cancelEditButton")
    .on("click","#cancelEditButton",function(){

        if($("#activityForm").attr("data-edit-id")){

            $("#activityForm").removeAttr("data-edit-id");

            $(".primaryButton").text("🚀 Submit Activity");

            $(this)
                .text("Reset")
                .removeClass("cancelEdit");

            $("#activityForm")[0].reset();

            document.querySelector("#faculty").tomselect.clear();

            document.querySelector("#activity").tomselect.clear();

            $("#fileList").empty();

            $("#existingAttachments").empty();

            $("#existingTitle").hide();

            selectedFiles = new DataTransfer();

            return;

        }

        $("#activityForm")[0].reset();

        document.querySelector("#faculty").tomselect.clear();

        document.querySelector("#activity").tomselect.clear();

        $("#fileList").empty();

    });

}

function loadEditForm(data){

    document.querySelector("#faculty").tomselect.setValue(data.faculty);

    document.querySelector("#activity").tomselect.setValue(data.activity);

    $("#id_activity_date")
         .val(data.activity_date);

    $("#entry_date").val(data.entry_date);

    $("#id_description")
          .val(data.description);

    $("#activityForm")
          .attr(
             "data-edit-id",
             data.submission_id
         );
    $(".primaryButton")
        .text("Update Activity");

    $("#cancelEditButton")
        .text("Cancel")
        .addClass("cancelEdit");

    $("#existingAttachments").empty();

    if(data.attachments.length > 0){

        $("#existingTitle").show();

    }else{

        $("#existingTitle").hide();

    }

    data.attachments.forEach(function(file){

        $("#existingAttachments").append(`

        <div class="existingFile" id="attachment-${file.id}">

            <a href="/download-proof/${file.id}">
                📄 ${file.name}
            </a>

            <button
                type="button"
                class="deleteAttachment"
                data-id="${file.id}">
                ✖
            </button>

        </div>

        `);

    });
}

$(document)

.off("click", ".deleteAttachment")

.on("click", ".deleteAttachment", function(){

    let id = $(this).data("id");

    Swal.fire({

        title: "Delete Attachment?",

        text: "This attachment will be permanently deleted.",

        icon: "warning",

        showCancelButton: true,

        confirmButtonColor: "#d33",

        cancelButtonColor: "#3085d6",

        confirmButtonText: "🗑 Yes, Delete",

        cancelButtonText: "Cancel"

    }).then((result) => {

        if(result.isConfirmed){

            $.ajax({

                url: "/delete-attachment/" + id + "/",

                type: "POST",

                headers:{

                    "X-CSRFToken": getCookie("csrftoken")

                },

                success:function(response){

                    $("#attachment-" + id).remove();

                    Swal.fire({

                        icon: "success",

                        title: "Deleted!",

                        text: "Attachment deleted successfully.",

                        timer: 1500,

                        showConfirmButton: false

                    });

                },

                error:function(){

                    Swal.fire(

                        "Error",

                        "Unable to delete attachment.",

                        "error"

                    );

                }

            });

        }

    });

});

