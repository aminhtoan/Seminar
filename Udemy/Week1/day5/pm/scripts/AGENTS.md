# Scripts Description

This folder contains lifecycle scripts for local Docker runtime.

## Windows (PowerShell)

- scripts/start.ps1
	- Builds and starts the Docker service in detached mode.
- scripts/stop.ps1
	- Stops and removes service containers.

## macOS/Linux (Bash)

- scripts/start.sh
	- Builds and starts the Docker service in detached mode.
- scripts/stop.sh
	- Stops and removes service containers.

## Expected outcome

- After start: app is reachable at http://localhost:8000
- After stop: containers are stopped and removed
