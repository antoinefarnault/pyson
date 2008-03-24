//Derniere url appellee avec la fonction get
var hist = '';

//textearea selectionner pour la fonction d'insertion de fichier 
var selected_textarea = null;


//script requis par dojo
dojo.require("dojo.widget.TabContainer");
dojo.require("dojo.widget.ContentPane");



function get(url, id, msg){
    ajax_loader(id, true);
    var req = null;
    hist = url;
    var ref  = hist.replace(/\/table.*?$/, '')

    if (!msg){
        msg ='';
    }

    if(window.XMLHttpRequest){
        req = new XMLHttpRequest();
    }
    else {
        alert("Your navigator is desuet !!! Download firefox....");
        return;
    }
    // Send request to get the structure
    req.open('GET', url);
    req.send(null);
    req.onreadystatechange = function() {
        if(req.readyState == '4'){
            if(req.status == '200'){
                var data = req.responseText;
                document.getElementById(id).innerHTML = msg +data;
                ajax_loader(id, false);
            }
        }
    }

}
function post(url, id, fobj){
    var req = null;
    var param = getFormValues(fobj, false);
    var ref  = hist.replace(/\/table.*?$/, '')

    if(window.XMLHttpRequest){
        req = new XMLHttpRequest();
    }
    else {
        alert("Your navigator is too old !!!");
        return;
    }
    // Send request to get the structure
    req.open('POST', url);
    if(fobj.getAttribute("enctype") == "multipart/form-data"){
        req.setRequestHeader("Content-Type", "multipart/form-data");
    } else {
        req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    }

    req.send(param);

    req.onreadystatechange = function() {
        if(req.readyState == '4'){
            if(req.status == '200'){
                var data = req.responseText;
                get(ref, id ,'<p class="important">'+ data+'</p>' );
            }
        }
    }
}
function getFormValues(fobj,valFunc){
    var str = "";
    var valueArr = null;
    var val = "";
    var cmd = "";
    for(var i = 0;i < fobj.elements.length;i++){
        switch(fobj.elements[i].type){
            case "text":
                    if(valFunc) {
                cmd = valFunc + "(" + 'fobj.elements[i].value' + ")";
                val = eval(cmd)
                    }
                    str += fobj.elements[i].name +
                            "=" + escape(fobj.elements[i].value) + "&";
                    break;
            case "select-one":
                    str += fobj.elements[i].name +
                    "=" + fobj.elements[i].options[fobj.elements[i].selectedIndex].value + "&";
            break;
            case "checkbox":
                    if  (fobj.elements[i].checked){
                str += fobj.elements[i].name + 
                        "=" + fobj.elements[i].value + "&";         
                    }
                    break;
            case "radio":
                    if  (fobj.elements[i].checked){
                str += fobj.elements[i].name + 
                        "=" + fobj.elements[i].value + "&";         
                    }
        }
        if (fobj.elements[i].tagName == 'TEXTAREA'){
            str += fobj.elements[i].name +    
                    "=" + escape(fobj.elements[i].value) + "&";  
        }
    
    }
    str = str.substr(0,(str.length - 1));
    return str;
}    

    // conteneur = id du bloc (<div>, <p> ...) contenant les checkbox
    // a_faire = '0' pour tout décocher
    // a_faire = '1' pour tout cocher

function GereChkbox(conteneur, a_faire) {
    var blnEtat=null;
    var chkBox = document.getElementsByTagName("input");
    for (var i=0; i< chkBox.length; i++){
        if(chkBox[i].getAttribute('type') == 'checkbox'){
            blnEtat = (a_faire=='0') ? false : (a_faire=='1') ? true : false;
            document.getElementById(chkBox[i].getAttribute("id")).checked=blnEtat;
            var row =   document.getElementById(chkBox[i].getAttribute("id")).parentNode.parentNode;
            if (blnEtat)
            row.style.background='#FFFFCC';
            else
                row.style.background='none';
        }
    }
}

function surligne(tr){

    if (checkbox.checked)
    checkbox.parentNode.parentNode.style.background='#FFFFCC';
    else
        checkbox.parentNode.parentNode.style.background='none';
}

function ajax_loader(id, bool){
    if (bool)
        document.getElementById(id).innerHTML = '<img src="/static/htdocs/img/ajax-loader.gif" alt="" />';
    else
        document.getElementById(id).innerHTML = document.getElementById(id).innerHTML.replace('<img src="/static/htdocs/img/ajax-loader.gif" alt="" />', '');

}

        
function insert_textarea(value){
    selected_textarea.value+=value;
}
        
        
        
        
        
        
        
        
        
        
        
        