$(function () {
  // Signup
  $(".signupBtn").click(function (e) {
    e.preventDefault();
    let email = $("#email").val();
    let password = $("#password").val();
    let cpassword = $("#cpassword").val();
    let name = $("#name").val();
    let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
    console.log(email, password, cpassword, csrfmiddlewaretoken, name);
    $.ajax({
      url: "/signup/",
      method: "POST",
      data: {
        name: name,
        email: email,
        password: password,
        cpassword: cpassword,
        csrfmiddlewaretoken: csrfmiddlewaretoken,
      },
      success: function (response) {
        if (response.status == "success") {
          $("#msg").removeClass("alert alert-danger");
          $("#msg").html(
            `${response.message}. You will be redirected to login page soon. If you are not redirected <a href="/"><b><u>Click here</u></b></a>`,
          );
          $("#msg").addClass("alert alert-success");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-success");
            window.location.href = "/";
          }, 3000);
        } else if (
          response.message == "User already exists, Please Login now"
        ) {
          $("#msg").removeClass("alert alert-success");
          $("#msg").html(
            `${response.message}. You will be redirected to login page soon. If you are not redirected <a href="/"><b><u>Click here</u></b></a>`,
          );
          $("#msg").addClass("alert alert-danger");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-danger");
            window.location.href = "/";
          }, 3000);
        } else {
          $("#msg").removeClass("alert alert-success");
          $("#msg").html(`${response.message}.`);
          $("#msg").addClass("alert alert-danger");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-danger");
          }, 3000);
        }
      },
      error: function (xhr, status, error) {
        $("#msg").removeClass("alert alert-success");
        $("#msg").html(`${xhr.responseText}.`);
        $("#msg").addClass("alert alert-danger");
        setTimeout(function () {
          $("#msg").html(``);
          $("#msg").removeClass("alert alert-danger");
        }, 3000);
      },
    });
  });
  //   Login
  $(".loginBtn").click(function (e) {
    e.preventDefault();
    let email = $("#email").val();
    let password = $("#password").val();
    let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: "/",
      method: "POST",
      data: {
        email: email,
        password: password,
        csrfmiddlewaretoken: csrfmiddlewaretoken,
      },
      success: function (response) {
        if (response.status == "success") {
          $("#msg").removeClass("alert alert-danger");
          $("#msg").html(
            `${response.message}. You will be redirected to home page soon. If you are not redirected <a href="/home/"><b><u>Click here</u></b></a>`,
          );
          $("#msg").addClass("alert alert-success");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-success");
            window.location.href = "/home/";
          }, 3000);
        } else if (response.message == "User do not exist, Please Signup now") {
          $("#msg").removeClass("alert alert-success");
          $("#msg").html(
            `${response.message}. You will be redirected to signup page soon. If you are not redirected <a href="/signup/"><b><u>Click here</u></b></a>`,
          );
          $("#msg").addClass("alert alert-danger");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-danger");
            window.location.href = "/signup/";
          }, 3000);
        } else {
          $("#msg").removeClass("alert alert-success");
          $("#msg").html(`${response.message}.`);
          $("#msg").addClass("alert alert-danger");
          setTimeout(function () {
            $("#msg").html(``);
            $("#msg").removeClass("alert alert-danger");
          }, 3000);
        }
      },
      error: function (xhr, status, error) {
        $("#msg").removeClass("alert alert-success");
        $("#msg").html(`${xhr.responseText}.`);
        $("#msg").addClass("alert alert-danger");
        setTimeout(function () {
          $("#msg").html(``);
          $("#msg").removeClass("alert alert-danger");
        }, 3000);
      },
    });
  });
  // Input elements styling for password reset
  $("input[type='email']").addClass("form-control")
  $("input[type='password']").addClass("form-control");

  // Youtube Link
  $(".ytBtn").click(function(e){
    e.preventDefault()
    let job = $("#job_role").val();
    let exp=$("#exp").val()
    let csrfmiddlewaretoken=$("input[name='csrfmiddlewaretoken']").val()
     $("#body").html(
       '<div class="shadow mt-3 p-3 now d-flex justify-center items-center"><div class="spinner-border text-primary"></div><pre> Processing...</pre></div>',
     );  
    $.ajax({
      url:"/home/",
      method:"POST",
      data:{
        job:job,
        csrfmiddlewaretoken:csrfmiddlewaretoken,
        exp:exp
      },
      success:function(response){
        if(response.status=="success"){
           $("#body").html(
             `<div class="shadow mt-3 p-3 now d-flex justify-center items-center"><p>${response.message}</p></div>`,
           );
        } else{
           $("#body").html(
             `<div class="alert alert-danger">${response.message}</div>`,
           );
        }
        
      },
      error:function(xhr,status,error){
         $("#body").html(
           `<div class="shadow mt-3 p-3 now d-flex justify-center items-center"><div class="alert alert-danger">${xhr.responseText}</div></div>`,
         );
      }
    })
  });
});
