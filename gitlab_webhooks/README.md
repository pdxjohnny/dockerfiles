Gitlab Webhooks
---
Python SimpleHTTPServer implementation of a webhook receiver.


On post the server will call the appropriate hook. The push hook
currently builds the the Docker image and pushes them to the registry
specified or the public registry.

```bash
python app.py 9898
```
