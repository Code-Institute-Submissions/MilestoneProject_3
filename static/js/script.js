$(document).ready(function(){
    /* Nav bar collpase activation */
    $('.sidenav').sidenav();
    /* Modal activation */
    $('.modal').modal();   
    
    /* Code to ensure modal does not close if fields are invalid */
    $(".submit").click(function(){
        let username_attr = $("#username").attr("class");
        let password_attr = $("#username").attr("class");
        console.log(attribute)
        if(username_attr=="validate valid" || password_attr=="validate valid"){
            $(".submit").addClass("modal-close")
        }        
    })

})


    