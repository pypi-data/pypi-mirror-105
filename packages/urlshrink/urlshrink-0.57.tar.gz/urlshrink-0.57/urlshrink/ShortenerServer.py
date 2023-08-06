import pyug
from flask import Flask, render_template, request, redirect, make_response, session
from loguru import logger as log
from multiprocessing import Process
from urllib.parse import urlparse
from datetime import datetime, timedelta
from hashids import Hashids
from base64 import b64encode
from io import BytesIO
from threading import Thread
from dataset import connect, Database, Table
from time import sleep
from privy import hide, peek
from random import randint, choices
from simplejson import dumps, loads
from hashlib import sha512
from string import ascii_letters, digits


try:
    import qrcode
except ImportError:
    qrcode = None


TIMESTAMP_FORMAT = "%Y.%m.%d %H:%M:%S"
CHARSET = ascii_letters + digits


class ShortenerServer(Process):
    _db: Database = None
    _url: Table = None
    _user: Table = None

    def __init__(self, db_path: str, salt: str, host: str = "127.0.0.1", port: int = 4004, debug: bool = False,
                 domain: str = "", qr: bool = False, anonymous: bool = False, max_tries_per_suffix: int = 4,
                 encryption_level: int = 0, secret_key: str = "thisIsBigSecret"):
        Process.__init__(self)
        self._db = connect("sqlite:///{}".format(db_path))
        self._url = self._db["url"]
        self._ips = self._db["ips"]
        self._user = self._db["users"]

        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        self.app.secret_key = secret_key
        self.domain = domain
        self.qr = qr
        self.anonymous = anonymous
        self.max_tries_per_suffix = max_tries_per_suffix
        self.encryption_level = encryption_level
        self.hashids = Hashids(salt)

        if self.qr and qrcode is None:
            self.qr = False

        # --------------- ROUTES ---------------
        @self.app.route("/")
        def root():
            return self.show_shorten_page()

        @self.app.route("/signup")
        def signup():
            return render_template("signup.html", **self._jp({}))

        @self.app.route("/login")
        def login():
            v = self.get_values()
            if self.has_and_not_none(v, ["username", "password"]):
                u = self._user.find_one(username=v["username"], password=v["password"])
                if u is not None:
                    session["cookie"] = u["cookie"]
                    return redirect("/u/{}".format(u["hashed_username"]))
                else:
                    return render_template("login.html", **self._jp({
                        "error": "Username or password incorrect."
                    }))
            return render_template("login.html", **self._jp({}))

        @self.app.route("/shorten")
        def shorten():
            return self.show_shorten_page()

        @self.app.route("/search")
        def search():
            v = self.get_values()
            d = {}
            u = self.get_current_user()

            if u is not None:
                d.update(u)

            if not self.has_and_not_none(v, ["suffix"]):
                return render_template("search.html", **self._jp(d))

            e = self._url.find_one(suffix=v["suffix"])

            if e is None:
                self.count_visit()
                d.update({"error": "The suffix '{}' does not exist.".format(v["suffix"])})
                return render_template("search.html", **self._jp(d))

            d.update(e)

            if e["encrypted"]:
                if u is not None:
                    self.count_visit()
                    d.update({
                        "qr": peek(e["qr"], u["cookie"]).decode("utf-8"),
                        "url": peek(e["url"], u["cookie"]).decode("utf-8"),
                        "creator_ip": peek(e["creator_ip"], u["cookie"]).decode("utf-8")
                    })
                elif "key" in v.keys():
                    if e["key"] == sha512(v["key"].encode("utf-8")).hexdigest():
                        self.count_visit()
                        d.update({
                            "qr": peek(e["qr"], v["key"]).decode("utf-8"),
                            "url": peek(e["url"], v["key"]).decode("utf-8"),
                            "creator_ip": peek(e["creator_ip"], v["key"]).decode("utf-8")
                        })
                    else:
                        e = self.count_visit(tries=1)
                        d = {"error": "Key is not correct. You have {} more tries.".format(self.tries_left(e))}
                else:
                    self.count_visit(tries=1)
                    d.update({"error": "This suffix requires a key."})
            else:
                d.update(e)

            if "error" not in d.keys():
                return render_template("statistics.html", **self._jp(d))

            return render_template("search.html", **self._jp(d))

        @self.app.route("/s/<path>")
        def redirect_to(path):
            e = self._url.find_one(**{"suffix": path})

            if e is None:
                self.count_visit()
                return render_template("shorten.html", **self._jp({"error": "Incorrect suffix."}))

            if e["key"] == "":
                self.count_visit()
                return redirect(e["url"])

            v = self.get_values()
            if self.has_and_not_none(v, ["key"]):
                if e["key"] == v["key"]:
                    self.count_visit()
                    return render_template("statistics.html", **self._jp(e))
                else:
                    d = self.count_visit(tries=1)
                    e["error"] = "Incorrect password. You have {} tries left.".format(self.tries_left(d))
                    return render_template("key.html", **self._jp(e))
            else:
                self.count_visit(tries=1)
                e["error"] = "No password supplied."
                return render_template("key.html", **self._jp(e))

        @self.app.route("/u/<path:path>")
        def user(path):
            u = self._user.find_one(hashed_username=path)
            if u is None:
                return redirect("/")
            session["cookie"] = u["cookie"]
            return render_template("user.html", **self._jp(u))

        @self.app.route("/logout")
        def logout():
            session.clear()
            return redirect("/")

        # API ROUTES
        @self.app.route("/api/user/generate_username")
        def api_user_generate_username():
            username = self.generate_unique_username()
            if username is None:
                return make_response(dumps({"error": True}))
            return make_response(dumps({"error": False, "username": username}))

        @self.app.route("/api/user/create", methods=["POST"])
        def api_user_create():
            data = loads(request.data)
            if not self.has_and_not_none(data, ["username", "password"]):
                return make_response(dumps({"error": True}))
            if self._user.find_one(username=data["username"]):
                return make_response(dumps({"error": True}))
            data["hashed_username"] = sha512(data["username"].encode('utf-8')).hexdigest()
            data["cookie"] = sha512(''.join(choices(CHARSET, k=64)).encode('utf-8')).hexdigest()
            data["shorties"] = ""
            self._user.insert(data)
            return make_response(dumps({"error": False, "username": data["username"],
                                        "hashed_username": data["hashed_username"]}))

    # --------------- STATIC METHODS ---------------

    @staticmethod
    def generate_username():
        return pyug.get_random_username() + "_" + str(randint(0, 1000))

    @staticmethod
    def get_remote_addr() -> str:
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return request.environ['REMOTE_ADDR']
        else:
            return request.environ['HTTP_X_FORWARDED_FOR']

    @staticmethod
    def get_values() -> dict:
        r = {}
        for item in request.values:
            r[item] = request.values[item]
        return r

    @staticmethod
    def is_url(url) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @staticmethod
    def has_and_not_none(d, keys) -> bool:
        dk = d.keys()
        if len(d.keys()) == 0:
            return False
        for k in keys:
            if k in dk and d[k] is None:
                log.debug(d, k)
                return False
        return True

    @staticmethod
    def generate_qrcode(url: str) -> str:
        c = qrcode.make(url)
        b = BytesIO()
        c.save(b, format="PNG")
        return b64encode(b.getvalue()).decode('utf-8')

    # --------------- CLASS METHODS ---------------

    def generate_unique_username(self, max_tries: int = 5):
        username = self.generate_username()
        hashed_username = sha512(username.encode("utf-8")).hexdigest()
        c = 0
        while self._user.find_one(username=hashed_username) is not None and c < max_tries:
            username = self.generate_username()
            hashed_username = sha512(username.encode("utf-8")).hexdigest()
            c += 1
        while self._user.find_one(username=hashed_username) is not None:
            return None
        return username

    def get_unused_username(self):
        username = pyug.get_random_username()  # 25.596 combinations
        while self._user.find_one({"username": username}) is not None:
            username = pyug.get_random_username()
        return username

    def show_shorten_page(self):
        v = self.get_values()
        d = {}

        u = self.get_current_user()
        if u is not None:
            d.update(u)

        if "url" in v.keys() and v["url"] != "":
            if not v["url"].startswith("http://") and not v["url"].startswith("https://"):
                v["url"] = "https://" + v["url"]

            if self.is_url(v["url"]):
                d.update(self.shorten_url(v))
                d["url"] = v["url"]
                return render_template("shorten.html", **self._jp(d))

            return render_template("shorten.html", **self._jp({"error": "URL is invalid."}))

        return render_template("shorten.html", **self._jp(d))

    def shorten_url(self, data: dict) -> dict:
        log.debug(data)

        e = {
            "creator_ip": self.get_remote_addr(),
            "url": data["url"],
            "suffix": self.hashids.encode(len(self._url)),
            "hits": 0,
            "last_visited": None,
            "qr": None,
            "delete_at": (datetime.now() + timedelta(weeks=420)).strftime(TIMESTAMP_FORMAT),
            "encrypted": False
        }

        if self.qr:
            e["qr"] = self.generate_qrcode(self.domain + e["suffix"])

        ue = e.copy()

        if "key" in data.keys() and data["key"] != "":
            e["creator_ip"] = hide(e["creator_ip"].encode("utf-8"), data["key"], self.encryption_level)
            e["url"] = hide(e["url"].encode("utf-8"), data["key"], self.encryption_level)
            e["qr"] = hide(e["qr"].encode("utf-8"), data["key"], self.encryption_level)
            e["key"] = sha512(data["key"].encode("utf-8")).hexdigest()
            e["encrypted"] = True

        if self.has_and_not_none(data, ["time", "unit"]):
            x = 0
            try:
                n = int(data["time"])
                if data["unit"] == "Seconds":
                    x = timedelta(seconds=n)
                elif data["unit"] == "Minutes":
                    x = timedelta(minutes=n)
                elif data["unit"] == "Hours":
                    x = timedelta(hours=n)
                elif data["unit"] == "Days":
                    x = timedelta(days=n)
                elif data["unit"] == "Weeks":
                    x = timedelta(weeks=n)
                e["delete_at"] = (datetime.now() + x).strftime(TIMESTAMP_FORMAT)
                ue["delete_at"] = e["delete_at"]
            except ValueError:
                pass

        u = self.get_current_user()
        if u is not None:
            if u["shorties"] == "":
                u["shorties"] = e["suffix"]
            else:
                u["shorties"] += "," + e["suffix"]
            self._user.update(u, ["username"])

            e["creator_ip"] = hide(e["creator_ip"].encode("utf-8"), u["cookie"], self.encryption_level)
            e["url"] = hide(e["url"].encode("utf-8"), u["cookie"], self.encryption_level)
            e["qr"] = hide(e["qr"].encode("utf-8"), u["cookie"], self.encryption_level)
            e["key"] = sha512(u["cookie"].encode("utf-8")).hexdigest()
            e["encrypted"] = True

        self._url.insert(e)

        return ue

    def count_visit(self, url=None, ip=None, tries=0):
        if self.anonymous:
            return None
        if url is None:
            url = request.path
        if ip is None:
            ip = self.get_remote_addr()
        e = self._ips.find_one(ip=ip, url=url)
        if e is None:
            e = {"ip": ip, "tries": tries, "hits": 1, "url": url}
            self._ips.insert(e)
        else:
            e["tries"] += tries
            e["hits"] += 1
            self._ips.update(e, ["ip", "url"])
        return e

    def tries_left(self, e: dict):
        return self.max_tries_per_suffix - e["hits"]

    def get_current_user(self):
        if "cookie" in session.keys():
            return self._user.find_one(cookie=session.get("cookie"))
        return None

    def find_shorties(self, user: dict) -> list:
        r = []
        for suffix in user["shorties"].split(","):
            n = self._url.find_one(suffix=suffix)
            if n is not None:
                if n["encrypted"]:
                    n["creator_ip"] = peek(n["creator_ip"], user["cookie"]).decode("utf-8")
                    n["url"] = peek(n["url"], user["cookie"]).decode("utf-8")
                r.append(n)
        return r

    def create_jinja_params(self, d: dict) -> dict:
        d.update({
            "domain": self.domain,
            "anonymous": self.anonymous,
            "port": self.port
        })

        u = self.get_current_user()
        if u is not None:
            s = self.find_shorties(u)
            d.update({
                "i_shrunk": len(s),
                "shrunk": s
            })
        else:
            d.update({
                "i_shrunk": 0,
                "shrunk": []
            })
        return d

    def _jp(self, d: dict) -> dict:
        return self.create_jinja_params(d)

    def clean_db(self):
        while True:
            for item in self._url.find(delete_at={'<': datetime.now().strftime(TIMESTAMP_FORMAT)}):
                log.debug("Deleting {}", item)
                self._url.delete(suffix=item["suffix"])
            sleep(1)

    def start_cleaner(self):
        dbct = Thread(target=self.clean_db)
        dbct.daemon = True
        dbct.start()

    def run(self) -> None:
        self.start_cleaner()
        self.app.run(self.host, self.port, self.debug)
