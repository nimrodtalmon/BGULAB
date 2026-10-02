"""BGULAB web server: renders the repo, signs lab members in, files requests.

Stateless: nothing here is written to disk or kept beyond a short cache.
"""

import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import content, github, govern
from app.gate import COOKIE, MAX_AGE, clean_name, lab_cookie, lab_name, password_ok

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory=content.ROOT / "static"), name="static")
templates = Jinja2Templates(directory=content.ROOT / "templates")

NAV = [("/", "Research"), ("/people", "People"), ("/pages/lab", "Lab")]  # the brand also links to /

# Old addresses, kept working after the round-2 merge.
MOVED = {
    "/pages/home": "/", "/pages/research": "/", "/pages/publications": "/",
    "/projects": "/", "/pages/contact": "/people",
    "/pages/onboarding": "/pages/lab", "/pages/resources": "/pages/lab",
    "/pages/style-guide": "/pages/lab",
    "/how": "/govern#how-this-works", "/log": "/govern#rounds",
}


# A page line "[[projects]]" is replaced by the project boxes.
PROJECTS_MARK = "<p>[[projects]]</p>"


def deployed_commit() -> str:
    return os.environ.get("RENDER_GIT_COMMIT", "")[:7] or "local"


def render(request: Request, template: str, status: int = 200, **ctx) -> HTMLResponse:
    rounds = content.rounds()
    name = lab_name(request)
    ctx.update(
        request=request,
        lab=name is not None,
        lab_name=name,
        nav=NAV,
        commit=deployed_commit(),
        latest_round=rounds[0]["number"] if rounds else None,
    )
    return templates.TemplateResponse(request, template, ctx, status_code=status)


def not_found(request: Request) -> HTMLResponse:
    return render(request, "message.html", status=404, title="Not found",
                  message="Nothing here. If something should be, request it with Govern.")


def sign_in_page(request: Request, title: str, status: int = 200, error: str = "") -> HTMLResponse:
    return render(request, "login.html", status=status, title=title,
                  next=request.url.path, error=error)


def show_page(request: Request, slug: str) -> HTMLResponse:
    doc = content.page(slug)
    if doc is None:
        return not_found(request)
    lab = lab_name(request) is not None
    if doc["lab_only"] and not lab:
        return sign_in_page(request, doc["title"])
    body = content.fold(doc["body"], lab)
    if PROJECTS_MARK in body:
        boxes = templates.get_template("projects.html").render(themes=content.projects())
        body = body.replace(PROJECTS_MARK, boxes)
    return render(request, "page.html", doc=doc, title=doc["title"], body=body)


def set_lab_cookie(request: Request, resp, name: str):
    resp.set_cookie(COOKIE, lab_cookie(name), max_age=MAX_AGE, httponly=True, samesite="lax",
                    secure=request.headers.get("x-forwarded-proto", request.url.scheme) == "https")
    return resp


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return show_page(request, "home")


@app.get("/pages/{slug}", response_class=HTMLResponse)
def page(request: Request, slug: str):
    path = f"/pages/{slug}"
    if path in MOVED:
        return RedirectResponse(MOVED[path], status_code=301)
    return show_page(request, slug)


@app.get("/projects", response_class=HTMLResponse)
@app.get("/how", response_class=HTMLResponse)
@app.get("/log", response_class=HTMLResponse)
def moved(request: Request):
    return RedirectResponse(MOVED[request.url.path], status_code=301)


@app.get("/people", response_class=HTMLResponse)
def people(request: Request):
    return render(request, "people.html", title="People", people=content.people())


@app.get("/how/code/{path:path}", response_class=HTMLResponse)
def code(request: Request, path: str):
    if lab_name(request) is None:
        return sign_in_page(request, "Code")
    text = content.code_file(path)
    if text is None:
        return not_found(request)
    return render(request, "code.html", title=path, path=path, text=text)


@app.get("/log/commit/{sha}", response_class=HTMLResponse)
def commit(request: Request, sha: str):
    if lab_name(request) is None:
        return sign_in_page(request, "Commit")
    c = github.commit(sha)
    if c is None:
        return render(request, "message.html", title="Commit",
                      message="Could not load this commit from GitHub.")
    return render(request, "commit.html", title=f"Commit {sha[:7]}", c=c)


def govern_page(request: Request, result=None, form=None, status: int = 200) -> HTMLResponse:
    lab = lab_name(request) is not None
    return render(request, "govern.html", status=status, title="Govern", result=result,
                  form=form or {}, pending=github.open_requests(), rounds=content.rounds(),
                  rules=content.rules_html(), procedure=content.claude_md_html(),
                  tree=content.code_tree() if lab else [])


@app.get("/govern", response_class=HTMLResponse)
def govern_form(request: Request):
    return govern_page(request)


@app.post("/govern", response_class=HTMLResponse)
def govern_submit(request: Request, name: str = Form(""), password: str = Form(""),
                  text: str = Form(""), page: str = Form("")):
    signed_in = lab_name(request)
    if signed_in:
        name = signed_in
    addr = request.headers.get("x-forwarded-for", request.client.host if request.client else "")
    result = govern.submit(name, password, text, addr.split(",")[0].strip(), bool(signed_in),
                           page)
    if "application/json" in request.headers.get("accept", ""):  # the popup
        resp = JSONResponse({"ok": result["ok"], "counted": result.get("counted", False),
                             "message": result["message"]})
    else:
        resp = govern_page(request, result=result,
                           form={} if result["ok"] else {"name": name, "text": text})
    if result.get("counted") and not signed_in:
        set_lab_cookie(request, resp, name)  # right password: stay signed in from now on
    return resp


@app.post("/login")
def login(request: Request, name: str = Form(""), password: str = Form(""),
          next: str = Form("/")):
    target = next if next.startswith("/") and not next.startswith("//") else "/"
    if not clean_name(name) or not password_ok(password):
        return render(request, "login.html", status=401, title="Sign in", next=target,
                      name=name, error="Name and the lab password, please.")
    return set_lab_cookie(request, RedirectResponse(target, status_code=303), name)


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, next: str = "/"):
    return render(request, "login.html", title="Sign in", next=next)


@app.post("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie(COOKIE)
    return resp
