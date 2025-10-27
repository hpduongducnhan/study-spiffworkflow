import asyncio


async def create_index():   
    from models import ensure_indexes
    await ensure_indexes()


async def init_bpmn():
    from models.initializer import initialize_models
    await initialize_models()

if __name__ == "__main__":
    asyncio.run(init_bpmn())