docker exec -it flask_flask_1 bash
docker exec -it flask_flask_1 python train_model.py

docker-compose up
docker-compose up --build

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"33,4,5,6"}' \
  http://localhost:5000/iris_post