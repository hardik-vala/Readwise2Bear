# Readwise2Bear
Export your Readwise highlights to Bear

## Usage

Run the following commands from the project root.

Build Docker image,

```
docker build -t readwise2bear .
```

Run container in interactive mode,

```
docker run -v "$(pwd):/root/readwise2bear" -it readwise2bear bash
```

Run script inside container,

```
./run.sh
```
