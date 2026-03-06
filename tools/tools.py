import sys
import asyncio

async def get_stdio__feishu_tools():
    """获取飞书工具"""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    npx_path = r""
    config = {
        "feishu_tools": {
            "transport": "stdio",
            "command": npx_path,
            "args": ["-y", "feishu-mcp"],
            "env": {
                "FEISHU_APP_ID": "cli_a92393113a39dcb2",
                "FEISHU_APP_SECRET": "cpLJ1LTBucTEe8AVPluU4cTIX42ZRwXW"
            }
        }
    }
    
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()
    return tools

async def get_stdio__search_tools():
    """获取搜索工具"""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    config = {
        "searchapi": {
            "transport": "stdio",
            "command": "node",
            "args": [r"E:\AI Teaching Agent Team\searchapi-mcp-server\dist\index.js"]
        }
    }
    
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()
    return tools

from app.agent.utills.mcp import create_mcp_stdio_client
import sys

async def get_stdio__shell_tools():
    params = {
        "command": sys.executable,  # 使用当前Python解释器
        "args": [
        r""
        ]
    }
    shell_client,shell_tools = await create_mcp_stdio_client("shell_tool", params) #创建mcp客户端并获得工具
    return shell_tools

async def get_stdio__playwright_tools():
    server_path = r"" # playwright-mcp-server.cmd 路径
    params = {
        "transport": "stdio",
        "command": server_path,
        "args": [],
    }
    playwright_client, playwright_tools = await create_mcp_stdio_client("playwright_tools", params) #创建mcp客户端并获得工具
    return playwright_tools

async def get_stdio__amap_tools():
    amap_key = ""
    params = {"amap": {
        "url": f"https://mcp.amap.com/sse?key={amap_key}",
        "transport": "sse"
    }}
    amap_client,amap_tools = await create_mcp_stdio_client("amap_tool", params) #创建mcp客户端并获得工具
    return amap_tools

async def get_stdio__github_tools():
    npx_path = r""
    params = {
        "command": npx_path,
        "args": ["-y","@modelcontextprotocol/server-github"],
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_api"
        }
    }
    github_client, github_tools = await create_mcp_stdio_client("github_tools", params) #创建mcp客户端并获得工具
    return github_tools

async def get_stdio__12306_tools():
    npx_path = r""
    params = {
        "command": "uv",
        "args": ["run", "python", "-m", "mcp_12306.cli"],
        "cwd": ""
    }
    mcp_12306_client, mcp_12306_tools = await create_mcp_stdio_client("12306_tools", params) #创建mcp客户端并获得工具
    return mcp_12306_tools

