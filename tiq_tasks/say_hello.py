from worker import tiq_broker


@tiq_broker.task("say_hello")
async def say_hello(name: str) -> str:
    print(f"Saying hello to {name}")
    return f"Hello, {name}!"