from langgraph.checkpoint.base import BaseCheckpointSaver, CheckpointTuple, Checkpoint, CheckpointMetadata, ChannelVersions
from typing import Sequence, Any, Dict
from pathlib import Path
import os
import json
import pickle
import base64
from langchain_core.runnables import RunnableConfig


class FileSaver(BaseCheckpointSaver[str]): 
    def __init__(self, base_path: str = r"E:\agent_chat_file+git+RAG\app\.temp"):
        super().__init__()
        self.base_path = base_path

        os.makedirs(base_path, exist_ok=True)

    def _get_checkpoint_path(self, thread_id, checkpoint_id):
        dir_path = os.path.join(self.base_path, thread_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, checkpoint_id + ".json")
        return file_path

    def get_serializable_checkpoint(self, data) -> str:
        pickled = pickle.dumps(data)
        return base64.b64encode(pickled).decode()
    
    def _deserialize_data(self, data):
        decoded = base64.b64decode(data)
        return pickle.loads(decoded)


    def get_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        """Fetch a checkpoint tuple using the given configuration.

        Args:
            config: Configuration specifying which checkpoint to retrieve.

        Returns:
            Optional[CheckpointTuple]: The requested checkpoint tuple, or None if not found.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        # 1. 找到正确的checkpoint文件路径
        thread_id = config["configurable"]["thread_id"]
        
        # 2. 读取checkpoint文件内容
        dir_path = os.path.join(self.base_path, thread_id)
        checkpoint_files = list(Path(dir_path).glob("*.json"))
        checkpoint_files.sort(key=lambda x: x.stem, reverse=True)
        
        if len(checkpoint_files) > 0:
            last_checkpoint_file = checkpoint_files[0]
            checkpoint_id = last_checkpoint_file.stem
            checkpoint_file_path = self._get_checkpoint_path(thread_id, checkpoint_id)
            
            print(f"读取checkpoint文件: {last_checkpoint_file.name}")
            
            try:
                # 对文件内容进行反序列化
                with open(checkpoint_file_path, "r", encoding="utf-8") as checkpoint_file:
                    data = json.load(checkpoint_file)
                
                checkpoint = self._deserialize_data(data["checkpoint"])
                metadata = self._deserialize_data(data["metadata"])
                
                # 返回CheckpointTuple对象
                return CheckpointTuple(
                    config={
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_id": checkpoint_id,
                        }
                    },
                    checkpoint=checkpoint,
                    metadata=metadata,
                )
            except Exception as e:
                print(f"读取checkpoint文件时出错: {e}")
                return None
        else:
            print(f"在 {dir_path} 目录中没有找到checkpoint文件")
            return None
    
    def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: Dict[str, Any],
    ) -> RunnableConfig:
        """Store a checkpoint with its configuration and metadata.

        Args:
            config: Configuration for the checkpoint.
            checkpoint: The checkpoint to store.
            metadata: Additional metadata for the checkpoint.
            new_versions: New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        # 1. 生成存储的JSON文件路径
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]
    
        checkpoint_path = self._get_checkpoint_path(thread_id, checkpoint_id)
        
        # 2. 将Checkpoint进行序列化
        checkpoint_data = {
            "checkpoint": self.get_serializable_checkpoint(checkpoint),
            "metadata": self.get_serializable_checkpoint(metadata),
        }

        # 3. 将Checkpoint存储到文件系统
        with open(checkpoint_path, "w", encoding="utf-8") as checkpoint_file:
            json.dump(checkpoint_data, checkpoint_file, indent=2, ensure_ascii=False)
        
        print(f"保存checkpoint文件: {checkpoint_path}")
        
        # 4. 生成返回值
        return {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": checkpoint_id,
            }
        }

    def put_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Store intermediate writes linked to a checkpoint.

        Args:
            config: Configuration of the related checkpoint.
            writes: List of writes to store.
            task_id: Identifier for the task creating the writes.
            task_path: Path of the task creating the writes.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        print(f"put_writes")
        
    async def aput(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: ChannelVersions,
    ) -> RunnableConfig:
        """Asynchronously store a checkpoint with its configuration and metadata.

        Args:
            config: Configuration for the checkpoint.
            checkpoint: The checkpoint to store.
            metadata: Additional metadata for the checkpoint.
            new_versions: New channel versions as of this write.

        Returns:
            RunnableConfig: Updated configuration after storing the checkpoint.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        return self.put(config, checkpoint, metadata, new_versions)

    async def aput_writes(
        self,
        config: RunnableConfig,
        writes: Sequence[tuple[str, Any]],
        task_id: str,
        task_path: str = "",
    ) -> None:
        """Asynchronously store intermediate writes linked to a checkpoint.

        Args:
            config: Configuration of the related checkpoint.
            writes: List of writes to store.
            task_id: Identifier for the task creating the writes.
            task_path: Path of the task creating the writes.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        return self.put_writes(config, writes, task_id, task_path)
    async def aget_tuple(self, config: RunnableConfig) -> CheckpointTuple | None:
        """Asynchronously fetch a checkpoint tuple using the given configuration.

        Args:
            config: Configuration specifying which checkpoint to retrieve.

        Returns:
            Optional[CheckpointTuple]: The requested checkpoint tuple, or None if not found.

        Raises:
            NotImplementedError: Implement this method in your custom checkpoint saver.
        """
        return self.get_tuple(config)