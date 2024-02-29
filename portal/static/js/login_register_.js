
function init_file() {
document.getElementById("loginPage").action = '/';
document.getElementById("loginPage").submit();
return true;
}

function init_register()
{
    var FirstName = document.getElementById('FirstName');
    var userName = document.getElementById('userName');
    var create_password = document.getElementById('create_password').value;
    var org_type = document.getElementById('org_type').value;
    var department = document.getElementById('department').value;

    var LastName = document.getElementById('LastName');
    var mail_id = document.getElementById('mail_id').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    var org_name = document.getElementById('org_name').value;
    var role = document.getElementById('role').value;


    var First_NameError = document.getElementById('FirstNameError');
    var Last_NameError = document.getElementById('LastNameError');
    var user_NameError = document.getElementById('userNameError');
    var passwordError = document.getElementById('passwordError');
    var cnfmpwdError = document.getElementById('confirmPasswordError');
    var mail_idError = document.getElementById('mailidError');
    var orgTypeError = document.getElementById('orgTypeError');
    var orgNameError = document.getElementById('orgNameError');
    var departmentError = document.getElementById('departmentError');
    var roleError = document.getElementById('roleError');

    // Reset error messages
    First_NameError.textContent = '';
    Last_NameError.textContent = '';
    user_NameError.textContent = '';
    passwordError.textContent = '';
    cnfmpwdError.textContent = '';
    mail_idError.textContent = '';
    orgTypeError.textContent = '';
    orgNameError.textContent = '';
    departmentError.textContent = '';
    roleError.textContent = '';
    document.getElementById('FirstName').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('LastName').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('userName').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('mail_id').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('create_password').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('confirmPassword').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('department').style.borderColor = 'rgb(122 122 122 / 0.53)';
    document.getElementById('role').style.borderColor = 'rgb(122 122 122 / 0.53)';

     if (FirstName.value.trim() == "") {
        document.getElementById('FirstName').style.borderColor = 'red';
        First_NameError.textContent = 'Please Enter First Name';

     }else if (LastName.value == "") {
        document.getElementById('LastName').style.borderColor = 'red';
        Last_NameError.textContent = 'Please Enter Last Name';

     }else if (userName.value.trim() =="") {
        document.getElementById('userName').style.borderColor = 'red';
        user_NameError.textContent = 'Please Enter User Name';


     }else if (!validateEmail(mail_id)) {
        document.getElementById('mail_id').style.borderColor = 'red';
        mail_idError.textContent = 'Please Enter valid Email Id';

     } else if(!validatePassword(create_password)) {
        document.getElementById('create_password').style.borderColor = 'red';
        passwordError.textContent = 'Password should be at least 8 characters, 1 lowercase, 1 uppercase, 1 digit';

     } else if(create_password !=confirmPassword) {
        document.getElementById('confirmPassword').style.borderColor = 'red';
        cnfmpwdError.textContent = 'Password doesnot match';

     } else if(org_type == "") {
        document.getElementById('org_type').style.borderColor = 'red';
        orgTypeError.textContent = 'Please Select Organisation Type';

     } else if(org_name == "") {
        document.getElementById('org_name').style.borderColor = 'red';
        orgNameError.textContent = 'Please Select Organization Name';


     } else if(department == "") {
        document.getElementById('department').style.borderColor = 'red';
        departmentError.textContent = 'Please Select Department';

     } else if(role == "") {
        document.getElementById('role').style.borderColor = 'red';
        roleError.textContent = 'Please Select Role';

     }else{
            const reg_username = userName.value;
            const reg_email = mail_id;


        var check_list={'reg_username':reg_username,"reg_email":reg_email}
        $.ajax({
                url: '/check',
                data: JSON.stringify(check_list),
                type: 'POST',
                contentType: "application/json",
                dataType: 'json',
                success: function (data)
                {
                    console.log(data['msg']);
                     if (data["msg"]=='user_name')
                     {
                         console.log("user_name");
                        document.getElementById('userName').style.borderColor = 'red';
                        user_NameError.textContent = 'User Name already existed';
                        return false
                     }
                      if(data["msg"]=='email_id')
                      {
                          console.log("email_id");
                          document.getElementById('mail_id').style.borderColor = 'red';
                          mailidError.textContent = 'Mail id already existed';
                         return false
                      }
                    var final_bills_request={"FirstName":FirstName.value,"userName":userName.value,"create_password":create_password,
                    "org_type":org_type,"department":department,"LastName":LastName.value,
                    "mail_id":mail_id,"confirmPassword":confirmPassword,"org_name":org_name,
                    "role":role};
                    $.ajax({
                                url: '/registration',
                                data: JSON.stringify(final_bills_request),
                                type: 'POST',
                                contentType: "application/json",
                                dataType: 'json',
                                success: function (data1)
                                {
                                    console.log(data1['status']);
                                    if(data1['status']=="successfully registered")
                                    {
                                       alert(data1['status'], function(){
                                            console.log("Callback executed");
                                             window.location.href = "/"
                                       });

                                    }
                                    else{
                                        alert(data1['status'])
                                        return false;
                                    }

                                },
                                error: function(data1)
                                {
                                    console.log(data1);
                                    return false;
                                }
                        });

                },
                error: function(data)
                {
                    console.log(data);
                    return false;
                }
        });
     }
 }


//const password2 = document.getElementById('password2');

const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}


function validatePasswordInput() {

    var password = document.getElementById('password').value;

    // Add your password validation criteria here
    if (validatePassword(password)) {
        document.getElementById('create_password').style.borderColor = 'green';
    } else {
        document.getElementById('create_password').style.borderColor = 'red';
    }
}

function validatePassword(password) {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return passwordRegex.test(password);
}


function validatePasswordMatch() {
    var password = document.getElementById('create_password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;

    if (password === confirmPassword) {
        document.getElementById('confirmPassword').style.borderColor = 'green';
    } else {
        document.getElementById('confirmPassword').style.borderColor = 'red';
    }
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateEmailInput() {

    var email = document.getElementById('mail_id').value;

    // Add your password validation criteria here
    if (validateEmail(email)) {
        document.getElementById('mail_id').style.borderColor = 'green';
    } else {
        document.getElementById('mail_id').style.borderColor = 'red';
    }
}


var currentCallback;

// override default browser alert
window.alert = function(msg, callback){
  $('.message').text(msg);
  $('.customAlert').css('animation', 'fadeIn 0.3s linear');
  $('.customAlert').css('display', 'inline');
  $('.customAlert').css('z-index', '1001');
  setTimeout(function(){
    $('.customAlert').css('animation', 'none');
  }, 300);
  currentCallback = callback;
}

$(function(){

  // add listener for when our confirmation button is clicked
  $('.confirmButton').click(function(){
    $('.customAlert').css('animation', 'fadeOut 0.3s linear');
    setTimeout(function(){
      $('.customAlert').css('animation', 'none');
      $('.customAlert').css('display', 'none');
    }, 300);
    currentCallback();
  })

});
