import subprocess
import shlex
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# 创建FastMCP实例
mcp = FastMCP()

@mcp.tool(name="run_shell_command", description="Run shell command")
def run_shell_command(
    command: str = Field(description="The shell command to run", example="dir")
) -> str:
    try:
        shell_command = shlex.split(command)
        if "rm" in shell_command:
            raise Exception("rm command is not allowed")
        res = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
        if res.returncode != 0:  # 如果返回码不为0 表示执行失败
            return res.stderr  # 返回错误信息
        return res.stdout  # 返回标准输出
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")  # 启动MCP服务端
