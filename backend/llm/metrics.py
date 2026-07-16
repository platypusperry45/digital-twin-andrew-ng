"""
Simple in-memory LLM metrics.

Later can be replaced with:
- Prometheus
- OpenTelemetry
- Grafana
"""


from threading import Lock


class Metrics:


    def __init__(self):

        self.requests = 0

        self.successes = 0

        self.failures = 0

        self.total_latency = 0

        self.lock = Lock()



    def record_request(self):

        with self.lock:
            self.requests += 1



    def record_success(
        self,
        latency
    ):

        with self.lock:

            self.successes += 1

            self.total_latency += latency



    def record_failure(self):

        with self.lock:
            self.failures += 1



    def summary(self):

        with self.lock:

            avg_latency = 0

            if self.successes:
                avg_latency = (
                    self.total_latency
                    /
                    self.successes
                )


            return {

                "requests":
                    self.requests,

                "successes":
                    self.successes,

                "failures":
                    self.failures,

                "average_latency_ms":
                    avg_latency
            }



metrics = Metrics()