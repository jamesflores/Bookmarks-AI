# Bookmarks AI

![Bookmarks Cover](https://cdn.bookmarks.jamesf.xyz/images/bookmarks-cover.png)

Bookmarks AI is a simple bookmarks storage webapp with AI auto classification and search. 

It is built with Django, Bootstrap, and the OpenAI API.

This app is a work-in-progress, but you are free to use it as you wish. Any feedback can be sent to james [ at ] jamesflores.net.

Demo: https://bookmarks.jamesf.xyz

----

## 🔨 Requirements
- I am running this on Heroku with Cloudflare (Flexible mode SSL) and using R2 for static file storage (S3 compatible).
  - You will have to adjust `settings.py` to use WhiteNoise if you prefer.
- Google Recaptcha is used on user registration and password reset.
  - You will need to create your own account and set the RECAPTCHA environment variables.
- SMTP server for sending out account emails (I use Amazon SES).
- OpenAI account to set the [Marvin](https://github.com/PrefectHQ/marvin) environment variables.

## 📖 Installation
```
$ git clone https://github.com/jamesflores/Bookmarks-AI.git
$ cd Bookmarks-AI
$ python -m venv venv
$ source venv/bin/activate

(venv) $ pip install -r requirements.txt
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
(venv) $ python manage.py runserver

# Load the site at http://127.0.0.1:8000
```

## Next Steps

- Add environment variables:
  - Set `BOOKMARKS_SECRET_KEY` to any [random set of characters](https://snippet.run/james/djsecret).
  - Set `DATABASE_URL` to use a Postgres database.
  - Set `RECAPTCHA_PRIVATE_KEY` and `RECAPTCHA_PUBLIC_KEY` for Google Recaptcha.
  - Set `MARVIN_OPENAI_API_KEY`, `MARVIN_LOG_LEVEL` and `MARVIN_CHAT_COMPLETIONS_MODEL` for AI functionality.
  - Set the following email environment variables for email:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  # django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.mail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=
EMAIL_HOST_USER=user
EMAIL_HOST_PASSWORD=pass
DEFAULT_FROM_EMAIL=me@mail.com
```
- Using Django Admin, update your site details (domain and display name).

----

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

## 🙏 Thanks

- A batteries-included Django starter project: https://github.com/wsvincent/djangox
- The AI engineering toolkit: https://github.com/PrefectHQ/marvin

## ⭐️ Support

Give a ⭐️!

## License

[The MIT License](LICENSE)
