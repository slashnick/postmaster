# Postmaster

## Public Description

Flag: `ASV{y0U_hAd_Me_@_EHLO}`

Now introducing: email-based flag delivery.

https://postmaster.boats/

(CTFd note: that site serves its own source code, no need to upload any files to CTFd)

## Design

This challenge is a website running a Postfix email server. Users can attempt to
send themselves the flag by submitting their name and email.

But there's a catch: the server only sends you the flag if the email address you
enter is `admin@email.invalid`.

For example, if I submit `Frosty` and `frosty@frosty.style`, I'll get an email
like this:

```
From: postmaster.boats <noreply@postmaster.boats>
To: Frosty <frosty@frosty.style>
Subject: Sorry, try again

No flag for you :(
```

## Walkthrough

You can inject additional To addresses into the email using the name field.

Let's say your email address is `user@example.com`. Submit
`me <user@example.com>, admin` as your name, and `admin@email.invalid` as your
email. You'll get an email with the flag (check spam if you don't see it).

**Why?**

With the inputs above, the email headers look something like this:

```
From: postmaster.boats <noreply@postmaster.boats>
To: me <user@example.com>, admin <admin@email.invalid>
Subject: Flag
```

With the line, `smtp_client.send_message(mail)`, Python will look at the email
headers to decide which recipients to tell Postmark to send this email to. Since
the To header is treated as a comma separated list, the server sends you a copy
of the email.
