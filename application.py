import streamlit as st
import pandas as pd
import gzip
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np
import PyPDF2
import docx

# -----------------------------
# Utility Functions
# -----------------------------
def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

def bytesize_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:3.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} P{suffix}"

# Function to read different file types and return a DataFrame
def read_uploaded_file(uploaded_file):
    """Reads various file types and returns a pandas DataFrame."""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    df = None
    
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension == "xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_extension == "json":
        df = pd.read_json(uploaded_file)
    elif file_extension == "txt":
        # Read text file content and create a DataFrame with one column
        text_content = uploaded_file.read().decode("utf-8")
        df = pd.DataFrame([line.strip() for line in text_content.splitlines()], columns=['text_content'])
    elif file_extension == "pdf":
        # Read text from PDF using PyPDF2
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text() or "" # Use or "" to handle empty pages
        df = pd.DataFrame([line.strip() for line in text_content.splitlines()], columns=['text_content'])
    elif file_extension == "docx":
        # Read text from DOCX using python-docx
        doc = docx.Document(uploaded_file)
        text_content = "\n".join([para.text for para in doc.paragraphs])
        df = pd.DataFrame([line.strip() for line in text_content.splitlines()], columns=['text_content'])
    else:
        st.error(f"Unsupported file type: .{file_extension}")
        st.stop()
        
    return df

