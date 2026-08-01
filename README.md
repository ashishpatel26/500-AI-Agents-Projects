# 500+ AI Agent Projects & Use Cases

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/ashishpatel26/500-AI-Agents-Projects?style=for-the-badge&color=yellow)](https://github.com/ashishpatel26/500-AI-Agents-Projects/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ashishpatel26/500-AI-Agents-Projects?style=for-the-badge&color=blue)](https://github.com/ashishpatel26/500-AI-Agents-Projects/network/members)
[![Contributors](https://img.shields.io/github/contributors/ashishpatel26/500-AI-Agents-Projects?style=for-the-badge&color=green)](https://github.com/ashishpatel26/500-AI-Agents-Projects/graphs/contributors)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](CONTRIBUTION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/ashishpatel26/500-AI-Agents-Projects?style=for-the-badge)](https://github.com/ashishpatel26/500-AI-Agents-Projects/commits/main)

**The most comprehensive collection of AI agent projects, use cases, and working implementations.**

[🚀 Quick Start](#-quick-start) • [🗺️ Browse Agents](#-browse-by-framework) • [🏭 By Industry](#-industry-use-cases) • [🤝 Contribute](#-contributing) • [📊 Frameworks Compared](#-framework-comparison)

</div>

---

![AI Agent Use Cases](images/AIAgentUseCase.jpg)

## What is this?

A curated collection of **500+ AI agent projects** — production examples, tutorials, and working code spanning every major framework (LangGraph, CrewAI, AutoGen, Agno) and industry (Healthcare, Finance, Education, Cybersecurity, and more).

**Who it's for:**
- 🧑‍💻 **Developers** building their first or next AI agent
- 🔬 **Researchers** surveying the agent landscape
- 🏢 **Teams** evaluating frameworks for production use
- 🎓 **Students** learning agent architectures from real examples

---

## ⚡ Quick Start

Pick a framework and run an agent in under 5 minutes:

```bash
# Clone the repo
git clone https://github.com/ashishpatel26/500-AI-Agents-Projects.git
cd 500-AI-Agents-Projects

# Run any agent from the agents/ directory
cd agents/01-web-research-agent
pip install -r requirements.txt
cp .env.example .env        # add your API key
python agent.py
```

> All agents in `agents/` are self-contained with their own `requirements.txt` and `.env.example`. No monorepo setup needed.

---

## 🗺️ Navigation Guide

| I want to... | Go to |
|---|---|
| Run a working agent right now | [`agents/`](agents/) |
| Browse by AI framework | [Framework-wise Use Cases](#-browse-by-framework) |
| Browse by industry | [Industry Use Cases](#-industry-use-cases) |
| Understand which framework to use | [Framework Comparison](#-framework-comparison) |
| Add my own agent | [Contributing](CONTRIBUTION.md) |
| Learn with a course | [`crewai_mcp_course/`](crewai_mcp_course/) |

---

## 📊 Framework Comparison

Choosing a framework? Here's when to use each:

| Framework | Best For | Complexity | Multi-Agent | Streaming | Local LLM |
|---|---|---|---|---|---|
| **LangGraph** | Stateful workflows, RAG pipelines, complex graphs | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **CrewAI** | Role-based teams, business automation, rapid prototyping | ⭐⭐ | ✅ | ✅ | ✅ |
| **AutoGen** | Code generation, research, self-healing workflows | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Agno** | Lightweight single agents, tool integration, fast iteration | ⭐ | ✅ | ✅ | ✅ |
| **LlamaIndex** | Document Q&A, enterprise RAG, data pipelines | ⭐⭐ | ⚠️ | ✅ | ✅ |

**Quick decision guide:**
- Just starting out → **Agno** or **CrewAI**
- Need stateful graphs + RAG → **LangGraph**
- Building code-writing / research agents → **AutoGen**
- Enterprise document pipelines → **LlamaIndex**

---

## 🏭 Industry Use Cases

![Industry Mind Map](images/industry_usecase1.png)

| Use Case | Industry | Description | Code |
|---|---|---|---|
| **HIA (Health Insights Agent)** | Healthcare | Analyses medical reports and provides health insights | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/harshhh28/hia) |
| **AI Health Assistant** | Healthcare | Diagnoses and monitors diseases using patient data | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/ahmadvh/AI-Agents-for-Medical-Diagnostics) |
| **Automated Trading Bot** | Finance | Automates stock trading with real-time market analysis | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/MingyuJ666/Stockagent) |
| **Agent Wallet SDK** | Finance | Non-custodial smart contract wallet SDK for AI agents with enforced spend limits | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/up2itnow0822/agent-wallet-sdk) |
| **Virtual AI Tutor** | Education | Provides personalized education tailored to users | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/hqanhh/EduGPT) |
| **24/7 AI Chatbot** | Customer Service | Handles customer queries around the clock | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/customer_support_agent_langgraph.ipynb) |
| **Product Recommendation Agent** | Retail | Suggests products based on user preferences and history | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/microsoft/RecAI) |
| **Self-Driving Delivery Agent** | Transportation | Optimizes routes and autonomously delivers packages | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/sled-group/driVLMe) |
| **Factory Process Monitoring Agent** | Manufacturing | Monitors production lines and ensures quality control | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/yuchenxia/llm4ias) |
| **Property Pricing Agent** | Real Estate | Analyzes market trends to determine property prices | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/AleksNeStu/ai-real-estate-assistant) |
| **Smart Farming Assistant** | Agriculture | Provides insights on crop health and yield predictions | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/mohammed97ashraf/LLM_Agri_Bot) |
| **Energy Demand Forecasting Agent** | Energy | Predicts energy usage to optimize grid management | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/yecchen/MIRAI) |
| **Content Personalization Agent** | Entertainment | Recommends personalized media based on preferences | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/crosleythomas/MirrorGPT) |
| **Legal Document Review Assistant** | Legal | Automates document review and highlights key clauses | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/firica/legalai) |
| **Recruitment Recommendation Agent** | Human Resources | Suggests best-fit candidates for job openings | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/sentient-engineering/jobber) |
| **Virtual Travel Assistant** | Hospitality | Plans travel itineraries based on preferences | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/nirbar1985/ai-travel-agent) |
| **AI Game Companion Agent** | Gaming | Enhances player experience with real-time assistance | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/onjas-buidl/LLM-agent-game) |
| **Real-Time Threat Detection Agent** | Cybersecurity | Identifies potential threats and mitigates attacks | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/NVISOsecurity/cyber-security-llm-agents) |
| **E-commerce Personal Shopper Agent** | E-commerce | Helps customers find products they'll love | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/Hoanganhvu123/ShoppingGPT) |
| **Logistics Optimization Agent** | Supply Chain | Plans efficient delivery routes and manages inventory | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/microsoft/OptiGuide) |
| **Vibe Hacking Agent** | Cybersecurity | Autonomous Multi-Agent Based Red Team Testing Service | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/PurpleAILAB/Decepticon) |
| **Agent Memory Guard** | Cybersecurity | Detects and blocks memory poisoning attacks (OWASP ASI06) in AI agent memory stores | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/OWASP/www-project-agent-memory-guard) |
| **Citadel** | Software Development | Orchestrates Claude Code agent fleets with lifecycle hooks, skills, campaign management, and postmortem-driven architecture | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/SethGammon/Citadel) |
| **MediSuite-AI-Agent** | Health Insurance | Automates hospital / insurance claiming workflow | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/ahmedmansour5/MediSuite-Ai-Agent) |
| **Lina Egyptian Medical Chatbot** | Healthcare | Egyptian medical assistant chatbot | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/dina-khalid/Lina-Egyptian-Medical-Chatbot) |
| **NextRole (AI Career Assistant)** | Human Resources | Tailors a resume to a job description and generates interview prep plus a day-of battlecard via a multi-agent system | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/tam159/next-role) |
| **PII Sanitization Agent** | Privacy/Compliance | Redacts PII (emails, phones, national IDs, bank accounts, API keys) from text before it reaches an LLM; fail-closed, multilingual, on-chain proof via TrustBoost | [![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer) |

---

## 🔧 Browse by Framework

### CrewAI

Role-based multi-agent framework. Great for business automation.

| Use Case | Industry | Description | GitHub |
|---|---|---|---|
| 📧 Email Auto Responder Flow | Communication | Automates email responses based on predefined criteria | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/flows/email_auto_responder_flow) |
| 📝 Meeting Assistant Flow | Productivity | Organizes meetings, scheduling and agenda preparation | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/flows/meeting_assistant_flow) |
| 🔄 Self Evaluation Loop Flow | Human Resources | Facilitates self-assessment for performance reviews | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/flows/self_evaluation_loop_flow) |
| 📈 Lead Score Flow | Sales | Evaluates and scores potential leads to prioritize outreach | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/flows/lead-score-flow) |
| 📊 Marketing Strategy Generator | Marketing | Develops marketing strategies by analyzing market trends | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/marketing_strategy) |
| 📝 Job Posting Generator | Recruitment | Creates job postings by analyzing job requirements | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/job-posting) |
| 🔄 Recruitment Workflow | Recruitment | Streamlines recruitment by automating hiring tasks | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment) |
| 🔍 Match Profile to Positions | Recruitment | Matches candidate profiles to suitable job positions | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/match_profile_to_positions) |
| 📸 Instagram Post Generator | Social Media | Generates and schedules Instagram posts automatically | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/instagram_post) |
| 🌐 Landing Page Generator | Web Development | Automates creation of landing pages for websites | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/landing_page_generator) |
| 🎮 Game Builder Crew | Game Development | Assists in game development by automating aspects of creation | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/game-builder-crew) |
| 💹 Stock Analysis Tool | Finance | Provides tools for analyzing stock market data | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/stock_analysis) |
| 🗺️ Trip Planner | Travel | Assists in planning trips with itineraries | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/trip_planner) |
| 🎁 Surprise Trip Planner | Travel | Plans surprise trips based on user preferences | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/surprise_trip) |
| 📚 Write a Book with Flows | Creative Writing | Assists authors with structured writing workflows | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/flows/write_a_book_with_flows) |
| 🎬 Screenplay Writer | Creative Writing | Aids in writing screenplays with templates and guidance | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/screenplay_writer) |
| ✅ Markdown Validator | Documentation | Validates Markdown files for proper formatting | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/markdown_validator) |
| 🧠 Meta Quest Knowledge | Knowledge Management | Manages Meta Quest knowledge for information retrieval | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/meta_quest_knowledge) |
| 🤖 NVIDIA Models Integration | AI Integration | Integrates NVIDIA AI models into workflows | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/integrations/nvidia_models) |
| 🗂️ Prep for a Meeting | Productivity | Prepares meeting materials and sets agendas | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/prep-for-a-meeting) |
| 🛠️ Starter Template | Development | Starter template for new CrewAI projects | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/starter_template) |
| 🔗 CrewAI + LangGraph Integration | AI Integration | Integration between CrewAI and LangGraph | [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/crewAIInc/crewAI-examples/tree/main/integrations/CrewAI-LangGraph) |

