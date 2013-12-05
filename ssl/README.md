The SSL certificates stored here are used to start the django application in SSL
mode:

```bash
python manage.py trunserver --ssl-priv-key=ssl/privkey.pem --ssl-cert=ssl/cacert.pem
```

And should not be used for any other purpose. Do not use these in production.

We're adding them to the repository because there is no risk of using these
in any MITM attack.
