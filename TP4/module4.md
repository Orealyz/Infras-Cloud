kubectl create namespace module4

namespace/module4 created

kubectl config set-context --current --namespace=module4
Context "minikube" modified.





Étape 1 — Créer un Pod “nu”
Créer un fichier manifest nommé pod-demo.yaml décrivant un Pod unique avec les
caractéristiques suivantes :
nom : demo-pod
label : app: demo
image : nginx:1.25
port exposé dans le conteneur : 80
politique de redémarrage : Always
Appliquer ce manifest.
Vérifier que le Pod apparaît, puis afficher ses détails.
Supprimer ensuite ce Pod et vérifier qu’il n’est pas recréé, ce qui démontre
l’absence de contrôleur.

kubectl apply -f pod-demo.yaml

pod/demo-pod created

Étape 2 — Déployer une application web via un
Deployment
Créer un fichier deployment-web.yaml décrivant un Deployment avec les
caractéristiques suivantes :
nom : web-demo
nombre de replicas : 3
selector basé sur le label : app: web-demo
template utilisant l’image : nginx:1.25
port du conteneur : 80
Appliquer le manifest.
Vérifier :
que le Deployment est présent,
qu’un ReplicaSet a été généré automatiquement,
que trois Pods sont créés et en cours d’exécution.
Supprimer un des Pods et observer que le ReplicaSet en crée
immédiatement un nouveau.

kubectl apply -f deployment-web.yaml

deployment.apps/web-demo created
kubectl get deployments

NAME       READY   UP-TO-DATE   AVAILABLE   AGE
web-demo   3/3     3            3           5s
kubectl get replicasets

NAME                  DESIRED   CURRENT   READY   AGE
web-demo-6bdfd9dd44   3         3         3       8s
kubectl get pods

NAME                        READY   STATUS    RESTARTS   AGE
web-demo-6bdfd9dd44-c5rzx   1/1     Running   0          11s
web-demo-6bdfd9dd44-qdft8   1/1     Running   0          11s
web-demo-6bdfd9dd44-znkd6   1/1     Running   0          11s

kubectl delete pod web-demo-6bdfd9dd44-c5rzx 
pod "web-demo-6bdfd9dd44-c5rzx" deleted
kubectl get pods -w

NAME                        READY   STATUS    RESTARTS   AGE
web-demo-6bdfd9dd44-qdft8   1/1     Running   0          2m6s
web-demo-6bdfd9dd44-sw7b8   1/1     Running   0          4s
web-demo-6bdfd9dd44-znkd6   1/1     Running   0          2m6s

Étape 3 — Modifier dynamiquement le nombre de
Pods
Augmenter le nombre de replicas du Deployment web-demo à 5.
Vérifier que deux Pods supplémentaires apparaissent.
Remettre ensuite le nombre de replicas à 2.
Observer que Kubernetes supprime automatiquement les Pods excédentaires.

kubectl get pods -w

NAME                        READY   STATUS    RESTARTS   AGE
web-demo-6bdfd9dd44-6787g   1/1     Running   0          2s
web-demo-6bdfd9dd44-gqhr5   1/1     Running   0          2s
web-demo-6bdfd9dd44-qdft8   1/1     Running   0          3m38s
web-demo-6bdfd9dd44-sw7b8   1/1     Running   0          96s
web-demo-6bdfd9dd44-znkd6   1/1     Running   0          3m38s

kubectl apply -f deployment-web.yaml

deployment.apps/web-demo configured


kubectl get pods -w

NAME                        READY   STATUS    RESTARTS   AGE
web-demo-6bdfd9dd44-qdft8   1/1     Running   0          4m17s
web-demo-6bdfd9dd44-znkd6   1/1     Running   0          4m17s

Étape 4 — Effectuer un rolling update de
l’application
Mettre à jour le Deployment web-demo pour remplacer l’image nginx:1.25 par
nginx:1.26 .
Suivre la progression du déploiement jusqu’à son achèvement.
Pendant la mise à jour, observer :
l’apparition d’un nouveau ReplicaSet,
la création progressive des Pods en version 1.26,
la suppression progressive des Pods en 1.25.
Vérifier qu’au final, tous les Pods utilisent bien la nouvelle version de
l’image.

kubectl apply -f deployment-web.yaml

deployment.apps/web-demo configured


 kubectl describe deployment web-demo
