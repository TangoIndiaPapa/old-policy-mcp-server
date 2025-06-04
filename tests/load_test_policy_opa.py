import time
import importlib.util
import os
import sys

from test_constants import SERVER_PATH

spec_server = importlib.util.spec_from_file_location("server", SERVER_PATH)
server_mod = importlib.util.module_from_spec(spec_server)
spec_server.loader.exec_module(server_mod)
PolicyMCPServer = server_mod.PolicyMCPServer

ITERATIONS=1000

def light_load_test(iterations=ITERATIONS):
    server = PolicyMCPServer()
    actions = [
        "where is waldo?",
        "where is carmen sandiego?",
        "need two sum problem solution for python",
        "useless",
        "hello, how are you?",
        "can you help me with brute force?",
        "this is a normal prompt"
    ]
    durations = []
    for i in range(iterations):
        action = actions[i % len(actions)]
        start = time.time()
        server.enforce_policy_opa(action)
        durations.append(time.time() - start)
    total = sum(durations)
    avg = total / iterations
    print(f"Total duration: {total:.3f} seconds for {iterations} iterations")
    print(f"Average time per call: {avg*1000:.2f} ms")

if __name__ == "__main__":
    light_load_test()
