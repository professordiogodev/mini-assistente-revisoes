# 🤖 Mini-Assistente: revisões de LLMs e micro-serviços

**Duração:** 90 minutos · **Linguagem:** Python · **Entrega:** Teams (screenshots + link do teu fork)

Hoje vais juntar tudo o que já fizemos (bigramas, LLMs locais com Ollama, Modelfiles,
micro-serviços e PM2) numa **pequena aplicação a sério**, com 3 serviços que falam entre si.

O código já está **quase todo feito**. Só tens de completar **7 TODOs pequenos**, e este guia
explica cada passo. Lê com calma: o mais importante é **perceberes o que estás a fazer**.

---

## 🗺️ O que vais construir

```
                    ┌──────────────────────┐
   Browser  ──────► │  GATEWAY  (porta 8000)│  ◄── a "porta de entrada"
                    └──────────┬───────────┘
                     ┌─────────┴──────────┐
                     ▼                    ▼
        ┌────────────────────┐   ┌────────────────────┐
        │ BIGRAMAS (5001)    │   │ LLM (5002)         │
        │ prevê a palavra    │   │ fala com o Ollama  │──► Ollama (11434)
        │ seguinte           │   │                    │    modelo "assistente"
        └────────────────────┘   └────────────────────┘
```

Escreves uma frase na página, e:
- o serviço de **bigramas** diz qual é a palavra mais provável a seguir à tua última palavra;
- o serviço **LLM** pede ao teu modelo local (com personalidade criada por ti) uma resposta.

São **duas formas de "prever texto"** lado a lado: uma muito simples (contar pares de palavras)
e outra muito poderosa (um LLM). É a melhor maneira de perceber a diferença!

### 📁 Ficheiros do projeto

| Ficheiro | O que é | Tens de mexer? |
|---|---|---|
| `corpus.txt` | Texto de "treino" dos bigramas | Não |
| `servico_bigramas/app.py` | Serviço 1: bigramas | **TODO 1, 2** |
| `servico_llm/Modelfile` | A "receita" do teu modelo | **TODO 3, 4** |
| `servico_llm/app.py` | Serviço 2: fala com o Ollama | **TODO 5** |
| `gateway/app.py` | Serviço 3: junta tudo | **TODO 6** |
| `gateway/index.html` | A página web | Não |
| `ecosystem.config.js` | Configuração do PM2 | **TODO 7** |
| `verificar.py` | Testa se está tudo bem | Não (só correr) |
| `RESPOSTAS.md` | 5 perguntas curtas | **Sim** |

### ⏱️ Plano da aula

| Parte | Tempo |
|---|---|
| 0. Preparar o ambiente | 10 min |
| 1. Serviço de bigramas | 15 min |
| 2. Modelfile + serviço LLM | 25 min |
| 3. Gateway | 15 min |
| 4. Tudo junto com o PM2 | 10 min |
| 5. Perguntas + entrega | 15 min |

### 📸 Screenshots a entregar (vai tirando ao longo da aula!)

Ao longo do guia vais ver caixas **📸 SCREENSHOT X**. No fim vais ter 6:

1. Browser com o resultado do `/prever` (Parte 1)
2. Terminal a conversar com o teu modelo `assistente` (Parte 2)
3. `python verificar.py` com tudo ✅ (Parte 3)
4. `pm2 status` com os 3 serviços `online` (Parte 4)
5. A página do Mini-Assistente a responder (Parte 4)
6. A página com o serviço de bigramas desligado (Parte 4)

---

## Parte 0 — Preparar o ambiente (10 min)

> Trabalha sempre no **terminal do WSL** (Ubuntu), como nas outras aulas.

### 0.1 Fazer fork e clonar

Um **fork** é uma cópia deste repositório na **tua** conta do GitHub. Assim podes guardar
as tuas alterações lá e entregar o link.

1. No topo desta página do GitHub, carrega em **Fork** → **Create fork**.
2. Na página do **teu** fork, carrega no botão verde **Code** e copia o endereço HTTPS.
3. No terminal:

```bash
cd ~
git clone https://github.com/O-TEU-UTILIZADOR/mini-assistente-revisoes.git
cd mini-assistente-revisoes
code .
```

> 💡 `code .` abre a pasta no VS Code. Confirma que no canto inferior esquerdo aparece **WSL**.

### 0.2 Ambiente virtual e bibliotecas

Um **ambiente virtual** (`.venv`) é uma pasta com um Python só para este projeto, para não
misturar bibliotecas de projetos diferentes.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

