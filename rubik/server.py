import uvicorn
from fastapi import FastAPI
from fastapi.params import Query
from fastapi.middleware.cors import CORSMiddleware
from cube import Cube
from kociembasolver import KociembaSolver


app = FastAPI()

# TODO: Remove

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(cube_str: str = Query(..., alias="cube", min_length=54, max_length=54)):
    # print(cube_str)
    cube: Cube
    solver: KociembaSolver
    try:
        cube = Cube(cube_str)
    except ValueError as e:
        return {"error": str(e)}

    try:
        solver = KociembaSolver(cube)
        solver.solve()
    except Exception as e:
        return {"error": str(e)}

    return {"cube": str(cube), "moves": solver.moves, "timeToSolve": solver.time_to_solve}

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
