# Home Assignment Algocell
## Development process, and what can be added
## Why docker
## Running Instructions
For both instructions docker needs to be installed. You can install it from [here](https://www.docker.com/products/docker-desktop/)
### To develop (from source code)
1. * If git is installed, run ```git clone https://github.com/bar2011/Algocell-home-assignment```
	* If git isn't installed, simply download the source code and extract the zip file
2. Run the command ```pip install huggingface-hub```
3. While inside the source code direcory run the command ```huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir .```
4. Open the [docker-compose.yml](./docker-compose.yml) file inside the directory which was created, and uncomment all lines saved for development and comment all lines saved for release.
5. On the same directory as before, run the command ```docker-compose up```
6. Open the [website](http://localhost:8501)
### To test (without source code)
1. Paste the contents of [docker-compose.yml](./docker-compose.yml) to a file a file with the same name.
2. While in the directory you pasted the file into, run the command ```docker-compose up```
3. Open the [website](http://localhost:8501)
