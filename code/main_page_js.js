$(document).ready(function(e) {
    function getChemValues() {
        var chem_vals = []

        //Assigns user inputted values to the respective chemical.
        const F_ACIDITY = $('#fAcidity').val();
        const V_ACIDITY = $('#vAcidity').val();
        const CIT_ACID = $('#citAcid').val();
        const RES_SUGAR = $('#resSugar').val();
        const CHLOR = $('#chlor').val();
        const F_SULFUR_D = $('#fSulfurD').val();
        const T_SULFUR_D = $('#tSulfurD').val();
        const DENSITY = $('#density').val();
        const PH = $('#pH').val();
        const SULPH = $('#sulph').val();
        const ALCH = $('#alch').val();

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

        //Print values to console for verification
        console.log("Value of fixed acidity is : " + F_ACIDITY);
        console.log("Value of volatile acidity is : " + V_ACIDITY);
        console.log("Value of citric acid is : " + CIT_ACID);
        console.log("Value of residual sugar is: " + RES_SUGAR)
        console.log("Value of chlorides is : " + CHLOR);
        console.log("Value of free sulfur dioxide is : " + F_SULFUR_D);
        console.log("Value of total sulfur dioxide is : " + T_SULFUR_D);
        console.log("Value of density is : " + DENSITY);
        console.log("Value of PH is : " + PH);
        console.log("Value of sulphates is : " + SULPH);
        console.log("Value of alcohol is : " + ALCH);

        return chem_vals;

    }

    function passToPython(){
        var data = getChemValues();
        $.ajax(
            {
                type:'POST',
                contentType: 'application/json;charset-utf-08',
                dataType:'json',
                url:'http://127.0.0.1:5000/pass_val?value=' + data,
                success:function (data){
                    var reply = data.reply;
                    if (reply === 'success'){
                        return;
                    }else{
                        alert("Some error.")
                    }
                }

            }
        )
    }

    //Function to run on form submitting
    $("#chemValues").submit(function(e) {
        //Prevent the default action
        e.preventDefault();

        passToPython();
    })



})
