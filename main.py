from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from endpoints.routes import user_router, payment_router

app = FastAPI(
    title="User Subscription API",
    description="API for user registration and payment handling",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    clean_errors = []
    for err in exc.errors():
        ctx = err.get("ctx")
        if ctx and "error" in ctx and isinstance(ctx["error"], Exception):
            ctx["error"] = str(ctx["error"])
        clean_errors.append(err)
    return JSONResponse(status_code=400, content={"detail": clean_errors})

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(payment_router, prefix="/payments", tags=["Payments"])