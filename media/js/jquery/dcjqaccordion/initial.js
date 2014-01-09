try{
    $(document).ready(function($){
        $('#accordion_menu').dcAccordion({
            eventType:'hover',
            autoClose:false,
            saveState:true,
            disableLink:false,
            speed:'slow',
            showCount:false,
            //showCount:true,
            autoExpand:true,
            menuClose:true,
            cookie:'dcjq-accordion',
            classExpand:'dcjq-current-parent'
    });
});
}catch(e){ alert(e) }
