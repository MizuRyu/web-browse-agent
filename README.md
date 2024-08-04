# web-browse-agent

gpt-4o-miniでwebブラウジング可能なエージェントを実装する。

### Tool
---
```web_page_reader```

ユーザーがURLを指定して命令した場合にスクレイピングするツール

```duckduckgo_search```

クエリに基づいてWeb検索を行うツール


### Environments
---
```
AZURE_OPENAI_ENDPOINT="https://<your-endpoint>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<your-api-key>"
API_TYPE="azure"
AZURE_OPENAI_API_VERSION="2024-02-01"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
```


### Requirements
---
tbl

### Installation
---

```
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

### Note
---
2024/08/04現在、Azure上で`gpt-4o-mini`を利用するには、 **west-us** のみ対応しています。他のリージョンでは展開できません。

詳細：[標準の展開モデルの可用性](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#standard-deployment-model-availability)