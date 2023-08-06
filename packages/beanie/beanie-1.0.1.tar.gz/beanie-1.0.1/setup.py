# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beanie',
 'beanie.executors',
 'beanie.migrations',
 'beanie.migrations.controllers',
 'beanie.odm',
 'beanie.odm.interfaces',
 'beanie.odm.operators',
 'beanie.odm.operators.find',
 'beanie.odm.operators.update',
 'beanie.odm.queries',
 'beanie.odm.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'motor>=2.1.0,<3.0.0',
 'pydantic>=1.8,<2.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['beanie = beanie.executors.migrate:migrations']}

setup_kwargs = {
    'name': 'beanie',
    'version': '1.0.1',
    'description': 'Asynchronous Python ODM for MongoDB',
    'long_description': '[![Beanie](https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/with_text.svg)](https://github.com/roman-right/beanie)\n\n# Getting Started with Beanie\n\n[Beanie](https://github.com/roman-right/beanie) - is an Asynchronous Python\nobject-document mapper (ODM) for MongoDB, based on [Motor](https://motor.readthedocs.io/en/stable/) and [Pydantic](https://pydantic-docs.helpmanual.io/).\n\nWhen using Beanie each database collection has a corresponding `Document` that\nis used to interact with that collection. In addition to retrieving data,\nBeanie allows you to add, update, or delete documents from the collection as\nwell.\n\nBeanie saves you time by removing boiler-plate code and it helps you focus on\nthe parts of your app that actually matter.\n\nData and schema migrations are supported by Beanie out of the box.\n\n## Installation\n\n### PIP\n\n```shell\npip install beanie\n```\n\n### Poetry\n\n```shell\npoetry add beanie\n```\n\n## Basic Example\n\n### Document models\n\n```python\nfrom typing import Optional\nfrom pydantic import BaseModel\nfrom beanie import Document, Indexed\n\n\nclass Category(BaseModel):\n    name: str\n    description: str\n\n\nclass Product(Document):  # This is the model\n    name: str\n    description: Optional[str] = None\n    price: Indexed(float)\n    category: Category\n\n    class Collection:\n        name = "products"\n```\nEach document by default has `id` ObjectId field, which reflects `_id` MongoDB document field. It can be used later as an argument for the `get()` method.\n\nMore details about Documents, collections, and indexes configuration could be found in the [tutorial](/tutorial/install/).\n\n### Initialization\n\n```python\nimport motor\nfrom beanie import init_beanie\n\n\nasync def init():\n    # Crete Motor client\n    client = motor.motor_asyncio.AsyncIOMotorClient(\n        "mongodb://user:pass@host:27017"\n    )\n\n    # Init beanie with the Note document class\n    await init_beanie(database=client.db_name, document_models=[Product])\n\n```\n\n### Create\n\n```python\nchocolate = Category(name="Chocolate")\n\n# Single:\n\nbar = Product(name="Tony\'s", price=5.95, category=chocolate)\nawait bar.insert()\n\n# Many\n\nmilka = Product(name="Milka", price=3.05, category=chocolate)\npeanut_bar = Product(name="Peanut Bar", price=4.44, category=chocolate)\nawait Product.insert_many([milka, peanut_bar])\n```\n\nOther details and examples could be found in the [tutorial](/tutorial/insert/)\n\n### Find\n\n```python\n# Single\n\n# By id\nbar = await Product.get("608da169eb9e17281f0ab2ff")\n\n# By name\nbar = await Product.find_one(Product.name == "Peanut Bar")\n\n# Many\n\n# By category\n\nchocolates = await Product.find(\n    Product.category.name == "Chocolate"\n).to_list()\n\n# And by price\n\nchocolates = await Product.find(\n    Product.category.name == "Chocolate",\n    Product.price < 5\n).to_list()\n\n# OR\n\nchocolates = await Product.find(\n    Product.category.name == "Chocolate").find(\n    Product.price < 5).to_list()\n\n# Complex example:\n\nclass ProductShortView(BaseModel):\n    name: str\n    price: float\n\n\nproducts = await Product.find(\n    Product.category.name == "Chocolate",\n    Product.price < 3.5\n).sort(-Product.price).limit(10).project(ProductShortView)\n\n# All\n\nall_products = await Product.all().to_list()\n```\n\nInformation about sorting, skips, limits, and projections could be found in the [tutorial](/tutorial/find/)\n\n### Update\n\n```python\n# Single \nawait Product.find_one(Product.name == "Milka").set({Product.price: 3.33})\n\n# Or\nbar = await Product.find_one(Product.name == "Milka")\nawait bar.update(Set({Product.price: 3.33}))\n\n# Or\nbar.price = 3.33\nawait bar.replace()\n\n# Many\nawait Product.find(\n    Product.category.name == "Chocolate"\n).inc({Product.price: 1})\n```\n\nMore details and examples about update queries could be found in the [tutorial](/tutorial/update/)\n\n### Delete\n\n```python\n# Single \nawait Product.find_one(Product.name == "Milka").delete()\n\n# Or\nbar = await Product.find_one(Product.name == "Milka")\nawait bar.delete()\n\n# Many\nawait Product.find(\n    Product.category.name == "Chocolate"\n).delete()\n```\n\nMore information could be found in the [tutorial](/tutorial/delete/)\n\n### Aggregate\n\n```python\n# With preset methods\n\navg_price = await Product.find(\n    Product.category.name == "Chocolate"\n).avg(Product.price)\n\n# Or without find query\n\navg_price = await Product.avg(Product.price)\n\n# Native syntax \n\nclass OutputItem(BaseModel):\n    id: str = Field(None, alias="_id")\n    total: int\n    \nresult = await Product.find(\n    Product.category.name == "Chocolate").aggregate(\n    [{"$group": {"_id": "$category.name", "total": {"$avg": "$price"}}}],\n    projection_model=OutputItem\n).to_list()\n\n```\n\nInformation about aggregation preset aggregation methods and native syntax aggregations could be found in the [tutorial](/tutorial/aggregate/)\n\n### Documentation\n\n- **[Tutorial](https://roman-right.github.io/beanie/tutorial/install/)** - Usage examples with descriptions\n- **[API](https://roman-right.github.io/beanie/api/document/)** - Full list of the classes and\n  methods\n\n### Example Projects\n\n- **[FastAPI Demo](https://github.com/roman-right/beanie-fastapi-demo)** - Beanie and FastAPI collaboration demonstration. CRUD and Aggregation.\n- **[Indexes Demo](https://github.com/roman-right/beanie-index-demo)** - Regular and Geo Indexes usage example wrapped to a microservice. \n\n### Articles\n\n- **[Announcing Beanie - MongoDB ODM](https://dev.to/romanright/announcing-beanie-mongodb-odm-56e)**\n- **[Build a Cocktail API with Beanie and MongoDB](https://developer.mongodb.com/article/beanie-odm-fastapi-cocktails/)**\n- **[MongoDB indexes with Beanie](https://dev.to/romanright/mongodb-indexes-with-beanie-43e8)**\n- **[Beanie Projections. Reducing network and database load.](https://dev.to/romanright/beanie-projections-reducing-network-and-database-load-3bih)**\n\n### Resources\n\n- **[GitHub](https://github.com/roman-right/beanie)** - GitHub page of the project\n- **[Changelog](https://roman-right.github.io/beanie/changelog)** - list of all the valuable changes\n- **[Discord](https://discord.gg/ZTTnM7rMaz)** - ask your questions, share ideas or just say `Hello!!`\n\n\n----\nSupported by [JetBrains](https://jb.gg/OpenSource)\n\n[![JetBrains](https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/jetbrains.svg)](https://jb.gg/OpenSource)\n',
    'author': 'Roman',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roman-right/beanie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
