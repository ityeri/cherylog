# When local testing, you can use this script to make test database container
# It is compatible with .env.example

podman run -d \
  --name cherylog-test-db \
  -e POSTGRES_DB=cherylog_test_db \
  -e POSTGRES_USER=cherylog \
  -e POSTGRES_PASSWORD=wasans \
  -p 5432:5432 \
  docker.io/library/postgres:16