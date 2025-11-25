minikube start --cpus=2 --memory=2048 --driver=docker
minikube status

minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

kubectl config current-context

minikube

kubectl get nodes

NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   83s   v1.32.0

Etape 4:


 kubectl get pods -n kube-system
NAME                               READY   STATUS    RESTARTS      AGE
coredns-668d6bf9bc-zkfwm           1/1     Running   0             111s
etcd-minikube                      1/1     Running   0             115s
kube-apiserver-minikube            1/1     Running   0             117s
kube-controller-manager-minikube   1/1     Running   0             116s
kube-proxy-xtkfv                   1/1     Running   0             111s
kube-scheduler-minikube            1/1     Running   0             115s
storage-provisioner                1/1     Running   1 (80s ago)   114s


kubectl describe node minikube

Name:               minikube
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=minikube
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=dd5d320e41b5451cdf3c01891bc4e13d189586ed-dirty
                    minikube.k8s.io/name=minikube
                    minikube.k8s.io/primary=true
                    minikube.k8s.io/updated_at=2025_11_24T10_41_35_0700
                    minikube.k8s.io/version=v1.35.0
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/cri-dockerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 24 Nov 2025 10:41:32 +0100
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  minikube
  AcquireTime:     <unset>
  RenewTime:       Mon, 24 Nov 2025 10:44:38 +0100
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  MemoryPressure   False   Mon, 24 Nov 2025 10:41:45 +0100   Mon, 24 Nov 2025 10:41:31 +0100   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Mon, 24 Nov 2025 10:41:45 +0100   Mon, 24 Nov 2025 10:41:31 +0100   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Mon, 24 Nov 2025 10:41:45 +0100   Mon, 24 Nov 2025 10:41:31 +0100   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Mon, 24 Nov 2025 10:41:45 +0100   Mon, 24 Nov 2025 10:41:32 +0100   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  192.168.49.2
  Hostname:    minikube
Capacity:
  cpu:                12
  ephemeral-storage:  498976Mi
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             16040568Ki
  pods:               110
Allocatable:
  cpu:                12
  ephemeral-storage:  498976Mi
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             16040568Ki
  pods:               110
System Info:
  Machine ID:                 d53d6e084a41471fbae81cec030b5de4
  System UUID:                b8dcd072-1a0b-4867-893c-4f57a56bb0f9
  Boot ID:                    c22de2df-d52b-4b16-ba9e-e3edf721fb59
  Kernel Version:             6.17.7-300.fc43.x86_64
  OS Image:                   Ubuntu 22.04.5 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  docker://27.4.1
  Kubelet Version:            v1.32.0
  Kube-Proxy Version:         v1.32.0
PodCIDR:                      10.244.0.0/24
PodCIDRs:                     10.244.0.0/24
Non-terminated Pods:          (7 in total)
  Namespace                   Name                                CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
  ---------                   ----                                ------------  ----------  ---------------  -------------  ---
  kube-system                 coredns-668d6bf9bc-zkfwm            100m (0%)     0 (0%)      70Mi (0%)        170Mi (1%)     3m5s
  kube-system                 etcd-minikube                       100m (0%)     0 (0%)      100Mi (0%)       0 (0%)         3m9s
  kube-system                 kube-apiserver-minikube             250m (2%)     0 (0%)      0 (0%)           0 (0%)         3m11s
  kube-system                 kube-controller-manager-minikube    200m (1%)     0 (0%)      0 (0%)           0 (0%)         3m10s
  kube-system                 kube-proxy-xtkfv                    0 (0%)        0 (0%)      0 (0%)           0 (0%)         3m5s
  kube-system                 kube-scheduler-minikube             100m (0%)     0 (0%)      0 (0%)           0 (0%)         3m9s
  kube-system                 storage-provisioner                 0 (0%)        0 (0%)      0 (0%)           0 (0%)         3m8s
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------    ------
  cpu                750m (6%)   0 (0%)
  memory             170Mi (1%)  170Mi (1%)
  ephemeral-storage  0 (0%)      0 (0%)
  hugepages-1Gi      0 (0%)      0 (0%)
  hugepages-2Mi      0 (0%)      0 (0%)
Events:
  Type    Reason                   Age    From             Message
  ----    ------                   ----   ----             -------
  Normal  Starting                 3m4s   kube-proxy       
  Normal  Starting                 3m10s  kubelet          Starting kubelet.
  Normal  NodeAllocatableEnforced  3m9s   kubelet          Updated Node Allocatable limit across pods
  Normal  NodeHasSufficientMemory  3m9s   kubelet          Node minikube status is now: NodeHasSufficientMemory
  Normal  NodeHasNoDiskPressure    3m9s   kubelet          Node minikube status is now: NodeHasNoDiskPressure
  Normal  NodeHasSufficientPID     3m9s   kubelet          Node minikube status is now: NodeHasSufficientPID
  Normal  RegisteredNode           3m6s   node-controller  Node minikube event: Registered Node minikube in Controller

