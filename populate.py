import subprocess
import json

#   ___                                    __      _            _
#  / _ \                                  / _|    (_)          | |
# / /_\ \  _ __   ___   _ __   __ _ ___  | |_ __ _ _ _ __ ___  | |
# |  _  | | '_ \ / _ \ | '_ \ / _` / __| |  _/ _` | | '__/ _ \ | |
# | | | | | | | |  __/ | |_) | (_| \__ \ | || (_| | | | |  __/ |_|
# \_| |_/ |_| |_|\___| | .__/ \__,_|___/ |_| \__,_|_|_|  \___| (_)
#                      | |
#                      |_|


def extract_value_from_json(file_path, key):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data.get(key, None)


def make_vault_api_call():
    # Commande curl avec authentification
    curl_command = [
        "curl",
        "-H",
        "Content-Type: application/json",
        "-H",
        "X-Vault-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "https://vault.jobjects.org/v1/data/app",
    ]

    # Exécution de la commande curl
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Affichage de la réponse
    if result.returncode == 0:
        print("Réponse de l'API:")
        return result.stdout
    else:
        print("Erreur lors de l'appel API:")
        print(result.stderr)


def make_ldap_call(anais_pwd):
    # Commande ldap avec authentification
    ldap_command = [
        "ldapsearch",
        "-H",
        "ldaps://idm.jobjects.org:636",
        "-w",
        anais_pwd,
        "-D",
        "uid=admin,cn=users,cn=accounts,dc=jobjects,dc=org",
        "-b",
        "cn=accounts,dc=jobjects,dc=org",
        'cn | grep ^cn | cut -d ":" -f2',
    ]
    # Exécution de la commande curl
    result = subprocess.run(ldap_command, capture_output=True, text=True)

    # Affichage de la réponse
    if result.returncode == 0:
        print("Réponse du LDAP: ok")
        result.stdout
    else:
        print("Erreur lors de l'appel LDAP")
        print(result.stderr)


def process_list(liste, auth_token):
    for line in liste:
        api_url = line.strip()
        if api_url:
            make_api_call(api_url, auth_token)


# Exemple d'utilisation
# Recup le pwd de vault => demander un token à l'équipe de sécurité
secret_file = make_vault_api_call()
anais_pwd = extract_value_from_json(secret_file, "password")
# Recup la liste des groupeS LDAP pour DFAB
liste = make_ldap_call(anais_pwd)

auth_token = "votre_token_d_authentification"
process_liste(liste, auth_token)
