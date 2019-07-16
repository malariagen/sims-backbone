#microk8s.enable registry
for i in production-nginx:latest production-backbone-server:latest production-import:latest malariagen/sims-postgres:latest
do
docker tag $i localhost:32000/$i
docker push localhost:32000/$i
done
