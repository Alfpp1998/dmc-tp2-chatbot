# Plan to turn your course final into the first working slice of AdAgent Copilot

## Strategic framing

I could not re-open the earlier uploaded rubric files because those uploads had expired from the workspace, so I based this roadmap on the course syllabus you pasted and on the AdAgent Copilot scope already established in our conversation.

The strongest strategy is **not** to build a smaller version of the entire diploma final. It is to build a **vertical slice** that already works end to end and that can later be extended into the diploma project. That recommendation is consistent with current guidance from LangChain and Rasa: multi-agent systems are useful when tasks require specialized context or too many tools, but not every complex project needs them; deterministic workflows are usually better when the process is known in advance; and Rasa flows are explicitly meant to encode the information to collect, the data to retrieve from APIs or databases, and the branching logic for task completion. For your course final, that means **one assistant, a small explicit toolset, and a controlled RAG layer** is the right level of ambition.

So my recommendation is this: make the course final the **foundational conversational layer** of AdAgent Copilot. In the course, you prove that the assistant can understand intents, query marketing data safely, retrieve knowledge from documents, explain answers in business language, and deploy as an app. Then, for the diploma final, you add the real recommendation engine, online feedback updates, and the multi-armed bandit layer on top of the same architecture.

## What the course final should actually be

The course final should be a project I would name **AdAgent Copilot Foundations**. Its target is narrower than the diploma final, but it still looks serious and directly reusable. The assistant should do four things well: answer marketing FAQ and metric-definition questions, answer controlled analytical questions over a public marketing dataset, explain the results in plain language, and generate a first campaign brief based on retrieved context plus the query output. That scope fits the course content exactly: it covers intent-based Rasa design, LLM-backed explanation, RAG over documents, basic agent/tool behavior, and deployment. It also creates reusable assets for the diploma final: intents, slots, training data, custom actions, a knowledge base, a query layer, and a demoable UI. 

The key product decision is to **separate deterministic work from generative work**. Fixed or repetitive questions, such as “what is CTR?” or “what channels exist in this dataset?”, should be handled by rules or retrieval-backed answers. Analytical questions such as “show CTR by channel for segment X” should route to structured tools. The LLM should then be used mainly for **explanation, rephrasing, and campaign-brief generation**, not as the main source of truth for your metrics. That design matches Rasa’s “adjustable risk profile” guidance for LLM use and is the cleanest way to satisfy the course topics on hallucination control and safe chatbot design.

Concretely, the assistant you present in the course should support a conversation like this: the user asks for CTR or CPC by channel or segment; Rasa classifies the intent and fills slots such as channel, segment, or date range; a custom action runs a safe query on the dataset; the assistant returns the metric; an LLM explains what it means; then the user asks “why is this channel underperforming?” or “draft a campaign idea for this segment,” and the system uses retrieved marketing definitions and templates to produce a grounded answer. That is already a convincing end-to-end course final, and every piece of it becomes part of the diploma final.

What I would **not** put into the course final is the multi-armed bandit, live click updates, MMM logic, or a full multi-agent decomposition. Those belong in the diploma extension, not in the first submission. LangChain’s own multi-agent guidance is clear that a single agent with the right tools is often enough until the number of tools, contexts, or specialized subtasks becomes too large.

## Architecture to implement now

At the center of the architecture should be **Rasa Open Source** as the conversation orchestrator. Rasa’s training data is YAML-based, intents and entities live in the NLU layer, slots act as assistant memory, and custom actions are the standard way to connect the assistant to APIs, databases, or other business logic. Recent Rasa versions also allow Python custom actions to run directly inside the assistant, which simplifies local development and makes early deployment easier; later, you can separate them into an action server when the diploma final grows in complexity.

Your **analytics tool** should be deliberately simple and safe. I would use a public campaign dataset in CSV or Parquet, normalize it into a clean master table, load it into DuckDB, and expose a small set of read-only analytical functions such as `get_ctr_by_channel`, `get_top_segments`, `get_cpc_by_campaign`, and `get_channel_summary`. DuckDB is a strong fit here because it is an in-process SQL analytical database, runs on a laptop or server, and can query Pandas DataFrames directly without a separate import step. That makes it ideal for a course project where speed and simplicity matter more than distributed infrastructure.

