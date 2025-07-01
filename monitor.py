import time
import instaloader
import requests

USERNAME = "weversonmeireles"
SESSION_FILE = "checkinstabr.session"
INTERVALO_SEGUNDOS = 20
LIMIAR_ALERTA = 40

TOKEN_BOT = "7845619981:AAFo4LGaqSMcbC2aoAjSubcqvDLRY6cvjNU"
CHAT_ID_GRUPO = "-1002622438551"
CHAT_ID_PRIVADO = "692686870"

ultimo_valor = None

def enviar_mensagem(chat_id, mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[ERRO AO ENVIAR MENSAGEM] {e}")

def get_followers_count():
    loader = instaloader.Instaloader()
    try:
        loader.load_session_from_file(username=None, filename=SESSION_FILE)
        profile = instaloader.Profile.from_username(loader.context, USERNAME)
        return profile.followers
    except Exception as e:
        print(f"[ERRO INSTALOADER] {e}")
        return None

def start_monitoring():
    global ultimo_valor
    ultimo_valor = get_followers_count()
    if ultimo_valor is None:
        print("[ERRO] Não foi possível obter número inicial de seguidores.")
        return

    print(f"[INICIADO] Seguidores atuais: {ultimo_valor}")
    enviar_mensagem(CHAT_ID_PRIVADO, f"🟢 Monitoramento iniciado.\nSeguidores: {ultimo_valor}")

    while True:
        time.sleep(INTERVALO_SEGUNDOS)
        atual = get_followers_count()
        if atual is None:
            continue

        diferenca = atual - ultimo_valor
        if diferenca > LIMIAR_ALERTA:
            enviar_mensagem(CHAT_ID_GRUPO, f"🚨 ALERTA: +{diferenca} seguidores em 20 segundos!")
        enviar_mensagem(CHAT_ID_PRIVADO, f"👥 Seguidores: {atual} (Δ {diferenca})")
        ultimo_valor = atual