Name:                   web-demo
Namespace:              module4
CreationTimestamp:      Mon, 24 Nov 2025 11:21:22 +0100
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               app=web-demo
Replicas:               2 desired | 1 updated | 3 total | 2 available | 1 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=web-demo
  Containers:
   nginx:
    Image:         nginx:1.26
    Port:          80/TCP
    Host Port:     0/TCP
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  web-demo-6bdfd9dd44 (2/2 replicas created)
NewReplicaSet:   web-demo-7df87f8bd7 (1/1 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  7m27s  deployment-controller  Scaled up replica set web-demo-6bdfd9dd44 from 0 to 3
  Normal  ScalingReplicaSet  3m51s  deployment-controller  Scaled up replica set web-demo-6bdfd9dd44 from 3 to 5
  Normal  ScalingReplicaSet  3m11s  deployment-controller  Scaled down replica set web-demo-6bdfd9dd44 from 5 to 2
  Normal  ScalingReplicaSet  6s     deployment-controller  Scaled up replica set web-demo-7df87f8bd7 from 0 to 1

kubectl rollout status deployment/web-demo
deployment "web-demo" successfully rolled out



Étape 5 — Déployer un DaemonSet
Créer un fichier daemonset-node-info.yaml décrivant un DaemonSet avec les
caractéristiques suivantes :
nom : node-info
label : app: node-info
image utilisée : busybox:1.36
exécution d’un script affichant régulièrement un message incluant le
hostname du nœud
(boucle infinie avec un sleep 30 entre chaque affichage)
Appliquer le manifest.
Vérifier :
que le DaemonSet est présent,
qu’un Pod est créé sur chaque nœud du cluster,
que les logs indiquent bien le hostname associé.

kubectl apply -f daemonset-node-info.yaml
daemonset.apps/node-info created

 kubectl get daemonsets
                          kubectl get pods -o wide
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
node-info   1         1         1       1            1           <none>          25s
NAME                        READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
node-info-s7hf9             1/1     Running   0          25s     10.244.0.12   minikube   <none>           <none>
web-demo-7df87f8bd7-9zhht   1/1     Running   0          5m2s    10.244.0.11   minikube   <none>           <none>
web-demo-7df87f8bd7-bp6tx   1/1     Running   0          5m11s   10.244.0.10   minikube   <none>           <none>

kubectl logs node-info-s7hf9
Hello from node-info-s7hf9
Hello from node-info-s7hf9
Hello from node-info-s7hf9


Étape 6 — Exécuter un Job “one-shot”
Créer un fichier job-pi.yaml décrivant un Job avec les caractéristiques suivantes :
nom : compute-pi
conteneur utilisant l’image perl:5.34.0
exécution d’un calcul de π avec une précision d’environ 50 chiffres
restartPolicy
 configuré à Never
backoffLimit
 fixé à 4
Appliquer le manifest.
Vérifier que le Job passe en fin d’exécution ( Completed ).
Afficher les logs pour vérifier la sortie du programme.

kubectl apply -f job-pi.yaml

job.batch/compute-pi created

kubectl get jobs

NAME         STATUS     COMPLETIONS   DURATION   AGE
compute-pi   Complete   1/1           23s        24s
kubectl logs job/compute-pi
3.1415926535897932384626433832795028841971693993751

Étape 7 — Planifier une tâche périodique via un
CronJob
Créer un fichier cronjob-hello.yaml décrivant un CronJob avec les caractéristiques
suivantes :
nom : hello-every-minute
planification : une exécution par minute
politique de concurrence : Forbid
historique conservé : 3 succès, 1 échec
utilisation de l’image busybox:1.36
exécution affichant la date suivie du message "Hello from CronJob"
Appliquer le manifest et attendre quelques minutes.
Observer la création successive de Jobs et de Pods associés.
Afficher les logs de l’un des Pods pour vérifier la sortie du script.

ubectl get cronjobs
NAME                 SCHEDULE    TIMEZONE   SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello-every-minute   * * * * *   <none>     False     0        <none>          3s
kubectl get jobs -w

NAME                          STATUS     COMPLETIONS   DURATION   AGE
compute-pi                    Complete   1/1           23s        20m
hello-every-minute-29399696   Complete   1/1           3s         2m37s
hello-every-minute-29399697   Complete   1/1           4s         97s
hello-every-minute-29399698   Complete   1/1           3s         37s

kubectl logs job/compute-pi
3.1415926535897932384626433832795028841971693993751


Étape 8 — Nettoyer toutes les ressources du TP
Supprimer successivement les ressources suivantes dans le namespace :
le CronJob hello-every-minute
le Job compute-pi
le DaemonSet node-info
le Deployment web-demo
éventuellement le Pod demo-pod s’il existe encore
Vérifier que le namespace ne contient plus aucune ressource liée au TP.

kubectl delete cronjob hello-every-minute
                              kubectl delete job compute-pi
                              kubectl delete daemonset node-info
                              kubectl delete deployment web-demo
                              kubectl delete pod demo-pod
                              kubectl get all

cronjob.batch "hello-every-minute" deleted
job.batch "compute-pi" deleted
daemonset.apps "node-info" deleted
deployment.apps "web-demo" deleted
Error from server (NotFound): pods "demo-pod" not found
NAME                            READY   STATUS        RESTARTS   AGE
pod/node-info-s7hf9             1/1     Terminating   0          25m
pod/web-demo-7df87f8bd7-9zhht   1/1     Terminating   0          30m
pod/web-demo-7df87f8bd7-bp6tx   1/1     Terminating   0          30m
