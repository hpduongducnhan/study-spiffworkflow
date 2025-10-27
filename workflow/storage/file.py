from .base import BaseStorage


class FileStorage(BaseStorage):
    async def load_workflow_from_configuration(self, file_path: str):
        with open(file_path, 'r') as file:
            data = file.read()
            if not data:
                raise ValueError("Configuration file is empty")
            data = data.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            return data

    async def load_workflow_runtime_state(self, wf_id: str):
        with open(f"{wf_id}_state.txt", 'r') as file:
            data = file.read()
            if not data:
                raise ValueError("State file is empty")
            data = data.replace('\n', '').replace('\r', '').replace('\t', '').strip()
            return data

    async def save_workflow_runtime_state(self, wf_id: str, state: str):
        with open(f"{wf_id}_state.txt", 'w') as file:
            file.write(state)