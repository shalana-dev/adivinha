const form = document.querySelector("#form");
const campoPalpite = document.querySelector("#palpite");
const dica = document.querySelector("#dica");
const tentativasNaTela = document.querySelector("#tentativas");
const botaoReiniciar = document.querySelector("#reiniciar");

let numeroSecreto = Math.floor(Math.random() * 100) + 1;
let tentativas = 0;

console.log("Psiu... o numero e " + numeroSecreto); // so para testar!

form.addEventListener("submit", function (evento) {
  evento.preventDefault();

  const palpite = Number(campoPalpite.value);
  tentativas = tentativas + 1;
  tentativasNaTela.textContent = "Tentativas: " + tentativas;

  dica.classList.remove("acertou", "maior", "menor");

  if (palpite === numeroSecreto) {
    dica.textContent = "ACERTOU em " + tentativas + " tentativas!";
    dica.classList.add("acertou");
    campoPalpite.disabled = true;
    botaoReiniciar.classList.remove("escondido");
  } else if (palpite < numeroSecreto) {
    dica.textContent = "O numero secreto e MAIOR que " + palpite;
    dica.classList.add("maior");
  } else {
    dica.textContent = "O numero secreto e MENOR que " + palpite;
    dica.classList.add("menor");
  }

  campoPalpite.value = "";
  campoPalpite.focus(); // cursor volta pro campo, pronto pro proximo palpite
});