Your **knowledge tool** should be a small RAG pipeline. The most important documents are not hundreds of files; they are a compact, curated corpus: your project one-pager, a marketing-metrics glossary, a data dictionary, a short explanation of the dataset fields, and one or two campaign-brief templates. The technical stack is straightforward: chunk the documents, create embeddings, index them in FAISS, retrieve the most relevant passages at runtime, and ask the LLM to answer only from that context. This follows the standard RAG pattern described by the original RAG paper and by current LangChain and Rasa documentation: retrieve relevant context first, then generate a grounded answer from it. FAISS is specifically built for efficient similarity search over dense vectors, and Hugging Face gives you easy inference and embedding options, including simple pipeline abstractions and common sentence-embedding models.

For the **LLM layer**, I would keep the prompts narrow. The LLM should receive either a structured analytics result or retrieved passages, and its job should be to translate those results into business language, compare options, or draft a campaign brief. This lowers hallucination risk and aligns with Rasa’s recommendation that you can use LLMs selectively while still controlling exactly where generated text is allowed.

For the **application shell**, I would place a very small API layer around your tools using FastAPI and show the experience through a lightweight chat UI in entity["company","Streamlit","python app framework"]. FastAPI is useful because it gives you validation and automatic OpenAPI documentation for tool endpoints, which makes your assistant-tool contract explicit and easier to debug. Streamlit is useful because it is a quick Python framework for dynamic data apps and is easy to deploy for demos. To package everything, use entity["company","Docker","container software"] for containerization and Compose to run multiple services together when you are ready to separate Rasa, the API, and any action server. Rasa’s deployment docs explicitly call out Docker Compose as a practical way to run the assistant together with an action server.

In practical terms, the architecture should look like this in your minds even if you do not yet draw it formally: **User interface → Rasa router → analytics tool or RAG tool → LLM explanation layer → answer**. That is enough to look like a real assistant today and to become a multi-agent marketing copilot later.

## Roadmap from course final to diploma final

### Foundation sprint

Start by defining the **smallest useful problem statement**: “A marketing assistant that answers campaign questions from public data and marketing documentation.” Then create the repository and the base Rasa project, ideally from `rasa init`, and establish your core project files: `nlu.yml`, `domain.yml`, `stories.yml` or `flows.yml`, `actions.py`, `data/`, and `tests/`. Rasa’s CLI supports exactly this iterative workflow with `rasa init`, `rasa train`, `rasa shell`, `rasa inspect`, and validation/testing commands. Interactive learning is especially helpful early on because it lets you teach the assistant from real conversations and correct mistaken intent or action predictions as you go.

The output of this sprint should be a **clean contract**, not a fancy model. You want a list of 6 to 8 intents, a first slot schema, one normalized dataset, and a first demo that can say hello, identify a couple of analytical requests, and answer a few FAQ-style questions. Example intents could be: `ask_metric_definition`, `ask_ctr_by_channel`, `ask_top_segment`, `ask_campaign_summary`, `generate_campaign_brief`, `help`, and `fallback`.

### Analytics sprint

Next, implement the structured analytics path. Build the normalized master table and define a small query interface in Python over DuckDB. Do **not** start with open-ended SQL generation. Instead, create parameterized functions that accept only the slots you support. Then connect those functions to Rasa through custom actions. Rasa’s custom actions are meant exactly for database queries, API calls, and dynamic business logic, and DuckDB is purposely good at fast SQL over local analytical data.

At the end of this sprint, your assistant should be able to answer questions like “Which channel has the highest CTR?” or “Show CPC for segment A,” then say something like “Instagram is best on CTR but worse on CPC.” The answer can still be templated at this stage; the important thing is that the structured result is right.

### Explanation sprint

Once the structured path works, add the LLM explanation layer. This should be a thin wrapper that receives the structured result and transforms it into plain marketing language: what happened, why it matters, and one suggested next action. This is the best place to show the “Rasa + LLM” part of the course without losing control. It also gives you a very visible demo improvement with relatively little engineering risk.

The output here should be an assistant that can answer the metric correctly and then explain it in a way a non-technical stakeholder would understand. That is already a strong course milestone.

### RAG sprint

Then add the document-backed knowledge layer. Curate a small set of documents, split them into chunks, embed them, index them in FAISS, and implement a retriever. LangChain’s retrieval abstractions are helpful because they let you keep the retriever and the answer-generation logic separate, while FAISS gives you efficient vector search and Hugging Face gives you straightforward local or API-based model options.

