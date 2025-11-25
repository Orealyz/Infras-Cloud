4. TP guidé
TP : Déployer une mini‑boutique et la connecter au réseau Kubernetes
Objectif global :
Déployer une application simple frontend + api + db .
Mettre en place les Services internes et l’Ingress.
Isoler la base via une NetworkPolicy.
Étape 0 — Installer un Ingress Controller local
Installer un Ingress Controller sur Minikube ou kind, selon l’environnement
utilisé.
Vérifier ensuite que le namespace ingress-nginx existe et que les Pods du
contrôleur sont en état Running .
Vérifier également que le Service associé expose bien un point d’entrée.

minikube addons enable ingress
💡  ingress est un addon maintenu par Kubernetes. Pour toute question, contactez minikube sur GitHub.
Vous pouvez consulter la liste des mainteneurs de minikube sur : https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ Utilisation de l'image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.4
    ▪ Utilisation de l'image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.4
    ▪ Utilisation de l'image registry.k8s.io/ingress-nginx/controller:v1.11.3
🔎  Vérification du module ingress...
🌟  Le module 'ingress' est activé

kubectl get pods -n ingress-nginx
                          kubectl get svc -n ingress-nginx
NAME                                        READY   STATUS      RESTARTS   AGE
ingress-nginx-admission-create-4dh2q        0/1     Completed   0          78s
ingress-nginx-admission-patch-5tm4k         0/1     Completed   1          78s
ingress-nginx-controller-56d7c84fd4-2wfnx   1/1     Running     0          78s
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             NodePort    10.108.226.230   <none>        80:32690/TCP,443:31123/TCP   78s
ingress-nginx-controller-admission   ClusterIP   10.97.55.228     <none>        443/TCP                      78s

Étape 1 — Créer un namespace dédié au projet
Créer un namespace nommé shop .
Configurer le contexte Kubernetes courant pour qu’il utilise automatiquement
ce namespace.
Vérifier qu’il apparaît bien dans la liste des namespaces.
kubectl create namespace shop
namespace/shop created
kubectl config set-context --current --namespace=shop
Context "minikube" modified.
kubectl get ns
NAME              STATUS   AGE
default           Active   176m
ingress-nginx     Active   105s
kube-node-lease   Active   176m
kube-public       Active   176m
kube-system       Active   176m
module4           Active   176m
shop              Active   7s

Étape 2 — Déployer les trois composants de
l’application
2.1 — Déploiement frontend
Module 5 – Networking Kubernetes
 11
Créer un fichier frontend-deploy.yaml contenant un Deployment configuré avec les
caractéristiques suivantes :
namespace : shop
nom : frontend
nombre de replicas : 2
label : app: frontend
image : nginx:1.27
conteneur exposant le port 80
Appliquer le fichier et vérifier que les deux Pods fonctionnent.
kubectl apply -f frontend-deploy.yaml

deployment.apps/frontend created


kubectl get pods -l app=frontend

NAME                        READY   STATUS    RESTARTS   AGE
frontend-7f9f97454b-7ntv5   1/1     Running   0          7s
frontend-7f9f97454b-psfpp   1/1     Running   0          7s

2.2 — Déploiement API
Créer un fichier api-deploy.yaml décrivant un Deployment dans shop :
nom : api
replicas : 2
label : app: api
image : hashicorp/http-echo:0.2.3
arguments du conteneur :
text=hello-from-api
listen=:8000
port exposé : 8000
Appliquer le fichier et vérifier la présence des Pods.

kubectl apply -f api-deploy.yaml

deployment.apps/api created
kubectl get pods -l app=api

NAME                   READY   STATUS    RESTARTS   AGE
api-84b84c597d-2s66g   1/1     Running   0          7s
api-84b84c597d-k48qk   1/1     Running   0          7s

2.3 — Déploiement base de données
Créer un fichier db-deploy.yaml décrivant un Deployment PostgreSQL dans shop :
nom : db
replicas : 1
label : app: db
image : postgres:16
variables d'environnement :
POSTGRES_PASSWORD = example
POSTGRES_DB = shop
port exposé : 5432
Appliquer et vérifier que le Pod est en cours d’exécution.

