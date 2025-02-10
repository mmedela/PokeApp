# Pokémon Search App

This project is a web application that allows users to search for Pokémon using the PokéAPI. The frontend is built with HTMX and Tailwind CSS, while the backend is powered by Flask. Advanced search filters are also included to refine searches based on attributes like generation, attack type, and weight range.

## Prerequisites
This guide assumes that **Docker** and **Python** are already installed on your machine. If not, please install it before proceeding.

## Building and Running the Application

1. **Clone the repository** (if you haven't already):
   ```sh
   git clone https://github.com/your-repo/pokemon-search-app.git
   cd pokemon-search-app
   ```

2. **Build the Docker container**:
   ```sh
   docker build -t pokemon-search-app .
   ```

3. **Run the container**:
   ```sh
   docker run -p 5000:5000 pokemon-search-app
   ```

4. **Access the application**:
   Open a browser and go to:
   ```
   http://localhost:5000
   ```

## Stopping the Container
To stop the running container, first find its ID with:
```sh
docker ps
```
Then, stop it using:
```sh
docker stop <container_id>
```

## Removing the Container (if needed)
If you want to remove the container completely, find its ID with `docker ps -a` and then run:
```sh
docker rm <container_id>
```

For any updates, rebuild the image and restart the container using the steps above.