This sprint should make the assistant reliably answer questions such as “what is ROAS?”, “what does reward mean in our table?”, or “what should a campaign brief contain?” It should also let the assistant ground campaign-brief generation in retrieved context instead of inventing structure from scratch. That is the piece that most cleanly satisfies your course topics on Rasa + RAG and autonomous conversational agents with external information sources.

### Packaging sprint

Finally, wrap the project as a small app. Put the assistant behind a REST endpoint, add a minimal front end, containerize the services, and make sure the project is easy to run from a fresh clone. A Streamlit chat UI is usually sufficient for the demo; it keeps the focus on the assistant and lets you include a small side panel with the last analytical result or retrieved passages. Use Docker Compose only when you need more than one service; until then, direct custom actions inside Rasa can simplify the local developer experience.

### Diploma extension sprint

After the course final is done, you can extend the same system into the diploma project by adding a **recommender layer** in stages. First, add a deterministic score-based recommendation over channels or campaigns. Next, add the mechanism to store new performance results. Only then add the multi-armed bandit logic and, if it becomes truly useful, split the architecture into specialized agents for exploration, recommendation, and campaign generation. That sequence keeps the architecture honest: every new piece is justified by a new problem, not by the desire to use a buzzword.

## Division of work for two people

The cleanest split is **conversation/orchestration owner** and **data/AI tools owner**, with both of you sharing the evaluation and demo narrative.

The first person should own the **assistant product layer**. That includes writing the user stories, defining intents and slots, preparing Rasa NLU examples, designing the dialogue flows or stories, wiring the custom actions into Rasa, handling fallbacks, building the Streamlit front end, and preparing the final demo sequence. This person should also own the README and the presentation storyline, because they are closest to the end-user interaction. The relevant stack here is Rasa, the front end in Streamlit, and the packaging layer with Docker.

The second person should own the **data and intelligence layer**. That includes normalizing the public dataset, defining the metric queries in DuckDB, building the small analytics service, curating the document corpus, chunking and embedding it, building the FAISS index, implementing the LangChain retrieval wrapper, and writing the LLM prompts for explanation and campaign-brief generation. If you decide to expose tools through an API, this person should also own the FastAPI contracts and validation models. The relevant stack here is DuckDB, Hugging Face, FAISS, LangChain, and FastAPI.

Both of you should jointly own three things. First, the **tool contract**, meaning the exact JSON inputs and outputs for each action. Second, the **evaluation set**, meaning 20 to 30 representative questions with expected behavior. Third, the **demo script**, because the success of the presentation will depend as much on sequencing as on engineering.

## Guardrails, evaluation, and demo criteria

The biggest architectural risk in your project is letting the model generate arbitrary database queries or arbitrary business advice. LangChain’s SQL-agent documentation explicitly warns that model-generated SQL has inherent risks and recommends scoping database permissions as narrowly as possible. For your course final, I would go one step further and avoid unrestricted SQL entirely: use read-only connections and a small allow-listed query layer exposed as tools. That keeps the project safer, easier to debug, and more defensible in front of a professor.

For hallucination control and evaluation, follow a very practical guardrail stack. Use document-grounded RAG for factual definitions; use structured query outputs for metrics; instruct the assistant to say when the answer is unavailable; keep generated campaign briefs explicitly tied to retrieved context and current analytics; and build a small evaluation set from the start. The generative AI profile from NIST is built precisely to help organizations incorporate trustworthiness considerations into AI design, development, use, and evaluation. OpenAI’s guardrail guidance recommends building a strong eval set and defining explicit hallucination criteria, while LangChain’s RAG evaluation guidance highlights answer relevance, answer accuracy, and retrieval quality as core measures. Rasa’s CLI also supports validation and end-to-end testing, which you should use before every milestone demo.

I would define course-final success in very concrete terms. The assistant should correctly handle a small set of FAQ and analytical intents; preserve enough slot memory to continue a conversation such as “now filter that by segment”; retrieve the right glossary or data-dictionary passage for knowledge questions; generate a campaign brief based on retrieved context and structured results; and run as a shareable app. If you can demonstrate those five capabilities live, your course final will already look like the first production slice of the diploma project rather than a disconnected exercise.

The most important PM decision, then, is simple: **present the course final as the foundational assistant for AdAgent Copilot, not as a toy chatbot**. If you do that, every week of work on the course will compound directly into the diploma final.