import string

#
# Template for /etc/yum.repos.d/Contrail.repo
#
yum_repo = string.Template('''
[contrail]
name = Contrail Repo
baseurl = http://ci-docker.englab.juniper.net/repository/$os/$release-$buildid-$os
enabled = 1
gpgcheck = 0

[contrail-tpc-binary]
name = Contrail Third Party Binary
baseurl = http://ci-nexus.englab.juniper.net/repository/yum-tungsten-tpc/master/binary
enabled = 1
gpgcheck = 0

[contrail-tpc-source]
name = Contrail Third Party Source
baseurl = http://ci-nexus.englab.juniper.net/repository/yum-tungsten-tpc/master/source
enabled = 1
gpgcheck = 0
''')

#
# Template for contrail-kube-manager
# This is a cloned from following file, must be kept in-sync
# https://github.com/Juniper/contrail-container-builder/blob/master/kubernetes/manifests/contrail-nested-kubernetes.yaml
#
contrail = string.Template('''
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: env
  namespace: kube-system
data:
  AUTH_MODE: keystone
  KEYSTONE_AUTH_HOST: $auth_host
  KEYSTONE_AUTH_ADMIN_TENANT: $auth_tenant
  KEYSTONE_AUTH_ADMIN_USER: $auth_user
  KEYSTONE_AUTH_ADMIN_PASSWORD: $auth_pwd
  KEYSTONE_AUTH_ADMIN_PORT: "$ks_port"
  KEYSTONE_AUTH_URL_VERSION: $ks_ver
  CLOUD_ORCHESTRATOR: kubernetes
  CONTROLLER_NODES: $ctrl_nodes
  CONFIG_NODES: $cfg_nodes
  CONFIG_API_VIP: $cfg_vip
  LOG_LEVEL: SYS_NOTICE
  RABBITMQ_NODES: $rabbitmq_nodes
  RABBITMQ_NODE_PORT: "$rabbitmq_port"
  ZOOKEEPER_SERVERS: $zk_nodes
  KUBEMANAGER_NESTED_MODE: "1"
  KUBERNETES_CLUSTER_NETWORK: "$cluster_network"
  KUBERNETES_CLUSTER_PROJECT: "$cluster_project"
  KUBERNETES_CLUSTER_NAME: $cluster_name
  KUBERNETES_POD_SUBNETS: $pod_subnet
  KUBERNETES_IP_FABRIC_SUBNETS: $fabric_subnet
  KUBERNETES_SERVICE_SUBNETS: $service_subnet
  KUBERNETES_IP_FABRIC_FORWARDING: "$fabric_fwd"
  KUBERNETES_IP_FABRIC_SNAT: "$fabric_snat"
  KUBERNETES_PUBLIC_FIP_POOL: "$fip_pool"
  KUBERNESTES_NESTED_VROUTER_VIP: $vrouter_vip
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-manager-config
  namespace: kube-system
data:
  KUBERNETES_API_SERVER: $master_ip
  KUBERNETES_API_SECURE_PORT: "6443"
  K8S_TOKEN_FILE: "/tmp/serviceaccount/token"
# Containers section
---
apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  name: contrail-kube-manager
  namespace: kube-system
  labels:
    app: contrail-kube-manager
spec:
  template:
    metadata:
      labels:
        app: contrail-kube-manager
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: "node-role.kubernetes.io/master"
                operator: Exists
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      - key: node.kubernetes.io/not-ready
        operator: Exists
        effect: NoSchedule
      automountServiceAccountToken: false
      hostNetwork: true
      containers:
      - name: contrail-kube-manager
        image: $kubemgr_image
        imagePullPolicy: ""
        envFrom:
        - configMapRef:
            name: env
        - configMapRef:
            name: kube-manager-config
        volumeMounts:
        - mountPath: /var/log/contrail
          name: kube-manager-logs
        - mountPath: /tmp/serviceaccount
          name: pod-secret
      imagePullSecrets:
      - name: 
      volumes:
      - name: kube-manager-logs
        hostPath:
          path: /var/log/contrail/kube-manager
      - name: pod-secret
        secret:
          secretName: contrail-kube-manager-token
---
apiVersion: extensions/v1beta1
kind: DaemonSet
metadata:
  name: contrail-kubernetes-cni-agent
  namespace: kube-system
  labels:
    app: contrail-kubernetes-cni-agent
spec:
  template:
    metadata:
      labels:
        app: contrail-agent
    spec:
      #Disable affinity for single node setup
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: "node-role.opencontrail.org/controller"
                operator: NotIn
                values:
                - "true"
      tolerations:
      - key: node.kubernetes.io/not-ready
        operator: Exists
        effect: NoSchedule
      automountServiceAccountToken: false
      hostNetwork: true
      containers:
      - name: contrail-kubernetes-cni-init
        image: $cni_init_image
        imagePullPolicy: ""
        securityContext:
          privileged: true
        envFrom:
        - configMapRef:
            name: env
        volumeMounts:
        - mountPath: /host/etc_cni
          name: etc-cni
        - mountPath: /host/opt_cni_bin
          name: opt-cni-bin
        - mountPath: /var/lib/contrail
          name: var-lib-contrail
      imagePullSecrets:
      - name: 
      volumes:
      - name: etc-cni
        hostPath:
          path: /etc/cni
      - name: opt-cni-bin
        hostPath:
          path: /opt/cni/bin
      - name: var-lib-contrail
        hostPath:
          path: /var/lib/contrail
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: contrail-kube-manager
  namespace: kube-system
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["*"]
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: contrail-kube-manager
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: contrail-kube-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: contrail-kube-manager
subjects:
- kind: ServiceAccount
  name: contrail-kube-manager
  namespace: kube-system
---
apiVersion: v1
kind: Secret
metadata:
  name: contrail-kube-manager-token
  namespace: kube-system
  annotations:
    kubernetes.io/service-account.name: contrail-kube-manager
type: kubernetes.io/service-account-token
''')

#
# Template for kubernetes nested instances, input for contrail-ansible
#
k8s = string.Template('''
global_configuration:
 REGISTRY_PRIVATE_INSECURE: $registry_insecure
 CONTAINER_REGISTRY: $registry

provider_config:
 bms:
   ssh_pwd: $bms_pwd
   ssh_user: $bms_usr
   ntpserver: $ntp

instances:
 $master_name:
   provider: bms
   ip: $master_ip
   roles:
     k8s_master:
 $slave1_name:
   provider: bms
   ip: $slave1_ip
   roles:
     k8s_node:
 $slave2_name:
   provider: bms
   ip: $slave2_ip
   roles:
     k8s_node:
''')
