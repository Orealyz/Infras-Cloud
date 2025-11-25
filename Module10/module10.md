# TP guidé
### Préparation du cloud
1. Choisir un cloud : Azure (AKS) ou GCP (GKE) ou AWS (EKS).
Je choisis GCP

2. Créer les ressources préalables :
Azure : Resource Group.
GCP : Projet.
AWS : Compte actif.

```
gcloud projects create tp-kube-project
Create in progress for [https://cloudresourcemanager.googleapis.com/v1/projects/tp-kube-project].
Waiting for [operations/create_project.global.8109570239206798258] to finish...done.                                                                                                       
Enabling service [cloudapis.googleapis.com] on project [tp-kube-project]...
Operation "operations/acat.p2-1088575790152-5070f708-8e09-41a4-8b38-7fcdead56481" finished successfully.
```

```
gcloud config set project tp-kube-project
Updated property [core/project].
```

###  Cluster Kubernetes
1. Créer un cluster managé :
2 nœuds minimum.
Version Kubernetes récente par défaut.

```
gcloud container clusters create tp-cluster \
                                       --zone=europe-west1-b \
                                       --num-nodes=2

Default change: VPC-native is the default mode during cluster creation for versions greater than 1.21.0-gke.1500. To create advanced routes based clusters, please pass the `--no-enable-ip-alias` flag
Note: The Kubelet readonly port (10255) is now deprecated. Please update your workloads to use the recommended alternatives. See https://cloud.google.com/kubernetes-engine/docs/how-to/disable-kubelet-readonly-port for ways to check usage and for migration instructions.
Note: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).
Creating cluster tp-cluster in europe-west1-b... Cluster is being health-checked (Kubernetes Control Plane is healthy)...done.                                                             
Created [https://container.googleapis.com/v1/projects/tp-kube-project/zones/europe-west1-b/clusters/tp-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west1-b/tp-cluster?project=tp-kube-project
kubeconfig entry generated for tp-cluster.
NAME        LOCATION        MASTER_VERSION      MASTER_IP     MACHINE_TYPE  NODE_VERSION        NUM_NODES  STATUS
tp-cluster  europe-west1-b  1.33.5-gke.1201000  35.195.28.33  e2-medium     1.33.5-gke.1201000  2          RUNNING
```

2. Récupérer la configuration kubeconfig .

```
gcloud container clusters get-credentials tp-cluster --zone=europe-west1-b

Fetching cluster endpoint and auth data.
kubeconfig entry generated for tp-cluster.

```

3. Vérifier l’accès avec kubectl get nodes .

```
kubectl get nodes

NAME                                        STATUS   ROLES    AGE     VERSION
gke-tp-cluster-default-pool-dfa793c4-djbb   Ready    <none>   3m38s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-dfa793c4-hk7p   Ready    <none>   3m36s   v1.33.5-gke.1201000

```

###  Namespace et objets de configuration
1. Créer un namespace tp-app .

```
kubectl create namespace tp-app

namespace/tp-app created

```
2. Créer un ConfigMap dans tp-app avec au minimum :
APP_MESSAGE (string libre).
UPLOAD_ALLOWED_EXT (ex : .txt ).

```
kubectl -n tp-app create configmap tp-config \
                                       --from-literal=APP_MESSAGE="TP Module 10 :)" \
                                       --from-literal=UPLOAD_ALLOWED_EXT=".txt"

configmap/tp-config created

```

3. Créer un Secret dans tp-app avec :
UPLOAD_PASSWORD (mot de passe attendu pour l’upload).

```
kubectl -n tp-app create secret generic tp-secret \
                                       --from-literal=UPLOAD_PASSWORD="passworddefou"

secret/tp-secret created

```
### Application Python
1. Créer un dossier app/ .
OK
2. Créer un fichier requirements.txt avec :
un micro framework HTTP (Flask ou FastAPI),
les libs nécessaires standard (pas de SDK cloud).

[Requirements](./app/requirements.txt)
3. Créer main.py avec :
[main.py](./app/main.py)
Lecture des variables d’environnement :
APP_MESSAGE ,
UPLOAD_ALLOWED_EXT ,
UPLOAD_PASSWORD (depuis les env injectées par le Secret).
Route GET / :
lit le contenu du répertoire /data ,
renvoie la liste des fichiers (au minimum : nom de fichier).
Route POST /upload :
attend un champ password ,
attend un fichier à uploader,
compare password à UPLOAD_PASSWORD ,
si mot de passe OK et extension autorisée → enregistre le fichier
dans /data ,
sinon → renvoie une erreur.
4. Tester l’app en local avec un serveur intégré.
```
export UPLOAD_PASSWORD=passworddefou
                            export APP_MESSAGE="Hello"
                            export UPLOAD_ALLOWED_EXT=".txt"


```
```
pip3 install -r requirements.txt
```

```
 python3 main.py
```

```
curl -X POST -F "password=passworddefou" -F "file=@test.txt" http://127.0.0.1:8000/upload

OK⏎                                                                                                           curl http://10.33.76.196:8000

{"files":["test.txt"],"message":"Hello"}

```
### Conteneurisation et registry
1. Créer un Dockerfile :
image de base Python officielle,
copie de requirements.txt ,
installation des dépendances,
copie de main.py ,
exposition du port de l’app (ex : 8000),
commande de démarrage de l’app.

