test -f swagger-codegen-cli.jar || wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar -O swagger-codegen-cli.jar
rm -rf python-flask-server
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python-flask -o python-flask-server
rm -rf server/bb-server
cp -pr python-flask-server server/bb-server
rm -rf typescript-angular2-client
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l typescript-angular2 -o typescript-angular2-client -c client.config.json
sed -i -e 's/models\.Array/Array/' typescript-angular2-client/model/Entities.ts typescript-angular2-client/model/Summary.ts
rm -rf python_client
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python -o python_client -c client.config.json
rm -rf apache2
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l apache2 -o apache2
