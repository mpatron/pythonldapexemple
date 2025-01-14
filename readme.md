# Python & LDAP

## Installation de ldapsearch

~~~bash
apt install ldap-utils
~~~

## Installation des CA pour LDAPS

### Sous Redhat

sudo cp ~/companyCA.crt /etc/pki/tls/certs/

### Sous Debian

~~~bash
sudo apt-get install -y ca-certificates
# sudo cp local-ca.crt /usr/local/share/ca-certificates
sudo curl -L -o /usr/local/share/ca-certificates/idm.jobjects.org.ca.crt http://idm.jobjects.org/ipa/config/ca.crt
ls -la /usr/local/share/ca-certificates
sudo update-ca-certificates
# Si le CA de freeipa n'est pas installer alors la connection ne peut pas foncitonner
ldapsearch -LLL -D uid=admin,cn=users,cn=accounts,dc=jobjects,dc=org -w 'HelloWorld!' -b cn=accounts,dc=jobjects,dc=org -H ldaps://idm.jobjects.org
~~~

## Python avec sa librairy LDAP

!! Ne pas utiliser python-ldap qui est un wrap de la librairy openldap, tout particulièrement de la librairy libldap. !!
Il faut utiliser la librairy ldap3 qui est du pure python. Cela permet d'être plus portable et ne pas nécessiter l'installation du client openldap.

~~~bash
sudo apt install python3
sudo apt install python3-pip python3-venv
python -m venv ./.venv
source ./.venv/bin/activate
(venv) $ python -m pip install ldap3
(venv) $ python -m pip install --upgrade ldap3
(venv) $ pip freeze > requirements.txt
(venv) $ deactivate
~~~

Ce code peut être exécuter directement dans une console python pour tester

~~~python
from ldap3 import Server, Connection, ALL
server = Server('idm.jobjects.org', get_info=ALL)
conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=jobjects,dc=org', 'HelloWorld!', auto_bind=True)
conn.search('cn=accounts,dc=jobjects,dc=org', '(objectclass=person)')
print(conn.entries)
conn.search('cn=accounts,dc=jobjects,dc=org', '(&(objectclass=person)(uid=admin))', attributes=['sn', 'krbLastPwdChange', 'objectclass'])
print(conn.entries)
print(conn.entries[0].entry_to_json())
~~~

La réinstallation des librairies nécessaires, peut se faire avec la simple commande suivante:

~~~bash
pip install -r requirements.txt
~~~
