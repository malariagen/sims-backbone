Install helm plugins
====================

````
    helm plugin install https://github.com/futuresimple/helm-secrets
    helm plugin install https://github.com/databus23/helm-diff --version master
````

Log in to your google account and set defaults
==============================================

Use your account details instead

````
    gcloud config set account googlecloud@malariagen.net
    gcloud auth login
    gcloud auth application-default login

    gcloud config set compute/zone europe-west1-b
    gcloud config set compute/region europe-west1
    gcloud config set project malariagen-sims
    #Don't need the --zone and --project because of the above
    gcloud container clusters get-credentials sims --zone europe-west1-b --project malariagen-sims
````

Check permissions
=================

````
    gcloud kms keyrings list --location global --project malariagen-sims
    gcloud kms keys list --location global --keyring malariagen-sims-keyring --project malariagen-sims

````
````
    helm secrets view sims/secrets.yaml
````

Running locally with microk8s
=========================

The main thing you'll need is a load balancer - install metallb and configure
````
    kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.7.3/manifests/metallb.yaml
    kubectl apply -f metallb.yaml
````

Using the dashboard
Get the IP via:

````
    kubectl get svc -n kube-system
````

then get the token using:

````
    kubectl describe secret kubernetes-dashboard --namespace=kube-system
````

Install or upgrade
==================

See the deploy script for how to run install or upgrade

## other useful hints
````
    --recreate-pods can be used as an argument to upgrade
````

Running commands on the pods
============================

find out the deployment pod name:

````
    kubectl --namespace sims-test get pod

````
