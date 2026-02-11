# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.19.2",
#     "pandas==2.3.3",
#     "python-lsp-ruff==2.3.0",
#     "python-lsp-server==1.14.0",
#     "vl-convert-python==1.9.0",
#     "websockets==16.0",
# ]
# ///

import marimo

__generated_with = "0.19.10"
app = marimo.App(
    width="medium",
    layout_file="layouts/2026-sql-data-modeling.slides.json",
    auto_download=["html"],
    sql_output="native",
)

with app.setup(hide_code=True):
    # Initialization code that runs before all other cells
    import marimo as mo
    import pandas as pd

    user_data = pd.read_csv(mo.notebook_location() / "public/data/fake_user_data.csv")


@app.cell(hide_code=True)
def _():
    title = mo.md(r"""# Data Modeling and SQL Databases""")
    author = mo.md(r"### Eli Mizrachi (they/them)")
    subsubtitle = mo.md("""SLAC National Accelerator Laboratory""")
    mo.vstack([title, author, subsubtitle], align="center", justify="center")
    return


@app.cell(hide_code=True)
def _():
    title1 = mo.md("## Outline")
    content1 = mo.md(r"""
    - Data Modeling
    - Data Transformation
    - SQL Databases
    - Closing thoughts
    """)

    # Everyone is secretly a data engineer, mechanical engineer, chemical engineer
    # We're all just bad at those jobs

    image1 = mo.image(
        "https://images.pexels.com/photos/86596/owl-bird-eyes-eagle-owl-86596.jpeg",
        width=300,
        height=300,
        caption="owl",
    )

    mo.vstack([title1, mo.hstack([content1, image1], gap=10, justify="start")], align="start")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    A Brief History of

    # Data Modeling
    """)
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("##  The Hierarchical Model")
    _col1 = mo.md(r"""
    - 1963: Rockwell Int'l requests part tracking system from IBM for Apollo program
    - 1965: Berman (IBM) and Nordyke (Rockwell) develop Disk Applications in a Teleprocessing Environment (DATE)
      - Decouple disk access from applications which execute queries against data
    - 1968: Information Control System/Data Language Interface (ICS/DL/I) begins operating
      - Sold as Information Management System (IMS) and still [available for purchase](https://www.ibm.com/products/ims)

    Sources: IBM ([1](https://www.ibm.com/history/information-management-system), [2](www.ibm.com/docs/en/zos-basic-skills?topic=now-history-ims-beginnings-nasa)), Computer History Museum ([1](https://www.computerhistory.org/collections/catalog/500001032))
    """)

    _col2 = mo.md("""
    ```ascii
    Rocket
    ├── Engine
    │   ├── #4-40 Screw
    │   │   └── QTY: 5
    │   └── #4-40 Nut
    │       └── QTY: 5
    └── Fuel Tank
        ├── #4-40 Screw
        │   └── QTY: 2
        └── #4-40 Nut
            └── QTY: 3
    ```
    Rocket BOM for demonstration purposes only
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.60, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("## The Relational Model")
    _col1 = mo.md(r"""
    - 1970: Edgar Codd (IBM) publishes mathematical formalism of relational model for databases to escape constraints of hierarchical model ([1](https://dl.acm.org/doi/10.1145/362384.362685), [2](https://www.ibm.com/history/relational-database))
      - Store data in relational tables, identify rows with "keys", operations to query data
    - 1974: Structured English Query Language (SEQUEL) developed by Bryce (IBM) and Chamberlin (IBM) ([3](https://dl.acm.org/doi/10.1145/800296.811515))
      > ...identify the basic functions that are required by database users and develop a simple and consistent set of rules for applying these functions to data.
    """)

    _col2_1 = mo.md("""
    | EMP | NAME  | SAL   | MGR      | DEPT       |
    |-----|-------|-------|----------|------------|
    |     | SMITH | 10000 | JONES    | TOY        |
    |     | JONES | 12000 | ANDERSON | FURNITURE  |
    |     | LEE   | 10000 | THOMAS   | APPLIANCES |
    """)

    _query = mo.md("""
    ```ascii
    SELECT NAME
    FROM   EMP
    WHERE  DEPT = 'TOY'
    ```
    """)

    _cap = mo.center(mo.md("The Original SQL Query"))

    _col2_2 = mo.vstack([_query, _cap])

    mo.hstack([mo.vstack([_title, _col1]), mo.vstack([_col2_1, _col2_2])], align="center", widths=[0.60, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Entity-Relationship Model""")

    _col1 = mo.md(r"""
    - 1976: Peter Chen (MIT) publishes entity-relationship (ER) model ([1](https://dl.acm.org/doi/10.1145/320434.320440))
    - Specified three categories of relationships between "entities" (i.e. nouns):
      - $1:1$ "one-to-one"
      - $1:n$ "one-to-many"
      - $n:m$ "many-to-many"
    - Extremely useful abstraction for reasoning about how real-world data is structured
      - Can derive hierarchical, relational models, or others
    """)

    _col2 = mo.image("public/img/chen-er-fig10.png")

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.6, 0.40])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    An Example of

    # Data Transformation
    """)
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md(r"""
    ## LZ Service Management

    Users in LZ often have multiple kinds of accounts for various services: gitlab, NERSC, online, slack, email, twiki.
    """)

    _col1 = mo.md("""- $1:1$: One user has **one** name, and one name identifies **one** user 😬
    - $1:n$: One account belongs to **one** user, and one user can have **many** accounts
      - Sometimes users have multiple accounts with a single service (e.g. email)!
    - $n:m$: One user can access **many** services, and services can have **many** users
    """)

    _col2 = user_data

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.60, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md(r"""
    ## Don't Try This At Home

    What's wrong with this?
    """)

    _col1 = mo.md("""
    - New services require new columns (can mean downtime for a database)
        - Data on services is embedded in column names
    - Awkward for users with multiple accounts on same service
    - Hard to query "all users of a service" or "all services for a user"
    - Users can change names, or share names
    """)

    _col2 = user_data

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.60, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("## Approaches to Data Transformation")

    _col1 = mo.md(r"""
    - Imperative programming: high probability of reinventing the wheel with nested loops
      - Please don't use plain python for this (unless using [numba](https://numba.pydata.org/))
    - Arrays (e.g. `numpy`, `awkward`): great for "low-level" operations
      - N.B. `pandas` is/was a fancy wrapper around `numpy`
    - Databases & Dataframes: lots of convenient functions for cleaning, querying, restructuring data
      - Can still use [`ufuncs`](https://numpy.org/doc/stable/reference/ufuncs.html) (universal functions) with little overhead
    """)

    _col2 = mo.mermaid("""
    %%{init: {'theme': 'neutral'} }%%
    graph TD
        IMP[**Imperative Programming**<br>Manual & Procedural]
        NP[**Arrays**<br>Vectorized & Positional]
        DF[**Databases & Dataframes**<br>Vectorized & Semantic]

        IMP --> NP
        NP --> DF

        style DF fill:#d4edda,stroke:#28a745,stroke-width:2px
        style NP fill:#fff3cd,stroke:#ffc107,stroke-width:2px
        style IMP fill:#f8d7da,stroke:#dc3545,stroke-width:2px

        linkStyle 0,1 stroke-width:2px;
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.6, 0.4])
    return


@app.cell
def _():
    split_user_data_code = mo.ui.code_editor(
        """split_user_data = user_data.assign(email=user_data["email"].str.split(", "))""", show_copy_button=False
    )
    return (split_user_data_code,)


@app.cell
def _(split_user_data_code):
    _ns = dict(globals())
    exec(split_user_data_code.value, _ns)
    split_user_data = _ns.get("split_user_data")
    return (split_user_data,)


@app.cell
def _(split_user_data, split_user_data_code):
    _title = mo.md("""## Step 1: Split User Data""")

    _col1 = mo.md("""
    - We have a comma-separated list in the e-mail column
    - Let's override it with a new one that makes it into a column of lists
    """)

    _col2 = mo.vstack([split_user_data_code, split_user_data])

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.45, 0.60])
    return


@app.cell
def _():
    un_nest_user_data_code = mo.ui.code_editor(
        """un_nest_split_user_data = split_user_data.explode("email", ignore_index=True)""",
        show_copy_button=False,
        disabled=True,
    )
    return (un_nest_user_data_code,)


@app.cell
def _(un_nest_user_data_code):
    _ns = dict(globals())
    exec(un_nest_user_data_code.value, _ns)
    un_nest_split_user_data = _ns.get("un_nest_split_user_data")
    return (un_nest_split_user_data,)


@app.cell
def _(un_nest_split_user_data, un_nest_user_data_code):
    _title = mo.md("""## Step 2: First Normal Form""")

    _col1_1 = mo.md("""
    - It's a lot easier to do analysis with one value per cell!
    - Dataframe libraries have methods to unpack lists:
      - `pandas` has `explode`, `polars` has `unnest`
      - `json_normalize` can unpack JSON files
    - [1st Normal Form (1NF)](https://en.wikipedia.org/wiki/First_normal_form): 2-D array with unique rows, one value per cell
    - Still a bit awkward to query: who has the most e-mail accounts? How many accounts does each person have?
    """)

    _col2 = mo.vstack([un_nest_user_data_code, un_nest_split_user_data])

    mo.hstack([mo.vstack([_title, _col1_1]), _col2], align="center", widths=[0.45, 0.60])
    return


@app.cell
def _(un_nest_split_user_data):
    _title = mo.md("""## Step 2.5: Normal Forms and Keys""")

    _col1_1 = mo.md("""
    - Key is a column that uniquely define a row
      - Composite key: set of columns which identify a row
      - Non-keys are "attributes" (can think of object-oriented programming)  
    - [2NF](https://en.wikipedia.org/wiki/Third_normal_form): 1NF and attributes depend on _entire_ key
    - [3NF](https://en.wikipedia.org/wiki/Third_normal_form): 2NF and attributes depend on _only_ the key
    """)

    _col2 = mo.vstack([un_nest_split_user_data])

    mo.hstack([mo.vstack([_title, _col1_1]), _col2], align="center", widths=[0.45, 0.60])
    return


@app.cell
def _():
    un_pivot_user_data_code = mo.ui.code_editor(
        """unpivot_user_data = un_nest_split_user_data.melt(
        id_vars=["name"],
        value_vars=["gitlab", "email", "nersc"],
        var_name="service_name",
        value_name="account_name",
        ).drop_duplicates().dropna(ignore_index=True)""",
        show_copy_button=False,
        disabled=True,
    )
    return (un_pivot_user_data_code,)


@app.cell
def _(un_pivot_user_data_code):
    _ns = dict(globals())
    exec(un_pivot_user_data_code.value, _ns)
    unpivot_user_data = _ns.get("unpivot_user_data")
    return (unpivot_user_data,)


@app.cell
def _(un_pivot_user_data_code, unpivot_user_data):
    _title = mo.md("""## Step 3: Unpivot""")

    _col1_1 = mo.md("""
    - (`service_name`, `account_name`) _or_ (`name`, `service_name`) work as a 3NF key
    - Picking good keys and attributes ultimately requires domain knowledge
    - Recall users:services are $m:n$
    - What if one account could authenticate you with multiple services?
        - accounts:services would also be $m:n$
    - More complex relationships often require multiple tables...
    """)

    _col2 = mo.vstack([un_pivot_user_data_code, unpivot_user_data])

    mo.hstack([mo.vstack([_title, _col1_1]), _col2], align="center", widths=[0.45, 0.60])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Living the

    # SQL DREAM[^1]

    [^1]: Databases Rule Everything Around Me
    """)
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("## Realities of Data Management")
    _col1 = mo.md("""
    - Modeling: "Should this be in one column, multiple columns, or a separate table?"
    - Transformation: "How can I reshape and modify my data and get it ready for analysis?"
    - ACID compliance
    - Replication: "Can we have another copy for performance/redunancy?"
    - Volume: "What if my data doesn't fit in RAM? Or on disk? Or on one machine?"
    """)

    _col2 = mo.callout("ℹ️ See backup for more; these are most related to SQL DBs", "info")

    mo.vstack([_title, mo.hstack([_col1, _col2])])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## SQL Databases""")
    _col1 = mo.md(r"""
    - Store data in rows ("records"), rows live in tables, tables live in databases
    - Some systems implement "catalogs" which house multiple databases
    - "NoSQL" databases also exist! (see backup)
      - Highly optimized for non-tabular data (e.g. vector stores, graphs)
      - Special mention: "Document" databases (store JSON-like data) have lost ground to SQL DBs which can handle JSON-like data
    """)

    _col2 = mo.mermaid("""
    graph BT
        Catalog[**Catalog**<br>Corporation]

        DB1[(**Database**<br>Subsidiary 1)]
        DB2[(**Database**<br>Subsidiary 2)]

        Table1[**Table**<br>Orders]
        Table2[**Table**<br>Customers]

        Row1(**Row 1**)
        Row2(**Row 2**)
        Row3(**Row 3**)

        Catalog --> DB1
        Catalog --> DB2

        DB1 --> Table1
        DB1 --> Table2

        DB2 ~~~ Table1
        DB2 ~~~ Table2

        Table1 --> Row1
        Table1 --> Row2
        Table1 --> Row3

        Table2 ~~~ Row1
        Table2 ~~~ Row2
        Table2 ~~~ Row3
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.60, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## ACID Compliance""")
    _col1 = mo.md(r"""
    - Atomicity: all operations in a transaction complete, or none of them do
    - Consistency: validation mechanisms and constraints, e.g "Why is this phone number 13 digits?"
    - Isolation: handle concurrent updates to the same data
    - Durability: changes should be saved to non-volatile memory to resist crashes/corruption
    """)

    _col2 = mo.mermaid("""
    %%{
      init: {
        'themeVariables': {
          'fontSize': '50px'
        }
      }
    }%%
    flowchart TB

    A["Atomicity <br> 🧩"]
    C["Consistency <br> ✅"]
    I["Isolation <br> 🔒"]
    D["Durability <br> 💎"]

    A~~~C 
    I~~~D
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.65, 0.30])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""
    ## Data Replication
    """)

    _col1 = mo.md(r"""
    - Sometimes you need another copy of your data
      - If too many people need access
      - If regulations require storage in multiple geographic regions
      - For redundancy/backups
    - Databases have declarative configurations for replication
    """)

    _col2 = mo.mermaid("""
    graph TB
        subgraph "US Region"
            US_APP[Application]
            US_DB[(Primary Database<br/>Read/Write)]
        end

        subgraph "EU Region"
            EU_APP[Application]
            EU_DB[(Replica Database<br/>Read-Only<br/><br/>GDPR Compliance:<br/>EU citizen data<br/>stays in EU)]
        end

        subgraph "Asia Region"
            ASIA_APP[Application]
            ASIA_DB[(Replica Database<br/>Read-Only<br/><br/>Low latency<br/>for local users)]
        end

        US_APP -->|Write| US_DB
        US_APP -->|Read| US_DB

        US_DB -.->|Replication| EU_DB
        US_DB -.->|Replication| ASIA_DB

        EU_APP -->|Read| EU_DB
        EU_APP -.->|Write requests| US_DB

        ASIA_APP -.->|Write requests| US_DB
        ASIA_APP -->|Read| ASIA_DB
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.35, 0.60])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Data Volume""")
    _col1 = mo.md(r"""
    - Sometimes you have gigabytes/terabytes/petabytes of data
    - Offload work to the database: save battery life and move less data across a network
    - What if your data doesn't fit into RAM or on your hard drive(s)?
    - Databases can easily query data on disk, let alone in RAM
      - Ran out of disk? Distributing ("sharding") across multiple machines is hard (for anything, not just DBs) but possible
    """)

    _fig1 = mo.mermaid("""
    graph TD
        A[(Table 1<br>Table 2<br>Table 3<br>Monolith Database<br>)] --> B[(Table 1.1.1...15<br>Table 2.1.1...15<br>Table 3.1.1...15<br>Physical Database 3)]
        A --> C[(Table 1.2.1...15<br>Table 2.2.1...15<br>Table 3.2.1...15<br>Physical Database 2)]
        A --> D[(Table 1.3.1...15<br>Table 2.3.1...15<br>Table 3.3.1...15<br>Physical Database 3)]
    """)

    _cap1 = mo.md("""Sharding case study at [Notion](https://www.notion.com/blog/sharding-postgres-at-notion)""")

    _col2 = mo.vstack([_fig1, mo.center(_cap1)])

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.45, 0.50])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Types of SQL Databases

    - Row-oriented (transactional)
    - Columnar (analytical)
      - Lakehouse
    """)
    return


@app.cell
def _():
    _title = mo.md(r"""### Row-Oriented Database""")
    _col1 = mo.md("""
    - Optimized for access to all information in a row
    - Great for reading or writing to individual rows
      - AKA "transactional" workloads where you need information on a specific record
    - e.g. PostgreSQL, MySQL
    """)
    _col2 = mo.image(
        "public/img/clickhouse-row-oriented.svg",
        caption="<a href='https://clickhouse.com/docs/knowledgebase/columnar-database'>Clickhouse</a>",
        width="1200px"
    )

    mo.hstack([mo.vstack([_title, _col1]), _col2], widths=[0.4, 0.6])
    return


@app.cell
def _():
    _title = mo.md(r"""### Column-Oriented Database""")
    _col1 = mo.md("""
    - Optimized for access to all information in a column
    - Great for reading about multiple records at once
      - AKA "analytical" workloads where you only need specific columns
    - e.g Clickhouse, DuckDB 
    """)
    _col2 = mo.image(
        "public/img/clickhouse-col-oriented.svg",
        caption="<a href='https://clickhouse.com/docs/knowledgebase/columnar-database'>Clickhouse</a>",
        width="1200px"
    )

    mo.hstack([mo.vstack([_title, _col1]), _col2], widths=[0.4, 0.6])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Drawbacks""")

    _col1 = mo.md(r"""
    - Databases require serious infrastructure support e.g. networking, containers/virtual machines...
    - Different SQL dialects and features for different databases
    - Less accessible than a simple filesystem (can be scary)
    - Data models and schemas can be challenging to manage
    """)

    _col2 = mo.callout(
        "⚠️ You will need to manage your schema eventually! Downstream management is good for flexibility but bad for concistency.",
        "warn",
    )

    mo.vstack([_title, mo.hstack([_col1, _col2])])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Data Lakehouse""")
    _col1 = mo.md(r"""
    - "Data Warehouse": analytical database with cleaned and joined data ready for queries
      - Pay for compute (expensive) and disk (cheap), overhead to maintain rigid schemas  
    - "Data Lake": Filesystem with assorted, unprocessed files (e.g. `CSV`, `JSON`, images)
      - Pay mostly for disk, compute what you need, no governance--watch the mess grow
    - "Data Lakehouse": Filesystem with columnar file formats like `.parquet`, `.root`
      - Files are tracked and managed, then _metadata_ is warehoused in a "catalog"
    """)

    _col2 = mo.mermaid("""
    flowchart TB

    WH["**90s-00s**<br>Data Warehouse"]
    DL["**2010s**<br>Data Lake"]
    LH["**2020s**<br>Data Lakehouse"]

    WH-->DL-->LH
    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.6, 0.35])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Data Lakehouse Concept""")
    _col1 = mo.md(r"""
    - Query your catalog to find out which files you need 
    - Process files with an engine: ALPACA, DuckDB, `polars`...
    - Similar cost to a data lake (catalog is $~10^6$ smaller than data)
    - Can support schemas and schema evolution, ACID
    - Warehouse-like system scales "easily" to petabytes
    - Drawbacks: still requires tuning, creates tons of (well-organized) files
    """)

    _col2 = mo.mermaid("""
    sequenceDiagram
        autonumber
        participant User
        participant Storage as Filesystem <br> (e.g. CFS)
        participant Catalog as Data<br>Catalog

        User->>Catalog: SELECT path FROM files<br>WHERE run in (1234)
        Catalog->>User: File list: [file1.root, file2.root]
        loop For each file
            User->>Storage: Get events from file
            loop For each event
                User->>Storage: Process event
            end
        end

    """)

    mo.hstack([mo.vstack([_title, _col1]), _col2], align="center", widths=[0.40, 0.60])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Closing Thoughts
    """)
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("""## Summary: How can SQL databases help?""")
    _col1 = mo.md(r"""
    - ACID compliance for reliability
    - Replication for safety/availability
    - Scalable for large volumes of data
    - Highly compatible with data modeling and transformations
    - Handle computation and move less data across a network
    """)

    _col2 = mo.callout("ℹ️ Subsets of these apply to NoSQL databases", "info")

    mo.vstack([_title, mo.hstack([_col1, _col2])])
    return


@app.cell(hide_code=True)
def _():
    _title = mo.md("## Takeaways")

    _col1 = mo.md(r"""
    - Good data modeling can make analysis more flexible
      - Don't be afraid to make more tables!
    - Databases can do many transformations
      - Dataframes can do even more
    - SQL isn't going anywhere
      - Dataframes are a great way to pick up concepts
    """)

    _col2 = mo.callout(
        "✅ Local engines like DuckDB+ibis, or `polars` are outstanding for querying multiple `.parquet` files on a single node.",
        "success",
    )

    mo.hstack([mo.vstack([_title, _col1]), _col2], widths=[0.45, 0.55])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Next Time?

    - LZ Metadata Databases
      - The Fate of the LZ Run DB Viewer
    - Advanced queries with ibis: joins, gaps and islands, ranking, aggregations
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Backup
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## NoSQL Databases

    - Vector: embed everything in a vector space, do similarity searches.
    - Document: basically JSON, store hierarchical data
    - Key-value: Lots of key-value pairs. Fast lookup and retrieval
    - Graph: lots of nodes and edges
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## More Realities

    - Frequency: "Can this change in 'real-time' I add or modify a new entry?"
    - Orchestration: "How can we schedule these jobs and their dependencies?"
    - Sources and sinks: `.root`, `.xlsx`, `.parquet`, `.CSV`, `.json`, databases, APIs...
    - Versioning: "my_dataset_v34.csv"
    - Lineage: "How did you create that column?"
    - Visualization: "Can I get a dashboard for this?"
    """)
    return


if __name__ == "__main__":
    app.run()
