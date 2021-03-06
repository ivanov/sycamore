// This is based on the Wikipedia JavaScript support functions
// if this is true, the toolbar will no longer overwrite the infobox when you move the mouse over individual items
var noOverwrite=false;
var alertText;
var clientPC = navigator.userAgent.toLowerCase(); // Get client info
var is_gecko = ((clientPC.indexOf('gecko')!=-1) && (clientPC.indexOf('spoofer')==-1)
                && (clientPC.indexOf('khtml') == -1) && (clientPC.indexOf('netscape/7.0')==-1));
var is_safari = ((clientPC.indexOf('applewebkit')!=-1) && (clientPC.indexOf('spoofer')==-1));
var is_modern_safari = false;
var can_alter_textarea = true;

if (is_safari) {
// Figure out if it's a new version of Safari or not
  index = clientPC.lastIndexOf('safari');
  version_number = clientPC.substring(index+7);
  //index = version_number.firstIndexOf('.')
  if (index) {
    index = version_number.indexOf('.')
    version_number = version_number.substring(0, index);
  }
  if (version_number >= 314) {
    is_modern_safari=true;
  }
}

var is_khtml = (navigator.vendor == 'KDE' || ( document.childNodes && !document.all && !navigator.taintEnabled ));
if (clientPC.indexOf('opera')!=-1) {
    var is_opera = true;
    var is_opera_preseven = (window.opera && !document.childNodes);
    var is_opera_seven = (window.opera && document.childNodes);
}

// Un-trap us from framesets
if( window.top != window ) window.top.location = window.location;

toolbar_td = document.createElement('td');
toolbar_innerHTML = '';
toolbar_innerHTML += '<span class="toolbarPaddingStart"></span>';
toolbar_innerHTML += addButton('bold.png','Bold text','\'\'\'','\'\'\'','Bold text'); 
toolbar_innerHTML += addButton('italic.png','Italic text','\'\'','\'\'','Italic text');
toolbar_innerHTML += addButton('extlink.png','External link','[',']','http://www.example.com');
toolbar_innerHTML += addButton('head.png','Headline','\n= ',' =\n','Headline text');
toolbar_innerHTML += addButton('hline.png','Horizontal line (use sparingly)','\n-----\n','','');
toolbar_innerHTML += addButton('center.png','Center','-->','<--','');
toolbar_innerHTML += addButton('sig.png','Signature','',' --' + userPageLink,'');
toolbar_innerHTML += addButton('image.png','Attached image','\n[[Image(',')]]','photo.jpg');
toolbar_innerHTML += addButton('plain.png','Ignore wiki formatting','{{{','}}}','Insert non-formatted text here');

infoBox = addInfobox('Click a button to get an example text','Please enter the text you want to be formated.\\nIt will be shown in the info box for copy and pasting.\\nExample:\\n$1\\nwill become:\\n$2');

toolbar_innerHTML += '<span class="toolbarPaddingEnd"></span>';
if (!infoBox) {
  toolbar_td.setAttribute('id', 'toolbar');
  toolbar_td.innerHTML = toolbar_innerHTML;
}
else {
  toolbar_td.setAttribute('id', 'toolbarWithInfo');
  toolbar_td.innerHTML = toolbar_innerHTML + infoBox;
}

//toolbar_padding = document.createElement('td');
//toolbar_padding.className = 'toolbarSize';
//toolbar_padding.innerHTML = '&nbsp;';
//document.getElementById('iconRow').appendChild(toolbar_padding);
//document.getElementById('iconRow').innerHTML += '<td class="toolbarSize"></td>';
title_element = document.getElementById('title');
title_body = title_element.getElementsByTagName("tbody").item(0);
title_row = title_body.getElementsByTagName("tr").item(0);
//document.getElementById('search_form').innerHTML = '&nbsp;';
title_row.removeChild(document.getElementById('search_form'));
title_row.appendChild(toolbar_td);

//title_element.innerHTML += toolbar_innerHTML;
//title_element.appendChild(document.createTextNode(toolbar_innerHTML));
//title_element.appendChild(document.createTextNode(toolbar_innerHTML));
//title_height = document.getElementById('title').offsetHeight + 10;
//title_text_parent = ((document.getElementById('title_text')).offsetParent);
//title_height = title_text_parent.offsetHeight;

//toolbar_div = document.getElementById(toolbar_id);
//try {
//  toolbar_div.style.cssText('top: '+title_height+'px;');
//}
//catch (e) {
//  toolbar_div.setAttribute('style', 'top: '+title_height+'px;');
//}

function addInfobox(infoText,text_alert) {
	alertText=text_alert;
	var clientPC = navigator.userAgent.toLowerCase(); // Get client info

	var re=new RegExp("\\\\n","g");
	alertText=alertText.replace(re,"\n");
        var returnString = "";

	// if no support for changing selection, add a small copy & paste field
	// document.selection is an IE-only property. The full toolbar works in IE and
	// Gecko-based browsers.
	if(!document.selection && !is_gecko && !is_modern_safari) {
 		infoText=escapeQuotesHTML(infoText);
                returnString += '<div style="clear:right;"></div>';
	 	returnString += "<form style=\"position: absolute; display:inline;\" name='infoform' id='infoform'>"+
			"<input id='infobox' style=\"margin-top: 1px;\" class=\"toolbarSize\" name='infobox' value=\""+
			infoText+"\" READONLY></form>";
                can_alter_textarea = false;
 	}
        return returnString;
}


