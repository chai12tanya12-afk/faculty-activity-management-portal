$(function () {

    function loadSection(url, element){

        $("#loading").show();

        $("#mainContent").css("opacity","0.4");

        console.log("Loading:", url);

        $("#mainContent").load(url, function(response, status){

            console.log("Status:", status);

            $("#loading").hide();

            if(status=="error"){

                $("#mainContent").html(
                    "<center><h3>Unable to load the page.</h3></center>"
                );

                $("#mainContent").css("opacity","1");

                return;
            }

            $(".mac-nav a").removeClass("activeMenu");
            element.addClass("activeMenu");

            document.activeElement.blur();

            $("#breadcrumb").html(
                '<a href="#" id="breadcrumbDashboard">Dashboard</a>' +
                (element.attr("id") !== "dashboardBtn"
                    ? ' > <span>' + element.text().trim() + '</span>'
                    : '')
            );

            $("#breadcrumbDashboard")
            .off("click")
            .on("click", function(e){

                e.preventDefault();

                $("#dashboardBtn").click();

            });

            if(url.includes("faculty-form")){
                initializeFacultyForm();
            }

            if(url.includes("monthly-report")){
                initializeMonthlyReport();
            }

            if(url.includes("show-activities")){
                initializeShowActivities();
            }

            $("#mainContent").css("opacity","1");

        });

    }

    $("#facultyBtn").click(function(e){

        e.preventDefault();

        loadSection($(this).data("url"),$(this));

    });

    $("#reportBtn").click(function(e){

        e.preventDefault();

        loadSection($(this).data("url"),$(this));

    });

    $("#activityBtn").click(function(e){

        e.preventDefault();

        loadSection($(this).data("url"),$(this));

    });

    $("#dashboardBtn").click(function(e){

        e.preventDefault();

        loadSection($(this).data("url"),$(this));

    });

    $("#dashboardBtn").click();

});

function showToast(message){

    $("#toast")
        .text(message)
        .fadeIn(300);

    setTimeout(function(){

        $("#toast").fadeOut(300);

    },3000);

}

function getCookie(name){

    let cookieValue = null;

    if(document.cookie && document.cookie !== ''){

        const cookies = document.cookie.split(';');

        for(let cookie of cookies){

            cookie = cookie.trim();

            if(cookie.startsWith(name + '=')){

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;

            }

        }

    }

    return cookieValue;

}