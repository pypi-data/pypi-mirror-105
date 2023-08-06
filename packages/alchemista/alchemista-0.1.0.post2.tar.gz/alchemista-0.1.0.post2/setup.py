# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alchemista']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.14,<2.0.0', 'pydantic>=1.8.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.6.0,<4.0.0']}

setup_kwargs = {
    'name': 'alchemista',
    'version': '0.1.0.post2',
    'description': 'Tools to convert SQLAlchemy models to Pydantic models',
    'long_description': '# Alchemista\n\nTools to generate Pydantic models from SQLAlchemy models.\n\nStill experimental.\n\n## How to use\n\nQuick example:\n\n```python\nfrom alchemista import sqlalchemy_to_pydantic\nfrom sqlalchemy import Column, Integer, String, create_engine, select\nfrom sqlalchemy.orm import declarative_base, sessionmaker\n\n\nBase = declarative_base()\nengine = create_engine("sqlite://", echo=True)\n\n\nclass Person(Base):\n    __tablename__ = "people"\n\n    id = Column(Integer, primary_key=True)\n    age = Column(Integer)\n    name = Column(String, nullable=False)\n\n\nPersonPydantic = sqlalchemy_to_pydantic(Person)\n\n\nBase.metadata.create_all(engine)\nSessionMaker = sessionmaker(bind=engine)\n\nperson = PersonPydantic.construct(name="Someone", age=25)\nwith SessionMaker.begin() as session:\n    session.add(Person(**person.dict()))\n\nwith SessionMaker.begin() as session:\n    person_db = session.execute(select(Person)).scalar_one()\n    person = PersonPydantic.from_orm(person_db)\n    print(person)\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Gabriel Galli',
    'author_email': 'ggabriel96@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggabriel96/alchemista',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
