function initializeMonthlyReport(){
    
    console.log("initializeMonthlyReport called");

    $(document)
    .off("submit", "#downloadForm")
    .on("submit", "#downloadForm", function(e){

        console.log("Download form submitted");

        e.preventDefault();

        Swal.fire({

            title:"Generating Report...",

            text:"Please wait.",

            allowOutsideClick:false,

            didOpen:()=>{

                Swal.showLoading();

            }

        });

        let formData = new FormData(this);

        fetch("/download-report/", {

            method: "POST",

            headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
            },

            body: formData

        })

        .then(async response => {

            if(!response.ok){

                Swal.close();

                let data = await response.json();

                Swal.fire({

                    icon:"warning",

                    title:"No Report Found",

                    text:data.message,

                    confirmButtonColor:"#0071e3"

                });

                return;
            }

            Swal.close();

            return response.blob();

        })

        .then(blob => {

            if(!blob) return;

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");

            a.href = url;

            a.download = "Monthly_Report.pdf";

            document.body.appendChild(a);

            a.click();

            document.body.removeChild(a);

            setTimeout(() => URL.revokeObjectURL(url), 1000);

            Swal.fire({

                icon:"success",

                title:"Download Started",

                text:"Your monthly report is downloading.",

                timer:1500,

                showConfirmButton:false

            });

        });

    });

}