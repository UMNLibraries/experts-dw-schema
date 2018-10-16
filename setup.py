# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['experts_dw']

package_data = \
{'': ['*']}

install_requires = \
['cx_oracle', 'sqlalchemy', 'sqlalchemy_mptt']

setup_kwargs = {
    'name': 'experts-dw',
    'version': '3.0.0',
    'description': 'Tools for working with the Experts@Minnesota Data Warehouse.',
    'long_description': '# Experts@Minnesota Database Schema\n\nSchema for the [Experts@Minnesota project](https://www.lib.umn.edu/about/experts) database.\n\n## Overview\n\nUMN Libraries created this database to complement the Elsevier product, Pure, which we have branded\n[Experts@Minnesota](https://experts.umn.edu). We did this both to provide alternative means of access\nto some of the data, as well as to maintain a vendor-independent, UMN-local copy of that data.\n\n## Access\n\nRead-only direct SQL access is available to anyone with a UMN internet ID. This database is on the OIT Oracle Hotel,\ncurrently only on the tst instance, with access granted via the `oit_expert_rd_all` role, managed by OIT. Each role\nmember must be an Oracle Hotel account, or "schema" in Oracle-speak. These accounts can be personal internet IDs or\ndepartmental/functional accounts. Note that personal internet IDs must use Duo two-factor authentication, so a \nfunctional/departmental account will be better for non-interactive, automated access. For access to the role and\ndatabase connection information, and to optionally create an Oracle Hotel account, send email to: dbrequests@umn.edu\nThe DBAs at that address will probably tell you to go to the\n[Access Request Forms on Service Now](https://umnprd.service-now.com/nav_to.do?uri=%2Fhome.do) and fill out the\n"IT Hosted Databases" form with the information described above. If you already have an Oracle Hotel account you\nwant to use, it may be faster to just go to that form directly.\n\nAlso, Elsevier has just added to Pure a new JSON-based web services API, which we are currently evaluating. We had\noriginally planned to design and implement our own web services API. However, it seems the Pure JSON-based API may\nmeet user needs, so we are deferring that plan for now.\n\n## Announcements & Discussion\n\nAnnouncements and discussion about this database and other Experts@Minnesota services happen on both the\n__Experts Data Warehouse-API__ Google Group and on the __#research-activity__ channel on\n[Tech-People UMN Slack](https://tech-people-umn.slack.com). Both are open to anyone with a UMN internet ID.\n\n## Maturity\n\nIt may be charitable to assign this database an alpha level of maturity. Probably obvious that this repository\nis a bit of a mess. We want your feedback to help make it better! Our goal was to release a useful, usable\nproduct to users as soon as possible. We recognize that we can\'t give you exactly what you need or want without\nworking directly with you to find out what that is. Please join the user community discussion by following\nthe instructions above.\n\n## Data Model Design\n\nOf course the Pure data model heavily influenced the design of this data model, but \n[Citation Style Language (CSL)](http://docs.citationstyles.org/en/stable/index.html) was at least as big an influence.\nAgain, one goal was vendor-independence. CSL is a popular standard used by many citation managers. Another goal\nwas to find a robust data model already implemented in popular web services APIs.\n[csl-data.json](https://github.com/citation-style-language/schema/blob/master/csl-data.json) was the best such model\nwe could find. Our upcoming web services will adhere to it as closely as possible.\n\n### Organizational Complexity\n\nAs the diagrams and documentation below should make painfully obvious, the data model is most complex\nwherever organizations are involved. We especially welcome feedback from users about these parts of the\ndata model. There are likely many improvements we could make to allow for more convenient and performant \nqueries, as well as conceptual clarity and simplicity.\n \n## Entity Relationship Diagram (ERD)\n\nThe following diagrams are exports from [Oracle SQL Developer](http://www.oracle.com/technetwork/developer-tools/sql-developer/overview/index-097090.html).\n\n[Scalable version (PDF)](https://github.com/UMNLibraries/experts_dw/blob/master/erd.pdf)\n\n![ERD](erd.png)\n\n## Data Dictionary\n\nThe following information, in a separate section for each table, is in the database itself, in the form of\ncomments on all tables and columns. We re-produce it here for convenience.\n\n### PERSON\n\nA person, usually an author of research outputs. May be internal or external to UMN.\n\n| Column | Description |\n| ------ | ----------- |\n| UUID | Universally-unique ID for the person, generated for this Experts@Minnesota database. |\n| PURE_UUID | Universally-unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). |\n| PURE_ID | Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure. |\n| ORCID | [Open Researcher and Contributor ID](https://orcid.org/) for the person. |\n| SCOPUS_ID | Unique ID for the person in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus). |\n| HINDEX | An index that attempts to measure both the productivity and impact of the published work of a scientist or scholar. Used only in some disciplines, so for many persons this will be NULL. [More info](https://blog.scopus.com/posts/the-scopus-h-index-what-s-it-all-about-part-i) on [blog.scopus.com](https://blog.scopus.com/posts/5-facts-about-scopus-and-the-h-index). |\n| EMPLID | UMN employee ID (emplid). |\n| INTERNET_ID | UMN internet ID. |\n| FIRST_NAME | The given name for the person. |\n| LAST_NAME | The family name for the person. |\n| PURE_INTERNAL | "Y" if Pure classifies the person as UMN-internal, "N" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure. |\n\n### PUB\n\nResearch output. Named "pub", short for "publication", due to Oracle character-lenght limits.\n\n| Column | Description |\n| ------ | ----------- |\n| UUID | Universally-unique ID for the item, generated for this Experts@Minnesota database. |\n| PURE_UUID | Universally-unique ID for the item in our [Elsevier Pure database](https://experts.umn.edu). |\n| SCOPUS_ID | Unique ID for the item in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus). |\n| PMID | Unique ID for the item in the [NCBI PubMed database](https://www.ncbi.nlm.nih.gov/pubmed/). |\n| DOI | [Digital Object Identifier](https://www.doi.org/) for the item. |\n| TYPE | Publication type or format of the item. See the [CSL spec](http://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types) for a list of values. |\n| TITLE | Primary title of the item. |\n| CONTAINER_TITLE | Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a journal article). |\n| ISSUED | Date the item was issued/published. |\n| ISSUED_PRECISION | Precision of the ISSUED column, in days: 366 (year), 31 (month), 1 (day). |\n| VOLUME | Volume holding the item (e.g. “2” when citing a chapter from book volume 2). |\n| ISSUE | Issue holding the item (e.g. “5” when citing a journal article from journal volume 2, issue 5). |\n| PAGES | Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue). |\n| CITATION_TOTAL | Number of citations of the item. |\n| ISSN | [International Standard Serial Number](http://www.issn.org/understanding-the-issn/what-is-an-issn/). |\n| OWNER_PURE_ORG_UUID | Unique ID for the organization that owns the item in our [Elsevier Pure database](https://experts.umn.edu). |\n\n### PUB_PERSON\n\nAssociates research outputs with persons (authors).\n\n| Column | Description |\n| ------ | ----------- |\n| PUB_UUID | Foreign key to PUB. |\n| PERSON_UUID | Foreign key to PERSON. |\n| PERSON_ORDINAL | The position of the person in the author list for the research output in Pure. |\n| PERSON_ROLE | "author" or "editor". Need to find Pure documentation on any other possible values. |\n| PERSON_PURE_INTERNAL | "Y" if Pure classified the person as UMN-internal at the time of publication of the research output, "N" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure. |\n| FIRST_NAME | The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME. |\n| LAST_NAME | The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME. |\n| EMPLID | De-normalization column. See the description in PERSON. |\n\n### PURE_ORG\n\nAn organization (e.g. university, college, department, etc.) in Pure. May be internal or external to UMN. Pure requires all UMN-internal organizations to be part of a single hierarchy, with UMN itself as the root. Note that sometimes we combine multiple UMN departments into one Pure organization. UMN-external organizations are never part of a hierarchy in Pure, and Pure gives us limited information for them in general.\n\n| Column | Description |\n| ------ | ----------- |\n| PURE_UUID | Universally-unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). |\n| PURE_ID | Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations. |\n| PARENT_PURE_UUID | Universally-unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations. |\n| PARENT_PURE_ID | Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations. |\n| PURE_INTERNAL | "Y" if Pure classifies the organization as UMN-internal, "N" otherwise. |\n| TYPE | "academic", "college", "corporate", "department", "government", "initiative", "institute", "medical", "private non-profit", "university", or "unknown" |\n| NAME_EN | Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name. |\n| NAME_VARIANT_EN | An alternative name of the organization. Called "name_variant_en" to be consistent with Pure naming, and to indicate that this is an English name. |\n| URL | The website for the organization. |\n\n### PURE_INTERNAL_ORG\n\nThe hierarchy (tree) of Pure UMN-internal organizations. This tree uses [nested sets](https://en.wikipedia.org/wiki/Nested_set_model), as implemented by the Python package [sqlalchemy_mptt](https://pypi.python.org/pypi/sqlalchemy_mptt/). However, because Oracle supports [recursive queries](https://explainextended.com/2009/09/28/adjacency-list-vs-nested-sets-oracle/), this may not be the best implementation. Because parent-child relationships (adjacency lists) already exist in the PURE_ORG table, this entire table may be unnecessary and may go away.\n\n| Column | Description |\n| ------ | ----------- |\n| ID | The unique ID for the node. Defined by sqlalchemy_mptt. |\n| LFT | The left number for the node. Defined by sqlalchemy_mptt. |\n| PARENT_ID | The unique ID for the parent of the node. Defined by sqlalchemy_mptt. |\n| level | The depth (i.e. generation) of this node in the tree. Defined by sqlalchemy_mptt. |\n| RGT | The right number for the node. Defined by sqlalchemy_mptt. |\n| TREE_ID | The unique ID of the tree that contains the node. Defined by sqlalchemy_mptt, which supports multiple trees in a single table. |\n| PURE_UUID | See the description in PURE_ORG. |\n| PURE_ID | See the description in PURE_ORG. |\n| NAME_EN | See the description in PURE_ORG. |\n\n### UMN_DEPT_PURE_ORG\n\nAssociates UMN departments with Pure organizations. Note that many UMN departments may map to one Pure organization.\n\n| Column | Description |\n| ------ | ----------- |\n| UMN_DEPT_ID | Unique ID for the UMN department in PeopleSoft. |\n| UMN_DEPT_NAME | Name of the UMN department in PeopleSoft. De-normalization column. |\n| PURE_ORG_UUID | Foreign key to PURE_ORG. |\n| PURE_ORG_ID | De-normalization column. See the description in PURE_ORG. |\n\n### UMN_PERSON_PURE_ORG\n\nAssociates persons that Pure classifies as UMN-internal with Pure organizations. We use this table, in addition to PERSON_PURE_ORG, because Pure attaches far more data to UMN-internal persons, some of which we use to ensure row uniqueness. Note that there are four columns in the primary key: PURE_ORG_UUID, PERSON_UUID, JOB_DESCRIPTION, and START_DATE. This is because UMN-internal persons may change positions, and also organization affiliations, over time. There may be multiple rows for the same person in this table.\n\n| Column | Description |\n| ------ | ----------- |\n| PERSON_UUID | Foreign key to PERSON. |\n| PURE_ORG_UUID | Foreign key to PURE_ORG. |\n| JOB_DESCRIPTION | The description of this job in PeopleSoft. Maybe be better to use a job code here instead. |\n| EMPLOYED_AS | Always "Academic" for the data we have loaded so far. Uncertain whether we will have other values in the future. |\n| STAFF_TYPE | "academic" or "nonacademic". |\n| START_DATE | The date the person started this job with this organization. |\n| END_DATE | The date the person ended this job with this organization. |\n| PRIMARY | "Y" if this is the person"s primary organization affiliation, otherwise "N". |\n| EMPLID | De-normalization column. See the description in PERSON. |\n| PURE_PERSON_ID | De-normalization column. See the description for PERSON.PURE_ID. |\n| PURE_ORG_ID | De-normalization column. See the description for PURE_ORG.PURE_ID. |\n\n### PERSON_PURE_ORG\n\nAssociates persons with their organizations.\n\n| Column | Description |\n| ------ | ----------- |\n| PERSON_UUID | Foreign key to PERSON. |\n| PURE_ORG_UUID | Foreign key to PURE_ORG. |\n\n### PUB_PERSON_PURE_ORG\n\nAssociates with persons with their organization affiliations at the time of publication of a research output.\n\n| Column | Description |\n| ------ | ----------- |\n| PUB_UUID | Foreign key to PUB. |\n| PERSON_UUID | Foreign key to PERSON. |\n| PURE_ORG_UUID | Foreign key to PURE_ORG. |\n\n',
    'author': 'David Naughton',
    'author_email': 'naughton@umn.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
