/**
 * Created by user on 14.08.16.
 */

tinymce.init({
    selector:'textarea#id_description',
    mode:"textareas",
    //plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    extended_valid_elements :  'script[type|src],iframe[src|style|width|height|scrolling|marginwidth|marginheight|frameborder],div[*],p[*],object[width|height|classid|codebase|embed|param],param[name|value],embed[param|src|type|width|height|flashvars|wmode]',
    // Theme options
    theme_advanced_buttons1 :  "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,bullist,numlist,sub,sup,|,forecolor,backcolor,formatselect,fontsizeselect",
    theme_advanced_buttons2 :  "preview,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,tablecontrols,removeformat,code,emotions",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    theme_advanced_statusbar_location : "bottom",
    theme_advanced_resizing : true
});

tinymce.init({
    selector:'textarea#id_bottom_   description'
});
