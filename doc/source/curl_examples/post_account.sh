TOKEN=`curl -s -i --cacert /opt/rucio/etc/web/ca.crt -H "Rucio-Account: root" -E /opt/rucio/etc/web/client.crt -X GET https://localhost/auth/x509 | grep X-Rucio-Auth-Token | awk '{print $2}'`
curl -s -i --cacert /opt/rucio/etc/web/ca.crt -H "X-Rucio-Auth-Token: $TOKEN" -H "Rucio-Type: user" -d '{"accountName": "jdoe", "accountType": "user"}' -X POST https://localhost/accounts/
