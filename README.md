# Home Assignment Algocell
## Approach
I built this assignment piece by piece, in the order of complexity (and of course some parts were built on other).

I started with reading the streamlit documentation.
It contained a section about integration with Docker, so some of the Dockerfile is simply taken from there (of course after copy-pasting I removed parts which weren't needed).<br>
After that I created the docker-compose.yml file for two reasons:
1. Convenience - it's much easier to type ```docker-compose up``` than remembering a more complex command.
2. Development - using docker compose gave me the tools to change the parameters so that the container will automatically update as I type into the python files, which made it much easier and shorter process than to build a container every time I tested the app.

Then I read some of the LangChain documentation, its capabilities, and what free LLM models I could use. I chose Llama-2-7b because it was free to download, didn't have a waitlist, and wasn't too large in size (around 4GB). I started with a simple prompt template without any kind of implementation of the RAG method, and I got it to answer questions which I hardcoded into the program.

After I got that to work, I created the base UI (only the chat part, because I wasn't ready yet for the file uploading) mainly from the documentation.

Than I simply connected the two parts, and linked what I wrote to the LLM model.

After that, I created the system to upload PDF files, and extract text out of them.

Then I read about RAG some more (I read about it from the start, just to have a basic understanding of what it is), and implemented another template just for the data, which I added to the messages list (without displaying it to the user). I gave the LLM all the previous messages including the data, and by doing that I tried to achieve both understanding of the data, and understanding of the conversation context.

I moved to tweaking the prompt template **a lot**, and at some point I decided to merge the data and question prompt templates into one, and remove the previous messages because it seemed to confuse the LLM. I wasn't able to get to good results, but I'll talk about that in the next section.

After I got to a point I was somewhat okay with, I created error handling both for the LLM and for the file uploading.

A bit more little tweaks, and that was the finish.
## Challenges
* Almost my whole git history was removed: until a pretty advanced part of the development, I loaded the binaries to the container by simply copying it from my system. When I tried to move the assignment to GitHub, I faced the problem that GitHub will accept files only up to 100 MiB (2GB with special software, but still not enough), and the model file was already added to my git history. When trying to delete it from my history using a command, I managed to delete **all** the files from **all** the previous commits. Thankfully, I copied the files into another folder before running the command (it stated in the documentation that it was dangerous), I forgot to copy the .git folder, because I hadn't turned on hidden files in Finder. So my whole git history was removed up to that point.
* I couldn't create a working prompt: because I had to use a free LLM, and I had to ran it locally (I tried using free APIs like OpenLLM and AwanLLM but all of either required API keys connected to my hugging face account, or weren't compatible with LangChain), the LLM I chose isn't very good (to say the least). Despite trying multiple times, with multiple templating techniques, none worked, so I simply chose the best one (which at least most of the time worked at getting information from the data), which wasn't good at all.
## Improvments that can be made
Sorted by importance:
1. Using a better LLM - no need for explanation. Llama-2-7b just isn't very good at handling complex prompts
2. Creating a better prompt template.
3. Inputting previous messages into the LLM, so that it can understand context.
4. Creating a custom callback handler, which is a class in LangChain which has functions which run every time the LLM completes a certain task. Creating a custom one will give the possibility of writing the LLM's message token after token, and not the whole message at once. This will improve the UX by making the user wait less time and by giving him the possibility to read as the LLM replies.

Of course there are many more, but those are some of the more important ones in my opinion.
## Docker
### Why use Docker
The short answer is that Docker solves one of the most frustrating problem developers face: when you run code that you know should work, but because of your OS or settings which you don't have time to change, it doesn't work on your machine.<br>
Docker does that by moving all of an app's code into a container, which creates an environment that can be replicated in almost 100% accuracy, regardless of the machine used.<br>
There are many more advantages to using Docker to run programs over the regular way of running programs, here are some of them:
* Docker makes it **really** easy to share code. First of all, instead of downloading the whole source code of an application, all of the software needed for it in the correct versions, you can just ask the developer to upload his app to the Docker Hub, and run it with one (most of the time not-so-long) command in the terminal.
* Docker also makes it easy to run code that is outdated. If you wrote code a couple of years ago, than that code is probably outdated, and contains features not fully supported or not supported at all. Without Docker, you would've had to reinstall the correct versions of all the software needed to run the app, and troubleshoot program conflicts with other apps which the software you reinstalled depended upon, and It's basically just a big headache. With Docker, since all the code is in its own container, which isn't connected to any of your computer, all the software in the container stayed on the same version, so you can just run one command and your app will run without any conflicts.
* For more complex apps, which use both a backend and a frontend, and maybe a database or two, you'll usually need more than one command to run the app. Docker has a lot of tools for situations like this (e.g. ```docker-compose```), which make it possible to run the whole app with just one command (e.g. ```docker-compose up```)
### Explanation of [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml)
####  [Dockerfile](./Dockerfile):
1. The first line specifies the base image the model should use. I chose ```python:3.12-slim``` mainly for convenience: choosing a lower level base image (such as ```alpine```, a very popular base image) would require installing python manually.
2. The next two lines copy all of the files in this directory into the directory ```/app``` in the container (excluding all files listed in [.dockerignore]())
3. Then there is the dependencies installation: first the essentials for downloading the ```llama-cpp-python``` python library, and then all of the python libraries listed in [requirements.txt](./requirements.txt).
4. After that, Docker downloads the binaries of the LLM model Llama-2 into the container via ```huggingface-cli```
5. Next, Docker exposes the port 8501, which is the default port for all ```streamlit``` apps.
6. The next line defines a health check that sends a request to ```streamlit``` health endpoint to ensure the application is running.
7. The last line specifies the command used to run the app.<br>

The commands used in this file are:
* FROM - used to specify a base image
* WORKDIR - used to specify the directory in which all commands will be run from
* COPY - used to copy files from the system to the container
* RUN - used to run a command at the path specified using WORKDIR (defaults to /)
* EXPOSE - used to expose a container port to the system
* HEALTHCHECK CMD - used to specify a command to check if the container is running
* ENTRYPOINT - used to specify the command to fully run the app<br>
#### [docker-compose.yml](./docker-compose.yml):
1. The first two lines define a service (in this case container) named web, which is the container containing this application
2. The next line either specifies the image we want to use to run the application, or (if you're developing) specifying to build the container from the current directory
3. Then, there is the same command written in the last line of the [Dockerfile](./Dockerfile), which we use to start this app
4. We specify that we want the port we exposed in the [Dockerfile](./Dockerfile) (port 8501) is mapped to the port 8501 in your system
5. If you uncommented the lines for development, there are another two lines, which say that we want to save our app folder, so that if you'll run this app multiple times, and while you ran the app you somehow generated new files in the ```/app``` folder, these files will be saved and not deleted with your container.
## Running Instructions
For both instructions docker needs to be installed. You can install it from [here](https://www.docker.com/products/docker-desktop/)
### To develop (from source code)
1. * If git is installed, run ```git clone https://github.com/bar2011/Algocell-home-assignment```
	* If git isn't installed, simply download the source code and extract the zip file
2. Run the command ```pip install huggingface-hub```
3. While inside the source code direcory run the command ```huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir .```
4. Open the [docker-compose.yml](./docker-compose.yml) file inside the directory which was created, and uncomment all lines saved for development and comment all lines saved for release.
5. Open the [Dockerfile](./Dockerfile) inside the same directory, uncomment and comment as mentioned in the last instruction. Also coommnet line with ```RUN huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf --local-dir .```
5. On the same directory as before, run the command ```docker-compose up```
6. Open the [website](http://localhost:8501)
### To test (without source code)
1. Paste the contents of [docker-compose.yml](./docker-compose.yml) to a file a file with the same name.
2. While in the directory you pasted the file into, run the command ```docker-compose up```
3. Open the [website](http://localhost:8501)
