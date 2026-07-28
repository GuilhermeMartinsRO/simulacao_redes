# Demonstração simples de criptografia RSA

Este projeto de terminal demonstra os três slides com uma única mensagem.

## Como executar

No Windows:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r .\demonstracao_criptografia_rsa\requirements.txt
.\venv\Scripts\python.exe .\demonstracao_criptografia_rsa\main.py
```

Digite uma mensagem curta quando solicitado. Para evitar a pergunta:

```powershell
.\venv\Scripts\python.exe .\demonstracao_criptografia_rsa\main.py --mensagem "Trabalho de redes"
```

## O que mostrar durante a apresentação

1. **Par de chaves:** Alice e Bob geram suas chaves RSA de 2048 bits. A chave
   pública pode ser distribuída, mas a privada deve permanecer secreta.
2. **Criptografia:** Alice usa a chave pública de Bob para criptografar. A mensagem
   trafega ilegível e Bob usa sua chave privada para recuperá-la.
3. **Assinatura digital:** Alice usa sua própria chave privada para assinar. Bob
   verifica com a chave pública de Alice. Quando o programa altera a mensagem, a
   assinatura passa a ser inválida.
