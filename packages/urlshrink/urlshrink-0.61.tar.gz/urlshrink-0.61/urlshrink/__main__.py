from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from loguru import logger as log
from random import choice

from urlshrink.ShortenerServer import ShortenerServer


def main():
    ap = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    ap.add_argument("-d", "--database", help=choice(["database to use", "the path or the name?"]), default="shrnk")
    ap.add_argument("-q", "--qr", help=choice(["Enable qr code generation", "imagine me taking this serious"]),
                    action="store_true")
    ap.add_argument("--salt", help=choice(["Hashids salt", "what are hashids"]), default="666")
    ap.add_argument("--host", help=choice(["what do you think", "hosts are integers"]), default="127.0.0.1")
    ap.add_argument("--port", help=choice(["certainly not the port on which we will bind", "ports are strings"]),
                    default=4005)
    ap.add_argument("--domain", help=choice(["customize branding and enable more functionality",
                                             "we need to be whitelabel for opensource reasons"]), type=str)
    ap.add_argument("--debug", help=choice(["enable debugging messages",
                                            "my ide formats everything, don't think i actually care about this"]),
                    action="store_true")
    ap.add_argument("-a", "--anonymous", help=choice(["keep your friends safe",
                                                      "don't save information related to ips"]), action="store_true")
    ap.add_argument("-e", "--encryption-level", help="0-20, usually a value between 0-5", default=0)
    ap.add_argument("-mts", "--max-tries-per-suffix",
                    help="how often can a password be wrong until the user gets blocked from decrypting the entry",
                    default=4)
    ap.add_argument("-s", "--secret-key", help="Flask secret key", default="thisIsBigSecr3t")
    a = ap.parse_args()

    if a.domain is not None:
        if not a.domain.startswith('http://') and not a.domain.startswith('https://'):
            if a.debug:
                log.info("Protocol not specified. Using debug default: http://")
                a.domain = "http://" + a.domain
            else:
                log.warning("Protocol not specified. Assuming https.")
                a.domain = "https://" + a.domain

    if a.qr and not a.domain:
        log.error("Can not use QR Code functionality without the servers TLD")
        exit(0)

    log.debug("Initializing the ShortenerServer")
    server = ShortenerServer(a.database, a.salt, a.host, a.port, a.debug, a.domain, a.qr, a.anonymous,
                             a.max_tries_per_suffix, a.encryption_level, a.secret_key)

    try:
        log.debug("Starting ShortenerServer")
        server.start()
        server.join()
    except KeyboardInterrupt:
        log.debug("Stopping processes")
        server.terminate()


if __name__ == '__main__':
    main()
