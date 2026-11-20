// ==========================================================================
// FICHEIRO DE CONFIGURAÇÃO DO PM2
// ==========================================================================
// O PM2 é um "gestor de processos": arranca os nossos 3 serviços de uma vez,
// mantém-nos a correr em segundo plano e volta a ligá-los se algum falhar.
//
// Não é preciso saber JavaScript: isto é só uma LISTA de serviços, e cada
// serviço tem:
//   name        -> nome que aparece no `pm2 status`
//   script      -> o ficheiro Python a correr
//   cwd         -> a pasta onde está esse ficheiro
//   interpreter -> o Python a usar (o do nosso ambiente virtual .venv)
//
// Para arrancar tudo:   pm2 start ecosystem.config.js
// ==========================================================================

const path = require("path");
const PYTHON = path.join(__dirname, ".venv", "bin", "python");

module.exports = {
  apps: [
    {
      name: "bigramas",
      script: "app.py",
      cwd: path.join(__dirname, "servico_bigramas"),
      interpreter: PYTHON,
    },
    {
      name: "llm",
      script: "app.py",
      cwd: path.join(__dirname, "servico_llm"),
      interpreter: PYTHON,
    },

    // ----------------------------------------------------------------------
    // TODO 7: falta o terceiro serviço, o GATEWAY!
    //   Copia um dos blocos de cima { ... }, cola-o aqui e muda:
    //     - o name para "gateway"
    //     - a pasta do cwd para "gateway"
    //   (não te esqueças da vírgula entre blocos)
    // ----------------------------------------------------------------------
  ],
};
