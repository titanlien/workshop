# helmfile-poc
Verify its values setting by `write-values`

```bash
$ helmfile -e asia write-values
$ cat helmfile-7325dc62/mao-asia.yaml
db_cret: I_am_base_cert
image:
  tag: asia
podAnnotations:
  zone: asia
```

```bash
$ helmfile -e taiwan write-values
$ cat helmfile-7325dc62/mao-taiwan.yaml
db_cert: Taiwan_SSL
db_cret: I_am_base_cert
image:
  tag: taiwan
podAnnotations:
  zone: asia
```
