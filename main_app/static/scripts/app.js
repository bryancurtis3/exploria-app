console.log("$J Activated!");


/* === LOGIC === */
signUpModal = function signUpModal(){
  $("#signUpModal").css("visibility","visible");
};


/* === EVENT LISTENERS === */

// Sign Up link opens Sign Up modal
$("#signUp").click(function(){
  signUpModal();
});
