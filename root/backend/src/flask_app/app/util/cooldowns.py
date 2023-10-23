import flask
import threading
import time

class CostEnum():
    NONE = 0
    LOW = 1 # e.g.: delete a comment, which needs just 2 db calls
    NORMAL = 2 # e.g.: submitting a post
    EXPENSIVE = 3 # e.g.: registering

MAX_REQUESTS = 7200 # max requests per hour
COOLDOWN_SECS = {CostEnum.NONE: 0, CostEnum.LOW: 1, CostEnum.NORMAL: 10, CostEnum.EXPENSIVE: 60}

# {"ip_address": {"func": cooldown until}}
cooldowns = dict()
_cooldowns_lock = threading.Lock()

def cooldown(cost):
    def f1(f):
        def f2(*args, **kwargs):
            addr = flask.request.remote_addr
            t = time.time()

            _cooldowns_lock.acquire()

            if addr in cooldowns:
                if f.__name__ in cooldowns[addr]:
                    if t < cooldowns[addr][f.__name__]:
                        cooldowns[addr][f.__name__] = t + COOLDOWN_SECS[cost]
                        _cooldowns_lock.release()
                        response = flask.make_response("Wait " + str(COOLDOWN_SECS[cost]) + "s before calling this endpoint again", 429)
                        response.headers.add("X-Wait-For", str(COOLDOWN_SECS[cost]))
                        return response
            else:
                cooldowns[addr] = dict()

            cooldowns[addr][f.__name__] = t + COOLDOWN_SECS[cost]

            if "__total__" in cooldowns[addr]:
                cooldowns[addr]["__total__"]["num"] += 1

                if cooldowns[addr]["__total__"]["num"] > MAX_REQUESTS:
                    return "Hourly request maximum reached", 429

                if cooldowns[addr]["__total__"]["last_reset"] + 3600 < t:
                    cooldowns[addr]["__total__"] = {"num": 1, "last_reset": t}
            else:
                cooldowns[addr]["__total__"] = {"num": 1, "last_reset": t}

            _cooldowns_lock.release()

            result = f(*args, **kwargs)

            response = flask.make_response(result)
            response.headers.add("X-Requests-Remaining", str(MAX_REQUESTS - cooldowns[addr]["__total__"]["num"]))

            return response

        f2.__name__ = f.__name__
        return f2
    return f1