kubectl apply -f db-deploy.yaml 

deployment.apps/db created
kubectl get pods -l app=db

NAME                 READY   STATUS    RESTARTS   AGE
db-97b7db6bb-jhtgk   1/1     Running   0          15s
db-97b7db6bb-kqf77   1/1     Running   0          15s

Étape 3 — Créer les Services internes
Créer un fichier services.yaml contenant trois Services ClusterIP dans le
namespace shop :
1. frontend-svc
selector : app: frontend
port : 80
2. api-svc
selector : app: api
port : 8000
3. db-svc
selector : app: db
port : 5432
Appliquer le fichier.
Vérifier que chaque Service possède une adresse CLUSTER-IP et des Endpoints
cohérents.

kubectl apply -f services.yaml
service/frontend-svc created
service/api-svc created
service/db-svc created
kubectl get svc -n shop
NAME           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
api-svc        ClusterIP   10.102.57.74    <none>        8000/TCP   4s
db-svc         ClusterIP   10.106.28.178   <none>        5432/TCP   4s
frontend-svc   ClusterIP   10.111.11.141   <none>        80/TCP     4s

Étape 4 — Tester la découverte DNS et la
communication interne
Créer un Pod temporaire de test basé sur l’image busybox:1.28 .
Depuis ce Pod :
afficher la configuration DNS,
vérifier la résolution des noms : api-svc et db-svc ,
effectuer un appel HTTP vers : http://api-svc:8000 ,
vérifier que la réponse contient le texte hello-from-api.

Supprimer ensuite le Pod de test.

kubectl run testpod --rm -i --tty --image=busybox:1.28 -- /bin/sh

If you don't see a command prompt, try pressing enter.
/ # nslookup api-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      api-svc
Address 1: 10.102.57.74 api-svc.shop.svc.cluster.local
/ # nslookup db-svc
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      db-svc
Address 1: 10.106.28.178 db-svc.shop.svc.cluster.local
/ # wget -qO- http://api-svc:8000
hello-from-api

Étape 5 — Créer et configurer l’Ingress
Créer un fichier ingress-shop.yaml contenant un Ingress dans le namespace shop
répondant aux caractéristiques suivantes :
nom : shop-ingress
hôte attendu : shop.local
deux chemins configurés :
/
 → Service frontend-svc, port 80
/api
 → Service api-svc, port 8000
annotation permettant de réécrire les chemins (pour NGINX) :
nginx.ingress.kubernetes.io/rewrite-target: "/"
Appliquer l’Ingress.
Vérifier qu’il est bien enregistré et que l’Ingress Controller l’a pris en charge.
Récupérer l’adresse IP du point d’entrée :
sous Minikube, utiliser l’adresse retournée par Minikube ;
sous kind, utiliser l’adresse du Service ingress-nginx-controller ou le port
forwarding prévu.
Ajouter une entrée dans ton fichier hosts local mappant :
<IP_INGRESS> shop.local
Tester ensuite depuis ta machine :
http://shop.local/
http://shop.local/api

 kubectl apply -f ingress-shop.yaml

ingress.networking.k8s.io/shop-ingress created
kubectl get ingress -n shop

NAME           CLASS   HOSTS        ADDRESS   PORTS   AGE
shop-ingress   nginx   shop.local             80      4s

curl http://shop.local/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
curl http://shop.local/api
hello-from-api

Étape 6 — Appliquer une NetworkPolicy pour isoler
la base
Créer un fichier np-db-allow-api.yaml contenant une NetworkPolicy limitant l’accès
au Pod PostgreSQL :
namespace : shop
nom : allow-api-to-db
cible protégée : tous les Pods portant app: db
type de règle : Ingress
seule source autorisée : les Pods portant app: api
port autorisé : 5432 en TCP
Appliquer la NetworkPolicy.
Tester l’accès réseau depuis :
un Pod api → la connexion vers db-svc:5432 doit réussir,
un Pod frontend → la connexion doit échouer.