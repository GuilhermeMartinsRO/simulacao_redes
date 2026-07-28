import argparse
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def gerar_chaves():
    privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return privada, privada.public_key()

def mostrar_chave_publica(chave_publica):
    return chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

def mostrar_chave_privada(chave_privada):
    return chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

def criptografar(mensagem, chave_publica):
    return chave_publica.encrypt(
        mensagem,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

def descriptografar(mensagem_cifrada, chave_privada):
    return chave_privada.decrypt(
        mensagem_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def assinar(mensagem, chave_privada):
    return chave_privada.sign(
        mensagem,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verificar(mensagem, assinatura, chave_publica):
    try:
        chave_publica.verify(
            assinatura,
            mensagem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def fluxo(texto):
    
    mensagem = texto.encode("utf-8")

    print("\n=== CRIPTOGRAFIA ===\n\n")
    
    print("\n=== Par de chaves ===")
    print ("Gerando as chaves da Alice")
    privada_alice, publica_alice = gerar_chaves()
    print (f"Chave privada da Alice: {mostrar_chave_privada(privada_alice)}\nChave publica Alice: {mostrar_chave_publica(publica_alice)}")
    print ("Gerando as chaves do Bob")
    privada_bob, publica_bob = gerar_chaves()
    print (f"Chave privada do Bob: {mostrar_chave_privada(privada_bob)}\nChave publica Alice: {mostrar_chave_publica(publica_bob)}")

    print(f"1. Bob fornece sua chave pública.")
    print(f"2. Alice criptografa para Bob: {texto!r}")
    try:
        cifrada = criptografar(mensagem, publica_bob)
    except ValueError:
        raise SystemExit("Use uma mensagem menor, com no máximo 190 bytes.")
    print(f"3. Pela rede trafega: {base64.b64encode(cifrada).decode()[:60]}...")
    aberta = descriptografar(cifrada, privada_bob)
    print(f"4. Bob abre com sua chave privada: {aberta.decode()!r}")


    print("\n\n=== ASSINATURA DIGITAL ===")
    assinatura = assinar(mensagem, privada_alice)
    print("1. Alice assina a mensagem com sua chave privada.")
    print("2. Bob verifica com a chave pública de Alice.")
    print("   Mensagem original:", "VÁLIDA" if verificar(
        mensagem, assinatura, publica_alice
    ) else "INVÁLIDA")
    print("   Mensagem alterada:", "VÁLIDA" if verificar(
        mensagem + b" alterada", assinatura, publica_alice
    ) else "INVÁLIDA")
    print("   Chave diferente:", "VÁLIDA" if verificar(
            mensagem, assinatura, publica_bob
        ) else "INVÁLIDA")


fluxo(input("Digite uma mensagem : "))