---

### AutoGen

Microsoft's framework for code generation, execution, and multi-agent research.

**Code Generation, Execution, and Debugging**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🤖 Automated Task Solving with Code Gen, Execution & Debugging | Software Development | Demonstrates automated task-solving by generating, executing, and debugging code | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_auto_feedback_from_code_execution) |
| 🧑‍💻 Code Generation and Q&A with Retrieval Augmented Agents | Software Development | Generates code and answers questions using retrieval-augmented methods | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_RetrieveChat) |
| 🧠 Code Generation and Q&A with Qdrant-based Retrieval | Software Development | Utilizes Qdrant for enhanced retrieval-augmented agent performance | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_RetrieveChat_qdrant) |

**Multi-Agent Collaboration**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🤝 Group Chat (3 members, 1 manager) | Collaboration | Demonstrates group task-solving via multi-agent collaboration | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat) |
| 📊 Data Visualization by Group Chat | Data Analysis | Uses multi-agent collaboration to create data visualizations | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_vis) |
| 🧩 Complex Task Solving by Group Chat (6 members) | Collaboration | Solves complex tasks collaboratively with a larger group | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_research) |
| 🧑‍💻 Task Solving with Coding & Planning Agents | Planning & Dev | Combines coding and planning agents for solving tasks | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_planning.ipynb) |
| 📐 Task Solving with Graph Transition Paths | Collaboration | Uses predefined transition paths in a graph for solving tasks | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_finite_state_machine) |
| 🧠 SocietyOfMindAgent Inner-Monologue | Cognitive Sciences | Simulates inner-monologue for problem-solving using group chats | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_society_of_mind) |
| 🔧 Group Chat with Custom Speaker Selection | Collaboration | Implements a custom function for speaker selection | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_customized) |