✔️ Depois do `activate`, deves ver `(.venv)` no início da linha do terminal.

As bibliotecas que instalaste são:
- **flask**: para criar serviços web (como na tarefa do Flaskerino);
- **requests**: para um programa Python fazer pedidos HTTP a outro serviço.

> ⚠️ **Sempre que abrires um terminal novo**, tens de ir à pasta do projeto e voltar a fazer
> `source .venv/bin/activate`.

### 0.3 Confirmar que o Ollama está pronto

```bash
ollama list
```

Deves ver pelo menos um modelo (o que usaste na Tarefa 4). **Aponta o nome**, vais precisar dele.

---

## Parte 1 — Serviço de bigramas (15 min)

📄 Abre `servico_bigramas/app.py`.

### 🧠 Lembrete: o que é um bigrama?

Um **bigrama** é um par de palavras seguidas. Na frase *"o modelo lê o texto"*, os bigramas são:
`(o, modelo)`, `(modelo, lê)`, `(lê, o)`, `(o, texto)`.

Se contarmos todos os bigramas de um texto grande, conseguimos **prever** a palavra seguinte:
basta escolher a que apareceu mais vezes depois da palavra atual. Por exemplo, depois de `o`
apareceu `modelo` 1 vez e `texto` 1 vez.

É um "modelo de linguagem" muito, muito simples, mas a ideia de fundo é a mesma de um LLM:
**prever a próxima palavra**.

### ✏️ TODO 1: contar os bigramas

Procura `TODO 1` na função `treinar_bigramas`. O ciclo `for` já percorre todos os pares
`(atual, seguinte)`. Só tens de **somar 1** à contagem certa.

<details>
<summary>🆘 Estou mesmo encravado/a (clica só se precisares)</summary>

```python
contagens[atual][seguinte] += 1
```
</details>

### ✏️ TODO 2: prever a palavra seguinte

Procura `TODO 2` na função `prever`. `opcoes` é um `Counter` com as palavras que aparecem
depois da palavra pedida. Tens de devolver **a mais frequente**.

Experimenta no terminal do Python para perceberes o `.most_common()`:

```python
>>> from collections import Counter
>>> c = Counter({"modelo": 5, "texto": 2})
>>> c.most_common(1)
[('modelo', 5)]
>>> c.most_common(1)[0]
('modelo', 5)
>>> c.most_common(1)[0][0]
'modelo'
```

<details>
<summary>🆘 Estou mesmo encravado/a</summary>

```python
return opcoes.most_common(1)[0][0]
```
</details>

### ▶️ Arrancar e testar

No terminal (com o `.venv` ativo):

```bash
python servico_bigramas/app.py
```

Este terminal fica **ocupado** com o serviço. É normal! Deixa-o aberto.

Abre no browser: <http://localhost:5001/prever?palavra=modelo>

Deves ver algo como:

```json
{ "palavra": "modelo", "seguinte": "de", "opcoes": { "de": 3, "lê": 1, ... } }
```

Experimenta outras palavras: `o`, `neurónio`, `temperatura`... e uma que não esteja no
`corpus.txt` (o que acontece?).

> 🔁 Se mudares o código, tens de **parar o serviço (Ctrl+C) e voltar a arrancá-lo**.

> 📸 **SCREENSHOT 1:** o browser com o resultado de `/prever?palavra=...` (escolhe a palavra que quiseres).

---

## Parte 2 — O teu modelo + serviço LLM (25 min)

### 2.1 O Modelfile

📄 Abre `servico_llm/Modelfile`.

### 🧠 Lembrete: o que é um Modelfile?

É uma "receita" que diz ao Ollama como criar um modelo **novo** a partir de um que já existe.
**Não treina nada**: só define

- `FROM`: o modelo base;
- `PARAMETER`: definições como a `temperature` (criatividade);
- `SYSTEM`: instruções que o modelo recebe **antes de cada pergunta** (a "personalidade").

### ✏️ TODO 3: escolher o modelo base

Na linha `FROM`, põe o nome do modelo que viste no `ollama list` (Parte 0.3).

### ✏️ TODO 4: dar-lhe uma personalidade

Escreve o texto do `SYSTEM`. Sê criativo/a! Mas inclui as duas regras:
**responder em português de Portugal** e **no máximo 3 frases** (senão demora muito).

Exemplo:

