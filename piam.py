import argparse
import shutil
import os
import ldap3


# Récuperation des groupes
def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Configuration des applications"
    )

    parser.add_argument(
        "-u",
        "--username",
        default="uid=admin,cn=users,cn=accounts,dc=jobjects,dc=org",
        help="Login de session.",
    )
    parser.add_argument(
        "-p", "--password", default="HelloWorld!", help="Mot de passe de session."
    )
    parser.add_argument(
        "-a",
        "--ad",
        default="idm.jobjects.org",
        help="fqdn de l'Active directory ou LDAPS.",
    )

    # Parse the arguments
    args = parser.parse_args()
    print(f"Argument login {args.username}")

    from ldap3 import Server, Connection, ALL

    server = Server(args.ad, get_info=ALL)
    conn = Connection(
        server,
        args.username,
        args.password,
        auto_bind=True,
    )
    conn.search("cn=users,cn=accounts,dc=jobjects,dc=org", "(objectclass=person)")
    print(conn.entries[0].entry_to_json())

    conn.search("cn=groups,cn=accounts,dc=jobjects,dc=org", "(objectclass=nestedgroup)")
    print(conn.entries)

    conn.search(
        "cn=accounts,dc=jobjects,dc=org",
        "(&(objectclass=person)(uid=admin))",
        attributes=["sn", "krbLastPwdChange", "objectclass"],
    )
    print(conn.entries)


if __name__ == "__main__":
    main()
    print("End.")