**Sequential Multi-Agent Chats**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🔄 Sequential Task-Solving (single initiating agent) | Workflow Automation | Automates sequential task-solving with a single initiating agent | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_multi_task_chats) |
| ⏳ Async Sequential Task-Solving | Workflow Automation | Handles asynchronous task-solving in a sequence of chats | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_multi_task_async_chats) |
| 🤝 Sequential Chats with Different Initiating Agents | Workflow Automation | Sequential task-solving with different agents initiating each chat | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchats_sequential_chats) |

**Nested Chats**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🧠 Solving Complex Tasks with Nested Chats | Problem Solving | Uses nested chats to solve hierarchical and complex problems | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nestedchat) |
| 🔄 Sequence of Nested Chats | Problem Solving | Demonstrates sequential task-solving using nested chats | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nested_sequential_chats) |
| 🏭 OptiGuide Supply Chain with Nested Chats | Supply Chain | Solves supply chain optimization using nested chats | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nestedchat_optiguide) |
| ♟️ Conversational Chess with Nested Chats | Gaming | Uses nested chats for playing conversational chess with tools | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_nested_chats_chess) |

**Tools**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🌐 Web Search: Solve Tasks Requiring Web Info | Information Retrieval | Searches the web to gather information for completing tasks | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_web_info.ipynb) |
| 🔧 Use Provided Tools as Functions | Tool Integration | Demonstrates how to use pre-provided tools as callable functions | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_function_call_currency_calculator) |
| 📚 RAG Group Chat | Collaboration | Enables group chat with Retrieval Augmented Generation | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat_RAG) |
| 🔊 Agent Chat with Whisper | Audio Processing | AI agent for transcription and translation using Whisper | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_video_transcript_translate_with_whisper) |
| 📊 SQL: Natural Language to SQL Query | Database Management | Converts natural language inputs into SQL queries | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_sql_spider.ipynb) |

