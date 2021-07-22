var country = document.getElementById('country');
    country.addEventListener('change', function () {
        console.log(this.value);
        var state = document.getElementById('state');
        var j = state.length;
        for(var i=j-1; i>=0; i--) {
            if(state.options[i].value != 0){
                state.options[i] = null;
            }
        }


        if(this.value == 'Canada'){
            console.log('valeur canada récupérée');
            var alberta = new Option('Alberta', 'Alberta');
            var colombie_britanique = new Option('Colombie-Britanique', 'Colombie-Britanique');
            var ile_du_prince = new Option('Ile-du-Prince-Edouard', 'Ile-du-Prince-Edouard');
            var manitoba = new Option('Manitoba', 'Manitoba');
            var nouveau_brunswick = new Option('Nouveau-Brunswick', 'Nouveau-Brunswick');
            var nouvelle_ecosse = new Option('Nouvelle-Ecosse', 'Nouvelle-Ecosse');
            var Nunavut = new Option('Nunavut', 'Nunavut');
            var ontario = new Option('Ontario', 'Ontario');
            var quebec = new Option('Québec', 'Quebec');
            var saskatchewan = new Option('Saskatchewan', 'Saskatchewan');
            var terre_neuve = new Option('Terre-Neuve-et-Labrador', 'Terre-Neuve-et-Labrador');
            var territoire_NO = new Option('Territoire du Nord-Ouest', 'Territoire-Nord-Ouest');
            var yukon = new Option('Yukon', 'Yukon');
            state.options[state.options.length] = alberta;
            state.options[state.options.length] = colombie_britanique;
            state.options[state.options.length] = ile_du_prince;
            state.options[state.options.length] = manitoba;
            state.options[state.options.length] = nouveau_brunswick;
            state.options[state.options.length] = nouvelle_ecosse;
            state.options[state.options.length] = Nunavut;
            state.options[state.options.length] = ontario;
            state.options[state.options.length] = quebec;
            state.options[state.options.length] = saskatchewan;
            state.options[state.options.length] = terre_neuve;
            state.options[state.options.length] = territoire_NO;
            state.options[state.options.length] = yukon;
        }
        else if(this.value == 'USA'){
            console.log('valeur usa récupérée');
        }
        else if(this.value == 'France'){
            console.log('valeur france récupérée');
        }
    })