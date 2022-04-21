# coding: utf-8
import ldap
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

from sigi.apps.servidores.models import Servidor
from sigi.settings import *


class Command(BaseCommand):
    help = "Sincroniza Usuários e Servidores com o LDAP"

    def handle(self, *args, **options):
        self.sync_groups()
        self.sync_users()

    def get_ldap_groups(self):
        filter = "(&(objectclass=Group))"
        values = [
            "cn",
        ]
        l = ldap.initialize(AUTH_LDAP_SERVER_URI)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(
                AUTH_LDAP_BIND_DN.encode("utf-8"), AUTH_LDAP_BIND_PASSWORD
            )

            page_control = ldap.controls.SimplePagedResultsControl(
                True, size=1000, cookie=""
            )
            result = []
            pages = 0

            while True:
                pages += 1
                response = l.search_ext(
                    AUTH_LDAP_GROUP,
                    ldap.SCOPE_SUBTREE,
                    filter,
                    values,
                    serverctrls=[page_control],
                )
                rtype, rdata, rmsgid, serverctrls = l.result3(response)
                result.extend(rdata)
                controls = [
                    control
                    for control in serverctrls
                    if control.controlType
                    == ldap.controls.SimplePagedResultsControl.controlType
                ]
                if not controls:
                    raise Exception("The server ignores RFC 2696 control")
                if not controls[0].cookie:
                    break
                page_control.cookie = controls[0].cookie
            # result_id = l.search(AUTH_LDAP_GROUP, ldap.SCOPE_SUBTREE, filter, values)
            # result_type, result_data = l.result(result_id, 1)
        finally:
            l.unbind()
        return result

    def get_ldap_users(self):
        filter = "(&(objectclass=user)(|(memberof=CN=lgs_ilb,OU=GruposAutomaticosOU,DC=senado,DC=gov,DC=br)(memberof=CN=lgt_ilb,OU=GruposAutomaticosOU,DC=senado,DC=gov,DC=br)(memberof=CN=lge_ilb,OU=GruposAutomaticosOU,DC=senado,DC=gov,DC=br)))"
        values = [
            "sAMAccountName",
            "userPrincipalName",
            "givenName",
            "sn",
            "cn",
        ]
        l = ldap.initialize(AUTH_LDAP_SERVER_URI)
        try:
            l.protocol_version = ldap.VERSION3
            l.set_option(ldap.OPT_REFERRALS, 0)
            l.simple_bind_s(
                AUTH_LDAP_BIND_DN.encode("utf-8"), AUTH_LDAP_BIND_PASSWORD
            )

            page_control = ldap.controls.SimplePagedResultsControl(
                True, size=1000, cookie=""
            )

            result = []
            pages = 0

            while True:
                pages += 1
                response = l.search_ext(
                    AUTH_LDAP_USER.encode("utf-8"),
                    ldap.SCOPE_SUBTREE,
                    filter,
                    values,
                    serverctrls=[page_control],
                )
                rtype, rdata, rmsgid, serverctrls = l.result3(response)
                result.extend(rdata)
                controls = [
                    control
                    for control in serverctrls
                    if control.controlType
                    == ldap.controls.SimplePagedResultsControl.controlType
                ]
                if not controls:
                    raise Exception("The server ignores RFC 2696 control")
                if not controls[0].cookie:
                    break
                page_control.cookie = controls[0].cookie
        # result_id = l.search(AUTH_LDAP_USER.encode('utf-8'), ldap.SCOPE_SUBTREE, filter, values)
        # result_type, result_data = l.result(result_id, 1)
        finally:
            l.unbind()
        return result

    def sync_groups(self):
        print("Syncing groups...")
        ldap_groups = self.get_ldap_groups()
        print(f"\tFetched groups: {ldap_groups}")
        for ldap_group in ldap_groups:
            try:
                group_name = ldap_group[1]["cn"][0]
            except:
                pass
            else:
                try:
                    group = Group.objects.get(name=group_name)
                except Group.DoesNotExist:
                    group = Group(name=group_name)
                    group.save()
                    print(f"\tGroup '{group_name}' created.")
        print("Groups are synchronized.")

    def sync_users(self):
        print("Syncing users...")
        ldap_users = self.get_ldap_users()
        print(f"\tFetched users: {ldap_users}")

        def get_ldap_property(ldap_user, property_name, default_value=None):
            value = ldap_user[1].get(property_name, None)
            return value[0].decode("utf8") if value else default_value

        for ldap_user in ldap_users:
            username = get_ldap_property(ldap_user, "sAMAccountName")
            if username:
                email = get_ldap_property(ldap_user, "userPrincipalName", "")
                first_name = get_ldap_property(ldap_user, "givenName", username)
                last_name = get_ldap_property(ldap_user, "sn", "")[:30]
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email=email)
                        old_username = user.username
                        user.username = username
                        print(
                            f"\tUser with email {email} had his/her username updated from [{old_username}] to [{username}]."
                        )
                    except User.DoesNotExist:
                        user = User.objects.create_user(
                            username=username,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                        )
                        print(f"\tUser '{username}' created.")

                if not user.first_name == first_name:
                    user.first_name = first_name
                    print(f"\tUser '{username}' first name updated.")
                if not user.last_name == last_name:
                    user.last_name = last_name
                    print(f"\tUser '{username}' last name updated.")
                if not user.email == email:
                    user.email = email
                    print(f"\tUser '{username}' email updated.")

                nome_completo = get_ldap_property(ldap_user, "cn", "")
                try:
                    servidor = user.servidor
                except Servidor.DoesNotExist:
                    try:
                        servidor = Servidor.objects.get(
                            nome_completo=nome_completo
                        )
                    except Servidor.DoesNotExist:
                        servidor = user.servidor_set.create(
                            nome_completo=nome_completo
                        )
                        print(f"\tServidor '{nome_completo}' created.")
                else:
                    if not servidor.nome_completo == nome_completo:
                        servidor.nome_completo = nome_completo
                        print(
                            f"\tFull name of Servidor '{nome_completo}' updated."
                        )

                servidor.user = user
                servidor.save()
                user.save()
        print("Users are synchronized.")
