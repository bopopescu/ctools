#!/usr/bin/bash
rm value_private_key.txt
rm value_public_key.txt
echo '  MigrationSshKey:' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
echo '    private_key: |' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
cat .ssh/id_rsa >> value_private_key.txt

input_private="value_private_key.txt"
while IFS= read -r line
do
  echo "      $line" >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
done < "$input_private"

echo '    public_key: |' >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
sed 's/ssh-rsa/      ssh-rsa/' .ssh/id_rsa.pub >> value_public_key.txt
cat value_public_key.txt >> tripleo-heat-templates/environments/contrail/contrail-services.yaml