**Multimodal Agents**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 🎨 Multimodal Agent with DALLE and GPT-4V | Multimedia AI | Combines DALLE and GPT-4V for multimodal agent communication | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_dalle_and_gpt4v.ipynb) |
| 🖌️ Multimodal Agent with Llava | Image Processing | Uses Llava for multimodal agent conversations | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_lmm_llava.ipynb) |
| 🖼️ Multimodal Agent with GPT-4V | Multimedia AI | Leverages GPT-4V for visual and conversational interactions | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_lmm_gpt-4v.ipynb) |

**Observability & Evaluation**

| Use Case | Industry | Description | Notebook |
|---|---|---|---|
| 📊 AgentEval: Multi-Agent Assessment System | Performance Evaluation | Evaluating LLM-based application utility | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agenteval_cq_math.ipynb) |
| 📊 Track LLM Calls and Errors using AgentOps | Monitoring & Analytics | Monitors LLM interactions, tool usage, and errors | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/agentchat_agentops.ipynb) |
| 🏗️ Auto Build Multi-agent System with AgentBuilder | AI Development | Automatically builds multi-agent systems | [![Notebook](https://img.shields.io/badge/View-Notebook-blue?logo=jupyter)](https://github.com/microsoft/autogen/blob/0.2/notebook/autobuild_basic.ipynb) |

---

### Agno

Lightweight, fast agent framework. Best for single-agent tools and rapid prototyping.

| Use Case | Industry | Description | Code |
|---|---|---|---|
| 🤖 Support Agent | AI Framework Support | Real-time answers, explanations, and code examples for Agno framework | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/agno_support_agent.py) |
| 🎥 YouTube Agent | Media & Content | Analyzes YouTube videos: summaries, timestamps, themes | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/youtube_agent.py) |
| 📊 Finance Agent (Thinking) | Finance | Real-time stock insights, analyst recommendations, financial deep-dives | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/thinking_finance_agent.py) |
| 📚 Study Partner | Education | Finds resources, answers questions, creates study plans | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/study_partner.py) |
| 🛍️ Shopping Partner Agent | E-commerce | Product recommender based on preferences from Amazon, Flipkart | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/shopping_partner.py) |
| 🎓 Research Scholar Agent | Education / Research | Advanced academic searches, publication analysis, structured reports | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/research_agent_exa.py) |
| 🧠 Research Agent | Media & Journalism | Deep investigations, NYT-style reports | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/research_agent.py) |
| 🍳 Recipe Creator | Food & Culinary | Personalized recipes based on ingredients and preferences | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/recipe_creator.py) |
| 🧠 Financial Reasoning Agent | Finance | Claude 3.5 Sonnet-based stock analysis with Yahoo Finance data | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/reasoning_finance_agent.py) |
| 🤖 Readme Generator Agent | Software Dev | Generates high-quality READMEs for GitHub repos | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/readme_generator.py) |
| 🎬 Movie Recommendation Agent | Entertainment | Personalized movie recommendations using Exa and GPT-4o | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/movie_recommedation.py) |
| 🔍 Media Trend Analysis Agent | Media & News | Analyzes emerging trends and influencers from digital platforms | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/media_trend_analysis_agent.py) |
| ⚖️ Legal Document Analysis Agent | Legal Tech | Analyzes legal PDFs and provides insights using vector embeddings | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/legal_consultant.py) |
| 🤔 DeepKnowledge | Research | Iterative search through knowledge base with deep reasoning | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/deep_knowledge.py) |
| 📚 Book Recommendation Agent | Publishing & Media | Personalized book suggestions using literary data and reader preferences | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/book_recommendation.py) |
| 🏠 MCP Airbnb Agent | Hospitality | Search Airbnb listings with MCP and Llama 4 | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/airbnb_mcp.py) |
| 🤖 Agno Assist Agent | AI Framework | GPT-4o agent for Agno framework Q&A with hybrid search | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/agno-agi/agno/blob/main/cookbook/examples/agents/agno_assist.py) |

