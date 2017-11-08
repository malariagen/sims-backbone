#test -f swagger-codegen-cli.jar || wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar -O swagger-codegen-cli.jar
test -f swagger-codegen-cli.jar || wget https://oss.sonatype.org/content/repositories/snapshots/io/swagger/swagger-codegen-cli/3.0.0-SNAPSHOT/swagger-codegen-cli-3.0.0-20171009.075709-6.jar -O swagger-codegen-cli.jar
if [ "$1" = "server" -o "$1" = "" ]
then
    rm -rf python-flask-server
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python-flask -o python-flask-server
    rm -rf server/bb_server
    cp -pr python-flask-server server/bb_server
fi
if [ "$1" = "client" -o "$1" = "" ]
then
    rm -rf typescript-angular-client
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l typescript-angular -o typescript-angular-client -c client.config.json
    rm -rf python_client
    java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python -o python_client -c client.config.json
fi
rm -rf apache2
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l apache2 -o apache2
