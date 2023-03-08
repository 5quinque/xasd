# xasd

```
python3.9 -v venv venv
source venv/bin/activate
pip install -e .
```

```
xasd_downloader

Usage:
    xasd_downloader [--consumers=CONSUMERS] [options]

Options:
    --consumers=CONSUMERS           Number of consumers that will download torrents asynchronously [default: 2]
    --log-level=LEVEL               Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
```

```
xasd_uploader

Usage:
    xasd_uploader watch <dir> [--consumers=CONSUMERS] [--producer=[inotify|amqp]] [options]
    xasd_uploader <path> [options]

Options:
    --consumers=CONSUMERS           Number of consumers that will upload files asynchronously [default: 2]
    --log-level=LEVEL               Set logger level, one of DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
    --producer=[inotify|amqp]       Which producer to use to monitor files to upload [default: inotify]
```

```
uvicorn xasd.api:app --reload --host 0.0.0.0 --port 8000
```

## frontend

see [frontend/README.md](frontend/README.md)

## docker

```bash
docker-compose build
docker-compose up
```