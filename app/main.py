"""BGULAB web server: renders the repo, gates members' views, files requests.

Stateless: nothing here is written to disk or kept beyond a short cache.
"""

import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import content, github, govern
from app.gate import COOKIE, MAX_AGE, is_member, member_cookie, password_ok

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=content.ROOT / "static"), name="static")
templates = Jinja2Templates(directory=content.ROOT / "templates")

NAV = [("/", "Home"), ("/pages/research", "Research"), ("/people", "People"),
       ("/projects", "Projects"), ("/pages/publications", "Publications"),
       ("/how", "How"), ("/log", "Log")]


def deployed_commit() -> str:
    return os.environ.get("RENDER_GIT_COMMIT", "")[:7] or "local"


def render(request: Request, template: str, status: int = 200, **ctx) -> HTMLResponse:
    rounds = content.rounds()
    ctx.update(
        request=request,
        member=is_member(request),
        nav=NAV,
        commit=deployed_commit(),
        latest_round=rounds[0]["number"] if rounds else None,
    )
    return templates.TemplateResponse(request, template, ctx, status_code=status)


def not_found(request: Request) -> HTMLResponse:
    return render(request, "message.html", status=404, title="Not found",
                  message="Nothing here. If something should be, request it with Govern.")


def gated(request: Request, doc: dict | None, template: str = "page.html") -> HTMLResponse:
    if doc is None:
        return not_found(request)
    if doc["visibility"] == "members" and not is_member(request):
        return render(request, "login.html", title=doc["title"], next=request.url.path)
    return render(request, template, doc=doc, title=doc["title"])


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return gated(request, content.page("home"))


@app.get("/pages/{slug}", response_class=HTMLResponse)
def page(request: Request, slug: str):
    return gated(request, content.page(slug))


@app.get("/people", response_class=HTMLResponse)
def people(request: Request):
    return render(request, "people.html", title="People", people=content.people())


@app.get("/projects", response_class=HTMLResponse)
def projects(request: Request):
    member = is_member(request)
    shown = [p for p in content.projects() if p["visibility"] == "public" or member]
    hidden = len(content.projects()) - len(shown)
    return render(request, "projects.html", title="Projects", projects=shown, hidden=hidden)


@app.get("/projects/{slug}", response_class=HTMLResponse)
def project(request: Request, slug: str):
    return gated(request, content.project(slug))


@app.get("/how", response_class=HTMLResponse)
def how(request: Request):
    tree = content.code_tree() if is_member(request) else []
    return render(request, "how.html", title="How", rules=content.rules_html(),
                  procedure=content.claude_md_html(), tree=tree)


@app.get("/how/code/{path:path}", response_class=HTMLResponse)
def code(request: Request, path: str):
    if not is_member(request):
        return render(request, "login.html", title="Code", next=request.url.path)
    text = content.code_file(path)
    if text is None:
        return not_found(request)
    return render(request, "code.html", title=path, path=path, text=text)


@app.get("/log", response_class=HTMLResponse)
def log(request: Request):
    pending = github.open_requests()
    return render(request, "log.html", title="Log", rounds=content.rounds(), pending=pending)


@app.get("/log/commit/{sha}", response_class=HTMLResponse)
def commit(request: Request, sha: str):
    if not is_member(request):
        return render(request, "login.html", title="Commit", next=request.url.path)
    c = github.commit(sha)
    if c is None:
        return render(request, "message.html", title="Commit",
                      message="Could not load this commit from GitHub.")
    return render(request, "commit.html", title=f"Commit {sha[:7]}", c=c)


@app.get("/govern", response_class=HTMLResponse)
def govern_form(request: Request):
    return render(request, "govern.html", title="Govern", result=None)


@app.post("/govern", response_class=HTMLResponse)
def govern_submit(request: Request, name: str = Form(""), password: str = Form(""),
                  text: str = Form("")):
    addr = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    result = govern.submit(name, password, text, addr.split(",")[0].strip(), is_member(request))
    return render(request, "govern.html", title="Govern", result=result,
                  form={} if result["ok"] else {"name": name, "text": text})


@app.post("/login")
def login(request: Request, password: str = Form(""), next: str = Form("/")):
    target = next if next.startswith("/") and not next.startswith("//") else "/"
    if not password_ok(password):
        return render(request, "login.html", status=401, title="Members", next=target,
                      error="Password not recognized.")
    resp = RedirectResponse(target, status_code=303)
    resp.set_cookie(COOKIE, member_cookie(), max_age=MAX_AGE, httponly=True, samesite="lax",
                    secure=request.headers.get("x-forwarded-proto", request.url.scheme) == "https")
    return resp


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, next: str = "/"):
    return render(request, "login.html", title="Members", next=next)


@app.post("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie(COOKIE)
    return resp