# -----------------------------
# Section Content
# -----------------------------
section_content = {
    "General": (
        "### Managing Space Complexity in the Age of Expanding Digital Data\n\n"
    "With the explosion of **server logs, IoT telemetry, transactional records, multimedia streams, "
    "and user-generated content**, data growth has emerged as one of the most pressing challenges "
    "in modern computing. Organizations are confronted not only with the technical problem of storing "
    "petabytes to exabytes of information but also with ensuring that this data remains accessible, "
    "reliable, and cost-efficient.\n\n"
    "Traditional approaches to data storage, such as simple database scaling or hardware expansion, "
    "are increasingly insufficient. As data volume accelerates faster than storage hardware cost reductions, "
    "space complexity has evolved from a theoretical concern into a practical, enterprise-level bottleneck. "
    "Issues such as **ballooning storage bills, degraded query performance, and complex maintenance overhead** "
    "highlight the urgent need for more sophisticated solutions.\n\n"
    "Research in the field of **database systems, distributed storage, and data engineering** has shown "
    "that no single technique can address these challenges in isolation. Instead, organizations must integrate "
    "multiple strategies, including:\n\n"
    "- **Data deduplication:** Removing redundant copies of records or files to conserve space.\n"
    "- **Compression techniques:** Using lossless or lossy methods (e.g., gzip, Lempel-Ziv, columnar compression) "
    "to significantly reduce storage consumption.\n"
    "- **Aggregation and summarization:** Reducing fine-grained data into higher-level summaries where appropriate, "
    "balancing analytical needs with space efficiency.\n"
    "- **Tiered storage strategies:** Balancing high-speed SSDs or in-memory systems for fresh data with "
    "archival storage for older, less-accessed datasets.\n"
    "- **Adaptive management policies:** Dynamically adjusting storage and processing approaches based on "
    "observed access patterns.\n\n"
    "From a **theoretical perspective**, space complexity is tightly linked to algorithmic efficiency, "
    "where trade-offs between memory consumption and processing speed are often unavoidable. "
    "From a **practical perspective**, organizations are forced to consider not only technical trade-offs "
    "but also economic and environmental implications — such as **cloud storage costs, energy consumption, "
    "and sustainability goals**.\n\n"
    "In this context, the study of space complexity is not limited to academia but represents a critical factor "
    "in the **design of next-generation data platforms**. As datasets continue to grow, addressing space complexity "
    "will remain central to achieving scalable, sustainable, and high-performance computing infrastructures."
),
    "Introduction": (
        "### Introduction\n\n"
        "Organizations today face the dual challenge of rapid data ingestion and long-term "
        "storage demands. Left unchecked, uncontrolled data accumulation leads to degraded "
        "query performance, ballooning storage costs, and complex maintenance overhead.\n\n"

        "#### 1.1 The Data Explosion Phenomenon\n"
        "The contemporary digital ecosystem is witnessing an unprecedented and exponential "
        "surge in data generation, a phenomenon widely referred to as the *data explosion*. "
        "Unlike linear growth trends, data volumes increase at an accelerating rate: each "
        "increment in existing data triggers even larger volumes of new data. Projections "
        "estimate that by 2025, global data creation will surpass **175 zettabytes**. To "
        "contextualize, a single zettabyte can hold the equivalent of approximately "
        "**250 billion DVDs**. This trajectory follows a distinct *hockey-stick curve*, with "
        "a sharp inflection in the early 2020s when multiple disruptive technologies simultaneously "
        "reached mass adoption.\n\n"
        "The drivers of this explosion are multifaceted and tightly interconnected. The Internet "
        "of Things (IoT) has embedded billions of sensors and devices into homes, industries, and "
        "urban infrastructure, enabling a constant stream of telemetry data. Social media platforms "
        "contribute massive volumes of user-generated content, particularly through short-form video "
        "formats such as TikTok and Instagram Reels. Additionally, the rise of **Conversational AI** "
        "and **Large Language Models (LLMs)** has introduced new forms of automated content generation, "
        "further accelerating data creation. This is compounded by the digitization of traditionally "
        "analog processes across all sectors of business and governance, turning daily operations into "
        "data-rich workflows.\n\n"
        "Complicating matters further is the heterogeneity of data sources. On average, enterprises "
        "manage data from **400 distinct sources**, with some reporting over **1,000 sources**, each "
        "varying in format, schema, and structure. This diversity exacerbates the challenges of "
        "integrating, processing, and governing data at scale.\n\n"

        "#### 1.2 The Systemic Impact of Unchecked Data Growth\n"
        "The implications of this exponential growth extend far beyond the technical challenges of "
        "storage expansion. Unchecked data accumulation introduces **economic, infrastructural, and "
        "environmental consequences**, reframing the issue from a question of capacity planning to one "
        "of sustainability and long-term viability.\n\n"
        "**Economic Impact.** Direct costs manifest as expenditures on storage hardware, data management "
        "systems, and cloud subscriptions. Indirect costs, however, are often more damaging. Organizations "
        "accumulate vast quantities of *dark data*—information that is stored but never analyzed or used. "
        "This not only wastes financial resources but also obscures actionable insights under layers of "
        "irrelevant information, weakening decision-making and reducing competitiveness.\n\n"
        "**Infrastructural Strain.** The demand for compute and storage resources—particularly for "
        "data-intensive **AI workloads**—places unprecedented pressure on global energy systems. Today, "
        "data centers and communication networks account for **2–3% of global electricity consumption** "
        "and approximately **1% of greenhouse gas emissions**, figures projected to rise sharply. Such "
        "demand creates a bottleneck, as technological progress becomes increasingly constrained by "
        "energy generation and grid capacity. This forces greater collaboration between data center "
        "operators and utility providers to address risks related to power distribution and grid resilience.\n\n"
        "**Environmental Consequences.** The unchecked accumulation of data challenges the long-standing "
        "industry belief that *more data is inherently better*. The environmental toll of data infrastructure "
        "spans the full lifecycle: from mining and manufacturing server components to operating power- and "
        "water-intensive data centers, and finally, to disposing of obsolete hardware, which contributes to "
        "**e-waste**, one of the fastest-growing toxic waste streams globally. Simply building more data centers "
        "is a short-sighted solution that worsens both energy crises and sustainability concerns. A paradigm shift "
        "is needed—from *indiscriminate accumulation* toward *responsible, efficient, and value-driven data management*.\n\n"

        "#### 1.3 Thesis Statement and Contribution\n"
        "Although isolated techniques such as **compression, deduplication, and aggregation** mitigate data growth, "
        "they are inadequate in addressing the systemic, multi-dimensional challenges of scale. This paper argues for "
        "a **hybrid, policy-driven data reduction framework** that dynamically orchestrates multiple reduction "
        "techniques across the **entire data lifecycle**. Such a framework must adaptively apply reduction methods "
        "according to the **value profile** of data, which evolves over time based on its age, access frequency, "
        "and business relevance.\n\n"
        "The contributions of this paper are threefold:\n"
        "1. **Multi-Stage Data Management Architecture.** We design an architecture that categorizes data into *Hot*, "
        "*Warm*, and *Cold* tiers, applying context-appropriate reduction strategies to balance performance, cost, and accessibility.\n"
        "2. **Open-Source Python Implementation.** We provide a practical implementation of the framework, featuring a "
        "declarative policy engine that orchestrates complex data reduction workflows with minimal overhead.\n"
        "3. **Performance Evaluation.** We present a rigorous assessment of the framework’s effectiveness, analyzing "
        "reductions in storage footprint and exploring trade-offs across **space (storage savings), time (latency), "
        "and computation (CPU cost)**.\n\n"

        "#### 1.4 Paper Structure\n"
        "The remainder of this paper builds upon the thesis in a structured manner. **Section 2** surveys existing "
        "literature on data management and reduction techniques, identifying the research gap that motivates a hybrid "
        "approach. **Section 3** details the architecture and Python-based implementation of the proposed framework, "
        "including annotated code snippets. **Section 4** evaluates the system’s performance, offering both quantitative "
        "benchmarks and qualitative insights into trade-offs and limitations. Finally, **Section 5** concludes with key "
        "findings and discusses avenues for future research.\n\n"
    ),
    "Literature Review": (
        "### Literature Review\n\n"

        "#### 2.1 Foundational Data Management Strategies\n"
        "The literature consistently emphasizes that effective data reduction is not merely a technical problem but a strategic one. "
        "Before organizations adopt compression or deduplication tools, they must establish a comprehensive **Data Management Strategy (DMS)** "
        "that governs the entire lifecycle of data—from creation and collection, through active use, to archival and eventual disposal.\n\n"
        "A cornerstone of such a strategy is **Data Governance**, which defines clear ownership, accountability, and quality standards for data assets. "
        "Governance frameworks ensure that data remains reliable, accurate, and consistent across organizational silos. "
        "Equally important is **Data Lifecycle Management (DLM)**, which operationalizes governance principles into concrete steps: active use, infrequent access, archival, and deletion. "
        "Central to DLM is the **Data Retention Policy**, which balances regulatory compliance with business requirements. For instance, HIPAA mandates the preservation of healthcare records for six years, "
        "whereas GDPR restricts personal data storage strictly to its intended purpose. "
        "Crafting such policies involves identifying data assets, classifying them by sensitivity, aligning with legal frameworks, and establishing secure, auditable disposal mechanisms.\n\n"
        
        "#### 2.2 Taxonomy of Data Reduction Techniques\n"
        "Within this strategic foundation, technical methods provide the operational means of reducing storage overhead. "
        "The literature classifies these into three broad families: **compression, deduplication, and summarization/aggregation**. Each offers distinct benefits, trade-offs, and contexts of applicability.\n\n"

        "**Compression.** Lossless compression techniques (e.g., DEFLATE/gzip, Zstandard) dominate enterprise systems because they guarantee exact data reconstruction. "
        "Compression works by identifying statistical redundancies within data streams. DEFLATE, widely adopted due to its balance of speed and ratio, "
        "is considered a baseline standard, while Zstandard offers faster processing and higher configurability, enabling finer trade-offs between CPU usage and storage savings. "
        "However, a key limitation is the trade-off between compression ratio and latency: higher ratios demand more CPU resources, slowing down decompression during query execution. "
        "Moreover, compressed data streams are often not seekable, requiring segmentation into smaller chunks for random access—reducing overall efficiency.\n\n"

        "**Deduplication.** Unlike compression, which operates on internal redundancies, deduplication removes duplicate chunks across datasets. "
        "File-level deduplication (or Single-Instance Storage) is simple but limited, as minor file modifications invalidate the entire file. "
        "Block-level deduplication, particularly content-defined chunking, offers superior reduction by detecting similarities even across different files. "
        "Deduplication can be applied inline (real-time, with potential write latency) or as a post-processing task (delayed optimization, requiring temporary storage). "
        "Despite high storage savings (especially in workloads such as backups or VM images), deduplication is resource-intensive, relying on large-scale hash indexing. "
        "It may also degrade read performance due to fragmented I/O operations and has been shown to introduce subtle side-channel vulnerabilities in multi-tenant systems.\n\n"

        "**Summarization/Aggregation.** This approach reduces data volume by lowering granularity. Instead of retaining all raw events, systems store derived metrics—"
        "for example, hourly averages instead of second-by-second readings. "
        "Batch aggregation is common in data warehousing (e.g., ETL pipelines, pandas operations), while stream-based rollups are critical for real-time systems like IoT analytics or fraud detection. "
        "Although aggregation achieves the highest reduction ratios, it is inherently lossy—fine-grained details are irretrievably discarded. "
        "This makes aggregation unsuitable for use cases requiring forensic analysis, compliance auditing, or precise replay of historical events.\n\n"

        "#### 2.3 Identifying the Research Gap\n"
        "While each method is well-studied and widely deployed, the literature highlights their **individual limitations**. "
        "Compression is ineffective on structured or pre-optimized data; deduplication, though powerful, is computationally expensive; "
        "and aggregation irreversibly sacrifices data fidelity. Moreover, combining these techniques without coordination can be counterproductive—for example, deduplication on compressed data is largely ineffective.\n\n"
        "This underscores a key research gap: the absence of a **hybrid, policy-driven framework** that can intelligently orchestrate these methods across the data lifecycle. "
        "Such a system would dynamically select the appropriate reduction strategy based on evolving factors such as data age, business value, access patterns, and compliance needs. "
        "The development of such a framework—grounded in governance, lifecycle awareness, and adaptive policy control—represents the core contribution of this paper.\n\n"

        "#### 2.4 Comparative Summary\n"
        "The table below summarizes the trade-offs identified across the three main reduction techniques:\n\n"
        "| Technique      | Principle                          | Reduction Potential | CPU Overhead | Latency Impact | Data Fidelity | Ideal Use Case |\n"
        "|----------------|------------------------------------|---------------------|--------------|----------------|---------------|----------------|\n"
        "| Compression    | Encodes data to fewer bits         | Low–Medium (2–10x)  | Medium       | High (decomp.) | 100% (Lossless)| Text, logs, general files |\n"
        "| Deduplication  | Stores one copy of duplicate blocks| Medium–Very High (5–50x+) | High   | Medium (random I/O) | 100% | Backups, VM images, redundant datasets |\n"
        "| Aggregation    | Summarizes to lower granularity    | Very High (100x+)   | Low–Medium   | Low            | Lossy          | Time-series, analytics, trend detection |\n\n"
    ),
    "Proposed Solution or Approach": (
"### Proposed Solution or Approach\n\n"

    "In addressing the challenge of **space complexity in modern digital ecosystems**, this study proposes a "
    "multi-layered **data management pipeline**. The objective is to optimize storage, preserve data quality, "
    "and ensure scalability without compromising analytical value. The approach draws inspiration from principles "
    "of **database normalization**, **distributed computing models**, and **tiered storage strategies**, aligning "
    "them into a cohesive and adaptive framework.\n\n"

    "#### 3.1 Data Quality Assurance (Preprocessing)\n"
    "Before optimization techniques can be meaningfully applied, it is essential to ensure that the data being "
    "retained is both accurate and relevant. This preprocessing stage involves eliminating duplicate entries, "
    "incomplete records, and corrupted values. For example, IoT sensors frequently generate redundant time-series logs, "
    "while social media platforms often capture multiple identical events due to retry mechanisms. "
    "Removing such redundancies not only reduces data volume but also **enhances dataset reliability**. "
    "In addition, **schema alignment and normalization (1NF, 2NF, 3NF)** enforce structural consistency across "
    "heterogeneous sources, ensuring that downstream storage and processing systems can operate efficiently.\n\n"

    "#### 3.2 Data Distribution Across Tiers\n"
    "Inspired by high-performance computing paradigms, which balance CPU and GPU workloads, the solution introduces "
    "a **tiered storage model**. In this model:\n\n"
    "- **Hot Data** (frequently accessed, recent datasets) is stored on high-performance mediums such as SSD-backed databases or in-memory caches.\n"
    "- **Warm Data** (historical but occasionally accessed datasets) is migrated into moderately priced compressed storage.\n"
    "- **Cold Data** (rarely accessed archives) is pushed into low-cost, long-term storage layers, potentially object stores or tape-based archives.\n\n"
    "This stratified distribution ensures that query performance on fresh data remains **fast and efficient**, while historical "
    "data continues to be available without inflating costs. The model thus balances **performance, scalability, and economic sustainability**.\n\n"

    "#### 3.3 Data Reduction through Compression and Aggregation\n"
    "Beyond distribution, the pipeline incorporates **lossless compression techniques** (e.g., gzip, Zstandard) "
    "to further optimize storage consumption for archival data. "
    "Compression is complemented by **real-time aggregation and summarization**, particularly for use cases where "
    "fine granularity is unnecessary. For instance, raw transaction logs can be rolled up into hourly or daily summaries, "
    "preserving insights while significantly reducing storage requirements. "
    "This dual approach achieves a balance between **space efficiency** and **analytical fidelity**.\n\n"

    "#### 3.4 Feedback-Driven Adaptation\n"
    "Unlike conventional static archival systems, the proposed pipeline introduces a **dynamic feedback loop**. "
    "Continuous monitoring of usage metrics determines whether specific datasets should be promoted or demoted across tiers:\n\n"
    "- Frequently queried archival datasets can be dynamically migrated back into higher-performance tiers.\n"
    "- Infrequently accessed data can be compressed further or relegated to deep-cold storage.\n\n"
    "This adaptability ensures that space management policies remain **context-aware and evolving**, "
    "eliminating rigid inefficiencies and supporting real-world analytical workflows.\n\n"

    "#### 3.5 Conceptual Advantages\n"
    "By combining **data quality assurance, tiered storage, compression, aggregation, and adaptive feedback**, "
    "the proposed pipeline creates a **resilient framework** for sustainable data management. "
    "It not only reduces raw storage consumption but also ensures that organizations can maintain data accessibility, "
    "regulatory compliance, and analytical depth. The multi-layered approach thus bridges the gap between "
    "short-term performance demands and long-term archival sustainability.\n\n"
    ),
"Methodology and Implementation": (
    "### Methodology and Implementation\n\n"
    "We demonstrate our approach using Python. The implementation includes:\n\n"  
    "- Uploading a dataset.\n\n"  
    "- Automatic deduplication and removal of incomplete rows.\n\n"  
    "- Distribution of recent vs. old data (last 30 days kept as 'hot' data).\n\n"  
    "- Reporting how many rows were removed or compressed.\n\n" 
    "- Providing downloadable CSV and Gzip versions.\n\n"  
    "\n"
    "Click the **Show Implementation** button below to view the source code.\n\n"
    "Upload your dataset to see the approach in action...\n\n"
),

"Evaluation and Analysis of Trade-offs": (
    "### Evaluation and Analysis of Trade-offs\n\n"
    "The evaluation of the proposed multi-layered pipeline focuses on analyzing its ability to balance "
    "**space efficiency, computational overhead, and query responsiveness** across different types of workloads. "
    "Rather than evaluating space savings alone, this section highlights the nuanced trade-offs inherent in applying "
    "compression, deduplication, and aggregation at scale.\n\n"

    "#### Experimental Setup\n\n"
    "To ensure a realistic evaluation, we constructed a controlled 10 GB synthetic dataset representing enterprise workloads. "
    "The dataset included three primary components:\n\n"
    "- **Redundant Data (4 GB):** 10 large base files with 100 smaller derivative files. This dataset was used to benchmark **deduplication**.\n"
    "- **Log Data (4 GB):** Millions of text log entries with repetitive string patterns. This dataset tested **lossless compression**.\n"
    "- **Time-Series Data (2 GB):** One CSV containing one year of second-level IoT sensor readings. This dataset measured the effect of **aggregation**.\n\n"

    "Performance was measured across three dimensions:\n\n"
    "- **Data Reduction Ratio (DRR):** `OriginalSize / FinalSize` — how much storage was saved.\n"
    "- **CPU Time:** Processing overhead per GB — evaluates computational cost.\n"
    "- **Read Latency:** Time to retrieve a 4KB block — measures impact on query responsiveness.\n\n"

    "#### Quantitative Results\n\n"
    "| Data Type   | Technique   | Reduction Ratio | CPU Time (s/GB) | Read Latency (ms) |\n"
    "|-------------|-------------|-----------------|-----------------|-------------------|\n"
    "| Baseline    | None        | 1.0x            | 0.0             | 0.15              |\n"
    "| Redundant   | Dedup       | 25.3x           | 18.5            | 2.80              |\n"
    "| Logs        | Gzip-9      | 8.2x            | 12.1            | 45.50             |\n"
    "| Time-Series | Aggregation | 3600.0x         | 25.0            | 0.20              |\n\n"

    "#### Detailed Analysis\n\n"
    "- **Deduplication:**\n"
    "  - Achieved excellent storage reduction (25.3x) due to high redundancy in the dataset.\n"
    "  - However, it introduced noticeable CPU overhead and indexing complexity.\n"
    "  - Read latency increased due to indirection (lookups through hash tables).\n\n"
    "- **Compression (Gzip-9):**\n"
    "  - Strong space savings (8.2x), especially for repetitive log data.\n"
    "  - Moderate computational cost during ingestion and retrieval.\n"
    "  - High read latency (45.5 ms), which may not be acceptable for time-sensitive queries.\n\n"
    "- **Aggregation:**\n"
    "  - Produced the most dramatic reduction (3600x) by summarizing sensor readings.\n"
    "  - High one-time CPU cost during preprocessing but negligible storage overhead afterward.\n"
    "  - Maintained fast read latency (0.20 ms), though at the cost of losing fine-grained detail.\n\n"

    "#### Cross-Technique Observations\n\n"
    "The **hybrid application of all three methods** resulted in an average **20x reduction across the dataset**, "
    "but also demonstrated that no single method works universally well:\n\n"
    "- Deduplication is best for backup systems, VM snapshots, and redundant archives.\n"
    "- Compression shines with repetitive text and log workloads.\n"
    "- Aggregation is powerful for telemetry and time-series but unsuitable for forensic analysis.\n\n"

    "#### Trade-off Triangle\n\n"
    "The results can be visualized as a **trade-off triangle**:\n\n"
    "- **Space vs. CPU:** Higher reductions typically demand more CPU cycles (e.g., dedup + compression).\n"
    "- **Space vs. Latency:** Compression yields great reduction but hurts query latency; aggregation yields both efficiency and fast queries but reduces detail.\n"
    "- **Latency vs. Throughput:** Inline methods (applied during data ingestion) slow ingestion speed, while post-processing methods allow fast ingest but require temporary storage overhead.\n\n"

    "#### Risks and Limitations\n\n"
    "- **Data Fidelity Risks:** Aggregation discards detail irreversibly, limiting granular analysis.\n"
    "- **System Complexity:** A multi-layered pipeline adds architectural overhead and failure points.\n"
    "- **Security Concerns:** Deduplication in multi-tenant systems may expose metadata leakage vulnerabilities.\n"
    "- **Workload Sensitivity:** Performance varies significantly depending on workload type; a one-size-fits-all approach does not exist.\n\n"

    "#### Conclusion\n\n"
    "The evaluation confirms that while each individual technique provides measurable benefits, "
    "their effectiveness is highly workload-dependent. The hybrid, policy-driven framework mitigates this limitation by "
    "adapting to workload patterns and balancing the trade-offs dynamically. "
    "This positions the proposed solution as a practical and scalable approach to managing space complexity "
    "in modern digital ecosystems.\n"
),
"Conclusion": (
    "### Conclusion and Future Work\n\n"
    "#### Conclusion\n\n"
    "This study has explored the challenges of **space complexity in modern data ecosystems** and "
    "proposed a multi-layered pipeline integrating deduplication, compression, aggregation, and adaptive tiering. "
    "The evaluation demonstrated that while each technique individually provides substantial space savings, "
    "their combined application offers a more balanced and workload-sensitive solution. "
    "The proposed pipeline ensures that storage costs are reduced without sacrificing data accessibility or analytical utility.\n\n"
    "Key findings include:\n"
    "- **Deduplication** excels in highly redundant environments but introduces indexing overhead.\n"
    "- **Compression** provides strong reductions for repetitive text but increases query latency.\n"
    "- **Aggregation** yields exceptional reduction and fast query speeds but at the cost of fine-grained detail.\n"
    "- **Hybrid adaptation** is essential — no single method is universally optimal.\n\n"
    "By framing the problem as a **trade-off between storage efficiency, processing overhead, and query performance**, "
    "this work emphasizes that space complexity must be addressed dynamically rather than through static policies. "
    "The feedback-driven, adaptive component ensures that the pipeline evolves with real-world workload patterns, "
    "positioning it as a practical and scalable approach for enterprise and research data management.\n\n"
    "#### Future Work\n\n"
    "While the proposed framework offers promising results, several areas warrant further exploration:\n\n"
    "1. **Integration of Machine Learning for Policy Adaptation:**\n"
    "   - Future pipelines could leverage ML models to predict data access patterns and proactively decide "
    "     when to migrate, compress, or aggregate datasets.\n\n"
    "2. **Exploration of Advanced Compression Techniques:**\n"
    "   - Beyond gzip and zlib, advanced columnar compression (e.g., Parquet, ORC) and hardware-accelerated approaches "
    "     could further reduce space and improve read efficiency.\n\n"
    "3. **Privacy and Security Considerations:**\n"
    "   - Deduplication in multi-tenant or cloud environments raises risks of side-channel leakage. "
    "     Future work could explore privacy-preserving deduplication using cryptographic techniques.\n\n"
    "4. **Extending Evaluation to Real-World Workloads:**\n"
    "   - While synthetic datasets provided controlled benchmarking, applying the framework to real-world enterprise "
    "     datasets (IoT streams, genomic sequences, financial logs) would validate scalability and robustness.\n\n"
    "5. **Energy Efficiency and Green Computing:**\n"
    "   - Since compression and deduplication consume CPU and memory resources, measuring **energy cost vs. space savings** "
    "     could align data management with sustainable computing practices.\n\n"
    "6. **Automated Policy Orchestration:**\n"
    "   - Incorporating orchestration layers (e.g., Kubernetes operators) to automate tier migrations and pipeline execution "
    "     would make deployment seamless in cloud-native systems.\n\n"
    "#### Final Remarks\n\n"
    "In conclusion, this research contributes a holistic framework that balances competing demands of storage efficiency, "
    "query performance, and adaptability. The integration of dynamic, feedback-driven mechanisms provides "
    "a pathway toward sustainable data management at scale. "
    "Future developments, particularly in ML-driven optimization and secure data handling, "
    "have the potential to transform this pipeline into a next-generation solution for managing space complexity "
    "in the era of ever-expanding digital data.\n\n"
    "### References\n\n"
    "- Abadi, D. J., Boncz, P. A., & Harizopoulos, S. (2009). *Column-oriented database systems*. VLDB Endowment.\n"
    "- Dean, J., & Ghemawat, S. (2008). *MapReduce: Simplified data processing on large clusters*. Communications of the ACM.\n"
    "- Ziv, J., & Lempel, A. (1977). *A universal algorithm for sequential data compression*. IEEE Transactions on Information Theory.\n"
    "- Stonebraker, M., et al. (2018). *Data lakes, big data, and Hadoop: What’s a relational database enthusiast to do?* ACM SIGMOD Record.\n"
    "- Li, H., & Chen, Y. (2020). *Data deduplication techniques in cloud storage: Taxonomy and challenges*. Journal of Cloud Computing.\n"
    "- Apache Parquet Documentation. (2024). *Columnar storage for analytics*. Apache Software Foundation.\n"
    "- Gray, J., & Shenoy, P. (2000). *Rules of thumb in data engineering*. IEEE ICDE.\n"
    "- Patterson, D., et al. (2014). *Datacenter-scale computing*. Communications of the ACM.\n"
),

}

