import sys
import os
import asyncio
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langgraph.prebuilt import create_react_agent
from model.model import llm

from memory.Filesaver import FileSaver
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from memory.Filesaver import FileSaver

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

async def Ai_teach_team_agent():
    # ========== 1. 初始化工具 ==========
    os.makedirs(r"E:\AI Teaching Agent Team\.temp", exist_ok=True)

    toolkit = FileManagementToolkit(root_dir=r"E:\AI Teaching Agent Team\.temp")
    file_tools = toolkit.get_tools()
    search = DuckDuckGoSearchRun()
    search_tools = [search]
    sub_agent_tools = file_tools + search_tools

    # ========== 2. 创建子智能体（移除 prompt 参数） ==========
    professor_agent = create_react_agent(
        model=llm,
        tools=sub_agent_tools,
        checkpointer=memory,
        debug=True
    )

    academic_advisor_agent = create_react_agent(
        model=llm,
        tools=sub_agent_tools,
        checkpointer=memory,
        debug=True
    )

    research_librarian_agent = create_react_agent(
        model=llm,
        tools=sub_agent_tools,
        checkpointer=memory,
        debug=True
    )

    teaching_assistant_agent = create_react_agent(
        model=llm,
        tools=sub_agent_tools,
        checkpointer=memory,
        debug=True
    )

    # ========== 3. 包装为工具函数 ==========
    @tool
    def call_professor(query: str) -> str:
        """你是一个专业教授...（保留原有完整描述）"""
        system_msg = {
            "role": "system",
            "content": """你是一位人工智能领域的专业教授。你的任务是：
            1. 根据用户提供的主题，从第一性原理出发，生成一份涵盖基本概念、高级主题和当前发展的详细文档。
            2. **绝对不允许向用户提问或请求澄清**，直接基于主题和你的知识（以及搜索工具）生成内容。
            3. 必须使用搜索工具查找最新的发展动态和实际应用案例。
            4. 最后将生成的文档写入 .temp 路径下的文件 'professor_agent_generate.md'（使用文件工具）。
            请立即开始执行。"""
        }
        result = professor_agent.invoke({
            "messages": [system_msg, {"role": "user", "content": query}]
        })
        return result["messages"][-1].content

    @tool
    def call_academic_advisor(query: str) -> str:
        """你是一个学业顾问...（保留原有完整描述）"""
        system_msg = {
            "role": "system",
            "content": """你是一位学业顾问。你的任务是：
            1. 根据用户提供的主题，创建一个详细的学习路线图，将主题分解为逻辑子主题，并按学习进度排列。
            2. 包括每个子主题的预估时间投入，以清晰的结构呈现。
            3. **绝对不允许向用户提问**，直接生成路线图。
            4. 可以使用搜索工具获取最新学习路径建议。
            5. 将生成的路线图写入 .temp 路径下的文件 'academic_advisor_agent_generate.md'。
    请立即开始执行。"""
        }
        result = academic_advisor_agent.invoke({
            "messages": [system_msg, {"role": "user", "content": query}]
        })
        return result["messages"][-1].content

    @tool
    def call_research_librarian(query: str) -> str:
        """你是一个专业的研究馆员...（保留原有完整描述）"""
        system_msg = {
            "role": "system",
            "content": """你是一位专业的研究馆员。你的任务是：
            1. 根据用户提供的主题，使用搜索工具查找高质量的学习资源，包括技术博客、GitHub 仓库、官方文档、视频教程和课程。
            2. 以精选列表形式呈现资源，附带描述和质量评估。
            3. **绝对不允许向用户提问**，直接生成资源列表。
            4. 将生成的列表写入 .temp 路径下的文件 'research_librarian_agent_generate.md'。
            请立即开始执行。"""
        }
        result = research_librarian_agent.invoke({
            "messages": [system_msg, {"role": "user", "content": query}]
        })
        return result["messages"][-1].content

    @tool
    def call_teaching_assistant(query: str) -> str:
        """你是一个教学助手...（保留原有完整描述）"""
        system_msg = {
            "role": "system",
            "content": """你是一位教学助手。你的任务是：
            1. 根据用户提供的主题，创建全面的练习材料，包括渐进式练习、测验、动手项目和实际应用场景。
            2. 使用搜索工具查找示例问题和案例。
            3. 为所有练习提供详细的解答和说明。
            4. **绝对不允许向用户提问**，直接生成练习材料。
            5. 将生成的练习材料写入 .temp 路径下的文件 'teaching_assistant_agent_generate.md'。
            请立即开始执行。"""
        }
        result = teaching_assistant_agent.invoke({
            "messages": [system_msg, {"role": "user", "content": query}]
        })
        return result["messages"][-1].content

    # ========== 4. 创建主智能体 ==========
    main_agent_tools = [
        call_professor,
        call_academic_advisor,
        call_research_librarian,
        call_teaching_assistant
    ]

    main_agent = create_react_agent(
        model=llm,
        tools=main_agent_tools,
        checkpointer=memory,
        debug=True
    )
    # ========== 5. 执行 ==========
    while True:
            user_input = input("\n用户: ")
            if user_input.lower() in ["exit", "quit","退出对话"]:
                break
            result = main_agent.invoke({
                "messages": [
                    {"role": "system", "content": "你是一个教学团队的主脑，可以调动你下面的四个助手（教授、学业顾问、研究馆员、教学助手）。根据用户的问题，你需要调用相应的助手来生成学习路线和资源，最后整合成一个完整的学习指南回复给用户。"},
                    {"role": "user", "content": user_input}]
                })
            print("\n=== 最终学习指南 ===\n")
            print(result["messages"][-1].content)

asyncio.run(Ai_teach_team_agent())
