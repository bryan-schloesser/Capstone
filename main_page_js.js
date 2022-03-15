$(document).ready(function(e) {
    //Gets graphs and hides them by default
    $('#graph1').hide();
    $('#graph2').hide();
    $('#graph3').hide();

    //Used to switch tabs on click and hide the other tabs
    $('ul.nav li a').click(function(e) {
        $(this).addClass('selected').parent().siblings().children().removeClass('selected');
        $(this.hash).show().siblings('div').hide();
    });
    //Requests graph 1 on click
    $('#graph1Nav').click(function(e) {
        $("#graph1 img").remove();
        getGraphImages(1);
    });
    //Requests graph 2 on click
    $('#graph2Nav').click(function(e) {
        $("#graph2 img").remove();
        getGraphImages(2);
    });
    //Requests graph 3 on click
    $('#graph3Nav').click(function(e) {
        $("#graph3 img").remove();
        getGraphImages(3);
    });

    //Function to get chemical values from the form.
    function getChemValues() {
        var chem_vals = [] //array to store user variables in.

        //Assigns user inputted values to the respective chemical.
        const F_ACIDITY = parseFloat($('#fAcidity').val());
        const V_ACIDITY = parseFloat($('#vAcidity').val());
        const CIT_ACID = parseFloat($('#citAcid').val());
        const RES_SUGAR = parseFloat($('#resSugar').val())
        const CHLOR = parseFloat($('#chlor').val());
        const F_SULFUR_D = parseFloat($('#fSulfurD').val());
        const T_SULFUR_D = parseFloat($('#tSulfurD').val());
        const DENSITY = parseFloat($('#density').val());
        const PH = parseFloat($('#pH').val());
        const SULPH = parseFloat($('#sulph').val());
        const ALCH = parseFloat($('#alch').val());

        //pushes each value to the list.
        chem_vals.push(F_ACIDITY)
        chem_vals.push(V_ACIDITY)
        chem_vals.push(CIT_ACID)
        chem_vals.push(RES_SUGAR)
        chem_vals.push(CHLOR)
        chem_vals.push(F_SULFUR_D)
        chem_vals.push(T_SULFUR_D)
        chem_vals.push(DENSITY)
        chem_vals.push(PH)
        chem_vals.push(SULPH)
        chem_vals.push(ALCH)

        //Returns list of values for use.
        return chem_vals;

    }

    //Function to pass the user input to python.
    function passToPython() {
        var values = getChemValues() //gets the array from the form.

        //AJAX is used to send a web request to python.
        $.ajax({
            url: "http://bryanschloesser.com:5000/get_prediction",
            dataType: 'html',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            data: {listinput: values},
            success: function(data){
                // If/Else Statement to make sure the rating of the wine only displays 1 - 10.
                if (parseInt(data) <= 1){
                    data = 1;
                }else if( parseInt(data) > 10){
                    data = 10
                }
                $("#prediction").html(data);
            }
        });
    }

    //Function to request a graph. Depending on the number entered, it will return a different graph image url.
    function getGraphImages(num) {
        //Ajax web request to ask for the file path and generate the graph.
        $.ajax({
            url: "http://bryanschloesser.com:5000/get_graph" + num,
            dataType: 'html',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            data: {},
            success: function (data) {
                //creates an html image tag with the filepath to the image to display.
                var img = document.createElement("img");
                img.src = data;
                img.width = 650;
                img.height = 450;
                img.id = data.slice(7,13); //removes everything in the response minus the url
                //adds the image element to the html.
                document.getElementById(String(img.id)).appendChild(img)
            },
        });
    }

    //Function to run on form submitting
    $("#chemForm").submit(function (e) {
        //Prevent the default action
        e.preventDefault();
        //Calls the function to pass the user variables to python to get a prediction.
        passToPython();
    });
})