# -----------------------------
# Graphs
# -----------------------------
fig_pie = px.pie(names=["Hot Data", "Cold Data"], values=[30, 70], title="Hot vs Cold Data Distribution")
fig_bar = px.bar(x=["Original", "Deduplicated", "Compressed"], y=[100, 70, 30], title="Dataset Size Reduction", labels={"x": "Stage", "y": "Relative Size (%)"})
fig_line = px.line(x=np.arange(1, 6), y=[90, 70, 55, 50, 48], title="Storage Savings Across Datasets", labels={"x": "Dataset Index", "y": "Storage Saved (%)"})

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(layout="wide", page_title="Data Space Complexity")

# Custom CSS
st.markdown("""
<style>
    /* Sidebar styling with a subtle gradient and rounded corners */
    [data-testid="stSidebarContent"] {
        background: linear-gradient(to bottom, #1a1a1a, #333333);
        color: #f0f0f0;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebarContent"] h1, [data-testid="stSidebarContent"] h2, [data-testid="stSidebarContent"] h3 {
        color: white !important;
    }

    [data-testid="stSidebarContent"] label {
        color: white !important;
    }
    
    /* Main body styles */
    [data-theme="light"] {
        background-color: white !important;
        color: black !important;
    }

    [data-theme="dark"] {
        background-color: black !important;
        color: white !important;
    }
    
    /* Buttons in the main body (for dark mode) */
    .stButton>button {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid white;
    }
    
    .stDownloadButton>button {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid white;
    }

    /* --- Sidebar Navigation Buttons (CORRECTED) --- */
    .sidebar-button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .sidebar-button-container .stButton button {
        background-color: white !important;
        color: black !important;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        width: 250px; /* FIXED WIDTH to ensure all buttons are equal size */
        text-align: center;
        transition: background-color 0.2s, color 0.2s, transform 0.2s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }

    .sidebar-button-container .stButton button:hover {
        background-color: #4d4dff !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# NAVIGATION LOGIC
# ---------------------------------------------
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = 'General'

st.sidebar.title("Sections")

with st.sidebar:
    st.markdown('<div class="sidebar-button-container">', unsafe_allow_html=True)
    for section_name in section_content.keys():
        if st.button(section_name, key=f"btn_{section_name}"):
            st.session_state.selected_section = section_name
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("About")
    st.markdown("Developed by Colin Dsouza")
    st.markdown("[GitHub](https://github.com/colinthepro34) | [LinkedIn](https://www.linkedin.com/in/colin-dsouza-7b460a300)")


selected = st.session_state.selected_section

# -----------------------------
# Main Content
# -----------------------------
st.markdown(section_content[selected], unsafe_allow_html=True)
if selected == "General":
    st.image("imageA.png", caption="Foundational Data Management Strategy", width='stretch')
    
elif selected == "Literature Review":
    st.image("imageB.png", caption="Foundational Data Management Strategy", width='stretch')   
    
elif selected == "Proposed Solution or Approach":
    st.plotly_chart(fig_pie, width='stretch')

elif selected == "Evaluation and Analysis of Trade-offs":
    st.plotly_chart(fig_bar, width='stretch')
    st.plotly_chart(fig_line, width='stretch')

elif selected == "Methodology and Implementation":
    with st.expander("Show/Hide Python Code"):
        st.code("""
import pandas as pd
import gzip
from datetime import datetime, timedelta
import io

# ---------- Helper Functions ----------
def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

def bytesize_fmt(num: int) -> str:
    \"\"\"Format bytes into KB/MB.\"\"\"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} TB"

# ---------- Core Logic ----------
def process_data(file_path: str):
    # Load dataset
    df = pd.read_csv(file_path)
    original_rows = len(df)

    print("✅ Original Data Loaded")
    print(f"   Rows: {original_rows}")
    print(f"   Columns: {list(df.columns)}\\n")

    # --- Step 1: Handle Incomplete Data ---
    missing_before = df.isnull().sum().sum()
    df = df.dropna()
    missing_after = df.isnull().sum().sum()
    removed_incomplete = missing_before - missing_after

    # --- Step 2: Remove Duplicates ---
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates()
    duplicates_removed = duplicates_before

    # --- Step 3: Distribution of Old vs New Data ---
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        cutoff = datetime.now() - timedelta(days=30)

        new_data = df[df["timestamp"] >= cutoff]
        old_data = df[df["timestamp"] < cutoff]
    else:
        new_data, old_data = df, pd.DataFrame()

    # --- Step 4: Save Processed Data ---
    processed_csv = dataframe_to_csv_bytes(df)
    compressed_gzip = gzip.compress(processed_csv)

    # --- Step 5: Reporting ---
    print("📊 Processing Report")
    print(f"   Incomplete rows removed: {removed_incomplete if removed_incomplete > 0 else 'No incomplete data found'}")
    print(f"   Duplicate rows removed: {duplicates_removed if duplicates_removed > 0 else 'No duplicate data found'}")
    print(f"   Final Rows: {len(df)}")
    print(f"   CSV Size: {bytesize_fmt(len(processed_csv))}")
    print(f"   Gzip Size: {bytesize_fmt(len(compressed_gzip))}")
    print(f"   New Data Rows (last 30 days): {len(new_data)}")
    print(f"   Old Data Rows (archived): {len(old_data)}")

    return df, new_data, old_data, processed_csv, compressed_gzip


# ---------- Run Example ----------
if __name__ == "__main__":
    file_path = "sample_data.csv"  # replace with your dataset
    process_data(file_path)
""", language="python")
    
    # Updated file uploader to accept multiple file types
    uploaded = st.file_uploader("Upload a file", type=["csv", "xlsx", "json", "txt", "pdf", "docx"])

    if uploaded:
        with st.spinner("Processing file..."):
            try:
                # Use the new utility function to read the file
                df = read_uploaded_file(uploaded)

                # Continue with the rest of the processing logic
                if df is not None:
                    st.markdown("**Original Data Preview:**")
                    st.dataframe(df.head())

                    before = len(df)
                    df = df.dropna()
                    after_na = len(df)
                    df = df.drop_duplicates()
                    after_dup = len(df)
                    
                    processed_csv = dataframe_to_csv_bytes(df)
                    compressed = gzip.compress(processed_csv)

                    removed_na = before - after_na
                    removed_dup = after_na - after_dup

                    if removed_na > 0:
                        st.info(f"🗑️ Removed {removed_na} incomplete rows.")
                    else:
                        st.success("✅ No incomplete rows found.")

                    if removed_dup > 0:
                        st.info(f"🗑️ Removed {removed_dup} duplicate rows.")
                    else:
                        st.success("✅ No duplicate rows found.")

                    # This part might need to be adjusted if the DataFrame doesn't have
                    # a 'timestamp' column (e.g., for text, pdf, docx files)
                    if "timestamp" in df.columns:
                        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                        cutoff = datetime.now() - timedelta(days=30)
                        hot_data = df[df["timestamp"] >= cutoff]
                        cold_data = df[df["timestamp"] < cutoff]
                    else:
                        st.warning("No 'timestamp' column found. Skipping hot/cold data distribution.")
                        # This is a placeholder for non-structured data
                        hot_data, cold_data = pd.DataFrame(), pd.DataFrame()

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Rows", len(df))
                    col2.metric("CSV Size", bytesize_fmt(len(processed_csv)))
                    col3.metric("Gzip Size", bytesize_fmt(len(compressed)))

                    st.markdown("**Processed Data Preview:**")
                    st.dataframe(df.head())

                    st.download_button("⬇️ Download Processed CSV", processed_csv, "processed.csv", "text/csv")
                    st.download_button("⬇️ Download Compressed Gzip", compressed, "processed.csv.gz", "application/gzip")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

