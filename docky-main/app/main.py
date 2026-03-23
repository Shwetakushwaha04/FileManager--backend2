from fastapi import FastAPI


from starlette.middleware.cors import CORSMiddleware

from app.lib import init_db
from app.routers import auth, document, folder, file, content


app = FastAPI(
  title="Doc Cloud",
  description="API for Document Storage Service",
  version="0.0.1",
  redoc_url=None
)

init_db(app)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  # allow_origins=allowed_origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)


@app.get("/")
def read_root():
  return {"app": "Doc cloud", "version": "0.0.1"}


app.include_router(auth.router, tags=["Auth"])
app.include_router(folder.router, tags=["Folders"], prefix="/folders")
app.include_router(document.router, tags=["Documents"], prefix="/documents")
app.include_router(file.router, tags=["Files"], prefix="/files")
app.include_router(content.router, tags=["Content"], prefix="/contents")