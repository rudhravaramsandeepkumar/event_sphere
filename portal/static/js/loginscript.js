const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});


function changeStylesright() {
  // Get elements with the class "myDiv"
  var divs = document.getElementsByClassName("toggle-container");
  var form_text = document.getElementsByClassName("form_text");

  // Loop through the elements and change styles
  for (var i = 0; i < divs.length; i++) {
    divs[i].style.left = "60%";
  }
  for (var i = 0; i < form_text.length; i++) {
    form_text[i].style.marginLeft = "8%";
    form_text[i].style.padding = "120px 20px 5px";
  }
}
function changeStylesleft() {
  // Get elements with the class "myDiv"
  var divs = document.getElementsByClassName("toggle-container");
  var form_text = document.getElementsByClassName("form_text");

  // Loop through the elements and change styles
  for (var i = 0; i < divs.length; i++) {
    divs[i].style.left = "40%";
  }
  for (var i = 0; i < form_text.length; i++) {
    form_text[i].style.marginLeft = "30%";
    form_text[i].style.padding = "20px 20px 5px";
  }
}