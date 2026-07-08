function initializeShowActivities() {

    

    $("#searchButton").click(function () {

        $.ajax({
            url: "/get-activities/",
            data: {

                month: $("#month").val(),

                from_date: $("#from_date").val(),

                to_date: $("#to_date").val()

            },   // <-- Add this comma

            beforeSend: function () {
                $("#loading").show();
            },

            success: function (response) {

                // Hide previous data
                $("#activityTable tbody").empty();

                // No records found
                if (response.data.length === 0) {

                    $("#loading").hide();

                    $("#activityTable tbody").html(
                        "<tr><td colspan='8' style='text-align:center;'>No activities found.</td></tr>"
                    );

                    return;
                }

                // Add rows
                response.data.forEach(function (item) {

                    $("#activityTable tbody").append(`

                        <tr>

                        <td>
                            <div class="facultyCell">
                                <div class="facultyName">${item.faculty_name}</div>
                                <div class="facultyId">ID: ${item.faculty_id}</div>
                            </div>
                        </td>

                        <td>${item.activity}</td>

                        <td>${item.activity_date}</td>

                        <td>
                            ${item.entry_datetime}
                            ${
                                item.updated_at &&
                                item.updated_at !== item.entry_datetime
                                ? `<br><small class="editedText">✏️ Edited: ${item.updated_at}</small>`
                                : ""
                            }
                        </td>

                        <td>

                            ${item.attachments.map(file=>`

                            <a
                                class="proof-link"
                                href="/download-proof/${file.id}"
                                title="${file.filename}">

                                📄 ${
                                    file.filename.length > 18
                                    ? file.filename.substring(0,18) + "..."
                                    : file.filename
                                }

                            </a><br>

                            `).join("")}

                            </td>

                        <td
                            class="descriptionCell"
                            title="${item.description}">
                            ${item.description}
                        </td>

                        <td class="actionButtons">

                            <button
                                class="editButton"
                                data-id="${item.submission_id}">
                                ✏ Edit
                            </button>

                            <button
                                class="deleteButton"
                                data-id="${item.submission_id}">
                                🗑 Delete
                            </button>

                        </td>

                        </tr>

                    `);

                });

            },   // <-- THIS COMMA WAS MISSING

            complete: function () {
                $("#loading").hide();
            }
        });

    });

    $(document)
    .off("click", ".deleteButton")
    .on("click", ".deleteButton", function(){

        let id = $(this).data("id");

        Swal.fire({

            title: "Delete Activity?",

            text: "This activity and all its attachments will be permanently deleted.",

            icon: "warning",

            showCancelButton: true,

            confirmButtonColor: "#d33",

            cancelButtonColor: "#3085d6",

            confirmButtonText: "🗑 Yes, Delete",

            cancelButtonText: "Cancel"

        }).then((result) => {

            if(result.isConfirmed){

                $.ajax({

                    url: "/delete-activity/" + id + "/",

                    type: "POST",

                    headers:{
                        "X-CSRFToken": getCookie("csrftoken")
                    },

                    beforeSend:function(){

                        Swal.fire({

                            title:"Deleting...",

                            text:"Please wait.",

                            allowOutsideClick:false,

                            didOpen:()=>{

                                Swal.showLoading();

                            }

                        });

                    },

                    success:function(response){

                        Swal.fire({

                            icon:"success",

                            title:"Deleted!",

                            text:response.message,

                            timer:1500,

                            showConfirmButton:false

                        });

                        $("#searchButton").click();

                    },

                    error:function(){

                        Swal.fire({

                            icon:"error",

                            title:"Deletion Failed",

                            text:"Unable to delete the activity."

                        });

                    }

                });

            }

        });

    });

    $(document)
    .off("click", ".editButton")
    .on("click", ".editButton", function(){

        let id=$(this).data("id");

        $.get("/edit-activity/"+id+"/",function(response){

            $("#facultyBtn").click();

            setTimeout(function(){

                loadEditForm(response);

            },400);

        });

    });

}