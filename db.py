from sqlalchemy import create_engine

db_url = "postgresql://user:user@localhost:5432/django_project"

migrate_script = """
DROP TABLE IF EXISTS FoodCategory;
DROP TABLE IF EXISTS Food;
DROP TABLE IF EXISTS additional;
CREATE TABLE FoodCategory (id INT generated always as identity, name_ru VARCHAR(255) UNIQUE, name_en VARCHAR(255) UNIQUE, name_ch VARCHAR(255) UNIQUE, order_id INT DEFAULT 10, PRIMARY KEY(id, name_ru));
CREATE TABLE Food (category VARCHAR(255) NOT NULL, FOREIGN KEY (category) REFERENCES FoodCategory(name_ru), is_vegan BOOLEAN NOT NULL, is_special BOOLEAN NOT NULL, code INT NOT NULL, internal_code INT UNIQUE, name_ru VARCHAR(255) NOT NULL PRIMARY KEY, description_ru VARCHAR(255), description_en VARCHAR(255), description_ch VARCHAR(255), cost FLOAT NOT NULL, is_publish BOOLEAN NOT NULL);
CREATE TABLE additional (food1 VARCHAR(255) NOT NULL, FOREIGN KEY (food1) REFERENCES Food(name_ru), food2 VARCHAR(255) NOT NULL, FOREIGN KEY (food2) REFERENCES Food(name_ru));
"""

engine = create_engine(db_url)

def migrate():
    engine.execute(migrate_script)
