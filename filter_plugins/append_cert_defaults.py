from collections import defaultdict


class FilterModule(object):
    def filters(self):
        return {
            "append_cert_defaults": self.append_cert_defaults,
        }

    def append_cert_defaults(self, certs, base_path, ca, **kwargs):

        print(certs)

        _certs = []

        for cert in certs:
            _cert_type = cert.get("cert_type", "sites")
            cert["cert_type"] = _cert_type

            if _cert_type == "ca":
                _path = [base_path, "ca"]
                cert["path"] = "/".join(_path)

                cert["basic_constraints"] = ["CA:TRUE"]
                cert["cipher"] = "auto"
                cert["selfsigned_not_before"] = cert.get("valid_from", None)
                cert["selfsigned_not_after"] = cert.get("valid_till", None)
                cert["privatekey_passphrase"] = cert.get("password", None)
                cert["provider"] = "selfsigned"

            if _cert_type == "sites":
                _path = [
                    base_path,
                    "sites",
                    (cert.get("host")).lower(),
                    (cert.get("common_name")).lower(),
                    (cert.get("common_name")).lower(),
                ]
                cert["path"] = "/".join(_path)

                cert["ownca_path"] = ca["cert"]
                cert["ownca_privatekey_path"] = ca["key"]
                cert["ownca_privatekey_passphrase"] = ca["pw"]
                cert["ownca_not_before"] = cert.get("valid_from", None)
                cert["ownca_not_after"] = cert.get("valid_till", None)
                cert["provider"] = "ownca"

            if _cert_type == "smime":
                _path = [
                    base_path,
                    "mails",
                    (cert.get("domain")).lower(),
                    (cert.get("name")).lower(),
                    (cert.get("name")).lower(),
                ]
                cert["path"] = "/".join(_path)

                _full_email = f"{cert.get('name')}@{cert.get('domain')}"
                cert["common_name"] = _full_email
                cert["email_address"] = _full_email
                cert["subject_alt_name"] = [f"email:{_full_email}"]
                cert["key_usage"] = [
                    "dataEncipherment",
                    "keyEncipherment",
                    "digitalSignature",
                ]
                cert["key_usage_critical"] = True
                cert["extended_key_usage"] = ["emailProtection", "clientAuth"]
                cert["use_common_name_for_san"] = False

                cert["ownca_path"] = ca["cert"]
                cert["ownca_privatekey_path"] = ca["key"]
                cert["ownca_privatekey_passphrase"] = ca["pw"]
                cert["ownca_not_before"] = cert.get("valid_from", None)
                cert["ownca_not_after"] = cert.get("valid_till", None)
                cert["provider"] = "ownca"

            cert = {key: value for key, value in cert.items() if value}
            _certs.append(cert)

        return _certs