---

### LangGraph

State-machine framework for complex, stateful agent workflows and RAG pipelines.

| Use Case | Industry | Description | Code |
|---|---|---|---|
| 🤖 Chatbot Simulation Evaluation | AI / QA | Simulate user interactions to evaluate chatbot performance | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/chatbot-simulation-evaluation/agent-simulation-evaluation.ipynb) |
| 🧠 Information Gathering via Prompting | Research | LangGraph workflow using prompting to gather information | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/chatbots/information-gather-prompting.ipynb) |
| 🧠 Code Assistant with LangGraph | Software Development | Resilient code assistant with error checking and iterative refinement | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/code_assistant/langgraph_code_assistant.ipynb) |
| 🧑‍💼 Customer Support Agent | Customer Support | Graph-based agent for handling customer inquiries | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/customer-support/customer-support.ipynb) |
| 🔁 Extraction with Retries | Data Extraction | Retry mechanisms for robust data extraction | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/extraction/retries.ipynb) |
| 🧠 Multi-Agent Workflow (Supervisor) | Workflow Orchestration | Supervisor agent orchestrating multiple specialized agents | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/agent_supervisor.ipynb) |
| 🧠 Hierarchical Agent Teams | Workflow Orchestration | Top-level supervisor delegates to specialized sub-agents | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/hierarchical_agent_teams.ipynb) |
| 🤝 Multi-Agent Collaboration | Workflow Orchestration | Multiple specialized agents working together on complex tasks | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/multi-agent-collaboration.ipynb) |
| 🧠 Plan-and-Execute Agent | Workflow Orchestration | Agent generates multi-step plan then executes sequentially | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/plan-and-execute/plan-and-execute.ipynb) |
| 🧠 SQL Agent | Database Interaction | Agent answers questions about SQL databases | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/sql-agent.ipynb) |
| 🧠 Reflection Agent | Workflow Orchestration | Agent critiques and revises its own outputs | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflection/reflection.ipynb) |
| 🧠 Reflexion Agent | Workflow Orchestration | Agent reflects on actions for iterative improvement | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb) |
| 🧠 Adaptive RAG | Information Retrieval | Dynamic retrieval adjusting based on query complexity | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_adaptive_rag.ipynb) |
| 🤖 Agentic RAG | Intelligent Agents | Agent determines best retrieval strategy before generating response | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_agentic_rag.ipynb) |
| 🧠 Corrective RAG (CRAG) | Information Retrieval | Evaluates and refines retrieved documents before generation | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_crag.ipynb) |
| 🧠 Self-RAG | Information Retrieval | System reflects on responses and retrieves additional info if needed | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_self_rag.ipynb) |
| 🧠 Adaptive RAG (Local) | Information Retrieval | Adaptive RAG with local models for offline use | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_adaptive_rag_local.ipynb) |
| 🧠 Self-RAG (Local) | Information Retrieval | Self-RAG using local models and data sources | [![Python](https://img.shields.io/static/v1?label=AI+Agent+Code&message=Python&color=%23244cd1)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rag/langgraph_self_rag_local.ipynb) |

---

## 🤝 Contributing

Contributions are welcome! 🎉 This repo grows through community contributions.

**Ways to contribute:**
1. **Add a working agent** — create a folder in `agents/` with runnable code
2. **Add an external link** — add a row to the industry or framework tables
3. **Fix a broken link** — open an issue or PR
4. **Improve documentation** — fix typos, add context, improve examples

**To contribute:**
1. Fork the repository
2. Create a branch: `feat/agent-name` or `fix/description`
3. Add your changes following the [Contributing Guidelines](CONTRIBUTION.md)
4. Open a PR using the PR template

See [CONTRIBUTION.md](CONTRIBUTION.md) for full requirements (metadata.yaml, requirements.txt, etc.).

---

## Star History

[![Star History Chart](images/star-history.svg)](https://star-history.com/#ashishpatel26/500-AI-Agents-Projects&Date)

<sub>Regenerated weekly from the GitHub API by [`.github/workflows/star-history.yml`](.github/workflows/star-history.yml). Click the chart for the interactive version.</sub>

---

## 📜 License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

<div align="center">

**⭐ Star this repo if you find it useful — it helps others discover it!**

[Report Issue](https://github.com/ashishpatel26/500-AI-Agents-Projects/issues) • [Request Agent](https://github.com/ashishpatel26/500-AI-Agents-Projects/issues/new?template=feature_request.md) • [Contribute](CONTRIBUTION.md)

</div>
