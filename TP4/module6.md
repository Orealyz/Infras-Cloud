4. TP guidé
Objectif global du TP
Déployer une application fictive “StudentAPI” dans un namespace dédié :
- Un frontend configuré par ConfigMap.
- Un backend utilisant un Secret pour ses credentials.
- Un ServiceAccount dédié pour le backend, relié à un Role RBAC.
L’application sera simulée par des conteneurs busybox qui affichent leurs
variables d’environnement, ce qui suffit pour vérifier l’injection.
É
Module 6 : Configuration & Secrets Kubernetes
8
Étape 1 — Créer un namespace dédié à l’application
Créer un namespace nommé studentapi .
Vérifier qu’il apparaît dans la liste des namespaces du cluster.
Tous les objets du TP doivent être créés dans ce namespace.
Étape 2 — Créer le ConfigMap du frontend
Créer un fichier nommé frontend-config.yaml contenant un ConfigMap dans le
namespace studentapi avec les clés suivantes :
WELCOME_MSG
 = "Bienvenue sur StudentAPI"
ITEMS_PER_PAGE
 = "20"
Appliquer ce fichier et vérifier que le ConfigMap existe et contient bien ces
deux clés.
Étape 3 — Créer le Secret du backend
Créer un fichier db-secret.yaml contenant un Secret de type Opaque dans studentapi ,
avec les clés suivantes (au format stringData ) :
DB_USER
 = studentapi
DB_PASSWORD
 = SuperSecret
Appliquer le fichier et vérifier que le Secret existe.
Vérifier que les données ne sont pas affichées en clair dans la description du
Secret.
Étape 4 — Créer le ServiceAccount utilisé par le
backend
Créer un fichier backend-sa.yaml contenant un ServiceAccount nommé backend-sa
dans studentapi .
Appliquer ce fichier, puis vérifier que le SA apparaît dans la liste.
Étape 5 — Déclarer un Role + RoleBinding
permettant au SA de lire le Secret
Module 6 : Configuration & Secrets Kubernetes
 9
Créer un fichier rbac-backend.yaml contenant deux objets :
1. Role nommé db-secret-reader autorisant l’accès get sur le Secret db-secret .
2. RoleBinding nommant le ServiceAccount backend-sa comme sujet de ce
Role.
Appliquer le fichier.
Tester que backend-sa a bien la permission de lire uniquement ce Secret.
Étape 6 — Déployer le backend consommant le
Secret
Créer un fichier backend-deployment.yaml contenant un Deployment avec les
caractéristiques suivantes :
nom : backend
namespace : studentapi
replica : 1
label : app: backend
ServiceAccount utilisé : backend-sa
image du conteneur : busybox:1.36
commande d’exécution affichant les variables d’environnement DB_USER et
DB_PASSWORD , puis dormant
variables d’environnement injectées depuis le Secret db-secret
Appliquer ce fichier.
Vérifier que le Pod est en état Running et que les logs affichent correctement les
deux variables.
Étape 7 — Déployer le frontend consommant le
ConfigMap
Créer un fichier frontend-deployment.yaml contenant un Deployment avec les
caractéristiques suivantes :
nom : frontend
namespace : studentapi
Module 6 : Configuration & Secrets Kubernetes
 10
replica : 1
label : app: frontend
image : busybox:1.36
aucune utilisation de ServiceAccount (désactivation via
automountServiceAccountToken: false )
injection des variables via envFrom pointant vers le ConfigMap frontend-config
commande d’exécution affichant les clés WELCOME_MSG et ITEMS_PER_PAGE ,
puis dormant
Appliquer ce fichier.
Vérifier que le Pod fonctionne et que les logs affichent les deux valeurs du
ConfigMap.
Étape 8 — Tester la propagation de modifications
du ConfigMap
Modifier la valeur WELCOME_MSG dans le fichier frontend-config.yaml , par exemple :
"Bienvenue sur StudentAPI (v2)"
Réappliquer le ConfigMap.
Redémarrer le Deployment frontend .