[Dockerfile](./app/Dockerfile)
2. Builder l’image Docker en local.

```
docker build -t tp-app .

```
3. Tagger l’image pour le registry du cloud :
GCP : Artifact Registry

```
gcloud artifacts repositories create tp-repo \
                                    --repository-format=docker \
                                    --location=europe-west1

Create request issued for: [tp-repo]
Waiting for operation [projects/tp-kube-project/locations/europe-west1/operations/12f8b76f-b70f-4008-ae7d-bfd6dc811eb7] to complete...done.                                                
Created repository [tp-repo].

```

```
docker tag tp-app europe-west1-docker.pkg.dev/tp-kube-project/tp-repo/tp-app:v1

```

```
gcloud auth configure-docker europe-west1-docker.pkg.dev

```
4. Pousser l’image dans le registry choisi.

```
docker push europe-west1-docker.pkg.dev/tp-kube-project/tp-repo/tp-app:v1

The push refers to repository [europe-west1-docker.pkg.dev/tp-kube-project/tp-repo/tp-app]
9f697f371e9b: Pushed 
d1e271c1242a: Pushed 
14de9bddedc2: Pushed 
331c75087496: Pushed 
5fb298eab43b: Pushed 
7276e9419b6d: Pushed 
77f7a48b68e6: Pushed 
c260bc0a2fb0: Pushed 
ab5274a5c04f: Pushed 
4c0d21a7af80: Pushed 
683afd177344: Pushed 
v1: digest: sha256:339f9d993bf667fd64acc3855b5303bd23ca7e5f60810dc3ecce72caeaba06c5 size: 2627

```

### Stockage – PVC RWX
1. Créer dans le namespace tp-app un PVC nommé shared-pvc avec :
mode d’accès : ReadWriteMany ,
taille : 1Gi,
[pv.yaml](./yaml/pv.yaml)
[pvc.yaml](./yaml/pvc.yaml)

```
kubectl apply -f pv.yaml
persistentvolume/shared-pv created

```
```
kubectl apply -f pvc.yaml
persistentvolumeclaim/shared-pvc created

```
2. Vérifier que le PVC passe en état Bound

```
kubectl -n tp-app get pvc
NAME         STATUS   VOLUME      CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
shared-pvc   Bound    shared-pv   1Gi        RWX                           <unset>                 15s

```
### Déploiement de l’application
1. Créer un Deployment dans le namespace tp-app avec :
2 replicas,
container utilisant l’image poussée au registry,
envFrom ou env pour :
injecter le ConfigMap (APP_MESSAGE, UPLOAD_ALLOWED_EXT),
injecter le Secret (UPLOAD_PASSWORD),
volume :
type : persistentVolumeClaim ,
claimName: shared-pvc ,
volumeMounts :
monter le volume sur /data .

[deploy.yaml](./yaml/deploy.yaml)
2. Appliquer le manifeste du Deployment.
```
kubectl apply -f deploy.yaml

deployment.apps/tp-deploy created

```
3. Vérifier que les Pods passent en Running .

```
kubectl  -n tp-app get pods 
NAME                        READY   STATUS    RESTARTS   AGE
tp-deploy-6f9647c8b-d68sr   1/1     Running   0          106s
tp-deploy-6f9647c8b-wwnv9   1/1     Running   0          69s

```

### Exposition de l’application
1. Créer un Service de type LoadBalancer dans tp-app :
cible : les Pods du Deployment,
port externe : 80,
port cible : port de l’app dans le container (ex : 8000).
[service.yaml](./yaml/service.yaml)
2. Appliquer le Service.

```
kubectl apply -f service.yaml

service/tp-service created
```
3. Récupérer l’IP publique du Service.

```
kubectl -n tp-app get svc tp-service

NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
tp-service   LoadBalancer   34.118.229.57   34.14.16.8    80:31411/TCP   2m14s


```
### Tests fonctionnels
1. Appeler GET / sur l’IP publique :
vérifier que la liste des fichiers est vide au départ.
```
curl -v http://34.14.16.8/

*   Trying 34.14.16.8:80...
* Connected to 34.14.16.8 (34.14.16.8) port 80
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 34.14.16.8
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Server: Werkzeug/3.1.3 Python/3.11.14
< Date: Tue, 25 Nov 2025 10:14:05 GMT
< Content-Type: application/json
< Content-Length: 41
< Connection: close
< 
{"files":[],"message":"TP Module 10 :)"}
* shutting down connection #0

```
2. Tester POST /upload :
avec un mauvais password → upload refusé,
avec le bon password (valeur du Secret) et une extension autorisée →
upload accepté.

```
curl -X POST -F "file=@test.txt" -F "password=wrongpass" http://34.14.16.8/upload

Wrong password⏎            
```

```
curl -X POST -F "file=@test.txt" -F "password=passworddefou" http://34.14.16.8/upload

OK⏎                           
```
3. Refaire GET / :
vérifier que le fichier apparaît dans la liste.

