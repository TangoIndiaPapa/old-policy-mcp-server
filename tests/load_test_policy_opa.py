import time
from policy_mcp_server.server import PolicyMCPServer

def light_load_test(iterations=1000):
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
