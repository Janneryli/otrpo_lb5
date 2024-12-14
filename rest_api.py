from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from neo4j import GraphDatabase
from fastapi.security import OAuth2PasswordBearer
import logging

# Инициализация приложения FastAPI
app = FastAPI(
    title="Graph API",
    description="""
Описание точек доступа API:

1. **GET /nodes**  
   Возвращает всех узлов с атрибутами `id` и `label`.

2. **GET /node/{node_id}**  
   Возвращает узел с его связями и всеми атрибутами узлов и связей.

3. **POST /nodes**  
   Добавляет узел и/или связи. Требуется авторизация через токен.

4. **DELETE /nodes/{node_id}**  
   Удаляет узел и его связи. Требуется авторизация через токен.

**Особенности:**
- Точки POST и DELETE защищены токеном авторизации.
- Работа с сегментом графа настраивается через параметры POST/DELETE.
    """,
    version="1.0.0"
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Конфигурация базы данных Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "12345678"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Настройка авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Простая проверка токена (заглушка)
async def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "test_token":  # Замените на вашу логику проверки токена
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Модели данных
class Node(BaseModel):
    id: int
    label: str

class NodeWithRelations(BaseModel):
    id: int
    label: str
    relations: list

# Функции базы данных
async def get_all_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.id AS id, n.name AS label")
        nodes = [record.data() for record in result]
        logging.info(f"Retrieved nodes: {nodes}")
        return nodes

async def get_node_with_relations(node_id: int):
    with driver.session() as session:
        result = session.run(
            "MATCH (n)-[r]->(m) WHERE n.id=$node_id RETURN n, collect(r), collect(m)",
            node_id=node_id
        )
        record = result.single()
        if not record:
            return None
        node = record["n"]
        relations = [
            {
                "type": rel.type,
                "target": {"id": target.get("id", None), "label": target.get("name", None)}
            }
            for rel, target in zip(record["collect(r)"], record["collect(m)"])
        ]
        return {"id": node.get("id"), "label": node.get("name"), "relations": relations}

async def create_node_and_relations(node: Node, token: str):
    with driver.session() as session:
        session.run(
            "CREATE (n:Node {id: $id, name: $label})",
            id=node.id, label=node.label
        )
        logging.info(f"Created node: {node}")
        return {"message": "Node created successfully"}

async def delete_node(node_id: int, token: str):
    with driver.session() as session:
        session.run("MATCH (n {id: $node_id}) DETACH DELETE n", node_id=node_id)
        logging.info(f"Deleted node with id: {node_id}")
        return {"message": "Node deleted successfully"}

async def get_graph_segment():
    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n.id AS source, r.type AS relation, m.id AS target")
        segment = [record.data() for record in result]
        logging.info(f"Graph segment: {segment}")
        return segment

# Эндпоинты API
@app.get("/nodes", response_model=list[Node])
async def read_all_nodes():
    return await get_all_nodes()

@app.get("/node/{node_id}", response_model=NodeWithRelations)
async def read_node(node_id: int):
    node = await get_node_with_relations(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.post("/nodes", response_model=dict)
async def create_node(node: Node, token: str = Depends(verify_token)):
    return await create_node_and_relations(node, token)

@app.delete("/nodes/{node_id}", response_model=dict)
async def delete_node_endpoint(node_id: int, token: str = Depends(verify_token)):
    return await delete_node(node_id, token)

@app.get("/graph-segment", response_model=list[dict])
async def read_graph_segment():
    return await get_graph_segment()

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
