# CS224U Project

## Abstract

Text to SQL is a natural language processing task which translates natural language sentences to an executable SQL query. Models trained on this relies on some inherent nature dataset to be structured. There are currently no benchmark defined for the model performance on unstructured dataset. Unstructured data is widely used by Security Incident and Event Management (SIEM) tools, used for threat detection and response. In this experimental protocol we propose methods to extend current Text to SQL task for a custom SIEM tool and propose relevant dataset, models and metrics for the same.

## Hypothesis

Text to SQL task aims to retrieve facts from the database by translating human language questions to corresponding SQL queries. Prominent dataset for the task includes WikiSQL \cite{zhongSeq2SQL2017} where dataset involved 80654 hand annotated examples of questions and SQL queries distributed across 24241 tables. Most of the queries are simple and involves a simple table without any foreign key joins. Spider \cite {Yu&al.18c} enriches the dataset by involving complex queries, including conditions such as order by, group by, nested and having clause. Models trained on the dataset requires understanding the complex schema structure with multiple tables and foreign key dependencies. Model trained on these dataset are vulnerable to adverse table perturbation as indicated by \cite{pi-etal-2022-towards} indicating that the models relying largely on underlying schema structure. BIRD \cite{li2024can} dataset aims to solve the perturbation issue by retaining dirty values in the dataset. Models trained on this network would require numeric reasoning, domain knowledge, synonym knowledge and value illustration in addition to understanding the underlying schema structure to craft an efficient SQL query. Wrong schema linking, misunderstanding of database context, misunderstanding of knowledge evidence are some of the reasons causing a performance degradation of these models.Based on Multi Agent Collaborative Framework for Text to SQL \cite{wang2024macsql} in context learning optimizes SQL query generation in such scenarios
Security Incident and Event Management (SIEM) is a tool for businesses to respond to threats before they affect the business operations. SIEM tools extends the functionality of SQL to operate on unstructured where column relations is not defined. SIEM instruct language are tool specific as noted in kusto query language \cite{KQL} or Splunk Query Language \cite{SPL}. Standard query language generator. Large language Model such as Open AI Codex \cite{OpenAICodex}, Code Llama \cite{CodeLlama} are mostly optimized to generate queries for standard programming language such as Python, Ruby, SQL etc. Generating code for customized query language would require an additional fine-tuning step.

Based on the above literature review we propose the following hypothesis. Frameworks for text to SQL can be extended to train a text to custom SIEM model. Taking advantage of the fact that most of the LLM models provide a decent translation for text to executable SQL, the output obtained from such models can be further used to fine-tune model for SQL to SIEM. This is illustrated in \ref{figure1}.

A typical scenario can be illustrated as below

\textbf{Natural Language}:
Identify the evidence of brute force activity against a user based on multiple authentication failures and at least one successful authentication within a given time window. Note that the query does not enforce any sequence, and does not require the successful authentication to occur last. The default failure threshold is 10, success threshold is 1, and the default time window is 20 minutes.

While training the prompting following context is provided \textbf{tablename}: asimauthenticationeventlogs and table schema to generate the intermediate SQL query. The Query generated is compared with the gold SQL with exact match to improve prompts using chain of thoughts. The SQL text generated is further passed down to a SQL to SIEM model to generate SIEM query for processing

## Dataset

As in the related studies and above proposed hypothesis we propose below dataset

1. Standard Dataset: This includes a subset from standard dataset frequently employed to assess the text to SQL tasks using large language models. The dataset under consideration are SPIDER \cite{Yu&al.18c} and BIRD \cite{li2024can}. To simulate on schema-less domain on which typical SIEM tools operate, the foreign key dependency information from some of the schema would be obfucated.

2. Curated Dataset: This include custom handcrafted data that mimics typical SIEM queries. The dataset from public GitHub repositories \cite{reprise99} and \cite{sentialqueries} which includes SIEM query for detecting threats in typical Microsoft Azure assets. The text is used as a natural language for the dataset, while a hand crafted SQL equivalent of the KSQL is used as a gold SQL text in this scenario. Schema source for the dataset is scraped from Schema definition link published. \cite{msschema}.

3. SQL to SIEM: This includes a handcrafted dataset which includes SQL query to SIEM query. A subset of queries from WikiSQL \cite{zhongSeq2SQL2017} is used for this translation.

## Metrics

A standard metric in the field of text generation BLEU is used as a standard metric. For the model SQL to SIEM query, BLEU is used as a metric for capturing the model's capacity of generating SIEM. Inspired from BIRD's data set evaluation \cite{li2024can} correctness of the query will be used to evaluate correctness of the query generated.

While for the Text to SQL we would rely on two metrics based on BIRD's evaluation \cite{li2024can}. The metrics would be reported on exact match accuracy (EM) for sample extracted from standard dataset. Exact match accuracy (EM) treats each clause as a set and compares the prediction for each clause to its corresponding clause in the reference query. A predicted SQL query is considered correct only if all its component match the ground truth label. Values are not taken as a measure for ground truth. For the current scope of the project we do consider execution accuracy (EX) or Valid Efficiency Score (VES) as defined in BIRD \cite{li2024can}.

## Models

To evaluate the effectiveness of the proposed model we consider the following model approach.

1. Text to SQL approach:

1.1 \emph{Pre-trained Large Language Model}: We evaluate the efficiency of SQL query generation based on the prompt input at this stage. A chain of thought approach is considered to improve the quality of SQL query generated using the standard DSPy package. We plan to evaluate Open AI's model namely GPT-3.5 and GPT-4 for the task along with other open source models baseline being GPT-3.5

2. \emph{SQL to SIEM model approach}: Since its a text generation task we evaluate on different stages.

2.1. \emph{T5 small Model}: The model will be considered as a baseline for BLEU.

2.2 \emph{Pre-Trained Large language model}: We would test the efficiency of the large language model to generate efficient SQL translation based on templates provided as a context for the models.

\section{General Reasoning}

The objective of the hypothesis is to test whether the existing pipeline for Text to SQL can be extend to a custom SIEM query language. SIEM query has a similar structure as a standard SQL query but would differ in terms of structure and function definitions. The data source on which the compiler operate on is unstructured

General purpose large language models are pre-trained with a large corpus of SQL data and provide a good baseline for generic Text to SQL task. Schema linking seems to be a major issue which reduces the accuracy of the model on tasks such as BIRD \cite{li2024can} which require domain level reasoning and downstream fine-tuning for these models.

For the hypothesis, models would be evaluated on the schema less dataset for tables related to cyber-security. Since there are no standard dataset for this task at the moment, a handcrafted limited dataset is created. The quality of evaluation is limited to the dataset constructed for the task. We generate an intermediate SQL response for the task so that the results are comparable with the standard published with these datasets. Since the data schema provided to the model is unstructured a potential performance degradation is further expected. More contextual information to be further used to optimize the model's performance to generate a more coherent response.

A baseline SQL to custom SIEM \cite{customsiem} translation task would be used for completing the pipeline for text to SIEM. The model is trained on limited dataset developed during the course of the project and is expected to provide a coherent translation for at least simple queries involving a single table
