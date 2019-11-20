DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
set -o allexport
source ${DIR}/../.envs/.local/.postgres
set +o allexport
export POSTGRES_HOST=localhost
pg_dump -U ${POSTGRES_USER} -h ${POSTGRES_HOST} backbone_service -s --no-owner -c > backbone_service.psql
