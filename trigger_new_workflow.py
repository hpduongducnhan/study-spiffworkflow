import os
import sys
import logging
import asyncio
import httpx


http_client = httpx.AsyncClient(proxy=None)


async def trigger_new_workflow():
    async def worker(wfcid: int, sem: asyncio.Semaphore):
        async with sem:
            res = await http_client.get(
                url=f'http://172.27.230.30:9001/api/start_workflow',
                params={'wf_config_id': wfcid}
            )
            print(f'Workflow started ', res.status_code, res.text)
            await asyncio.sleep(0.2)  # thêm độ trễ nhỏ để tránh quá tải

    sem = asyncio.Semaphore(30)  # chỉ cho phép 30 task chạy đồng thời
    tasks = [asyncio.create_task(worker('8865a29d-7b8a-4766-86f5-48ea9b958cf2', sem)) for i in range(10000)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(trigger_new_workflow())