kubectl get pods --all-namespaces

NAMESPACE     NAME                               READY   STATUS    RESTARTS       AGE
kube-system   coredns-668d6bf9bc-zkfwm           1/1     Running   0              3m34s
kube-system   etcd-minikube                      1/1     Running   0              3m38s
kube-system   kube-apiserver-minikube            1/1     Running   0              3m40s
kube-system   kube-controller-manager-minikube   1/1     Running   0              3m39s
kube-system   kube-proxy-xtkfv                   1/1     Running   0              3m34s
kube-system   kube-scheduler-minikube            1/1     Running   0              3m38s
kube-system   storage-provisioner                1/1     Running   1 (3m3s ago)   3m37s


kubectl get pods -n kube-system | grep coredns

coredns-668d6bf9bc-zkfwm           1/1     Running   0               3m49s

kubectl logs coredns-668d6bf9bc-zkfwm   -n kube-system

.:53
[INFO] plugin/reload: Running configuration SHA512 = 9e2996f8cb67ac53e0259ab1f8d615d07d1beb0bd07e6a1e39769c3bf486a905bb991cc47f8d2f14d0d3a90a87dfc625a0b4c524fed169d8158c40657c0694b1
CoreDNS-1.11.3
linux/amd64, go1.21.11, a6338e9
[INFO] 127.0.0.1:49413 - 60298 "HINFO IN 2599021592254878397.5660598956364560182. udp 57 false 512" NXDOMAIN qr,rd,ra 132 0.028311595s


Etape5:
kubectl create deployment hello-minikube --image=registry.k8s.io/echoserver:1.10

kubectl get pods 
NAME                             READY   STATUS         RESTARTS   AGE
hello-minikube-d6fc6dbb4-74wbj   0/1     ErrImagePull   0          8s


kubectl get deployments

NAME             READY   UP-TO-DATE   AVAILABLE   AGE
hello-minikube   1/1     1            1           44s

kubectl describe deployment hello-minikube

Name:                   hello-minikube
Namespace:              default
CreationTimestamp:      Mon, 24 Nov 2025 10:58:34 +0100
Labels:                 app=hello-minikube
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=hello-minikube
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=hello-minikube
  Containers:
   echoserver:
    Image:         registry.k8s.io/echoserver:1.10
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   hello-minikube-8696bfd944 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  4m7s  deployment-controller  Scaled up replica set hello-minikube-8696bfd944 from 0 to 1

Etape 6

kubectl expose deployment hello-minikube --type=NodePort --port=8080

service/hello-minikube exposed


kubectl get services

NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-minikube   NodePort    10.98.121.110   <none>        8080:32749/TCP   39s
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP          22m


minikube service hello-minikube --url

http://192.168.49.2:32749

curl http://192.168.49.2:32749



Hostname: hello-minikube-8696bfd944-xpgxq

Pod Information:
        -no pod information available-

Server values:
        server_version=nginx: 1.13.3 - lua: 10008

Request Information:
        client_address=10.244.0.1
        method=GET
        real path=/
        query=
        request_version=1.1
        request_scheme=http
        request_uri=http://192.168.49.2:8080/

Request Headers:
        accept=*/*
        host=192.168.49.2:32749
        user-agent=curl/8.15.0

Request Body:
        -no body in request-


Etape7

kubectl delete service hello-minikube

service "hello-minikube" deleted


kubectl delete deployment hello-minikube

deployment.apps "hello-minikube" deleted

kubectl get pods
                                     kubectl get services
                                     kubectl get deployments

NAME                              READY   STATUS        RESTARTS   AGE
hello-minikube-8696bfd944-xpgxq   1/1     Terminating   0          9m45s
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   26m
No resources found in default namespace.

minikube stop

✋  Nœud d'arrêt "minikube" ...
🛑  Mise hors tension du profil "minikube" via SSH…
🛑  1 nœud arrêté.
minikube status

minikube
type: Control Plane
host: Stopped
kubelet: Stopped
apiserver: Stopped
kubeconfig: Stopped

minikube delete

🔥  Suppression de "minikube" dans docker...
🔥  Suppression du conteneur "minikube" ...
🔥  Suppression du répertoire /home/rmartin/.minikube/machines/minikube…
💀  Le cluster "minikube" a été supprimé.
