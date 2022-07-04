const btn = document.getElementById("btn");
const btnText = document.getElementById("btnText");

btn.onclick = function () {
  btnText.innerHTML = "Woohooo!!";
  btn.classList.add("active");
};

function delay(URL) {
  setTimeout(function () {
    window.location = URL;
  }, 2000);
}
