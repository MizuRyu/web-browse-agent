import os
import sys

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import tool
from langchain_community.tools import DuckDuckGoSearchRun

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

SYSTEM_PROMPT = """
### Instructions
あなたはuserの質問に対して、インターネットでWebページを調査し、回答をするタスクが与えられています。

### Constraints
1. 回答はできるだけ短く、要約して解凍してください。
2. 文章が長くなる場合、開業して見やすくしてください。
3. 回答の最後に開業した後、参照したページのURLを記載してください。
4. [output format]の形式に従って回答をしてください。

### output format
（質問）
[質問文]
（検索クエリ）
[検索に使用したクエリ]
----
（Agentの回答）
[回答文]

参照したページのURL:
[URL]
"""

search = DuckDuckGoSearchRun()

@tool
def web_page_reader(url: str) -> str:
    """
    指定されたURLのウェブページの内容を読み込み、文字列として返します。

    Args:
        url (str): ウェブページのURL。

    Returns:
        str: ウェブページの内容。
    """
    loader = WebBaseLoader(url)
    content = loader.load()[0].page_content
    return content

@tool
def duckduckgo_search(query: str) -> str:
    """
    このツールはWeb上の最新情報を検索します。引数で検索キーワードを受け取ります。最新情報が必要ない場合はこのツールは使用しません。
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

tools = [web_page_reader, duckduckgo_search]

# prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# model定義
llm = AzureChatOpenAI(
    openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    max_tokens=1000,
)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

if __name__ == "__main__":
    user_input = "このWebページ要約して。https://zenn.dev/pharmax/articles/8796b892eed183"
    result = agent_executor.invoke(
        {"input": user_input},
    )