```
SYSTEM """
És o Professor Byte, um robô simpático que explica informática a alunos.
Usas sempre exemplos do dia a dia.
Respondes sempre em português de Portugal e em no máximo 3 frases.
"""
```

### ▶️ Criar o modelo e testar

Abre um **segundo terminal** (o primeiro está ocupado com os bigramas!), vai à pasta do projeto e:

```bash
ollama create assistente -f servico_llm/Modelfile
ollama run assistente
```

Faz-lhe 2 ou 3 perguntas. Para sair, escreve `/bye`.

> 💡 Se mudares o Modelfile, tens de voltar a correr o `ollama create ...` para atualizar o modelo.

> 📸 **SCREENSHOT 2:** o terminal com a conversa com o teu `assistente`.

### 2.2 O serviço LLM

📄 Abre `servico_llm/app.py`.

### 🧠 Como é que um programa fala com o Ollama?

O Ollama, além do terminal, tem uma **API HTTP** em `http://localhost:11434`.
O nosso serviço envia-lhe um pedido **POST** com um JSON assim:

```json
{ "model": "assistente", "prompt": "O que é um bigrama?", "stream": false }
```

e o Ollama responde com:

```json
{ "model": "assistente", "response": "Um bigrama é...", "done": true }
```

O dicionário `pedido` já está feito no código. Falta **enviá-lo** e **tirar o texto da resposta**.

### ✏️ TODO 5: enviar a pergunta ao Ollama

Segue os passos a) e b) que estão no comentário do código.

<details>
<summary>🆘 Estou mesmo encravado/a</summary>

```python
resposta = requests.post(OLLAMA_URL, json=pedido, timeout=120)
return resposta.json()["response"]
```
</details>

### ▶️ Arrancar e testar

No segundo terminal (com o `.venv` ativo!):

```bash
source .venv/bin/activate
python servico_llm/app.py
```

Abre no browser:
<http://localhost:5002/perguntar?pergunta=O que é um neurónio?>

(espera uns segundos, o modelo está a pensar 🧠)

---

## Parte 3 — O Gateway (15 min)

📄 Abre `gateway/app.py`.

### 🧠 Para que serve um gateway?

O utilizador não devia ter de saber que existem 2 serviços em 2 portas diferentes.
O **gateway** é o único serviço que o browser conhece: recebe o pedido e **chama os outros**,
juntando as respostas num só JSON. Lembra-te da *Integração de Sistemas #1*: é a mesma ideia.

Na função `perguntar()`, a chamada ao serviço de **bigramas já está feita como exemplo**. Lê-a
com atenção:

```python
r = requests.get(f"{URL_BIGRAMAS}/prever", params={"palavra": ...}, timeout=5)
sugestao = r.json()["seguinte"]
```

1. `requests.get(...)` faz um pedido GET, igual ao que fizeste no browser na Parte 1;
2. `params=` acrescenta o `?palavra=...` ao endereço;
3. `r.json()` transforma a resposta num dicionário Python, e tiramos a chave que queremos.

### ✏️ TODO 6: chamar o serviço LLM

Faz o mesmo para o serviço LLM. As indicações estão no comentário do código.

<details>
<summary>🆘 Estou mesmo encravado/a</summary>

```python
try:
    r = requests.get(
        f"{URL_LLM}/perguntar",
        params={"pergunta": texto},
        timeout=120,
    )
    resposta_llm = r.json()["resposta"]
except requests.exceptions.RequestException:
    resposta_llm = "(serviço LLM em baixo)"
```
</details>

### ▶️ Arrancar e verificar tudo

Abre um **terceiro terminal**, ativa o `.venv` e:

```bash
python gateway/app.py
```

Agora tens 3 terminais, um por serviço. Abre um **quarto terminal** e corre o verificador:

```bash
source .venv/bin/activate
python verificar.py
```

Ele testa todas as partes e diz-te o que falta. Corrige o que estiver ❌ até ficar tudo ✅.

> 📸 **SCREENSHOT 3:** o resultado do `python verificar.py` com tudo ✅.

---

## Parte 4 — Tudo junto com o PM2 (10 min)

### 🧠 Porquê o PM2?

Ter 3 terminais abertos é chato, e se um serviço rebentar fica em baixo. O **PM2** arranca
todos os serviços **em segundo plano**, com um só comando, e volta a ligá-los se falharem.

Primeiro, **para os 3 serviços** que tens a correr: em cada terminal, `Ctrl+C`.

### ✏️ TODO 7: acrescentar o gateway ao PM2

