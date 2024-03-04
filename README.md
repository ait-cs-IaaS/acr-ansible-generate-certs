# Ansible-Role: acr-ansible-generate-certs

AIT-CyberRange: Generates certs and respective keys. 


## Requirements

- Debian or Ubuntu 

## Role Variables

```yaml
# List of certificate information as dicts
certificates: []

# Path to certs data-dir (destination)
ca_base_path: ''

# Password for signing CA
ca_pw: ''

# Path to local CA certificate
ca_cert: ''

# Path to local CA private key
ca_key: ''

ca_check_valid_till: '+8w'
```

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - acr-ansible-generate-host-certs
      vars:
        certificates: [
            {
                "cert_type": "smime", # determines type of certificate 
                "common_name": "security@austricom.at",
                "domain": "austricom.at",
                "email_address": "security@austricom.at",
                "key_usage_critical": true,
                "name": "security",
                "subject_alt_name": [
                    "email:security@austricom.at"
                ]
            }
        ]
        ca_base_path: "/tmp/data/certs"
        ca_cert: "/tmp/data/certs/ca.crt"
        ca_key: "/tmp/data/certs/ca.key"
        ca_pw: "secretpassword"
```

## License

GPL-3.0

## Author

- Lenhard Reuter