
// These values are updated every 5 minutes
// using https://catalogd.archive.org/report/space.php
// More questions? emijrp AT gmail DOT com
    
var timenow = new Date().getTime();
var period = 20; // period update in miliseconds
var spliter = ",";
var spliter_r = new RegExp(/(^|\s)(\d+)(\d{3})/);

function init() {
    adjustSizes();

    var lang = "";
    var header = "";
    if (navigator.systemLanguage) {
        lang = navigator.systemLanguage;
    }else if (navigator.userLanguage) {
        lang = navigator.userLanguage;
    }else if(navigator.language) {
        lang = navigator.language;
    }else {
        lang = "en";
    }

    if (lang.length>2) { lang=lang.substring(0,2); }

    switch(lang){
        case "example":
            header='<a href="http://www.wikimedia.org"></a>:';
            spliter='&nbsp;';
            break;
        case "es":
            header='Bytes preservados en <a href="https://archive.org">Internet Archive</a>:';
            spliter='.';
            break;
        default:
            header='Total bytes preserved in <a href="https://archive.org">Internet Archive</a>:';
            spliter=',';
    }
    
    document.getElementById('header').innerHTML = header;
    
    window.setTimeout(update, period);
}

function update() {
   timenow2 = new Date().getTime();
   if (Math.round(((timenow2-timenow)/1000)+1) % 300 == 0) { window.setTimeout(window.location.reload(), 1100); } //refresh page
   sizenow = sizeinit + (timenow2-timeinit) * fillrate;
   sizenowtext = ""+Math.round(sizenow);
   for(var i=3; i<sizenowtext.length; i+=3) {
      sizenowtext = sizenowtext.replace(spliter_r,'$2'+spliter+'$3');
   }
   document.getElementById('counter').innerHTML = sizenowtext;
   window.setTimeout(update, period);
}

function adjustSizes(){
    var width=800;
    var height=600;
    if (self.innerWidth) { 
        width=self.innerWidth;
        height=self.innerHeight;
    } else if (document.documentElement && document.documentElement.clientWidth) { 
        width=document.documentElement.clientWidth;
        height=document.documentElement.clientHeight;
    } else if (document.body) {
        width=document.body.clientWidth;
        height=document.body.clientHeight;
    }
    document.getElementById('wrapper').style.height=(height-10)+'px';
    document.getElementById('header').style.fontSize=width/45+'pt';
    document.getElementById('footer').style.fontSize=width/45+'pt';
    document.getElementById('counter').style.fontSize=width/19+'pt';
}

window.onload = init;
window.onresize = adjustSizes;
