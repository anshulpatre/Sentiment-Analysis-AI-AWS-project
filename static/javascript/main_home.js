const btn = document.getElementById("btn");
const btnText = document.getElementById("btnText");

btn.onclick = function () {
  btnText.innerHTML = "Woohooo!!";
  btn.classList.add("active");
};
