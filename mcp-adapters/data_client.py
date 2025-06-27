from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import types

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
import os

_ = load_dotenv()

model = ChatOpenAI(model="gpt-4.1-nano")

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command = "python",  # Executable
    args = ["./data_server.py"],  # Optional command line arguments
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = load_mcp_tools(session)
            memory = MemorySaver()
            agent_executor = create_react_agent(model, tools, checkpointer=memory)
            config = {"configurable": {"thread_id": "default-thread"}}

            while True:
                user_input = input("질문을 입력하세요 (종료하려면 'q' 입력): ")
                if user_input.lower() in ["q", "quit", "exit"]:
                    print("종료합니다.")
                    break

                # 프롬프트를 별도로 가공하지 않고 바로 메시지로 전달
                for step in agent_executor.stream({"messages": [user_input]}, config, stream_mode="values"):
                    # 마지막 메시지 출력
                    print("======= Response =======")
                    print(step["messages"][-1].content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())