// this function generates the actual toolbar buttons with localized text
// we use it to avoid creating the toolbar where javascript is not enabled
function addButton(imageFile, speedTip, tagOpen, tagClose, sampleText) {

	speedTip=escapeQuotes(speedTip);
	tagOpen=escapeQuotes(tagOpen);
	tagClose=escapeQuotes(tagClose);
	sampleText=escapeQuotes(sampleText);
	var mouseOver="";
        var buttonString="";

	// we can't change the selection, so we show example texts
	// when moving the mouse instead, until the first button is clicked
	if(!document.selection && !is_gecko && !is_modern_safari) {
		// filter backslashes so it can be shown in the infobox
		var re=new RegExp("\\\\n","g");
		tagOpen=tagOpen.replace(re,"");
		tagClose=tagClose.replace(re,"");
		mouseOver = "onMouseover=\"if(!noOverwrite){document.infoform.infobox.value='"+tagOpen+sampleText+tagClose+"'};\"";
	}

	buttonString += "<a href=\"javascript:insertTags";
	buttonString += "('"+tagOpen+"','"+tagClose+"','"+sampleText+"');\">";

        buttonString += "<img src=\""+buttonRoot+"/"+imageFile+"\" ALT=\""+speedTip+"\" TITLE=\""+speedTip+"\""+mouseOver+" class=\"editBarIcon\" style=\"behavior: url('" + urlPrefix + "/pngbehavior.htc');\">";
	buttonString += "</a>";
	return buttonString;
}

function escapeQuotes(text) {
	var re=new RegExp("'","g");
	text=text.replace(re,"\\'");
	re=new RegExp('"',"g");
	text=text.replace(re,'&quot;');
	re=new RegExp("\\n","g");
	text=text.replace(re,"\\n");
	return text;
}

function escapeQuotesHTML(text) {
	var re=new RegExp('"',"g");
	text=text.replace(re,"&quot;");
	return text;
}

// apply tagOpen/tagClose to selection in textarea,
// use sampleText instead of selection if there is none
// copied and adapted from phpBB
function insertTags(tagOpen, tagClose, sampleText) {

	var txtarea = document.editform.savetext;
	// IE
	if(document.selection  && !is_gecko && !is_modern_safari) {
		var theSelection = document.selection.createRange().text;
		if(!theSelection) { theSelection=sampleText;}
		txtarea.focus();
		if(theSelection.charAt(theSelection.length - 1) == " "){// exclude ending space char, if any
			theSelection = theSelection.substring(0, theSelection.length - 1);
			document.selection.createRange().text = tagOpen + theSelection + tagClose + " ";
		} else {
			document.selection.createRange().text = tagOpen + theSelection + tagClose;
		}

	// Mozilla
	} else if(txtarea.selectionStart || txtarea.selectionStart == '0') {
 		var startPos = txtarea.selectionStart;
		var endPos = txtarea.selectionEnd;
		var scrollTop=txtarea.scrollTop;
		var myText = (txtarea.value).substring(startPos, endPos);
		if(!myText) { myText=sampleText;}
		if(myText.charAt(myText.length - 1) == " "){ // exclude ending space char, if any
			subst = tagOpen + myText.substring(0, (myText.length - 1)) + tagClose + " ";
		} else {
			subst = tagOpen + myText + tagClose;
		}
		txtarea.value = txtarea.value.substring(0, startPos) + subst +
		  txtarea.value.substring(endPos, txtarea.value.length);
		txtarea.focus();

		var cPos=startPos+(tagOpen.length+myText.length+tagClose.length);
		txtarea.selectionStart=cPos;
		txtarea.selectionEnd=cPos;
		txtarea.scrollTop=scrollTop;

	// All others
	} else {
		var copy_alertText=alertText;
		var re1=new RegExp("\\$1","g");
		var re2=new RegExp("\\$2","g");
		copy_alertText=copy_alertText.replace(re1,sampleText);
		copy_alertText=copy_alertText.replace(re2,tagOpen+sampleText+tagClose);
		var text;
		if (sampleText) {
			text=prompt(copy_alertText);
		} else {
			text="";
		}
		if(!text) { text=sampleText;}
		text=tagOpen+text+tagClose;
		document.infoform.infobox.value=text;
		// in Safari this causes scrolling
		if(!is_safari) {
			txtarea.focus();
		}
		noOverwrite=true;
	}
	// reposition cursor if possible
	if (txtarea.createTextRange) txtarea.caretPos = document.selection.createRange().duplicate();
}


// Resize the edit box by increments of 5 rows
// and updates the user preference using XMLHttpRequest
// args: mode - string, values 'bigger' or 'smaller'
//       url - string, old-style resize link

// designed to be called by an onclick form element so
// returns "false" if the editor was resized successfully,
// otherwise returns true
function sizeEditor( mode , url) {
    var height_change;
    var min_height = 10;
    var max_height = 100;

    // calculate the change in size 
    if ( mode == 'bigger' ) {
        height_change = 5;
    } else if ( mode == 'smaller' )  {
        height_change = -5;
    }
    
    // get the element from the form
    var editor = document.getElementById( 'savetext' );
    var editor_height = editor.rows;

    // make sure we have valid objects before continuing
    if ( editor && editor_height ) {

        // calc new height and make sure it is a number
        var new_height = parseInt(editor_height) + height_change;
        if (isNaN(new_height)) {
            return true;
        }

        // set the editor rows to the new height if it's in range
        if ( new_height < min_height ) {
            editor.rows = min_height;
        } else if (new_height > max_height) {
            editor.rows = max_height;
        } else {
            editor.rows = new_height;
        }

       // save the choice in the user's preferences
        var client = new XMLHttpRequest();
        client.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200)
                returnStatus(this.status);
        }
        client.open("GET", url+'&rows='+editor.rows);
        client.send("");
        return false;

    } else {

        return true;

    }
}