📄 Abre `ecosystem.config.js`. Não te assustes com o `.js`: é só uma **lista de serviços**,
e cada um diz *que ficheiro correr, em que pasta e com que Python*. Já lá estão o `bigramas`
e o `llm`. Acrescenta o `gateway` seguindo o comentário.

<details>
<summary>🆘 Estou mesmo encravado/a</summary>

```js
    {
      name: "gateway",
      script: "app.py",
      cwd: path.join(__dirname, "gateway"),
      interpreter: PYTHON,
    },
```
</details>

### ▶️ Arrancar tudo

```bash
pm2 start ecosystem.config.js
pm2 status
```

Deves ver os 3 serviços com o estado **online**.

> 📸 **SCREENSHOT 4:** o `pm2 status` com os 3 serviços `online`.

Agora abre a aplicação: **<http://localhost:8000>** 🎉

Escreve uma frase (ex.: *"O que faz o modelo"*) e vê as duas respostas lado a lado.

> 📸 **SCREENSHOT 5:** a página com uma pergunta tua e as duas respostas.

### 🔌 Experiência: desligar um micro-serviço

```bash
pm2 stop bigramas
```

Volta à página e faz outra pergunta. O que acontece ao estado e às respostas?

> 📸 **SCREENSHOT 6:** a página com o `bigramas: desligado`.

Volta a ligá-lo:

```bash
pm2 start bigramas
```

### Comandos úteis do PM2

| Comando | O que faz |
|---|---|
| `pm2 status` | Lista os serviços e o estado |
| `pm2 logs` | Mostra os prints e erros (Ctrl+C para sair) |
| `pm2 restart all` | Reinicia tudo (usa depois de mudares código) |
| `pm2 stop all` | Para tudo |
| `pm2 delete all` | Remove tudo do PM2 |

---

## Parte 5 — Perguntas e entrega (15 min)

### 5.1 Responder às perguntas

📄 Abre `RESPOSTAS.md` e responde às 5 perguntas (1 a 3 frases cada).
Algumas pedem-te para experimentar coisas, por isso faz isso com a aplicação a correr.

### 5.2 Enviar para o teu fork

```bash
git add .
git commit -m "Atividade de revisões concluída"
git push
```

> 💡 Se o `git push` pedir password, usa um **token** do GitHub (como nas outras aulas),
> ou faz o push pelo separador **Source Control** do VS Code.

Abre o teu fork no GitHub e confirma que as tuas alterações estão lá
(por exemplo, abre o `RESPOSTAS.md`).

### 5.3 Entregar no Teams ✅

Na tarefa do Teams, entrega:

1. **As 6 screenshots**
2. **O link do teu fork** (ex.: `https://github.com/o-teu-utilizador/mini-assistente-revisoes`)

### 5.4 Arrumar

```bash
pm2 delete all
```

---

## 🛟 Problemas comuns

| Problema | Solução |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Esqueceste-te do `source .venv/bin/activate` neste terminal. |
| `Address already in use` | Esse serviço já está a correr (noutro terminal ou no PM2). Faz `pm2 delete all` e fecha os outros terminais. |
| O `/prever` dá `"seguinte": null` | A palavra não está no `corpus.txt`, ou falta o TODO 2. Mudaste o código e não reiniciaste o serviço? |
| `Não consegui ligar ao Ollama` | Corre `ollama serve` noutro terminal (ou confirma que o Ollama está aberto). |
| `model 'assistente' not found` | Falta o `ollama create assistente -f servico_llm/Modelfile`. |
| O LLM demora muito | É normal na primeira pergunta (o modelo está a ser carregado). Confirma que tens a regra das "3 frases" no SYSTEM. |
| No PM2 aparece `errored` | Corre `pm2 logs NOME` para ver o erro. Muitas vezes é o `.venv` que não foi criado na pasta do projeto. |
| `pm2: command not found` | Instala com `npm install -g pm2` (como na aula do PM2). |

---

## ⭐ Desafio extra (só se acabares cedo)

1. Acrescenta texto teu ao `corpus.txt` (por exemplo, um parágrafo dos teus apontamentos),
   faz `pm2 restart bigramas` e vê como as previsões mudam.
2. Cria no serviço de bigramas uma rota `/gerar?palavra=o&n=8` que gera uma frase de `n`
   palavras, chamando `prever()` repetidamente (cada palavra prevista passa a ser a próxima entrada).
   Que problema aparece? Porque é que os LLMs não têm este problema?
