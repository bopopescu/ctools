#!/usr/bin/bash
rm value_private_key.txt
rm value_public_key.txt
sed -i '/ContrailIssuSshKey/d' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
sed -i '/public_key/d' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
sed -i '/ISSU ssh public key/d' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
sed -i '/private_key/d' tripleo-heat-templates/environments/contrail/contrail-issu.yaml
sed -i '/ISSU ssh private key/d' tripleo-heat-templates/environments/contrail/contrail-issu.yaml

echo '  ContrailIssuSshKey:' >> tripleo-heat-templates/environments/contrail/contrail-issu.yaml
echo '    private_key: |' >> tripleo-heat-templates/environments/contrail/contrail-issu.yaml
cat .ssh/id_rsa >> value_private_key.txt

input_private="value_private_key.txt"
while IFS= read -r line
do
  echo "      $line" >> tripleo-heat-templates/environments/contrail/contrail-issu.yaml
done < "$input_private"

echo '    public_key: |' >> tripleo-heat-templates/environments/contrail/contrail-issu.yaml
sed 's/ssh-rsa/      ssh-rsa/' .ssh/id_rsa.pub >> value_public_key.txt
cat value_public_key.txt >> tripleo-heat-templates/environments/contrail/contrail-issu.yaml
