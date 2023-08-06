#!/usr/bin/env python3
from prometheus_client import Gauge
from prometheus_client import start_http_server
import time
import requests
import os
from requests.auth import HTTPBasicAuth

TC_BASE_URL = os.environ["TC_BASE_URL"]
auth = HTTPBasicAuth(os.environ["TC_USER"], os.environ["TC_PW"])


def run():
    start_http_server(9300)
    g_connected = Gauge(
        "teamcity_agent_connected",
        "desc",
        ["agent_name", "agent_pool", "os_name", "ip"],
    )
    g_enabled = Gauge(
        "teamcity_agent_enabled", "desc", ["agent_name", "agent_pool", "os_name", "ip"]
    )
    g_authorized = Gauge(
        "teamcity_agent_authorized",
        "desc",
        ["agent_name", "agent_pool", "os_name", "ip"],
    )

    while True:
        next_run = time.time() + 5
        response = requests.get(
            "{}agents".format(TC_BASE_URL),
            auth=auth,
            headers={"Accept": "application/json"},
        )
        for agent in response.json()["agent"]:
            agentdetailsResponse = requests.get(
                "{}agents/id:{}".format(TC_BASE_URL, agent["id"]),
                auth=auth,
                headers={"Accept": "application/json"},
            )
            agentdetails = agentdetailsResponse.json()
            os_name = [
                property["value"]
                for property in agentdetails["properties"]["property"]
                if property["name"] == "teamcity.agent.jvm.os.name"
            ][0]
            g_connected.labels(
                agent_name=agentdetails["name"],
                agent_pool=agentdetails["pool"]["name"],
                os_name=os_name,
                ip=agentdetails["ip"],
            ).set(1 if agentdetails["connected"] else 0)
            g_enabled.labels(
                agent_name=agentdetails["name"],
                agent_pool=agentdetails["pool"]["name"],
                os_name=os_name,
                ip=agentdetails["ip"],
            ).set(1 if agentdetails["enabled"] else 0)
            g_authorized.labels(
                agent_name=agentdetails["name"],
                agent_pool=agentdetails["pool"]["name"],
                os_name=os_name,
                ip=agentdetails["ip"],
            ).set(1 if agentdetails["authorized"] else 0)
        while next_run > time.time():
            time.sleep(1)


if __name__ == "__main__":
    run()
