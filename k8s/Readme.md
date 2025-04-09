start minikube tunnel in a seperate command prompt terminal- minikube tunnel

in another terminal login to the Docker desktop and give the curl, for example: curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d "{\"url\":\"https://playvalorant.com/en-us/news/game-updates/valorant-episode-8-act-2-launches/\"}"

you will get an output like this: {"short_url": "http://localhost:5000/A1B2C3"}
