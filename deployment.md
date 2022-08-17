# Deployment instructions

I set this up on a Digital Ocean box. Here are the steps I went through:

## Create a droplet

I created an Ubuntu 22.04 droplet in the SFO2 region, with IPv6 enabled.

## DNS

Go to a registrar, buy a domain, and point the NS records to:

* `ns1.digitalocean.com.`
* `ns2.digitalocean.com.`
* `ns3.digitalocean.com.`

Log into Digital Ocean, go to the Networking tab, and create a zone for this
domain.

Add these DNS records:

* `CNAME` `www` -> `@`
* `A` `@` -> droplet ip
* `AAAA` `@` -> droplet ip
* `CAA` `@` -> `0 issue "letsencrypt.org"`
* `TXT` `@` -> `v=spf1 a -all`
* `TXT` `_dmarc` -> `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s`

## nginx

Install nginx and certbot

```
sudo apt-get install -y nginx
sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Get a TLS cert

```
DOMAIN=postmaster.boats
sudo certbot certonly --nginx --email [my email] --agree-tos --no-eff-email \
 -d $DOMAIN -d www.$DOMAIN
```

Copy the included `infra/nginx.conf` file to `/etc/nginx/nginx.conf`.

```
sudo nginx -s reload
```

## Python apps & dependencies

```
sudo mkdir /var/ctf
```

- Copy the included directory `app` to `/var/ctf/app`

Set up the directory structure and install Python requirements.

```
sudo apt-get install -y python3-pip python3-venv
sudo useradd -r -d /nonexistent -s /usr/sbin/nologin app
sudo bash -c "cd /var/ctf/app && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt"
```

## uwsgi

```
sudo apt-get install -y uwsgi uwsgi-plugin-python3
sudo ln -s ../apps-available/app.ini /etc/uwsgi/apps-enabled/app.ini
```

- Copy the included `infra/uwsgi.ini` to `/etc/uwsgi/apps-available/app.ini`

```
sudo systemctl restart uwsgi
```

# Postfix

```
sudo DEBIAN_PRIORITY=low apt-get install -y postfix
```

Enter these answers at the interactive prompts:
- General type of mail configuration: Internet Site
- System mail name: `postmaster.boats`
- Root and postmaster mail recipient: (empty)
- Other destinations to accept mail for: `postmaster.boats, localhost`
- Force synchronous updates on mail queue?: No
- Local networks: (default)
- Mailbox size limit: `0`
- Local address extension character: `+`
- Internet protocols to use: all