```
curl -v http://34.14.16.8/

*   Trying 34.14.16.8:80...
* Connected to 34.14.16.8 (34.14.16.8) port 80
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 34.14.16.8
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Server: Werkzeug/3.1.3 Python/3.11.14
< Date: Tue, 25 Nov 2025 10:35:30 GMT
< Content-Type: application/json
< Content-Length: 76
< Connection: close
< 
{"files":["test.txt"],"message":"TP Module 10 :)"}
* shutting down connection #0

```
### Tests RWX et stateless
1. Vérifier que les 2 Pods du Deployment sont en Running .

```
kubectl -n tp-app get pods

NAME                         READY   STATUS    RESTARTS   AGE
tp-deploy-864cf8f47f-58gjj   1/1     Running   0          3m3s
tp-deploy-864cf8f47f-tffhh   1/1     Running   0          2m57s

```
2. Se connecter en shell sur le premier Pod :
lister les fichiers dans /data .

```
kubectl -n tp-app exec -it tp-deploy-864cf8f47f-58gjj -- ls -l /data

total 20
drwx------ 2 root root 16384 Nov 25 09:46 lost+found
-rw-r--r-- 1 root root    13 Nov 25 10:33 test.txt
-rw-r--r-- 1 root root     0 Nov 25 10:30 test2.txt

```
3. Se connecter sur le deuxième Pod :
vérifier que les mêmes fichiers sont visibles dans /data .

```
kubectl -n tp-app exec -it tp-deploy-864cf8f47f-tffhh -- ls -l /data

total 20
drwx------ 2 root root 16384 Nov 25 09:46 lost+found
-rw-r--r-- 1 root root    13 Nov 25 10:33 test.txt
-rw-r--r-- 1 root root     0 Nov 25 10:30 test2.txt

```
4. Supprimer un des Pods du Deployment.
```
kubectl -n tp-app get pods

NAME                         READY   STATUS    RESTARTS   AGE
tp-deploy-864cf8f47f-58gjj   1/1     Running   0          4m34s
tp-deploy-864cf8f47f-tffhh   1/1     Running   0          4m28s

```
```
kubectl -n tp-app delete pod tp-deploy-864cf8f47f-58gjj
pod "tp-deploy-864cf8f47f-58gjj" deleted

```
5. Vérifier :
le Service continue de répondre via l’autre Pod,
le Pod recréé par le Deployment voit immédiatement les fichiers dans
/data .

```
curl -v http://34.14.16.8/

*   Trying 34.14.16.8:80...
* Connected to 34.14.16.8 (34.14.16.8) port 80
* using HTTP/1.x
> GET / HTTP/1.1
> Host: 34.14.16.8
> User-Agent: curl/8.15.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Server: Werkzeug/3.1.3 Python/3.11.14
< Date: Tue, 25 Nov 2025 10:38:09 GMT
< Content-Type: application/json
< Content-Length: 76
< Connection: close
< 
{"files":["test.txt","lost+found","test2.txt"],"message":"TP Module 10 :)"}
* shutting down connection #0

```

```
kubectl -n tp-app get pods

NAME                         READY   STATUS    RESTARTS   AGE
tp-deploy-864cf8f47f-5hk99   1/1     Running   0          47s
tp-deploy-864cf8f47f-tffhh   1/1     Running   0          5m20s

```

Nouveau pod voit bien les fichiers directement.
```
kubectl -n tp-app exec -it tp-deploy-864cf8f47f-5hk99 -- ls -l /data

total 20
drwx------ 2 root root 16384 Nov 25 09:46 lost+found
-rw-r--r-- 1 root root    13 Nov 25 10:33 test.txt
-rw-r--r-- 1 root root     0 Nov 25 10:30 test2.txt
```
### Nettoyage
1. Dans le namespace tp-app , supprimer :
Deployment,
Service,
PVC,
ConfigMap,
Secret,
namespace tp-app .

```
kubectl -n tp-app delete deployment tp-deploy
                             kubectl -n tp-app delete service tp-service
                             kubectl -n tp-app delete pvc shared-pvc
                             kubectl -n tp-app delete configmap tp-config
                             kubectl -n tp-app delete secret tp-secret
                             kubectl delete namespace tp-app

deployment.apps "tp-deploy" deleted
service "tp-service" deleted
persistentvolumeclaim "shared-pvc" deleted
configmap "tp-config" deleted
secret "tp-secret" deleted
namespace "tp-app" deleted

```
2. Dans le cloud, supprimer :
le cluster Kubernetes managé,
le registry utilisé,
les ressources associées créées uniquement pour le TP (Resource
Group, projet, etc.).

```
gcloud container clusters delete tp-cluster --zone europe-west1-b
The following clusters will be deleted.
 - [tp-cluster] in [europe-west1-b]

Do you want to continue (Y/n)?  y

Deleting cluster tp-cluster...done.                                                                                                                                                        
Deleted [https://container.googleapis.com/v1/projects/tp-kube-project/zones/europe-west1-b/clusters/tp-cluster].

```